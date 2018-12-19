from typing import NamedTuple, List
import re

TESTINPUT = """position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>"""

rgx = "position=<(.*)> velocity=<(.*)>"

class Star:
    def __init__(self, x: int, y: int, dx: int, dy: int):
        self.x, self.y = x, y
        self.dx, self.dy = dx, dy

    def step(self, num_steps: int=1):
        self.x += num_steps * self.dx
        self.y += num_steps * self.dy

        return self

    @staticmethod
    def from_line(line: str) -> 'Star':
        pos, velo = re.match(rgx, line).groups()
        x, y = [int(p) for p in pos.split(',')]
        dx, dy = [int(v) for v in velo.split(',')]

        return Star(x, y, dx, dy)

    def __repr__(self) -> str:
        return f"Star(x={self.x}, y={self.y}, dx={self.dx}, dy={self.dy})"

def show(stars: List[Star]) -> str:
    locations = set()
    for star in stars:
        locations.add((star.x, star.y))
 
    xx = [star.x for star in stars]
    yy = [star.y for star in stars]

    min_x, max_x = min(xx), max(xx)
    min_y, max_y = min(yy), max(yy)


    grid = [['#' if (x, y) in locations else '.'
            for x in range(min_x, max_x+1)]
            for y in range(min_y, max_y+1)]

    return "\n".join("".join(row) for row in grid)

def grid_size(stars: List[Star]) -> int:
    xx = [star.x for star in stars]
    yy = [star.y for star in stars]

    min_x, max_x = min(xx), max(xx)
    min_y, max_y = min(yy), max(yy)

    return (max_x - min_x) * (max_y - min_y)

if __name__ == "__main__":
    testlines = TESTINPUT.split('\n')
    teststars = [Star.from_line(line) for line in testlines]
    
    with open("input.txt") as f:
        lines = [line.strip() for line in f]

    stars = [Star.from_line(line) for line in lines]
    
    for star in stars:
        star.step(10100)
    for i in range(10):
        print(i, grid_size(stars))
        print(show(stars))
        for star in stars:
            star.step()
        
        


        