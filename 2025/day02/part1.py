import re

if __name__ == "__main__":
    total = 0
    for b, e in map(lambda e: tuple(map(int, e.split("-"))), input().split(",")):
        for n in range(b, e+1):
            if re.match(r"^(\d+)\1$", str(n)):
                # print(n)
                total += n
    print(total)
