from variant import Variant

class Option:
    def __init__(self, mask=None):
        self._val = None
        self._default_val = None
        self._mask = mask or '$'

    def assigned(self):
        return self.get() is not None

    def type(self):
        return self.get().type()

    def nargs(self):
        return self.get().type()

    def set_val(self, val):
        assert isinstance(val, Variant)
        self._val = val

    def set_default_val(self, val):
        assert isinstance(val, Variant)
        self._default_val = val

    def get(self):
        if self._val or self._default_val:
            return (self._val or self._default_val)
        return None

    def to_string(self):
        val = self.get()
        if val is None:
            return ''
        str_val  = val.to_string()

        return self._mask.replace('$', str_val)
