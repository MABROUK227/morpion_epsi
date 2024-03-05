# Import libraries
import math 
import copy


X = "X"
O = "O"
EMPTY = None

# Initial State of the Board
def initial_start():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]
    
# Player Turn
def player(board):
    count_x = 0
    count_o = 0
    for i in board:
        for j in i:
            if j == "X":
                count_x += 1
            elif j == "O":
                count_o += 1
    
    if count_x == count_o:
        return "X"
    else:
        return "O"
    
# Possible Actions Available on the Board
def actions(board):
    moves_available = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                moves_available.add((i,j))
    return moves_available

# Results after move (i & j)
def result(board, action):
    if action not in actions(board):
        raise ValueError("Action Impossible")
    row, col = action
    current_player = player(board)
    new_board = [row[:] for row in board]
    new_board[row][col] = current_player
    
    return new_board

# Return Winner (if a player win)
def winner(board):
    for player in [X, O]:
        for i in range(3):
            # Rows Checking
            if all(board[i][j] == player for j in range(3)):
                return player
            
            # Columns Checking
            if all(board[j][i] == player for j in range(3)):
                return player
        
        # Diagonals Checking
        if all(board[i][i] == player for i in range(3)):
            return player
        if all(board[i][2 - i] == player for i in range(3)):
            return player
    
    return None

# Return True if game is finish
def terminal(board):
    return winner(board) is not None or all(board[i][j] != EMPTY for i in range(3) for j in range(3))

#  Returns 1 if X has won the game, -1 if O has won, 0 otherwise
def utility(board):
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0

# Returns minimum utility value over all legal moves
def min_value(board):
    if terminal(board):
        return utility(board), None

    f = float("inf")
    optimal_action = None
    for action in actions(board):
        max_val, _ = max_value(result(board, action))
        if max_val < f:
            f = max_val
            optimal_action = action

    return f, optimal_action

# Returns maximum utility value over all legal moves
def max_value(board):
    if terminal(board):
        return utility(board), None

    f = float("-inf")
    optimal_action = None
    for action in actions(board):
        min_val, _ = min_value(result(board, action))
        if min_val > f:
            f = min_val
            optimal_action = action

    return f, optimal_action

# Return optimal action for current player
def minimax(board):
    if terminal(board):
        return None
    if player(board) == X:
        value, action = max_value(board)
    else:
        value, action = min_value(board)

    return action