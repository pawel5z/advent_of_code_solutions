from typing import List, Callable, Iterable
import itertools
import operator


def int_concat(a: int, b: int) -> int:
    return int(str(a) + str(b))


def is_possible_to_produce(test_value: int, operands: List[int]) -> bool:
    operators = [operator.add, operator.mul, int_concat]
    for op_sequence in itertools.product(operators, repeat=len(operands) - 1):
        result = operands[0]
        for op, operand in zip(op_sequence, operands[1:]):
            result = op(result, operand)
        if result == test_value:
            return True
    return False


if __name__ == "__main__":
    result = 0

    while True:
        try:
            test_value_text, operands_text = tuple(input().split(':'))
            test_value = int(test_value_text)
            if is_possible_to_produce(test_value, list(map(int, operands_text.split()))):
                result += test_value
        except EOFError:
            break

    print(result)
