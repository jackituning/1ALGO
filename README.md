# Project 1ALGO
Python game named "Jeu de tour et des reines" 
1 - Game Rules
Two players compete on a square board consisting of 𝑛×𝑛
n×n cells, where 𝑛
n is an even integer. By default, 𝑛=8.

Each player has two types of pieces:

A queen, which moves orthogonally or diagonally to an empty square, not necessarily adjacent. The movement is valid only if all cells between the starting and destination squares are empty (similar to a chess queen but without capturing an opponent's piece on the destination square).
A rook, which moves orthogonally to an empty square, not necessarily adjacent. The movement is valid only if all cells between the starting and destination squares are empty (similar to a chess rook but without capturing an opponent's piece on the destination square).
Initially, each player has one queen and 
𝑛
2
/
/
4
−
1
n 
2
 //4−1 rooks, arranged on the board as follows (the first player has blue and purple pieces, while the second player has red and orange pieces):

Example configuration omitted for brevity.

Example Move
Following the initial setup, the first player moves one of their rooks after selecting it:

Example move illustration omitted.

Capture Rules
After a player moves a rook, captures are possible under the following condition:
If the final position of the rook is not on the same row or column as the player's queen, these two pieces form the two vertices of a diagonal of an imaginary rectangle. If one or two opponent rooks are located on the other vertices of this rectangle, they are captured.

This capture rule only applies after a rook's movement, not a queen's. Additionally, only opponent rooks can be captured; queens are immune to capture.

Capture Example
The second player selects their rook located on the fourth row and sixth column and moves it to the seventh row and sixth column, capturing the first player's rook positioned on the seventh row and eighth column:

Capture example illustration omitted.

Queen's Movement Example
Later in the game, the second player moves their queen diagonally:

Queen move illustration omitted.

Winning Condition
A player loses the game if they are left with two or fewer pieces (queen and rooks combined).

Victory Example
The second player wins:

Victory example illustration omitted.

2 - Python Implementation
The game must be implemented using the Tkinter graphical library. Alternative libraries will not be accepted.

An object-oriented approach is mandatory, with strict adherence to the principle of encapsulation. Projects failing to comply will be rejected.

You must implement at least two classes:

Player Class

Attributes:
Coordinates of the player's queen on the board.
Number of remaining pieces.
Game Class

Attributes:
A 2D list modeling the game board.
Additional attributes as needed.
Required Features
Your program must include the following features:

Board Dimensions:
Allow users to choose the board size via a menu. The number of rows and columns must be even and range between 6 and 12.

Board Display:

Display the grid and the pieces.
Indicate which player's turn it is.
Piece Selection:

On their turn, a player selects the piece they want to move using the mouse.
The player can only select their own pieces and valid moves according to the rules.
Highlight the selected piece (e.g., with a circle).
Move Execution:

The player selects the destination square for the previously selected piece, adhering to the movement rules.
Update the board to reflect the move and handle possible captures.
Turn Management:

Alternate turns between the players.
Victory Condition:

Declare the winner when the opponent has two or fewer pieces remaining.
Endgame Management:

Display the result.
Offer the option to start a new game.
