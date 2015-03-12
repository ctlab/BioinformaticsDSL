class Option:
    def __init__(self, node):
        self.type = node.attrib.get('type', 'void')
        self.repr = node.attrib.get('repr')
        self.nargs = node.attrib.get('nargs')