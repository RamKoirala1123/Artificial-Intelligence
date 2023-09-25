from flask import Flask, render_template
from mandc import Solution

from heuristics import solve_eight_puzzle

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/mandc')
def screen1():
    s = Solution()
    if s.solve():
        graph_data = s.get_graph_data()
        return render_template('mandc.html', graph_data=graph_data)
    else:
        return "No solution found"

@app.route('/heuristics')
def screen2():
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
    # print('the graph_data is', graph_data)
    return render_template('heuristics.html', graph_data=graph_data)



if __name__ == '__main__':
    app.run(debug=True)