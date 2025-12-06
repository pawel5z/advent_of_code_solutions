import sys
from functools import reduce


if __name__ == "__main__":
    worksheet: list[str] = []
    operators: list[str] = []

    for line in sys.stdin.readlines():
        if "+" in line or "*" in line:
            operators = line.split()
        else:
            worksheet.append(line.rstrip("\n"))

    width = len(worksheet[0])
    columns: list[list[int]] = []

    height = len(worksheet)
    columns.append([])
    for c in range(width):
        is_separator = True
        for r in range(height):
            if worksheet[r][c] != " ":
                is_separator = False
                break
        if is_separator:
            columns.append([])
            continue

        number = 0
        for r in range(height):
            digit = worksheet[r][c]
            if digit == " " and number != 0:
                break
            number = number * 10 + (int(digit) if digit != " " else 0)
        columns[-1].append(number)

    total = 0
    for i, op in enumerate(operators):
        match op:
            case "+":
                total += reduce(lambda acc, e: acc + e, columns[i], 0)
            case "*":
                total += reduce(lambda acc, e: acc * e, columns[i], 1)

    print(total)
