import re


def get_multiplication_results(line: str):
    return sum(map(lambda match: int(match[1]) * int(match[2]), re.finditer(r'mul\((\d+),(\d+)\)', line)))


if __name__ == "__main__":
    sum_of_all_multiplications = 0

    while True:
        try:
            sum_of_all_multiplications += get_multiplication_results(input())
        except EOFError:
            break

    print(sum_of_all_multiplications)
