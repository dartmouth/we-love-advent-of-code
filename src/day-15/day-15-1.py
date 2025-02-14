def step(direction):

    dir_chg = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}

    return dir_chg[direction]


def push(locations, start, direction):

    to_move = []  # stack
    d_r, d_c = step(direction)
    robot_loc = start

    r, c = robot_loc
    while locations[r][c] not in (".", "#"):
        to_move.append((locations[r][c], r, c))
        r = r + d_r
        c = c + d_c

    if locations[r][c] == ".":
        while to_move:
            item, old_row, old_col = to_move.pop(-1)
            new_row = old_row + d_r
            new_col = old_col + d_c
            locations[new_row][new_col] = item
            if item == "@":
                locations[old_row][old_col] = "."
                robot_loc = new_row, new_col

    return robot_loc


def find_robot(locations):

    for r, row in enumerate(locations):
        try:
            return r, row.index("@")
        except:
            continue

    raise ValueError("No robot found in locations.")


def final_box_coords(locations):

    box_coords = []
    for r, row in enumerate(locations):
        for c, item in enumerate(row):
            if locations[r][c] == "O":
                box_coords.append((r, c))

    return box_coords


def sum_box_coords(locations, directions):
    """
    >>> sum_box_coords(*get_input('15-test-sm.txt'))
    2028
    >>> sum_box_coords(*get_input('15-test.txt'))
    10092
    """

    curr = find_robot(locations)

    for direction in directions:
        curr = push(locations, curr, direction)

    return sum((100 * r + c for r, c in final_box_coords(locations)))


def get_input(filename):

    with open(filename) as f:
        raw_locations, raw_directions = f.read().split("\n\n")

    locations = [list(row) for row in raw_locations.splitlines()]

    return locations, raw_directions.replace("\n", "")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(sum_box_coords(*get_input("src/day-15/input.txt")))
