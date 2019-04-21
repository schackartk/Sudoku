# Sudoku

Let's play sudoku!

This game is played by the usual rules:
 * Fill out each square in the 9x9 grid with the numbers 1-9
 * You cannot change the numbers provided at the beginning of the game (shown in green)
 * Each row, column and 3x3 grid cannot contain any repeated digits

The game has three `--difficulty` levels: Easy, Medium, and Hard.

By including the `--tip` flag, the program will color:
 * Moves that conflict with immutable digits in red
 * Moves that conflict with your other move(s) in yellow
  
To place a digit, type row,column:move. For instance, to place a 5 in the top left corner you would type `1,1:5`.

To remove a digit you placed, you can type row,column:d. For instance to remove the digit in the top left corner you would type `1,1:d`.

Testing is made possible using the `--seed` and `--coloroff` flags to alter the behavior of the `random` module and turn off all coloring.

# Expected behavior

```
$ ./sudoku.py
usage: sudoku.py [-h] -d str [-s] [-t] [-c]
sudoku.py: error: the following arguments are required: -d/--difficulty

$ ./sudoku.py -h
usage: sudoku.py [-h] -d str [-s] [-t] [-c]

Commandline Sudoku game

optional arguments:
  -h, --help            show this help message and exit
  -d str, --difficulty str
                        Game difficulty (E)asy, (M)edium, or (H)ard) (default:
                        None)
  -s, --seed            A seed to allow for testing (default: False)
  -t, --tip             Color bad placements (default: False)
  -c, --coloroff        Turn off coloring for testing (default: False)
  
$ ./sudoku.py -d Medium -s -t -c



-------------------------------------
|   ⁝   ⁝   | 5 ⁝   ⁝ 4 |   ⁝ 9 ⁝   |
·····································
|   ⁝   ⁝ 9 | 6 ⁝   ⁝   |   ⁝ 5 ⁝ 4 |
·····································
|   ⁝   ⁝   |   ⁝ 2 ⁝   |   ⁝   ⁝   |
-------------------------------------
|   ⁝   ⁝ 6 |   ⁝   ⁝   |   ⁝ 3 ⁝ 5 |
·····································
| 4 ⁝   ⁝   |   ⁝   ⁝   |   ⁝   ⁝ 8 |
·····································
| 5 ⁝ 1 ⁝   |   ⁝   ⁝   | 7 ⁝   ⁝   |
-------------------------------------
|   ⁝   ⁝   |   ⁝ 8 ⁝   |   ⁝   ⁝   |
·····································
| 7 ⁝ 6 ⁝   |   ⁝   ⁝ 9 | 1 ⁝   ⁝   |
·····································
|   ⁝ 2 ⁝   | 4 ⁝   ⁝ 6 |   ⁝   ⁝   |
-------------------------------------



What is your next move? (format as row,column:number):
```
See colored_conflicts.jpg for an example of the output with color enabled. This was generated with:

`$ ./sudoku.py -d Medium -s -t`

Followed by entering: `1,1:1`, `1,2:3`, `1,3:2`, `1,7:2`, `2,1:9`, `4,1:9`

# Test suite
A passing test suite looks like this:
```
$ make test
python3 -m pytest -p no:warnings -v test.py
=============================== test session starts ================================
platform linux -- Python 3.7.1, pytest-4.0.2, py-1.7.0, pluggy-0.8.0 -- /rsgrps/bh_class/conda/bin/python3
cachedir: .pytest_cache
rootdir: /rsgrps/bh_class/schackartk/Sudoku, inifile:
plugins: remotedata-0.3.1, openfiles-0.3.1, doctestplus-0.2.0, arraydiff-0.3
collected 7 items

test.py::test_usage PASSED                                                   [ 14%]
test.py::test_bad_difficulty PASSED                                          [ 28%]
test.py::test_make_board PASSED                                              [ 42%]
test.py::test_modify_board PASSED                                            [ 57%]
test.py::test_print_board PASSED                                             [ 71%]
test.py::test_check_board PASSED                                             [ 85%]
test.py::test_winning_state PASSED                                           [100%]

============================= 7 passed in 1.02 seconds =============================
```
  
# Author
Code written by Kenneth Schackart (schackartk@email.arizona.edu)
