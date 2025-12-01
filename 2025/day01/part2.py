import fileinput
import math

if __name__ == "__main__":
    position = 50
    position_zero_count = 0
    zero_transition_count = 0

    for rotation_text in fileinput.input():
        rotation_text = rotation_text.strip()

        coeff = 1
        match rotation_text[0]:
            case "L":
                coeff = -1

        rot_dist_to_zero = 0
        if position != 0:
            rot_dist_to_zero = position if coeff == -1 else 100 - position

        rot_dist = int(rotation_text[1:])

        # Count in transition through zero with reminider of full rotation.
        if position != 0 and rot_dist % 100 > rot_dist_to_zero:
            zero_transition_count += 1

        # Count in number of periods.
        zero_transition_count += math.floor(rot_dist / 100)

        position = (position + coeff * rot_dist) % 100
        if position == 0:
            position_zero_count += 1

    print(position_zero_count + zero_transition_count)
