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

    l1 = np.array(sorted(l1))
    l2 = np.array(sorted(l2))

    print(np.abs(l1 - l2).sum())
