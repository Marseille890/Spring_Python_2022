import pathlib
import typing as tp
import random

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """ Прочитать Судоку из указанного файла """
    with open(path) as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """ Вывод Судоку """
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values, n):
    """ Сгруппировать значения values в список, состоящий из списков по n элементов
        >>> group([1,2,3,4], 2)
        [[1, 2], [3, 4]]
        >>> group([1,2,3,4,5,6,7,8,9], 3)
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        """
    new_values = list()
    for i in range(n):
        new_values.append(values[(i * n):((i + 1) * n)])
    return new_values


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """ Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """ Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    return [i[pos[1]] for i in grid]


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """ Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    rows = pos[0] // 3
    cols = pos[1] // 3
    block = []
    for i in range(rows * 3, (rows + 1) * 3):
        for j in range(cols * 3, (cols + 1) * 3):
            block.append(grid[i][j])
    return block


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """ Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == '.':
                return (i, j)


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """ Вернуть множество всех возможных значений для указанной позиции

    >>> grid = read_sudoku('puzzles/puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> set(values) == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> set(values) == {'2', '5', '9'}
    True
    """
    possible_values = set()
    for i in '1234456789':
        if i not in get_row(grid, pos) and i not in get_col(grid, pos) and i not in get_block(grid, pos):
            possible_values.add(str(i))
    return possible_values


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла

    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """

    empty_position = find_empty_positions(grid)

    if empty_position is None:  # Судоку решен
        return grid
    else:
        possible_values = find_possible_values(grid, empty_position)
        for i in '123456789':
            if i in possible_values:
                grid[empty_position[0]][empty_position[1]] = i  
                if find_empty_positions(grid) is not None:  
                    solve(grid)
                    if find_empty_positions(grid) is None: 
                        return grid
            if i == '9':
                if find_empty_positions(grid) is None:
                    return grid
                grid[empty_position[0]][empty_position[1]] = '.'

def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """
    # TODO: Add doctests with bad puzzles
    for i in range(len(solution)):
        for j in range(len(solution)):
            if get_row(solution, (i, j)).count(solution[i][j]) + get_col(solution, (i, j)).count(solution[i][j]) + get_block(solution, (i, j)).count(solution[i][j]) != 3 or solution[i][j] == '.':
                return False
    return True


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    sudoku = [['.' for i in range(9)] for j in range(9)]  # Пустой судоку

    # Заполняем диагональные блоки судоку рандомными числами
    for k in range(3):  # Фиксируем блок
        used_values = ''
        for row in range(k * 3, (k + 1) * 3):  # Фиксируем строку в блоке
            col = k * 3  # Начальный столбец в блоке
            while col < (k + 1) * 3:  # Пока столбец не достигнет конечного в блоке
                val = str(random.randint(1, 9))
                if val not in used_values:
                    sudoku[row][col] = val
                    used_values += val
                    col += 1
    solve(sudoku)

    # В решенном судоку рандомно оставляем только N элементов
    k = 0
    while k < (81 - N):
        i = random.randint(0, 8)
        j = random.randint(0, 8)
        if sudoku[i][j] != '.':
            sudoku[i][j] = '.'
            k += 1
    return sudoku


if __name__ == "__main__":
    for fname in ["/Users/sofia.dibel/Documents/pybook-assignments-master/homework02/puzzle1.txt", "/Users/sofia.dibel/Documents/pybook-assignments-master/homework02/puzzle2.txt", "/Users/sofia.dibel/Documents/pybook-assignments-master/homework02/puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)