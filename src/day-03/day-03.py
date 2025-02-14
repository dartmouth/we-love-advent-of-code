import re


def mul(x, y):
    return x * y


def part_01(memory):
    instructions = re.findall(pattern=r"mul\([0-9]+,[0-9]+\)", string=memory)
    return sum(map(eval, instructions))


def part_02(memory):
    cleaned_memory = re.sub(
        pattern=r"don't\(\).*?do\(\)", repl="", string=memory, flags=re.DOTALL
    )
    return part_01(cleaned_memory)


if __name__ == "__main__":
    with open("src/day-03/input.txt") as f:
        memory = f.read()

    print(part_01(memory))
    print(part_02(memory))
