#!/usr/bin/python3
import xml.etree.ElementTree as ET
from os import path, system
from step import Step
from pipeline_tools import *

class Pipeline:
    def __init__(self, pipeline, package_manager):
        tree = ET.parse(pipeline)
        self._root = tree.getroot()
        self._imports = {}
        self._inputs = {}
        self._outputs = {}
        self._options = {}
        self._step_pipelines = {}
        self._steps = []
        self._package_manager = package_manager
        self._test_avaliable = None

    def _get_output(self, name):
        return self._outputs.get(name, None)

    def _process_option(self, node, args):
        opt = Option(None, node.attrib.get('type', 'void'), node.attrib.get('repr'))
        name = node.attrib['name']
        if name in args:
            opt.val = args[name]
        elif 'default' in node.attrib:
            opt.val = node.attrib['default']

        if opt.type == 'void':
            if opt.val in [None, 'no', 'No', '0', 'f', 'false', 'False', '']:
                opt.val =  None
            else:
                opt.val = ""

        return opt if opt.val != None else None

    def _eval_expression(self, expr):
        expr_args = []
        for child in expr:
            if child.tag == 'var':
                expr_args.append(self._get_explicit_value(child))
            elif child.tag == 'mod':
                expr_args.append(self._eval_expression(child))

        if expr.tag == 'arg':
            assert len(expr_args) == 1
            return  expr_args[0]
        else:
            assert expr.tag == 'mod', expr.tag
            return apply_modifyer(expr.attrib['name'], expr.attrib.get('params'), expr_args)


    def _get_explicit_value(self, node):    
        if 'val' in node.attrib:
            return node.attrib['val']
        elif 'ref' in node.attrib:
            parts = node.attrib['ref'].split('.')
            if len(parts) == 1: #local variable
                if parts[0] in self._inputs:
                    return self._inputs[parts[0]].val
                else:
                    raise RuntimeError('Reference to undefined symbol')
            elif len(parts) == 2: #some pipeline output
                if parts[0] not in self._step_pipelines:
                    raise RuntimeError('Reference to undefined step')
                output = self._step_pipelines[parts[0]]._get_output(parts[1])
                if output is None:
                    raise RuntimeError('Undefined step output %s.%s has:%s' % (parts[0], parts[1], self._step_pipelines[parts[0]]._outputs))
                return output.val
            else:
               raise RuntimeError('Wrong reference format')
        return None

    def _process_arg(self, arg, args):
        args[arg.attrib['name']] = self._get_explicit_value(arg) or self._eval_expression(arg) 


    def _gen_step(self, node):
        text = []
        step_name = node.attrib['label']
        self._test_avaliable = 'true' #to-do

        step_descr = node.find('description') 
        if step_descr is not None:
            text.append('#' + step_descr.text.strip())

        for child in node:
            if child.tag in self._imports:
                args = {}
                for arg in child.findall('arg'):
                    self._process_arg(arg, args)

                interface = self._package_manager.find_interface(*self._imports[child.tag])
                if interface is not None:
                    first = True
                    for impl_pl_path in self._package_manager.get_implementations(interface):
                        step_pl = Pipeline(impl_pl_path, self._package_manager)
                        step_text = step_pl.generate(args)
                        text.append(gen_cmd_check(step_pl._test_avaliable, first))
                        first = False
                        text.append(step_text)
                        self._step_pipelines[step_name] = step_pl
                    if not first:
                        text.append(gen_cmd_check(step_pl._test_avaliable, first=False, last=True))
                    break


                step_pl_path = self._package_manager.find_pipeline(*self._imports[child.tag])
                if step_pl_path is not None:
                    step_pl = Pipeline(step_pl_path, self._package_manager)
                    text.append(step_pl.generate(args))
                    self._step_pipelines[step_name] = step_pl
                    break
                else:
                    raise RuntimeError('cant import pipeline ' + ' '.join(self._imports[child.tag]))
                
        return Step('\n'.join(text))

    def _gen_shell_step(self, node):
        fmt = node.attrib['fmt']
        cmd = node.attrib['cmd']
        self._test_avaliable = 'hash %s 2> /dev/null' % cmd
        content = []
        for token in fmt.split():
            if token == 'cmd':
                content.append(cmd)
            elif token == '[option]...':
                for opt in self._options.values():
                    if opt is not None:
                        content.append(opt.prefix + opt.val)
            elif token in self._inputs:
                inp = self._inputs[token]
                content.append(inp.prefix + inp.val)
            elif token in self._outputs:
                outp = self._outputs[token]
                content.append(outp.prefix + outp.val)
            elif token in ['>', '>>', '|', ';']:
                content.append(token)

        return Step(" ".join(content))

    def _steps2script(self):
        return '\n'.join([step.text() for step in self._steps])


    def generate(self, args):
        for import_pl in self._root.findall('import'):
            self._imports[import_pl.attrib['what']] = (import_pl.attrib['package'], import_pl.attrib['what'])

        for inp in self._root.findall('input'):
            self._inputs[inp.attrib['name']] = self._process_option(inp, args) 
        for output in self._root.findall('output'):
            self._outputs[output.attrib['name']] = self._process_option(output, args) 

        for opt in self._root.findall('option'):
            self._options[opt.attrib['name']] = self._process_option(opt, args) 

        for child in self._root:
            if child.tag == 'step':
                self._steps.append(self._gen_step(child))
            elif child.tag == 'shell':
                self._steps.append(self._gen_shell_step(child))
        

        return self._steps2script();