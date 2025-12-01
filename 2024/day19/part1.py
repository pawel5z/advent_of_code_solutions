from typing import *
from tqdm import tqdm
import sys
import re


if __name__ == '__main__':
    patterns: List[str] = list(map(lambda s: s.strip(), input().split(',')))
    # print(patterns)
    input()

    result = 0
    regex = f'({'|'.join(patterns)})+'
    # print(regex)

    for string in tqdm(sys.stdin.readlines()):
        if re.fullmatch(regex, string.strip()):
            # print(string)
            result += 1

    print(result)
