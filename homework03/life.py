import pathlib
import random
import pygame

from pygame.locals import *
from typing import List, Optional, Tuple


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    
    def __init__(
        self,
        size: Tuple[int, int],
        randomize: bool=True,
        max_generations: Optional[float]=float('inf')
    ) -> None:
     
        self.rows, self.cols = size
        self.prev_generation = self.create_grid()
        self.curr_generation = self.create_grid(randomize=randomize)
        self.max_generations = max_generations
        self.generations = 1


    def create_grid(self, randomize: bool=False) -> Grid:

        grid = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                if randomize:
                    cell = random.randint(0,1)
                else:
                    cell = 0
                row.append(cell)
            grid.append(row)
        return grid


    def get_neighbours(self, cell: Cell) -> Cells:

        cells = []
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if 0 <= i < self.rows and 0 <= j < self.cols and not(i == cell[0] and j == cell[1]):
                    cells.append(self.curr_generation[i][j])
        return cells
       

    def get_next_generation(self) -> Grid:

        new_grid = self.create_grid()
        for i in range(self.rows):
            for j in range(self.cols):
                k = sum(self.get_neighbours((i, j)))
                if self.curr_generation[i][j] == 0:
                    if k == 3:
                        new_grid[i][j] = 1
                    else:
                        new_grid[i][j] = 0
                else:
                    if k == 2 or k == 3:
                        new_grid[i][j] = 1
                    else:
                        new_grid[i][j] = 0
        return new_grid
        

    def step(self) -> None:
        
        self.prev_generation = self.curr_generation.copy()
        self.curr_generation = self.get_next_generation()
        self.generations += 1
        

    @property
    def is_max_generations_exceeded(self) -> bool:

        return self.generations <= self.max_generations
      

    @property
    def is_changing(self) -> bool:

        return self.prev_generation != self.curr_generation

       
    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        
        with open('grid.txt', 'r') as f:
            a = [i.split() for i in f]
            b = [list(str(a[i][0])) for i in range(len(a))]
            c = [[int(j) for j in b[i]] for i in range(len(b))]
            return c


    def save(self, filename: pathlib.Path) -> None:

        f = open('save.txt', 'w')
        a = [''.join(map(str, self.curr_generation[i])) for i in range(len(self.curr_generation))]
        b = '\n'.join(a)
        f.write(str(b))   
        f.close()


#random.seed(1234)       
#life = GameOfLife((5, 5))
#print(life.curr_generation)
#print(life.from_file(pathlib.Path('grid.txt')))
#life.save(pathlib.Path('save.txt'))
#life.step()
#print(life.prev_generation)
#print(life.curr_generation)


        
