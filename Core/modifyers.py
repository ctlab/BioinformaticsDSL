def base_name(mod_params, args):
    assert len(args) == 1
    return '.'.join(args[0].split('.')[:-1])

def join(mod_params, args):
    return (mod_params or '').join(args)

def get_modifyers_map():
    return\
        {
            'base_name' : base_name,
            'join' : join
        }
