from typing import List
import re
import numpy as np


def get_xmas_count_horizontally(word_search: List[str]) -> int:
    return sum(len(re.findall(r'XMAS', row)) + len(re.findall(r'SAMX', row)) for row in word_search)


def transpose_word_search(word_search: List[str]) -> List[str]:
    return list(''.join(row) for row in np.array([list(row) for row in word_search]).T.tolist())


def flip_word_search(word_search: List[str]) -> List[str]:
    return list(''.join(row) for row in np.fliplr(np.array([list(row) for row in word_search])).tolist())


def diagonalize_word_search(word_search: List[str]) -> List[str]:
    a = np.array([list(row) for row in word_search])
    a_diag_length = np.diag(a).size
    diagonalized_a = np.full((sum(a.shape) - 1, a_diag_length), '.')

    # Copy main diagonal and upper part.
    for i in range(0, a.shape[1]):
        diag = np.diag(a, i)
        diagonalized_a[
            a.shape[1] - 1 - i,
            a_diag_length - diag.size:
        ] = diag

    # Copy lower part.
    for i in range(1, a.shape[0]):
        diag = np.diag(a, -i)
        diagonalized_a[
            a.shape[1] - 1 + i,
            a_diag_length - diag.size:
        ] = diag

    return list(''.join(row) for row in diagonalized_a.tolist())


if __name__ == "__main__":
    word_search: List[str] = []

    while True:
        try:
            word_search.append(input())
        except EOFError:
            break

    print(
        get_xmas_count_horizontally(word_search)
        + get_xmas_count_horizontally(transpose_word_search(word_search))
        + get_xmas_count_horizontally(diagonalize_word_search(word_search))
        + get_xmas_count_horizontally(diagonalize_word_search(flip_word_search(word_search)))
    )
