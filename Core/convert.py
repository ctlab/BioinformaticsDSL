#!/usr/bin/python3
import xml.etree.ElementTree as ET
from os import path, system
import sys
#from exceptions import RuntimeError

def apply_modifyer(mod, args):
    #TO-DO mod lib
    if mod == 'base_name':
        assert len(args) == 1
        return '.'.join(args[0].split('.')[:-1])
    elif mod == 'concat':
        return ''.join(args)

    raise RuntimeError('Unknown modifyer ' + mod)

class Option:
    def __init__(self, val, opt_type, prefix=None):
        self.val = val
        self.type = opt_type
        self.prefix = prefix or ''


class Pipeline:
    def __init__(self, pipeline):
        tree = ET.parse(pipeline)
        self._root = tree.getroot()
        self._imports = {}
        self._inputs = {}
        self._outputs = {}
        self._options = {}
        self._step_pipelines = {}

    def _get_output(self, name):
        return self._outputs.get(name, None)

    def _import(self, pkg, what):
        storage = 'Utils'
        pipeline = path.join(storage, pkg, what + '.xml')
        return Pipeline(pipeline)

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
            return apply_modifyer(expr.attrib['name'], expr_args)


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
                    raise RuntimeError('Undefined step output %s.%s' % (parts[0], parts[1]))
                return output.val
            else:
               raise RuntimeError('Wrong reference format')
        return None

    def _process_arg(self, arg, args):
        args[arg.attrib['name']] = self._get_explicit_value(arg) or self._eval_expression(arg) 

    def _gen_step(self, node):
        text = []
        step_name = node.attrib['label']

        step_descr = node.find('description') 
        if step_descr is not None:
            text.append('#' + step_descr.text.strip())

        for child in node:
            if child.tag in self._imports:
                args = {}
                for arg in child.findall('arg'):
                    self._process_arg(arg, args)

                step_pl = self._import(*self._imports[child.tag])
                text.append(step_pl.generate(args))
                self._step_pipelines[step_name] = step_pl
                break

        return '\n'.join(text)

    def _gen_shell(self, node):
        fmt = node.attrib['fmt']
        cmd = node.attrib['cmd']
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

        return " ".join(content)


    def generate(self, args):
        text = []
        #text.append("#pipeline " + self._root.attrib['name'])
        #for child in self._root:
        #    text.append(str(child.tag) + str(child.attrib))

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
                text.append(self._gen_step(child))
            elif child.tag == 'shell':
                text.append(self._gen_shell(child))
        

        return '\n'.join(text)


def main():
    if len(sys.argv) < 3:
        print('usage:\nconvert <pipeline>.xml <output>.sh (arg_name=arg_value)*')
        return

    pl_file = sys.argv[1]
    script = sys.argv[2]
    print(' '.join(sys.argv))
    args = {arg : value for (arg, value) in [item.split('=') for item in sys.argv[3:]]}

    pipeline = Pipeline(pl_file)
    out_file = open(script, 'w')
    output = pipeline.generate(args)
    out_file.write(output)
    out_file.close()
    system('chmod +x ' + script)
    print(output)

if __name__ == '__main__':
    main()