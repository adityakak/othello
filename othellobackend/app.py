from OthelloAB import findNextMoveAB, findPossibleMoves
from OthelloNN import findNextMoveNN
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

duration = 3.5

def parseScore(board):
    whiteScore = blackScore = 0
    for i in board:
        if i == "x":
            blackScore += 1
        elif i == "o":
            whiteScore += 1
    return whiteScore, blackScore

def response(move):
    whiteScore, blackScore = parseScore(move)
    response_json = dict()
    response_json['move'] = move
    response_json['whiteScore'] = whiteScore
    response_json['blackScore'] = blackScore
    return jsonify(response_json)

@app.route('/minimax', method = ['POST'])
def get_moveAB():
    board = request.json['board']
    player = request.json['player']
    endTime = time.time() + duration
    depth = 1
    move = None
    while time.time() < endTime:
        move = findNextMoveAB(board, player, depth)
        depth += 1
    return response(move)

@app.route('/nn', method = ['POST'])
def get_moveNN():
    board = request.json['board']
    player = request.json['player']
    duration = 3.5
    endTime = time.time() + duration
    depth = 1
    move = None
    while time.time() < endTime:
        move = findNextMoveNN(board, player, depth)
        depth += 1
    return response(move)

@app.route('/validSquares', method = ['POST'])
def possible():
    board = request.json['board']
    player = request.json['player']
    coordinate = request.json['coordinate']
    possible_moves = findPossibleMoves(board, player)
    if coordinate not in possible_moves:
        return jsonify({'valid': False})
    return jsonify({'valid': True})


if __name__ == '__main__':
    app.run(host = "0.0.0.0")
