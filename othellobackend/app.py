from OthelloAB import findNextMove
import time

app = Flask(__name__)


@app.route('/minimax, method = ['POST'])
def get_move():
    board = request.json['board']
    player = request.json['player']
    duration = 3.5
    endTime = time.time() + duration
    depth = 1
    move = None
    while time.time() < end_time:
        move = findNextMove(board, player, depth)
        depth += 1
    return jsonify(move)


if __name__ == '__main__':
    app.run(host = "0.0.0.0")
