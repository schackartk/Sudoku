# Sudoku

Let's play sudoku!

This game plays by the usual rules:
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


