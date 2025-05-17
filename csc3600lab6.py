import heapq

class PuzzleState:
    def __init__(self, board, move=0, previous=None):
        self.board = board
        self.move = move
        self.previous = previous
        self.zero_pos = self.find_zero()
        self.priority = self.move + self.heuristic()

    def find_zero(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

    def heuristic(self):
        """Use Manhattan distance as heuristic"""
        goal = {
            1: (0, 0), 2: (0, 1), 3: (0, 2),
            8: (1, 0), 0: (1, 1), 4: (1, 2),
            7: (2, 0), 6: (2, 1), 5: (2, 2)
        }
        distance = 0
        for i in range(3):
            for j in range(3):
                value = self.board[i][j]
                if value != 0:
                    goal_i, goal_j = goal[value]
                    distance += abs(i - goal_i) + abs(j - goal_j)
        return distance

    def is_goal(self):
        goal_board = [
            [1, 2, 3],
            [8, 0, 4],
            [7, 6, 5]
        ]
        return self.board == goal_board

    def generate_neighbors(self):
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        x, y = self.zero_pos

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < 3 and 0 <= ny < 3:
                new_board = [row[:] for row in self.board]
                new_board[x][y], new_board[nx][ny] = new_board[nx][ny], new_board[x][y]
                neighbor = PuzzleState(new_board, self.move + 1, self)
                neighbors.append(neighbor)

        return neighbors

    def __lt__(self, other):
        return self.priority < other.priority

    def __str__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.board])

def a_star(initial_board):
    start = PuzzleState(initial_board)
    open_set = []
    heapq.heappush(open_set, start)
    visited = set()

    while open_set:
        current = heapq.heappop(open_set)

        if current.is_goal():
            return current

        visited.add(tuple(map(tuple, current.board)))

        for neighbor in current.generate_neighbors():
            if tuple(map(tuple, neighbor.board)) not in visited:
                heapq.heappush(open_set, neighbor)

    return None

def print_solution(solution):
    path = []
    current = solution
    while current:
        path.append(current)
        current = current.previous
    path.reverse()

    for step, state in enumerate(path):
        print(f"Step {step}:")
        print(state)
        print()

    print(f"Total moves (g(n)) = {len(path) - 1}")

if __name__ == "__main__":
    initial_board = [
        [3, 2, 4],
        [5, 0, 8],
        [7, 6, 1]
    ]
    solution = a_star(initial_board)
    if solution:
        print_solution(solution)
    else:
        print("No solution found.")
