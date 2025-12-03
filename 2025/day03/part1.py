import os
import sys

if __name__ == "__main__":
    total_output_joltage = 0
    for bank in sys.stdin.readlines():
        batteries_indices = [(bat, i) for i, bat in enumerate(map(int, bank.strip()))]
        tens_digit, tens_digit_idx = max(batteries_indices[:-1], key=lambda e: e[0])
        units_digit, _ = max(batteries_indices[tens_digit_idx + 1:], key=lambda e: e[0])
        total_output_joltage += tens_digit * 10 + units_digit
    print(total_output_joltage)
