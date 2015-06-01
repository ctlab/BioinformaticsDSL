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
        text.append('\nelif')
    else:
        return '\nelse echo "cant run any implementation of step"; exit 1;\nfi\n'

    assert(test_avaliable is not None)
    text.append(test_avaliable)
    text.append('; then')

    return ' '.join(text) 


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
