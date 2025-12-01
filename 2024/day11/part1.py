from typing import List


def blink(stones: List[int]) -> List[int]:
    result = []

    for stone in stones:
        if stone == 0:
            result.append(1)
        elif len(str(stone)) % 2 == 0:
            stone_string = str(stone)
            result.append(int(stone_string[:len(stone_string) // 2]))
            result.append(int(stone_string[len(stone_string) // 2:]))
        else:
            result.append(stone * 2024)

    return result


if __name__ == '__main__':
    stones: List[int] = list(map(int, input().split()))

    # print(stones)

    for _ in range(25):
        stones = blink(stones)

    print(len(stones))
