from math import inf as infinity

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0
    for row in board:
      for col in row:
        if col == 'X':
          x_count += 1
        elif col == 'O':
            o_count += 1
    if x_count == o_count:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions_set=set()
    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY:
                actions_set.add((row, col))
    return actions_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    row = action
    col = action
    new_board = []
    for row in board:
      new_row = row[:]
      new_board.append(new_row)
    new_board[action[0]][action[1]] = player(board)
    return new_board



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows
    if board[0][0] == board[0][1] and board[0][2]==board[0][0] and board[0][2] == board[0][1] :
            return board[0][0]
    elif board[1][0] == board[1][1] and board[1][2]==board[1][0] and board[1][1] == board[1][2] :
      return board[1][0]
    elif board[2][0] == board[2][1] and board[2][0]==board[2][2] and board[2][2] == board[2][1] :
      return board[2][0]
    # Check diagonals
    elif board[0][0] == board[1][1] == board[2][2] :
        return board[0][0]
    elif board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]
    # check columns
    elif board[0][0] == board[1][0] == board[2][0] :
        return board[0][0]
    elif board[0][1] == board[1][1] == board[2][1]  :
        return board[0][1]
    elif board[0][2] == board[1][2] == board[2][2]  :
        return board[0][2]
    # No winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board)!=None:
        return True

    for row in board:
        if EMPTY in row:
            return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0




def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    player_turn = player(board)
    if player_turn == X:
        best_score = -infinity 
        best_move = None
        for action in actions(board):
            new_score = (min_value(result(board, action)))
            if new_score > best_score:
                best_score = new_score
                best_move = action
    else:
        best_score = infinity 
        best_move = None
        for action in actions(board):
            new_score = max_value(result(board, action))
            if new_score < best_score:
                best_score = new_score
                best_move = action

    return best_move

def max_value(board):
    if terminal(board):
        return utility(board)

    v =-infinity
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    if terminal(board):
        return utility(board)

    v = infinity
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v

