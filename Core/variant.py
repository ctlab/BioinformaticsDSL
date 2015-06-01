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
        res._nargs = 1
        return res

    @classmethod
    def from_variant_list(cls, variant_list):
        assert len(variant_list) > 0
        res = cls()
        res._nargs = len(variant_list)
        if (res._nargs > 1):
            res._value = [var._value for var in variant_list]
        else:
            res._value = variant_list[0]._value
        res._type = variant_list[0]._type
        return res

    def type(self):
        return self._type

    def nargs(self):
        return self._nargs

    def to_string(self, delim=None):
        if (self._type == 'void'):
            return ''
        elif (self._nargs == 1):
            return self._value
        else:
            return (delim or ' ').join(self._value)

    def _get_single(self, value):
        if self._type == 'void' or self._type == 'bool':
            return value == 'True'
        if self._type == 'str':
            return value
        elif self._type == 'int':
            return int(value)
        elif self._type == 'float':
            return float(value)
        elif self._type.startwith(file):
            return value

    def get(self):
        if self._nargs == 1:
            return self._get_single(self._value)
        else:
            return [self._get_single(value) for value in self._value]



if __name__ == '__main__':
    print('variant is not runnable')

