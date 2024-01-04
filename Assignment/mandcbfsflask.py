from flask import Flask, render_template
from collections import deque
import sys
from io import StringIO

app = Flask(__name__)

Parent, Move, node_list = dict(), dict(), dict()

class Solution():
    def __init__(self):
        self.start_state = (3, 3, 1)
        self.goal_state = (0, 0, 0)
        self.options = [(1, 0), (0, 1), (1, 1), (0, 2), (2, 0)]

        self.boat_side = ["right", "left"]

        self.visited = {}
        self.solved = False
        self.q = deque()

    def is_valid_move(self, number_missionaries, number_cannnibals):
        """
        Checks if number constraints are satisfied
        """
        return (0 <= number_missionaries <= 3) and (0 <= number_cannnibals <= 3)

    def is_goal_state(self, number_missionaries, number_cannnibals, side):
        return (number_missionaries, number_cannnibals, side) == self.goal_state

    def is_start_state(self, number_missionaries, number_cannnibals, side):
        return (number_missionaries, number_cannnibals, side) == self.start_state

    def number_of_cannibals_exceeds(self, number_missionaries, number_cannnibals):
        number_missionaries_right = 3 - number_missionaries
        number_cannnibals_right = 3 - number_cannnibals
        return (number_missionaries > 0 and number_cannnibals > number_missionaries) \
               or (number_missionaries_right > 0 and number_cannnibals_right > number_missionaries_right)

    def solve(self):
        self.visited = dict()
        Parent[self.start_state] = None
        Move[self.start_state] = None
        self.q = deque()
        self.q.append(self.start_state + (0, ))
        self.visited[self.start_state] = True

        # Redirect stdout to capture print statements
        sys.stdout = StringIO()

        while self.q:
            number_missionaries, number_cannnibals, side, depth_level = self.q.popleft()

            op = -1 if side == 1 else 1

            can_be_expanded = False

            if self.is_goal_state(number_missionaries, number_cannnibals, side):
                print(f"Final state: ({number_missionaries}, {number_cannnibals}, {side})")
                print("Goal state reached!")
                break

            elif self.number_of_cannibals_exceeds(number_missionaries, number_cannnibals):
                print(f"Visiting state: ({number_missionaries}, {number_cannnibals}, {side})")
                print("Cannibals exceed missionaries! Skipping this state.")
                continue

            print(f"Visiting state: ({number_missionaries}, {number_cannnibals}, {side})")

            for x, y in self.options:
                next_m, next_c, next_s = number_missionaries + op * x, number_cannnibals + op * y, int(not side)
                if (next_m, next_c, next_s) not in self.visited:
                    if self.is_valid_move(next_m, next_c):
                        can_be_expanded = True
                        self.visited[(next_m, next_c, next_s)] = True
                        self.q.append((next_m, next_c, next_s, depth_level + 1))
                        Parent[(next_m, next_c, next_s)] = (number_missionaries, number_cannnibals, side)
                        Move[(next_m, next_c, next_s)] = (x, y, side)

            if not can_be_expanded:
                print("No valid moves from this state.")

            print(f"BFS Queue: {[(state[0], state[1], state[2]) for state in self.q]}")

        # Get the captured print statements
        output = sys.stdout.getvalue()

        # Reset stdout to default
        sys.stdout = sys.__stdout__

        return output

# Initialize the solver outside the route to persist data between requests
solver = Solution()

@app.route('/')
def index():
    # Run the solve method on each request to reflect any changes
    output = solver.solve()

    return render_template('mandcbfs.html', output=output)

if __name__ == '__main__':
    app.run(debug=True)