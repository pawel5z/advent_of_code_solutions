from typing import List
import re
import numpy as np


def word_search_to_ndarray(ws: List[str]) -> np.ndarray:
    return np.array([list(row) for row in word_search])


def ndarray_to_word_search(a: np.ndarray) -> List[str]:
    return list(''.join(row) for row in a.tolist())


def get_cross_mas_count_horizontally(word_search: List[str]) -> int:
    return sum(len(re.findall(r'MAS', row)) + len(re.findall(r'SAM', row)) for row in word_search)


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

    total_cross_mas_count = 0
    word_search: np.ndarray = word_search_to_ndarray(word_search)
    for r in range(word_search.shape[0] - 3 + 1):
        for c in range(word_search.shape[1] - 3 + 1):
            ws_part = word_search[r: r+3, c: c+3]
            mas_count = 0
            mas_count += get_cross_mas_count_horizontally(
                diagonalize_word_search(ndarray_to_word_search(ws_part)))
            mas_count += get_cross_mas_count_horizontally(
                diagonalize_word_search(flip_word_search(ndarray_to_word_search(ws_part))))
            if mas_count == 2:
                total_cross_mas_count += 1

    print(total_cross_mas_count)
