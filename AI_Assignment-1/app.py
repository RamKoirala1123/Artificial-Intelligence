from flask import Flask, render_template
import os
from collections import deque

app = Flask(__name__)

os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

Parent, Move, node_list = dict(), dict(), dict()


class Solution():

    def __init__(self):

        self.start_state = (3, 3, 1)
        self.goal_state = (0, 0, 0)
        self.options = [(1, 0), (0, 1), (1, 1), (0, 2), (2, 0)]

        self.boat_side = ["right", "left"]

        self.visited = {}
        self.solved = False


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
    
    # def already()

    def solve(self):
        self.visited = dict()
        Parent[self.start_state] = None
        Move[self.start_state] = None
        return self.bfs()


    def bfs(self):
        q = deque()
        q.append(self.start_state + (0, ))
        self.visited[self.start_state] = True

        while q:
            number_missionaries, number_cannnibals, side, depth_level = q.popleft()

            op = -1 if side == 1 else 1

            can_be_expanded = False

            if self.is_goal_state(number_missionaries, number_cannnibals, side):
                return True
            
            elif self.number_of_cannibals_exceeds(number_missionaries, number_cannnibals):
                continue
            
            for x, y in self.options:
                next_m, next_c, next_s = number_missionaries + op * x, number_cannnibals + op * y, int(not side)
                if (next_m, next_c, next_s) not in self.visited:
                    if self.is_valid_move(next_m, next_c):
                        can_be_expanded = True
                        self.visited[(next_m, next_c, next_s)] = True
                        q.append((next_m, next_c, next_s, depth_level + 1))
                        Parent[(next_m, next_c, next_s)] = (number_missionaries, number_cannnibals, side)
                        Move[(next_m, next_c, next_s)] = (x, y, side)
                
                if not can_be_expanded:
                    pass
        return False


    def get_graph_data(self):
        nodes = []
        edges = []
        levels = {}

        for state, parent_state in Parent.items():
            if parent_state is not None:
                edge_data = {
                    'from' : str(parent_state),
                    'to': str(state),
                    'arrows': 'to'
                }
                edges.append(edge_data)
            if parent_state is not None:
            # Determine the level of the current node based on the parent's level
                current_level = levels[parent_state] + 1
            else:
            # The root node is at level 0
                current_level = 0
                
            levels[state] = current_level
            node_data = {
                'id': str(state),
                'label': str(state),
                'level': current_level,
                'color': 'blue' if self.is_start_state(*state) else 'green' if self.is_goal_state(*state) else 'red' if self.number_of_cannibals_exceeds(state[0], state[1]) else 'orange'
            }
            nodes.append(node_data)
        return {
            'nodes': nodes,
            'edges': edges
        }


@app.route('/')
def index():
    s = Solution()
    if s.solve():
        graph_data = s.get_graph_data()
        return render_template('index.html', graph_data=graph_data)
    else:
        return "No solution found"


if __name__ == "__main__":
    app.run(debug=True)
