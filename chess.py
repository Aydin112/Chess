import time

# Initialize board data
data = []
b = [" "] * 64

# Function to print the chessboard
def printboard():
    # Render all pieces on the board
    for i in data:
        if i is not None:
            i.render()

    print(f'----------------- ')
    for i in range(8):
        print(f'|{"|".join(b[i*8:(i+1)*8])}|')
        print(f'----------------- ')

# Helper functions
def find_on_board(x, y):
    return x + (y * 8)

def check_for_clash(x, y):
    kill_index = -1  # No clashes by default
    for index, piece in enumerate(data):
        if piece and piece.x == x and piece.y == y:
            kill_index = index
    return kill_index

# Define the Move class
class Move:
    def __init__(self, x: int, y: int, kill_index: int):
        self.x = x
        self.y = y
        self.kill_index = kill_index

    def display(self) -> str:
        if self.kill_index == -1:
            return f'Move to x:{self.x} y:{self.y}'
        return f'Move to x:{self.x} y:{self.y} and make a kill'

# Base class for chess pieces
class Piece:
    def __init__(self, x: int, y: int, player: bool):
        self.x = x
        self.y = y
        self.player = player  # True for Player 1, False for Player 2

    def render(self):
        pass  # To be implemented by subclasses

    def aval_moves(self):
        return []  # To be implemented by subclasses

# Pawn piece
class Pawn(Piece):
    def render(self):
        b[find_on_board(self.x, self.y)] = "P" if self.player else "p"

    def aval_moves(self):
        moves = []
        direction = -1 if self.player else 1  # Player 1 moves up, Player 2 moves down
        next_y = self.y + direction

        if 0 <= next_y < 8:
            # Move forward if no clash
            if check_for_clash(self.x, next_y) == -1:
                moves.append(Move(self.x, next_y, -1))
            
            # Check capture left
            if self.x > 0 and check_for_clash(self.x - 1, next_y) != -1:
                moves.append(Move(self.x - 1, next_y, check_for_clash(self.x - 1, next_y)))

            # Check capture right
            if self.x < 7 and check_for_clash(self.x + 1, next_y) != -1:
                moves.append(Move(self.x + 1, next_y, check_for_clash(self.x + 1, next_y)))

        return moves

# Rook piece
class Rook(Piece):
    def render(self):
        b[find_on_board(self.x, self.y)] = "R" if self.player else "r"

    def aval_moves(self):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Right, Left, Up, Down

        for dx, dy in directions:
            nx, ny = self.x, self.y
            while True:
                nx += dx
                ny += dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    clash_index = check_for_clash(nx, ny)
                    if clash_index == -1:
                        moves.append(Move(nx, ny, -1))
                    else:
                        if data[clash_index].player != self.player:
                            moves.append(Move(nx, ny, clash_index))
                        break
                else:
                    break
        return moves

# Initialize the game
def initialize_game():
    # Add pawns for player 1
    for i in range(8):
        data.append(Pawn(i, 6, True))
    # Add pawns for player 2
    for i in range(8):
        data.append(Pawn(i, 1, False))

    # Add Rooks
    data.append(Rook(0, 7, True))  # Player 1 Rook
    data.append(Rook(7, 7, True))
    data.append(Rook(0, 0, False))  # Player 2 Rook
    data.append(Rook(7, 0, False))

# Function to perform a move
def perform_move(piece_index, target_x, target_y):
    piece = data[piece_index]
    valid_moves = piece.aval_moves()
    selected_move = None

    for move in valid_moves:
        if move.x == target_x and move.y == target_y:
            selected_move = move
            break

    if selected_move:
        if selected_move.kill_index != -1:
            print(f"Captured piece at ({selected_move.x}, {selected_move.y})")
            data[selected_move.kill_index] = None

        piece.x = target_x
        piece.y = target_y
        return True
    else:
        print("Invalid move!")
        return False

# Game loop
initialize_game()

while True:
    printboard()
    print("Choose a piece to move (index):")
    for index, piece in enumerate(data):
        if piece is not None:
            print(f"{index}: {type(piece).__name__} at ({piece.x}, {piece.y})")

    try:
        selected_piece = int(input("Select piece index: "))
        if selected_piece < 0 or selected_piece >= len(data) or data[selected_piece] is None:
            print("Invalid piece selection.")
            continue

        piece = data[selected_piece]
        print(f"Available moves for {type(piece).__name__} at ({piece.x}, {piece.y}):")
        available_moves = piece.aval_moves()

        for move in available_moves:
            print(move.display())

        target_x = int(input("Enter target x coordinate (0-7): "))
        target_y = int(input("Enter target y coordinate (0-7): "))

        if perform_move(selected_piece, target_x, target_y):
            print("Move successful.")
        else:
            print("Move failed. Try again.")
    except ValueError:
        print("Invalid input, please enter a number.")
    
    # Brief delay for better experience
    time.sleep(1)
