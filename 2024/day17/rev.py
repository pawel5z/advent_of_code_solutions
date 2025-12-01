"""Reconstructs the lowest possible A register value for which a machine
defined in puzzle input prints itself.
"""

from typing import List, Dict, Set, Tuple
import sys


def run_equiv_puzzle_machine(a: int) -> List[int]:
    """Equivalent of the machine from puzzle input.
    """
    result: List[int] = []

    digit = a % 8
    result.append((digit ^ 5 ^ (a // 2 ** (digit ^ 1))) % 8)
    a //= 8

    while a > 0:
        digit = a % 8
        result.append((digit ^ 5 ^ (a // 2 ** (digit ^ 1))) % 8)
        a //= 8

    return result


if __name__ == '__main__':
    puzzle_output_str: str = '2,4,1,1,7,5,1,4,0,3,4,5,5,5,3,0'
    puzzle_output_list: List[int] = list(map(int, puzzle_output_str.split(',')))
    rev_output = list(reversed(puzzle_output_list))
    # print(target_output)

    a = 0

    for i, output_digit in enumerate(rev_output):
        ok = False

        for d in range(8):
            if ok:
                break

            divisor = 2 ** (d ^ 1)

            for remainder in range(divisor):
                a_cand = (a << 3 | d) + remainder
                updated_d = a_cand % 8
                updated_divisor = 2 ** (updated_d ^ 1)

                if (updated_d ^ 5 ^ (a_cand // updated_divisor)) % 8 == output_digit:
                    a = a_cand
                    ok = True
                    break

        if not ok:
            raise ValueError

    print(a)
