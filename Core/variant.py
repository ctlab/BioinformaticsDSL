#!/usr/bin/python3
import copy



class Variant:
    def __init__(self):
        '''Do not use constructor from outside'''
        pass

    @classmethod
    def from_string(cls, str_value, val_type=None):
        res = cls()
        res._value = str_value
        res._type = val_type or 'string'
        return res


    @classmethod
    def from_variant_list(cls, variant_list):
        assert len(variant_list) > 0
        res = cls()
        res._value = variant_list
        res._type = 'list'
        return res

    def get(self, val_type):
        if val_type == 'string':
            return self._value

        if val_type == 'void':
            return self._value.strip() not in ['', 'False', '0']
    

        if val_type == 'int':
            return self._value

    def convert(self, val_type):
        if val_type == self._type:
            return copy.deepcopy(self)

        if self._type == 'string':
            do_nothing = ['void', 'file', 'int']
            if val_type in do_nothing:
                return copy.deepcopy(self)

        if self._type == 'list':
            if val_type == 'string':
                return Variant.from_string(' '.join([elem.get('string') for elem in self._value]), 'string')

        raise RuntimeError('Unable to convert %s from %s to %s' % (str(self._value), self._type, val_type))



if __name__ == '__main__':
    print('variant is not runnable')

