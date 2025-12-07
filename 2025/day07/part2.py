import sys
from functools import reduce


if __name__ == "__main__":
    particles = {}
    for y, line in enumerate(sys.stdin.readlines()):
        for x, symbol in enumerate(line):
            match symbol:
                case "S":
                    particles[(x, y)] = 1
                case "^":
                    if (x, y) in particles:
                        count = particles.pop((x, y))
                        for new_pos in [(x-1, y), (x+1, y)]:
                            if new_pos in particles:
                                particles[new_pos] += count
                            else:
                                particles[new_pos] = count
        particles = {(x, y+1): count for (x, y), count in particles.items()}

    print(reduce(lambda acc, e: acc + e, particles.values(), 0))
