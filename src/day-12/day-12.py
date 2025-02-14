from dataclasses import dataclass
from enum import Enum, auto
from typing import NamedTuple


def input_multiline() -> str:
    contents = []
    print("Enter/Paste your content. Ctrl-D or Ctrl-Z ( windows ) to save it.")
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)
    return "\n".join(contents)


class Direction(Enum):
    UP = auto()
    LEFT = auto()
    DOWN = auto()
    RIGHT = auto()


class Position(NamedTuple):
    x: int
    y: int

    def get_orthogonal_positions(self):
        return {
            Position(self.x + c.x, self.y + c.y)
            for c in {
                Position(0, 1),
                Position(0, -1),
                Position(1, 0),
                Position(-1, 0),
            }
        }


class Fence(NamedTuple):
    pos: Position
    side: Direction

    def get_side_adjacent_fences(self) -> set["Fence"]:
        if self.side in {Direction.LEFT, Direction.RIGHT}:
            return {
                Fence(Position(self.pos.x, self.pos.y + 1), self.side),
                Fence(Position(self.pos.x, self.pos.y - 1), self.side),
            }
        else:
            return {
                Fence(Position(self.pos.x + 1, self.pos.y), self.side),
                Fence(Position(self.pos.x - 1, self.pos.y), self.side),
            }


@dataclass
class Region:
    plant: str
    positions: set[Position]
    fences: set[Fence]

    def __init__(self, plant: str, positions: set[Position], perimeter: set[Position]):
        self.plant = plant
        self.positions = positions
        self.fences = self._make_fences(positions, perimeter)

    def _make_fences(
        self, positions: set[Position], perimeter: set[Position]
    ) -> set[Fence]:
        fences: set[Fence] = set()
        for s in positions:
            fences.update(
                {
                    Fence(position, dir)
                    for position, dir in {
                        (Position(s.x + 1, s.y), Direction.RIGHT),
                        (Position(s.x - 1, s.y), Direction.LEFT),
                        (Position(s.x, s.y + 1), Direction.DOWN),
                        (Position(s.x, s.y - 1), Direction.UP),
                    }
                    if position in perimeter
                }
            )
        return fences


class Farm:
    regions: list[Region]

    _position_to_plant: dict[Position, str]

    def __init__(self, input: str):
        grid = [[c for c in line] for line in input.strip().splitlines()]
        plants: dict[Position, str] = dict()
        for y, row in enumerate(grid):
            for x, plant_type in enumerate(row):
                plants[Position(x, y)] = plant_type

        self._position_to_plant = plants
        self._make_regions()

    def _make_regions(self):
        regions: list[Region] = list()
        unassigned: set[Position] = set(self._position_to_plant)
        while len(unassigned) > 0:
            position = unassigned.pop()
            new_region = self._make_region(position)
            regions.append(new_region)
            unassigned = unassigned - new_region.positions

        self.regions = regions

    def _make_region(
        self,
        region_root: Position,
    ):
        region_plant_type = self._position_to_plant[region_root]
        region_positions: set[Position] = set()
        perimeter: set[Position] = set()

        region_edge: set[Position] = set([region_root])
        while len(region_edge) > 0:
            current_position = region_edge.pop()
            region_positions.add(current_position)
            for candidate in current_position.get_orthogonal_positions():
                if candidate in region_positions:
                    continue
                elif (
                    candidate in self._position_to_plant
                    and self._position_to_plant[candidate] == region_plant_type
                ):
                    region_edge.add(candidate)
                else:
                    perimeter.add(candidate)

        return Region(
            region_plant_type,
            region_positions,
            perimeter,
        )


def solution(input_value: str):
    farm = Farm(input_value)

    total = sum((len(region.positions) * len(region.fences) for region in farm.regions))
    return str(total)


def solution_two(input_value: str):
    farm = Farm(input_value)
    total = 0
    for section in farm.regions:
        sides = get_sides(section.fences)
        total += len(section.positions) * len(sides)
    return str(total)


def get_sides(fence: set[Fence]) -> list[set[Fence]]:
    sides: list[set[Fence]] = list()
    unsided_fence: set[Fence] = set(fence)

    while len(unsided_fence) > 0:
        start_of_side = unsided_fence.pop()
        side = make_side(unsided_fence, start_of_side)
        unsided_fence = unsided_fence - side
        sides.append(side)

    return sides


def make_side(unsided_fence: set[Fence], start_of_side: Fence) -> set[Fence]:
    side: set[Fence] = set()
    side_edge = set([start_of_side])
    while len(side_edge) > 0:
        current = side_edge.pop()
        side.add(current)
        new_edge_fences = {
            adjacent_fence
            for adjacent_fence in current.get_side_adjacent_fences()
            if adjacent_fence in unsided_fence and adjacent_fence not in side
        }

        side_edge.update(new_edge_fences)
    return side


if __name__ == "__main__":
    input = input_multiline()
    print(solution(input))
    print(solution_two(input))
