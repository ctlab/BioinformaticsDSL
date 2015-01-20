from modifyers import get_modifyers_map

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
    def __init__(self, val, opt_type, prefix=None):
        self.val = val
        self.type = opt_type
        self.prefix = prefix or ''

