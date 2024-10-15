import heapq

class PuzzleState:
    def __init__(self, board, zero_pos, g=0, parent=None):
        self.board = board
        self.zero_pos = zero_pos  # (row, col) of the zero tile
        self.g = g  # cost to reach this state
        self.h = self.misplaced_tiles()  # heuristic
        self.f = self.g + self.h  # total cost
        self.parent = parent  # reference to the parent state for tracing the path

    def misplaced_tiles(self):
        # Use the user-defined goal state
        goal = self.goal_state()
        return sum(1 for i in range(9) if self.board[i] != goal[i])

    def goal_state(self):
        # Return the goal state based on user input
        return [0, 1, 2, 3, 4, 5, 6, 7, 8]

    def get_neighbors(self):
        # Generate neighboring states
        neighbors = []
        row, col = self.zero_pos
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_board = self.board[:]
                # Swap the zero tile with the neighboring tile
                new_board[row * 3 + col], new_board[new_row * 3 + new_col] = new_board[new_row * 3 + new_col], new_board[row * 3 + col]
                neighbors.append(PuzzleState(new_board, (new_row, new_col), self.g + 1, self))
        
        return neighbors

    def __lt__(self, other):
        return self.f < other.f

    def print_path(self):
        # Print the path from the initial state to the goal
        if self.parent is not None:
            self.parent.print_path()
        print(self.board_to_string())
        print("\n")

    def board_to_string(self):
        # Convert the board to a string for easier visualization
        return "\n".join(
            " ".join(str(self.board[i * 3 + j]) for j in range(3)) for i in range(3)
        )

def a_star(initial_board):
    zero_pos = initial_board.index(0)
    initial_state = PuzzleState(initial_board, (zero_pos // 3, zero_pos % 3))
    
    open_set = []
    heapq.heappush(open_set, initial_state)
    closed_set = set()

    while open_set:
        current_state = heapq.heappop(open_set)

        if current_state.h == 0:  # Goal reached
            print("Solution found:")
            current_state.print_path()
            return current_state.g

        closed_set.add(tuple(current_state.board))

        for neighbor in current_state.get_neighbors():
            if tuple(neighbor.board) in closed_set:
                continue
            
            if not any(neighbor.board == state.board for state in open_set):
                heapq.heappush(open_set, neighbor)

    return None  # No solution found

# Function to take user input
def get_board_input(prompt):
    while True:
        try:
            board = list(map(int, input(prompt).split()))
            if len(board) != 9 or set(board) != set(range(9)):
                raise ValueError
            return board
        except ValueError:
            print("Invalid input. Please enter 9 unique integers from 0 to 8.")

# Get initial and goal state from user
initial_board = get_board_input("Enter the initial board (9 numbers from 0 to 8, space-separated): ")
goal_board = get_board_input("Enter the goal board (9 numbers from 0 to 8, space-separated): ")

# Set the goal state dynamically
PuzzleState.goal_state = lambda self: goal_board

# Solve the puzzle
steps = a_star(initial_board)
print(f'Solution found in {steps} moves' if steps is not None else 'No solution found.')
