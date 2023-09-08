from flask import Flask, render_template
from collections import deque
import heapq

app = Flask(__name__)

class EightPuzzleState:
    def __init__(self, state, parent=None, move=None, level=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.level = level

    def __str__(self):
        return str(self.state)

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(str(self.state))

    def is_goal(self, goal_state):
        return self.state == goal_state

    def get_possible_moves(self):
        moves = []
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    if j > 0:
                        moves.append((0, -1))  # Move Left
                    if i < 2:
                        moves.append((1, 0))   # Move Down
                    if i > 0:
                        moves.append((-1, 0))  # Move Up
                    if j < 2:
                        moves.append((0, 1))   # Move Right
        return moves

    def generate_child(self, move):
        new_state = [list(row) for row in self.state]
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    ni, nj = i + move[0], j + move[1]
                    new_state[i][j], new_state[ni][nj] = new_state[ni][nj], new_state[i][j]
        return EightPuzzleState(new_state, parent=self, move=move, level=self.level + 1)

def calculate_misplaced_tiles(current_state, goal_state):
    misplaced = 0
    for i in range(3):
        for j in range(3):
            if current_state[i][j] != goal_state[i][j]:
                misplaced += 1
    return misplaced

def solve_eight_puzzle(initial_state, goal_state):
    queue = deque()
    visited = set()


    initial_node = EightPuzzleState(initial_state)
    # goal_node = EightPuzzleState(goal_state)

    queue.append(initial_node)
    visited.add(str(initial_state))

    nodes = []
    edges = []
    h_value = calculate_misplaced_tiles(initial_node.state,goal_state)
    nodes.append({
                    'color': 'green',
                    'id': str( initial_node),
                    'label': str( initial_node),
                    'level':  initial_node.level,
                    'h_value': f'g={initial_node.level}, h={h_value}, f={initial_node.level + h_value}',
                })

    while queue:
        current_node = queue.popleft()
        print('the current node is',current_node)

        if current_node.is_goal(goal_state):
            break
        # siblings = [current_node.generate_child(move) for move in current_node.get_possible_moves()]
        siblings = []
        for move in current_node.get_possible_moves():
                child_node = current_node.generate_child(move) 
                if str(child_node.state) not in visited:
                    print('the childrens aree', child_node) 
                    nodes.append({
                        'color': 'orange' if not child_node.is_goal(goal_state)  else 'green',
                        'id': str(child_node),
                        'label': str(child_node),
                        'level': child_node.level,
                        'h_value': f'g={child_node.level}, h={calculate_misplaced_tiles(child_node.state,goal_state)}, f={child_node.level + calculate_misplaced_tiles(child_node.state,goal_state)}',
                    })
                    edges.append({
                    'arrows': 'to',
                    'from': str(current_node),
                    'to': str(child_node)
                    }) 
                    visited.add(str(child_node.state)) 
                    siblings.append(child_node)

        if siblings:
                    # Find the sibling with the minimum number of misplaced tiles among siblings
                    min_sibling = min(siblings, key=lambda node: calculate_misplaced_tiles(node.state, goal_state))
                    print('the min sibling is',min_sibling)
        for node_data in nodes:
            if node_data['id'] == str(min_sibling):
                node_data['color'] = 'green'
            if node_data['id'] == str(goal_state):
                node_data['color'] = 'green'
        
        queue.append(min_sibling)
        print('the child_node is',child_node)
    
    return nodes, edges


@app.route('/index')
def index():
    initial_state = [
        [2, 8, 3],
        [1, 6, 4],
        [7, 0, 5]
    ]

    goal_state = [
        [1, 2, 3],
        [8, 0, 4],
        [7, 6, 5]
    ]

    nodes, edges = solve_eight_puzzle(initial_state, goal_state)
    graph_data = {
        'nodes': nodes,
        'edges': edges
    }
    print('the graph_data is', graph_data)
    return render_template('heuristics1.html', graph_data=graph_data)

if __name__ == "__main__":
    app.run(debug=True)
