from typing import Optional
import re


def calculate_prize_cost(ax: int, ay: int, bx: int, by: int, x: int, y: int) -> Optional[int]:
    determinant = ax * by - ay * bx
    try:
        a = (x * by - y * bx) / determinant
        b = (ax * y - ay * x) / determinant
    except ZeroDivisionError:
        return None

    if a != int(a) or b != int(b) or a >= 100 or b >= 100:
        return None

    return 3 * a + b


if __name__ == '__main__':
    result = 0

    while True:
        try:
            match = re.match(r'Button A: X\+(\d+), Y\+(\d+)', input())
            ax, ay = map(int, (match[1], match[2]))
            match = re.match(r'Button B: X\+(\d+), Y\+(\d+)', input())
            bx, by = map(int, (match[1], match[2]))
            match = re.match(r'Prize: X=(\d+), Y\=(\d+)', input())
            x, y = map(int, (match[1], match[2]))
            cost = calculate_prize_cost(ax, ay, bx, by, x, y)
            if cost is not None:
                result += cost
            input()
        except EOFError:
            break

    print(int(result))
