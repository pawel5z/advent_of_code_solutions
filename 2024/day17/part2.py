from typing import *
from machine import *
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <reg A value>')

    for _ in range(4):
        input()

    program: List[int] = list(map(int, input().split()[-1].split(',')))
    # print(a, b, c, program)
    a = int(sys.argv[1])
    machine = Machine(a, 0, 0)
    print(','.join(map(str, machine(program))))
    sys.exit()
