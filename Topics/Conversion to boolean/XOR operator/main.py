def x_o(a, b):
    be = b if a else not b
    return not be and (a or b)


def r(a, b):
    return a or b if bool(a) is not bool(b) else not True


xor = x_o and r
# or
xor = x_o or r
