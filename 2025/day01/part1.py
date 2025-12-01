import fileinput

if __name__ == "__main__":
    position = 50
    position_zero_count = 0

    for rotation_text in fileinput.input():
        rotation_text = rotation_text.strip()

        coeff = 1
        match rotation_text[0]:
            case "L":
                coeff = -1
        position = (position + coeff * int(rotation_text[1:])) % 100

        if position == 0:
            position_zero_count += 1

    print(position_zero_count)
