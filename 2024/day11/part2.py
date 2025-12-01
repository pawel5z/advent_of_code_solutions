from typing import List, Dict, Tuple
from tqdm import tqdm

mem: Dict[Tuple[int, int], int] = {}
BLINK_COUNT = 75


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


def eval_stones(stones: List[int], depth: int) -> int:
    if depth == BLINK_COUNT:
        return len(stones)

    result = 0

    for stone in stones:
        value = mem.get((stone, depth))

        if value is not None:
            result += value
            continue

        substones = blink([stone])
        stone_eval = eval_stones(substones, depth + 1)
        mem[(stone, depth)] = stone_eval
        result += stone_eval

    return result


if __name__ == '__main__':
    stones: List[int] = list(map(int, input().split()))

    # print(stones)

    print(eval_stones(stones, 0))
