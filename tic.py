import sys
import random

# Initialize a 3x3x3 board (0 = empty, 1 = X (human), 2 = O (AI))
board = [[[0 for _ in range(3)] for _ in range(3)] for _ in range(3)]

# Players: 0 for human (X), 1 for AI (O)
players = ['X', 'O']
current_player = 0  # Start with human

def print_board():
    """Print the 3D board layer by layer."""
    for layer in range(3):
        print(f"Layer {layer + 1}:")
        for row in range(3):
            print("  " + " | ".join([str(board[layer][row][col]) if board[layer][row][col] != 0 else " " for col in range(3)]))
            if row < 2:
                print("  ---+---+---")
        print()

def get_move():
    """Get a valid move from the human player."""
    while True:
        try:
            layer = int(input(f"Player {players[current_player]}, enter layer (1-3): ")) - 1
            row = int(input("Enter row (1-3): ")) - 1
            col = int(input("Enter column (1-3): ")) - 1
            if 0 <= layer < 3 and 0 <= row < 3 and 0 <= col < 3 and board[layer][row][col] == 0:
                return layer, row, col
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Please enter numbers between 1 and 3.")

def get_possible_moves(board):
    """Get a list of all possible moves (layer, row, col)."""
    moves = []
    for layer in range(3):
        for row in range(3):
            for col in range(3):
                if board[layer][row][col] == 0:
                    moves.append((layer, row, col))
    return moves

def check_win(board, player):
    """Check if a player has won on the given board."""
    # Check all rows, columns, and diagonals in each layer
    for layer in range(3):
        for i in range(3):
            # Rows
            if all(board[layer][i][j] == player for j in range(3)):
                return True
            # Columns
            if all(board[layer][j][i] == player for j in range(3)):
                return True
        # Diagonals in layer
        if all(board[layer][i][i] == player for i in range(3)) or all(board[layer][i][2-i] == player for i in range(3)):
            return True
    
    # Check verticals (columns across layers)
    for row in range(3):
        for col in range(3):
            if all(board[layer][row][col] == player for layer in range(3)):
                return True
    
    # Check space diagonals
    if all(board[i][i][i] == player for i in range(3)) or all(board[i][i][2-i] == player for i in range(3)):
        return True
    if all(board[i][2-i][i] == player for i in range(3)) or all(board[i][2-i][2-i] == player for i in range(3)):
        return True
    
    return False

def evaluate(board):
    """Evaluate the board: +10 if AI wins, -10 if human wins, 0 otherwise."""
    if check_win(board, 2):  # AI (O)
        return 10
    elif check_win(board, 1):  # Human (X)
        return -10
    else:
        return 0

def minimax(board, depth, is_maximizing, alpha, beta):
    """Minimax with alpha-beta pruning."""
    score = evaluate(board)
    if score != 0 or depth == 0:
        return score
    
    if is_maximizing:  # AI's turn (maximize)
        max_eval = -float('inf')
        for move in get_possible_moves(board):
            layer, row, col = move
            board[layer][row][col] = 2  # AI move
            eval = minimax(board, depth - 1, False, alpha, beta)
            board[layer][row][col] = 0  # Undo
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:  # Human's turn (minimize)
        min_eval = float('inf')
        for move in get_possible_moves(board):
            layer, row, col = move
            board[layer][row][col] = 1  # Human move
            eval = minimax(board, depth - 1, True, alpha, beta)
            board[layer][row][col] = 0  # Undo
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def get_ai_move(board):
    """Get the best move for AI using minimax."""
    best_val = -float('inf')
    best_move = None
    for move in get_possible_moves(board):
        layer, row, col = move
        board[layer][row][col] = 2  # AI move
        move_val = minimax(board, 4, False, -float('inf'), float('inf'))  # Depth 4
        board[layer][row][col] = 0  # Undo
        if move_val > best_val:
            best_val = move_val
            best_move = move
    return best_move

def check_draw(board):
    """Check if the board is full (draw)."""
    return all(board[layer][row][col] != 0 for layer in range(3) for row in range(3) for col in range(3))

# Main game loop
print("Welcome to 3D Tic Tac Toe! You are X, AI is O.")
print_board()

while True:
    if current_player == 0:  # Human's turn
        layer, row, col = get_move()
    else:  # AI's turn
        print("AI is thinking...")
        layer, row, col = get_ai_move(board)
        print(f"AI plays: Layer {layer+1}, Row {row+1}, Column {col+1}")
    
    board[layer][row][col] = current_player + 1
    print_board()
    
    if check_win(board, current_player + 1):
        if current_player == 0:
            print("You win!")
        else:
            print("AI wins!")
        sys.exit()
    elif check_draw(board):
        print("It's a draw!")
        sys.exit()
    
    current_player = 1 - current_player  # Switch player
