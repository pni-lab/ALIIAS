# sc: https://github.com/semente/python-baseconv/blob/master/baseconv.py

class BaseConverter:
    def __init__(self, base):
        self.custom_base = base
        self.hex_base = '0123456789abcdef'

    def base2base(self, input, from_base, to_base):

        x = 0
        for digit in input:
            try:
                x = x * len(from_base) + from_base.index(digit)
            except ValueError:
                raise ValueError('invalid digit "%s"' % digit)

        # create the result in base 'len(to_digits)'
        if x == 0:
            res = to_base[0]
        else:
            res = ''
            while x > 0:
                digit = x % len(to_base)
                res = to_base[digit] + res
                x = int(x // len(to_base))
        return res

    def custom2hex(self, input):
        return self.base2base(input, from_base=self.custom_base, to_base=self.hex_base)

    def hex2custom(self, input):
        return self.base2base(input, from_base=self.hex_base, to_base=self.custom_base)
