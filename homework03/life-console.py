import curses

from life import GameOfLife
from ui import UI

from time import sleep

class Console(UI):


    def __init__(self, life: GameOfLife) -> None:
        
        super().__init__(life)


    def draw_borders(self, screen) -> None:
        
        r = self.life.rows + 1
        c = self.life.cols + 1
        self.screen = curses.newwin(r + 2, c + 2, 0, 0)
        for i in range(r + 1):
            for j in range(c + 1):
                if i == 0:
                    if j == 0 or j == c:
                        self.screen.addch(0, j, "+")
                    else:
                        self.screen.addch(0, j, "-")
                elif i == r:
                    if j == 0 or j == c:
                        self.screen.addch(i, j, "+")
                    else:
                        self.screen.addch(i, j, "-")
                else:
                    if j == 0 or j == c:
                        self.screen.addch(i, j, "|")
        self.screen.refresh()


    def draw_grid(self, screen) -> None:
        
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j] == 1:
                    self.screen.addch(i + 1, j + 1, "*")
        self.screen.refresh()
                    

    def run(self) -> None:
        
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        while True:
            self.screen.erase()
            self.draw_borders(self.screen)
            self.draw_grid(self.screen)
            sleep(1)
            self.life.step()
        curses.endwin()


life = GameOfLife((20, 20), max_generations=50)
ui = Console(life)
ui.run()
