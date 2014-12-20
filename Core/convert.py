#!/usr/bin/python3
import xml.etree.ElementTree as ET
from os import path, system
import sys
#from exceptions import RuntimeError

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
        opt_repr = node.attrib.get('repr', '')
        opt_type = node.attrib.get('type', 'void')
        opt_val = None
        name = node.attrib['name']
        if name in args:
            opt_val = args[name]
        elif 'default' in node.attrib:
            opt_val = node.attrib['default']

        if opt_type == 'void':
            if opt_val in [None, 'no', 'No', '0', 'f', 'false', 'False']:
                return None
            else:
                opt_val = ""

        return (opt_val, opt_repr, opt_type) if opt_val != None else None

    def _process_arg(self, arg, args):
        if 'val' in arg.attrib:
            args[arg.attrib['name']] = arg.attrib['val']
        elif 'ref' in arg.attrib:
            parts = arg.attrib['ref'].split('.')
            if len(parts) == 1:
                if parts[0] in self._inputs:
                     args[arg.attrib['name']] = self._inputs[parts[0]][0]
            elif len(parts) == 2:
                #some pipeline output
                if parts[0] not in self._step_pipelines:
                    raise RuntimeError('Reference to undefined step')
                output = self._step_pipelines[parts[0]]._get_output(parts[1])
                if output is None:
                    raise RuntimeError('Undefined output %s.%s' % (parts[0], parts[1]))
                args[arg.attrib['name']] = output[0]
            else:
               raise RuntimeError('Wrong reference format')


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
                        opt_repr = opt[1]
                        opt_val = opt[0] 
                        content.append(opt_repr + opt_val)
            elif token in self._inputs:
                inp_val, inp_repr, inp_type = self._inputs[token]
                content.append(inp_repr + inp_val)
            elif token in self._outputs:
                outp_val, outp_repr, outp_type = self._outputs[token]
                content.append(outp_repr + outp_val)
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