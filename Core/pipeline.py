#!/usr/bin/python3
import xml.etree.ElementTree as ET
from step import Step
from pipeline_tools import *
import re
from variant import Variant
from option import Option

class Pipeline:
    def __init__(self, pipeline, package_manager):
        tree = ET.parse(pipeline)
        self._root = tree.getroot()
        self._imports = {}
        self._inputs = {}
        self._outputs = {}
        self._options = {}
        self._step_pipelines = {}
        self._dependencies = {}

        self._steps = {}
        self._shell_steps = []

        self._package_manager = package_manager
        self._test_avaliable = None

    def _get_output(self, name):
        return self._outputs.get(name, None)

    def _process_option(self, node, args):
        '''Return Option, that contain values produced using args comed from step declaration'''
        opt = Option(node.attrib.get('repr'))
        name = node.attrib['name']

        if 'default' in node.attrib:
            opt.set_default_val(Variant.from_string(node.attrib['default'], node.attrib['type']))
        elif 'default_ref' in node.attrib:
            ref = node.attrib['default_ref'].strip()
            if ref in self._inputs:
                opt.set_default_val(self._inputs[ref].get())
            else:
                raise RuntimeError('Reference to currently undefined symbol: ' + ref)
        else:
            for child in node: #check by RELAXNG
                if child.tag == 'default':
                    opt.set_default_val(self._eval_expression(child))

        if name in args:
            opt.set_val(args[name])
        
        return opt

    def _eval_expression(self, expr):
        '''Return Variant with steps's expr results'''

        expr_args = []
        for child in expr:
            if child.tag == 'var':
                expr_args.append(self._get_explicit_value(child))
            elif child.tag == 'mod':
                expr_args.append(self._eval_expression(child))

        if expr.tag == 'mod':
            return apply_modifyer(expr.attrib['name'], expr.attrib.get('params'), expr_args)
        else:
            if len(expr_args) > 1: # len==0 check by RELAXNG
                return apply_modifyer('list', None, expr_args)
            return  expr_args[0]


    def _get_explicit_value(self, node): 
        '''Return Variant with step's arg value'''

        if 'val' in node.attrib:
            return Variant.from_string(node.attrib['val'], node.attrib.get('type'))
        elif 'ref' in node.attrib:
            parts = node.attrib['ref'].split('.')
            if len(parts) == 1: #local variable
                option_name = parts[0]
                if option_name in self._inputs:
                    return self._inputs[option_name].get()
                if option_name in self._outputs:
                    return self._outputs[option_name].get()
                else:
                    raise RuntimeError('Reference to undefined option: ' + option_name)
            elif len(parts) == 2: #some pipeline output
                step_name, output_name = parts
                if step_name not in self._step_pipelines:
                    raise RuntimeError('Reference to undefined step: ' + step_name)
                output = self._step_pipelines[step_name]._get_output(output_name)
                
                if output is None:
                    raise RuntimeError('Undefined step output %s.%s has:%s' % (parts[0], parts[1], self._step_pipelines[parts[0]]._outputs))
                
                return output.get()
            else:
               raise RuntimeError('Wrong reference format')

        return None

    def _process_arg(self, node, args):
        args[node.attrib['name']] = self._get_explicit_value(node) or self._eval_expression(node)


    def _gen_step(self, node):
        text = []
        step_name = node.attrib['name']

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
                        text.append(gen_cmd_check(step_pl._test_avaliable, last=True))
                    break


                step_pl_path = self._package_manager.find_pipeline(*self._imports[child.tag])
                if step_pl_path is not None:
                    step_pl = Pipeline(step_pl_path, self._package_manager)
                    text.append(step_pl.generate(args))
                    self._step_pipelines[step_name] = step_pl
                    break
                else:
                    raise RuntimeError('cant import pipeline ' + ' '.join(self._imports[child.tag]))
                
        return Step('\n'.join(text), 'pl')

    def _gen_shell_step(self, nodes, pl_name):
        cmds = []
        self._test_avaliable = 'true' #to-do
        for node in nodes:
            fmt = node.attrib["c"]

            for token in self._inputs:
                fmt = fmt.replace('$(%s)' % token, self._inputs[token].to_string())

            for token in self._outputs:
                fmt = fmt.replace('$(%s)' % token, self._outputs[token].to_string())

            fmt = re.sub(r'\$\([^\)]+\)', '', fmt)

            cmds.append(fmt)

        text = "step " + pl_name + "\n"
        text += "\n".join(["try " + cur_cmd for cur_cmd in cmds])
        text += "\nnext\n"

        return Step(text, 'sh')

        def _gen_r_step(self, nodes, pl_name):
            cmds = []
            self._test_avaliable = 'true'
            for node in nodes:
                fmt = node.attrib["r"]

                for token in self._inputs:
                    fmt = fmt.replace('$(%s)' % token, self._inputs[token].to_string())

                for token in self._outputs:
                    fmt = fmt.replace('$(%s)' % token, self._outputs[token].to_string())

                fmt = re.sub(r'\$\([^\)]+\)', '', fmt)

                cmds.append(fmt)
            text = "\n".join(cmds)
            return Step(text, 'r')

    def _steps2script(self):
        if (len(self._shell_steps) != 0):
            return '\n'.join([step.text() for step in self._shell_steps])

        text = []
        for step_name in toposort(self._dependencies):
            text.append(self._steps[step_name].text())

        return '\n'.join(text)

    def _process_dependencies(self, node):
        step_name = node.attrib['name']
        self._dependencies[step_name] = set()
        for child in node:
            if child.tag in self._imports:
                for arg in child.findall('arg'):
                    if 'ref' in arg.attrib:
                        parts = arg.attrib['ref'].split('.')
                        if len(parts) == 2: #some pipeline output
                            self._dependencies[step_name].add(parts[0])

    def generate(self, args):
        for import_pl in self._root.findall('import'):
            for pkg_name in import_pl.attrib['what'].split(", "):
                self._imports[pkg_name] = (import_pl.attrib['package'], pkg_name)

        for inp in self._root.findall('input'):
            self._inputs[inp.attrib['name']] = self._process_option(inp, args)

        for output in self._root.findall('output'):
            self._outputs[output.attrib['name']] = self._process_option(output, args)


        sh_node = self._root.find('sh') 
        if sh_node is None:
        
            for child in self._root:
                if child.tag == 'step':
                    self._process_dependencies(child)


            for child in self._root:
                if child.tag == 'step':
                    self._steps[child.attrib['name']] = self._gen_step(child)
        else:
            sh_nodes = []
            for child in self._root:
                if child.tag == 'sh':
                    sh_nodes.append(child)

            self._shell_steps.append(self._gen_shell_step(sh_nodes, self._root.attrib['name']))
            
        return self._steps2script();