#!/usr/bin/env python3
"""
Author : schackartk
Date   : 2019-04-17
Purpose: Generate a game of sudoku
"""

import argparse
import sys
import random
import re


# --------------------------------------------------
def get_args():
    """get command-line arguments"""
    parser = argparse.ArgumentParser(
        description='Commandline Sudoku game',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        '-d',
        '--difficulty',
        help='Game difficulty (E)asy, (M)edium, or (H)ard)',
        metavar='str',
        type=str,
        required=True)

    parser.add_argument(
        '-s', '--seed', help='A seed to allow for testing', action='store_true')

    parser.add_argument(
        '-t', '--tip', help='Color bad placements', action='store_true')

    parser.add_argument(
        '-c', '--coloroff', help='Turn off coloring for testing', action='store_true')

    return parser.parse_args()


# --------------------------------------------------
class color:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'


# --------------------------------------------------
def warn(msg):
    """Print a message to STDERR"""
    print(msg, file=sys.stderr)


# --------------------------------------------------
def die(msg='Something bad happened'):
    """warn() and exit with error"""
    warn(msg)
    sys.exit(1)


# --------------------------------------------------
def make_board(diff):
    cells = [[], [], [], [], [], [], [], [], []]

    if diff == 'E':
        cells[0] = [' ', ' ', ' ', 'b', 'f', ' ', 'g', ' ', 'a']
        cells[1] = ['f', 'h', ' ', ' ', 'g', ' ', ' ', 'i', ' ']
        cells[2] = ['a', 'i', ' ', ' ', ' ', 'd', 'e', ' ', ' ']
        cells[3] = ['h', 'b', ' ', 'a', ' ', ' ', ' ', 'd', ' ']
        cells[4] = [' ', ' ', 'd', 'f', ' ', 'b', 'i', ' ', ' ']
        cells[5] = [' ', 'e', ' ', ' ', ' ', 'c', ' ', 'b', 'h']
        cells[6] = [' ', ' ', 'i', 'c', ' ', ' ', ' ', 'g', 'd']
        cells[7] = [' ', 'd', ' ', ' ', ' ', 'e', ' ', 'c', 'f']
        cells[8] = ['g', ' ', 'c', ' ', 'a', 'h', ' ', ' ', ' ']

    if diff == 'M':
        cells[0] = [' ', 'b', ' ', 'f', ' ', 'h', ' ', ' ', ' ']
        cells[1] = ['e', 'h', ' ', ' ', ' ', 'i', 'g', ' ', ' ']
        cells[2] = [' ', ' ', ' ', ' ', 'd', ' ', ' ', ' ', ' ']
        cells[3] = ['c', 'g', ' ', ' ', ' ', ' ', 'e', ' ', ' ']
        cells[4] = ['f', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'd']
        cells[5] = [' ', ' ', 'h', ' ', ' ', ' ', ' ', 'a', 'c']
        cells[6] = [' ', ' ', ' ', ' ', 'b', ' ', ' ', ' ', ' ']
        cells[7] = [' ', ' ', 'i', 'h', ' ', ' ', ' ', 'c', 'f']
        cells[8] = [' ', ' ', ' ', 'c', ' ', 'f', ' ', 'i', ' ']

    if diff == 'H':
        cells[0] = [' ', ' ', ' ', 'f', ' ', ' ', 'd', ' ', ' ']
        cells[1] = ['g', ' ', ' ', ' ', ' ', 'c', 'f', ' ', ' ']
        cells[2] = [' ', ' ', ' ', ' ', 'i', 'a', ' ', 'h', ' ']
        cells[3] = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        cells[4] = [' ', 'e', ' ', 'a', 'h', ' ', ' ', ' ', 'c']
        cells[5] = [' ', ' ', ' ', 'c', ' ', 'f', ' ', 'd', 'e']
        cells[6] = [' ', 'd', ' ', 'b', ' ', ' ', ' ', 'f', ' ']
        cells[7] = ['i', ' ', 'c', ' ', ' ', ' ', ' ', ' ', ' ']
        cells[8] = [' ', 'b', ' ', ' ', ' ', ' ', 'a', ' ', ' ']

    return (cells)


# --------------------------------------------------
def modify_board(cells, seed):
    diction = {}
    new_cells = [[], [], [], [], [], [], [], [], []]
    hor_cells = [[], [], [], [], [], [], [], [], []]
    vert_cells = [[], [], [], [], [], [], [], [], []]
    diag_cells = [[], [], [], [], [], [], [], [], []]
    this_row = ['', '', '', '', '', '', '', '', '']
    immut = []
    if seed:
        random.seed(seed)

    for l in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']:
        num = str(random.choice(range(1, 10)))
        while num in diction.values():
            num = str(random.choice(range(1, 10)))
        diction[l] = num
    diction[' '] = ' '

    for row in range(0, 9):
        for col in range(0, 9):
            this_row[col] = diction[cells[row][col]]
        new_cells[row] = this_row.copy()

    flip_hor = random.choice([0, 1])
    flip_vert = random.choice([0, 1])
    flip_diag = random.choice([0, 1])

    if flip_hor:
        for row in range(0, 9):
            for col in range(0, 9):
                this_row[col] = new_cells[row][8 - col]
            hor_cells[row] = this_row.copy()
    else:
        hor_cells = new_cells

    if flip_vert:
        for row in range(0, 9):
            for col in range(0, 9):
                this_row[col] = hor_cells[8 - row][col]
            vert_cells[row] = this_row.copy()
    else:
        vert_cells = hor_cells

    if flip_diag:
        for row in range(0, 9):
            for col in range(0, 9):
                this_row[col] = vert_cells[col][row]
            diag_cells[row] = this_row.copy()
    else:
        diag_cells = vert_cells

    for row in range(0, 9):
        for col in range(0, 9):
            if diag_cells[row][col].isdigit():
                immut.append((row, col))

    return diag_cells, immut


# --------------------------------------------------
def print_board(cells, immut, bad, cannot, tip, color_off):
    minor_border = '·' * 37
    major_border = '-' * 37

    print(major_border)

    for i in range(0, 9):
        for j in range(0, 9):
            print('|' if not j % 3 else '⁝', end='')
            if tuple([i, j]) in immut and not color_off:
                print(color.GREEN + '{:^3}'.format(str(cells[i][j])) + color.END, end='')
            elif tuple([i, j]) in cannot and tip and not color_off:
                print(color.RED + '{:^3}'.format(str(cells[i][j])) + color.END, end='')
            elif tuple([i, j]) in bad and tip and not color_off:
                print(color.YELLOW + '{:^3}'.format(str(cells[i][j])) + color.END, end='')
            else:
                print('{:^3}'.format(str(cells[i][j])), end='')
        print('|')
        print(minor_border if (i + 1) % 3 else major_border)


# --------------------------------------------------
def check_board(cells, immut):
    bad = []
    cannot = []

    for row in range(0, 9):
        for col in range(0, 9):
            now_cell = cells[row][col]
            if not now_cell == ' ' and tuple([row, col]) not in immut:
                for check_row in range(0, 9):
                    if now_cell == cells[check_row][col] and not check_row == row:
                        cannot.extend([(row, col)]) if tuple([check_row, col]) in immut else bad.extend([(row, col)])
                for check_col in range(0, 9):
                    if now_cell == cells[row][check_col] and not check_col == col:
                        cannot.extend([(row, col)]) if tuple([row, check_col]) in immut else bad.extend([(row, col)])
                for check_row in range((row // 3) * 3, (row // 3) * 3 + 3):
                    for check_col in range((col // 3) * 3, (col // 3) * 3 + 3):
                        if now_cell == cells[check_row][check_col] and not check_col == col and not check_row == row:
                            cannot.extend([(row, col)]) if tuple([check_row, check_col]) in immut else bad.extend(
                                [(row, col)])

    if (0 == sum(' ' in row for row in cells)) and len(bad) == 0 and len(cannot) == 0:
        won = True
    else:
        won = False

    return set(bad), set(cannot), won


# --------------------------------------------------
def main():
    args = get_args()
    difficulty = args.difficulty
    seed = args.seed
    color_off = args.coloroff

    if args.seed:
        random.seed(args.seed)
    tip = True if args.tip else False

    if re.compile('^[Ee]').match(difficulty):
        diff = 'E'
    elif re.compile('^[Mm]').match(difficulty):
        diff = 'M'
    elif re.compile('^[Hh]').match(difficulty):
        diff = 'H'
    else:
        die('--difficulty "{}" must be (E)asy, (M)edium, or (H)ard'.format(difficulty))

    cells = make_board(diff)  # Make a seed board based on the difficulty level
    cells, immut = modify_board(cells, seed)  # Fill in the board with numbers and mutate

    over = False
    bad = set()
    cannot = set()

    while not over:
        print('\n\n')
        print_board(cells, immut, bad, cannot, tip, color_off)
        print('\n\n')

        resp = input('What is your next move? (format as row,column:number): ')
        move_match = re.compile('(?P<row>\d)' + '[\D]' + '(?P<col>\d)' + '[\D]''(?P<move>[d\d])').match(resp)

        row, col, move = ['', '', '']
        if move_match:
            row = int(move_match.group('row'))
            col = int(move_match.group('col'))
            move = move_match.group('move')
            for num in [row, col]:
                if not 0 < num < 10:
                    warn('Invalid location entry "{}" must be integers 1-9'.format(resp))
                    move = ' '
            if tuple([row - 1, col - 1]) in immut:
                print('Location ({},{}) is immutable, please select another location.'.format(row, col))
                continue
            elif move.isdigit():
                if 0 < int(move) < 10:
                    cells[row - 1][col - 1] = move
                else:
                    print('Move "{}" must be 1-9'.format(move))
            elif move == 'd':
                cells[row - 1][col - 1] = ' '
            else:
                print('Invlaid move "{}", must be 1-9 or "d"'.format(move))
            bad, cannot, over = check_board(cells, immut)
        else:
            print('Invalid move entry "{}", must be 1-9 formatted as row,column:number'.format(resp))

    print('Congratulations, you won!')


# --------------------------------------------------
if __name__ == '__main__':
    main()
