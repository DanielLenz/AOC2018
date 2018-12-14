from typing import Tuple, List, NamedTuple, Dict
from collections import Counter

TESTRAW = """1, 1
1, 6
8, 3
3, 4
5, 5
8, 9"""

TESTRESULT = 17

class Point(NamedTuple):
    x: int
    y: int

    def manhattan_distance(self, other: 'Point') -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    @staticmethod
    def from_line(line: str) -> 'Point':
        x, y = line.split(", ")
        return Point(int(x), int(y))

    def total_manhattan_distance(self, others: List["Point"]) -> int:
        return sum(self.manhattan_distance(point) for point in others)

def closests(points: List[Point]) -> Dict[Point, int]:
    min_x, min_y, max_x, max_y = minmax_from_points(points)

    grid = {}

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            this = Point(x, y)
            distances = [
                (this.manhattan_distance(point), i)
                for i, point in enumerate(points)]
            
            distances.sort()

            if distances[0][0] == distances[1][0]:
                # If two closest points are equally close
                grid[this] = None
            else:
                grid[this] = distances[0][1]
    
    return grid

def minmax_from_points(points: List[Point]) -> Tuple[int]:
    min_x = min(point.x for point in points)
    min_y = min(point.y for point in points)
    max_x = max(point.x for point in points)
    max_y = max(point.y for point in points)

    return min_x, min_y, max_x, max_y


def largest_finite_grid(grid: Dict[Point, int]) -> int:
    min_x, min_y, max_x, max_y = minmax_from_points(grid)

    boundary_idx = set()
    for point, idx in grid.items():
        if point.x in (min_x, max_x) or point.y in (min_y, max_y):
            boundary_idx.add(idx)

    c = Counter()
    for point, idx in grid.items():
        if idx not in boundary_idx:
            c[idx] += 1

    return c.most_common(1)[0][1]


def count_points_within(points: List[Point], total_distance: int) -> int:
    """Count number of points with distances within a certain upper limit."""
    min_x, min_y, max_x, max_y = minmax_from_points(points)
    
    count = 0
    for x in range(min_x, max_x + 1):
        print(min_x, x, max_x)
        for y in range(min_y, max_y + 1):
            if Point(x, y).total_manhattan_distance(points) < total_distance:
                count += 1

    return count


if __name__ == "__main__":
    testlines = TESTRAW.split('\n')
    testpoints = [Point.from_line(line) for line in testlines]
    
    with open('input.txt') as f:
        points = [Point.from_line(line.strip()) for line in f]


    testgrid = closests(testpoints)
    grid = closests(points)

    # print(largest_finite_grid(testgrid))
    print(largest_finite_grid(grid))

    # print(count_points_within(testpoints, total_distance=32))
    print(count_points_within(points, total_distance=10000))