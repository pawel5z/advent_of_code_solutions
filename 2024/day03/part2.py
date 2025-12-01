import re
import sys


def get_multiplication_results(line: str):
    correct_instructions = re.finditer(r'do\(\)|don\'t\(\)|mul\((\d+),(\d+)\)', line)
    enabled = True
    result = 0
    for instruction in correct_instructions:
        match instruction[0]:
            case 'do()':
                enabled = True
            case 'don\'t()':
                enabled = False
            case _:
                if enabled:
                    result += int(instruction[1]) * int(instruction[2])
    return result


if __name__ == "__main__":
    print(get_multiplication_results(sys.stdin.read()))
