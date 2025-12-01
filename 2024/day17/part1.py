from typing import *
from machine import *

if __name__ == '__main__':
    a = int(input().split()[-1])
    b = int(input().split()[-1])
    c = int(input().split()[-1])
    input()
    program: List[int] = list(map(int, input().split()[-1].split(',')))
    # print(a, b, c, program)
    machine = Machine(a, b, c)
    print(','.join(map(str, machine(program))))
