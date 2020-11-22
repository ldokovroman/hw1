import pathlib
import typing as tp
from random import randint

T = tp.TypeVar("T")



def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid



def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """ Прочитать Судоку из указанного файла """
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку """
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(grid[row][col].center(width) + ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:

    a = []
    for i in range(0, n):
        b = []
        for j in range(n * i, n * (i + 1)):
            b.append(values[j])
        a.append(b)
        
    return a


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:

    a = grid[pos[0]]
    
    return a
    

def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    
    a = []
    for i in range(len(grid)):
        a.append(grid[i][pos[1]])

    return a


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:

    a = []
    x = pos[0] // 3
    y = pos[1] // 3
    for i in range(0, 3):
        for j in range(0, 3):
            a.append(grid[x * 3 + i][y * 3 + j])

    return a
            
def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:

    q = True
    i = 0
    while i < len(grid) and q == True:
        j = 0
        while j < len(grid) and q == True:
            if grid[i][j] == ".":
                q = False
                return i, j
            j = j + 1
        i = i + 1
    if q == True:
            return -1, -1

def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:

    a = set()
    b = [1] * 10
    c = get_row(grid, pos)
    for i in c:
        if i != '.' and b[int(i)] == 1:
            b[int(i)] = 0

    c = get_col(grid, pos)
    for i in c:
        if i != '.' and b[int(i)] == 1:
            b[int(i)] = 0

    c = get_block(grid, pos)
    for i in c:
        if i != '.' and b[int(i)] == 1:
            b[int(i)] = 0
            
    for i in range(1, 10):
        if b[i] == 1:
            a.add(str(i))
            
    return a
    

def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:

    y, x = find_empty_positions(grid)
    if y == -1:
        return grid
    a = find_possible_values(grid, (y, x))
    if len(a) == 0:
        return grid
    for i in a:
        grid[y][x] = i
        b = solve(grid)
        if find_empty_positions(b)[0] == -1:
            return b
        grid[y][x] = "."
    return grid
        

def check_solution(solution: tp.List[tp.List[str]]) -> bool:

    for i in range(len(solution)):
        for j in range(len(solution)):
            a = [0] * 10
            b = get_row(solution, (i, j))
            for k in b:
                if k == '.' or a[int(k)] == 1:
                    return False
                a[int(k)] = 1

            a = [0] * 10
            b = get_col(solution, (i, j))
            for k in b:
                if k == '.' or a[int(k)] == 1:
                    return False
                a[int(k)] = 1

            a = [0] * 10
            b = get_block(solution, (i, j))
            for k in b:
                if k == '.' or a[int(k)] == 1:
                    return False
                a[int(k)] = 1

        return True
       
    

def generate_sudoku(N: int) -> tp.List[tp.List[str]]:

    grid = []
    for i in range(0, 9):
        grid.append(['.'] * 9)
    y, x = randint(0, 8), randint(0, 8)
    grid[y][x] = str(randint(1, 9))
    grid = solve(grid)
    n = 81 - N
    while n > 0:
        y, x = randint(0, 8), randint(0, 8)
        if grid[y][x] != '.':
            grid[y][x] = '.'
            n = n - 1
    return grid



if __name__ == '__main__':
    for fname in ['puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt']:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
