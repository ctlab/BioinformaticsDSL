from variant import Variant
from modifyers import get_modifyers_map
from collections import defaultdict
from itertools import takewhile, count, chain

def apply_modifyer(mod, mod_params, args):
    modifyers = get_modifyers_map()
    if mod not in modifyers:
        raise RuntimeError('Unknown modifyer ' + mod)

    return modifyers[mod](mod_params, args)

def gen_cmd_check(test_avaliable, first=False, last=False):
    text = []
    if first:
        text.append('if')
    elif not last:
        text.append(';\nelif')
    else:
        return ';\nelse echo "cant run any implementation of step"; exit 1;\nfi\n'

    assert(test_avaliable is not None)
    text.append(test_avaliable)
    text.append('; then')

    return ' '.join(text) 

class Option:
    def __init__(self, opt_type, prefix=None, nargs=None):
        self._val = None
        self._default_val = None
        self._type = opt_type
        self._prefix = prefix or ''
        self._nargs = nargs or 1

    def type(self):
        return self._type

    def set_val(self, val):
        assert type(val) is Variant
        self._val = val

    def set_default_val(self, val):
        assert type(val) is Variant
        self._default_val = val

    def get(self):
        if self._val or self._default_val:
            return (self._val or self._default_val).convert(self._type)

        return None

    def __str__(self):
        val = self.get()
        if self.get() is None:
            return ''
        if self._type == 'void':
            return self._prefix if self.get().get('void') else ''
        elif self._type == 'list':
            return ' '.join(self.get().get('list'))
        else:
            return self._prefix + ' ' + self.get().get('string') if val is not None else ''


def toposort(graph):
    levels_by_name = {}
    names_by_level = defaultdict(set)

    def walk_depth_first(name):
        if name in levels_by_name:
            return levels_by_name[name]
        children = graph.get(name, None)
        level = 0 if not children else (1 + max(walk_depth_first(lname) for lname in children))
        levels_by_name[name] = level
        names_by_level[level].add(name)
        return level

    for name in graph:
        walk_depth_first(name)

    res = list(takewhile(lambda x: x is not None, (names_by_level.get(i, None) for i in count())))
    return chain.from_iterable(res)
