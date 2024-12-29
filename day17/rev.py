from typing import List, Dict, Set, Tuple
import sys


def run_equiv_puzzle_machine(a: int) -> List[int]:
    """Equivalent of the puzzle machine.
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

    # print(run_equiv_puzzle_machine(42))
    # sys.exit()

    a = 0

    for i, output_digit in enumerate(rev_output):
        ok = False

        for d in range(8):
            if ok:
                break

            output_fragment = puzzle_output_list[len(puzzle_output_list) - i - 1:]
            divisor = 2 ** (d ^ 1)

            for remainder in range(divisor):
                # a_cand = (a << 3 | d)
                a_cand = (a << 3 | d) + remainder
                # a_cand = a * divisor + remainder
                # a_cand = (a << 3) + remainder
                # a_cand = a + remainder
                partial_output = run_equiv_puzzle_machine(a_cand)
                new_d = a_cand % 8
                new_divisor = 2 ** (new_d ^ 1)

                # if (new_d ^ 5 ^ (a_cand // divisor)) % 8 == output_digit and partial_output == output_fragment:
                # if (new_d ^ 5 ^ (a_cand // new_divisor)) % 8 == output_digit:
                if partial_output == output_fragment:
                    a = a_cand
                    ok = True
                    break

        if not ok:
            raise ValueError

    print(a)
