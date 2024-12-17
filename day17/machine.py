from typing import *


class Machine():
    a: int = 0
    b: int = 0
    c: int = 0
    isp: int = 0
    __last_isp: int = -1

    def __init__(self, a: int, b: int, c: int):
        self.a = a
        self.b = b
        self.c = c

    def __call__(self, program: List[int]) -> List[int]:
        output: List[int] = []

        while 0 <= self.isp < len(program) and self.__last_isp != self.isp:
            operator = program[self.isp]
            operand = program[self.isp + 1]
            literal = operand
            combo = self.__combo_value(operand)
            forward_isp = True
            self.__last_isp = self.isp

            match operator:
                case 0:  # adv --- division
                    self.a = self.a // 2 ** combo
                case 1:  # bxl --- bitwise XOR
                    self.b = self.b ^ literal
                case 2:  # bst
                    self.b = combo % 8
                case 3:  # jnz
                    if self.a != 0:
                        self.isp = literal
                        forward_isp = False
                case 4:  # bxc
                    self.b = self.b ^ self.c
                case 5:  # out
                    output.append(combo % 8)
                case 6:  # bdv
                    self.b = self.a // 2 ** combo
                case 7:
                    self.c = self.a // 2 ** combo
                case _:
                    raise ValueError

            if forward_isp:
                self.isp += 2

        return output

    def __combo_value(self, operand: int) -> int:
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return self.a
            case 5:
                return self.b
            case 6:
                return self.c
            case _:
                raise ValueError
