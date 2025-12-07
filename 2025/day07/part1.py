import sys


if __name__ == "__main__":
    beams = set()
    split_count = 0
    for y, line in enumerate(sys.stdin.readlines()):
        for x, symbol in enumerate(line):
            match symbol:
                case "S":
                    beams.add((x, y))
                case "^":
                   if (x, y) in beams:
                       beams.remove((x, y))
                       beams.update([(x-1, y), (x+1, y)])
                       split_count += 1
        beams = {(x, y+1) for x, y in beams}

    print(split_count)
