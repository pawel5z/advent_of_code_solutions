import sys
from functools import reduce
import operator


if __name__ == "__main__":
    LENGTH = 12
    total_output_joltage = 0
    for bank in sys.stdin.readlines():
        batteries_indices = [(bat, i) for i, bat in enumerate(map(int, bank.strip()))]
        digits = []
        prev_digit_idx = -1
        for i in range(LENGTH):
            digit, prev_digit_idx = max(
                batteries_indices[prev_digit_idx + 1 : len(batteries_indices) - (LENGTH - i - 1)],
                key=lambda e: e[0]
            )
            digits.append(digit)
        total_output_joltage += reduce(lambda acc, e: acc * 10 + e, digits, 0)
    print(total_output_joltage)
