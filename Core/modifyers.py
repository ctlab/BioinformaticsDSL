from variant import Variant

def base_name(mod_params, args):
    assert len(args) == 1
    return Variant.from_string('.'.join(args[0].to_string().split('.')[:-1]))

def join(mod_params, args):
    str_value =  (mod_params or '').join([arg.to_string() for arg in args])
    return Variant.from_string(str_value, 'string')

def to_list(mod_params, args):
	return Variant.from_variant_list(args)

def get_modifyers_map():
    return\
        {
            'base_name' : base_name,
            'join' : join,
            'list'  : to_list
        }
