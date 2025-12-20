import sys
from shapes import *


if __name__ == "__main__":
    shapes: list[Shape] = []
    fittable_region_count = 0

    reading_shape: bool = False
    shape_lines: list[str] = []
    for line in sys.stdin.readlines():
        if ":" in line and not "x" in line:
            shape_lines = []
            reading_shape = True
            continue
        elif line.isspace():
            shapes.append(Shape(shape_lines))
            reading_shape = False
            continue
        elif reading_shape:
            shape_lines.append(line.strip())
        else:
            # regions to the end
            dim_str, shape_counts_str = line.split(":")
            w, h = tuple(map(int, dim_str.split("x")))
            shape_counts = list(map(int, shape_counts_str.split()))

            min_required_space = sum(shape_count * shapes[i].space for i, shape_count in enumerate(shape_counts))
            print(min_required_space, w * h)
            if min_required_space <= w * h:
                fittable_region_count += 1


    # for shape in shapes:
    #     print(shape.space)
    #     print(shape.coords)

    print(fittable_region_count)
