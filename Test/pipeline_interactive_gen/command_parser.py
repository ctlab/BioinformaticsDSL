#!/usr/bin/python3
import argparse
import shlex
import sys
import xml.etree.ElementTree as ET
import itertools
from option import Option
sys.path.insert(0, "../../Core")
from package_manager import PackageManager
from xml.dom import minidom

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def add_arg(parser, name, prefix, nargs):
    if prefix:
        parser.add_argument(prefix, dest=name)
    else:
        parser.add_argument(name, nargs=nargs)


class CommandParser:

    def _pipeline2parser(self, cmd):
        pm = PackageManager('../../Utils')
        th = pm.find_pipeline('genome', 'tophat')
        tree = ET.parse(th)
        root = tree.getroot()

        fmt = root.find('shell').attrib['fmt']
        inputs = {}
        outputs = {}
        options = {}

        for node in root.findall('output'):
            inputs[node.attrib['name']] = Option(node)
        for node in root.findall('input'):
            outputs[node.attrib['name']] =Option(node)
        for node in root.findall('option'):
            options[node.attrib['name']] =Option(node)

        parser = argparse.ArgumentParser()
        for token in fmt.split(' '):
            if token == '[options]...':
                for opt_name in options.keys():
                    add_arg(parser, opt_name, options[opt_name].repr, options[opt_name].nargs)
            elif token in inputs:
                add_arg(parser, token, inputs[token].repr, inputs[token].nargs)
            elif token in outputs:
                add_arg(parser, token, outputs[token].repr, outputs[token].nargs)

        return parser

    def gen_step(self, cmd, args):
        step = ET.Element('step')
        step.set('label', 'step1')

        descr = ET.SubElement(step, 'description')
        descr.text = 'Generated step'

        pl = ET.SubElement(step, cmd)
        for arg, value in vars(args).items():
            if value is not None:

                values = None
                if type(value) is not list:
                    values = [value]
                else:
                    values = value

                for val in values:
                    arg_node = ET.SubElement(pl, 'arg')
                    arg_node.set('name', arg)
                    arg_node.set('val', str(val))

        return prettify(step)

    def parse(self, command_str):
        cmd = command_str[0:command_str.find(' ')]
        args_str = command_str[command_str.find(' '): - 1]
        lexer = shlex.shlex(args_str)
        lexer.whitespace_split = True
        tokens = [repr(token)[1:-1] for token in lexer]

        parser = self._pipeline2parser(cmd)
        res = parser.parse_args(tokens)
        print(self.gen_step(cmd, res))      

def main():
    cp = CommandParser()
    cp.parse('tophat --output-dir tophat_out d_melanogaster_BDGP5.25.62 SRR031714_1.fastq SRR031714_2.fastq')

if __name__ == '__main__':
    main()