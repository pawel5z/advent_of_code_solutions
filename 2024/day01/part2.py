import numpy as np

if __name__ == "__main__":
    l1, l2 = [], []
    while True:
        try:
            input_list = input().split()
        except EOFError:
            break

        e1, e2 = int(input_list[0]), int(input_list[1])
        l1.append(e1)
        l2.append(e2)

    unique_l2 = set(l2)
    l2_occurrences = dict()
    for e2 in unique_l2:
        l2_occurrences[e2] = 0
        for e in l2:
            if e2 == e:
                l2_occurrences[e2] += 1

    total_similiarity_score = 0
    for e1 in l1:
        total_similiarity_score += e1 * l2_occurrences.get(e1, 0)
    print(total_similiarity_score)
