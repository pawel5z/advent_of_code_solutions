from typing import *
from tqdm import tqdm
import sys
import re


mem: Dict[str, int] = {}


def count_divisions(string: str, patterns: List[str]) -> int:
    if string == '':
        return 1

    if string in mem.keys():
        return mem[string]

    mem[string] = 0

    for pattern in patterns:
        if string[:len(pattern)] == pattern:
            mem[string] += count_divisions(string[len(pattern):], patterns)

    return mem[string]


if __name__ == '__main__':
    patterns: List[str] = list(map(lambda s: s.strip(), input().split(',')))
    # print(patterns)
    input()

    result = 0

    for string in sys.stdin.readlines():
        string = string.strip()
        # print(string)
        result += count_divisions(string, patterns)

    print(result)
