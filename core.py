from .utils import *


def run():
    a = inp_str()
    c = a.copy()
    print(c, end='\n\n\n')
    t = solve(c)
    print(t[0])
    clipboard.copy(t[0])
