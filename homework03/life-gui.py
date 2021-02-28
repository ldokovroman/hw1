import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):

    def __init__(self, life: GameOfLife, cell_size: int=10, speed: int=10) -> None:

        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.screen = pygame.display.set_mode((life.rows, life.cols))
        self.life.rows=life.rows//self.cell_size
        self.life.cols=life.cols//self.cell_size
        self.width = life.rows * self.cell_size
        self.height = life.cols * self.cell_size


    def draw_lines(self) -> None:

        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (0, y), (self.width, y))
        
        

    def draw_grid(self) -> None:

        for i in range(self.life.cols):
            for j in range(self.life.rows):
                x = j * self.cell_size
                y = i * self.cell_size
                if self.life.curr_generation[i][j] == 1:
                    pygame.draw.rect(self.screen, pygame.Color('green'), (x, y, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'), (x, y, self.cell_size, self.cell_size))
        

    def run(self) -> None:

        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        running = True
        pausa=False
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button==1:
                        x_mouse, y_mouse = pygame.mouse.get_pos()
                        column = x_mouse // self.cell_size
                        row = y_mouse // self.cell_size
                        self.life.curr_generation=life.prev_generation
                        if self.life.curr_generation[row][column] == 0:
                            self.life.curr_generation[row][column] = 1
                        else:
                            self.life.curr_generation[row][column] = 0                        
                        self.draw_grid()                      
                        self.draw_lines()
                        pygame.display.flip()
                if event.type == pygame.KEYDOWN:
                    if event.key==K_SPACE:
                        pausa = not pausa
            if not pausa and self.lifeis_max_generations_exceeded and self.life.is_changing:
                self.draw_grid()
                self.draw_lines()
                pygame.display.flip()
                clock.tick(self.speed)
                self.life.step()

life = GameOfLife((250, 250),False)
gui = GUI(life, 20)
gui.run()





        
