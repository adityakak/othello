from OthelloAB import findNextMoveAB, findPossibleMoves, newBoardState
#from OthelloNN import findNextMoveNN
import time
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

@app.route('/minimax', methods=['POST', 'OPTIONS'])
def get_moveAB():
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = jsonify({'status': 'success'})
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
    board = request.json['board']
    player = request.json['player']
    stringBoard = convertBoardToString(board)

    opponent = 'x' if player == 'o' else 'o'
    if len(findPossibleMoves(stringBoard, player)) == 0:
        whiteScore, blackScore = parseScore(stringBoard)
        if len(findPossibleMoves(stringBoard, opponent)) == 0:
            return jsonify({'board': convertBoardToArray(stringBoard), 'whiteScore': whiteScore, 'blackScore': blackScore, 'gameOver': 2}), 200
        else:
            return jsonify({'board': convertBoardToArray(stringBoard), 'whiteScore': whiteScore, 'blackScore': blackScore, 'gameOver': 0}), 200
        
    endTime = time.time() + duration
    depth = 1
    move = None
    while time.time() < endTime:
        move = findNextMoveAB(stringBoard, player, depth)
        depth += 1

    newState = newBoardState(stringBoard, player, move)
    whiteScore, blackScore = parseScore(newState)
    if len(findPossibleMoves(newState, opponent)) == 0 and len(findPossibleMoves(newState, player)) == 0:
        return jsonify({'board': convertBoardToArray(newState), 'whiteScore': whiteScore, 'blackScore':blackScore, 'gameOver': 2}), 200
    elif len(findPossibleMoves(newState, opponent)) == 0:
        return jsonify({'board': convertBoardToArray(newState), 'whiteScore': whiteScore, 'blackScore':blackScore, 'gameOver': 1}), 200
    return jsonify({'board': convertBoardToArray(newState), 'whiteScore': whiteScore, 'blackScore':blackScore, 'gameOver': 0}), 200

"""
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
"""
@app.route('/validSquares', methods=['POST', 'OPTIONS'])
def possible():
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = jsonify({'status': 'success'})
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
    
    data = request.get_json()
    board = data['board']
    player = data['player']
    coordinate = data['coordinate']

    position = (coordinate[0] * 8) + coordinate[1]

    stringBoard = convertBoardToString(board)
    possible_moves = findPossibleMoves(stringBoard, player)

    if position not in possible_moves:
        return jsonify({'valid': False, 'board': data['board']}), 200
    newState = newBoardState(stringBoard, player, position)
    whiteScore, blackScore = parseScore(newState)
    return jsonify({'valid': True, 'board': convertBoardToArray(newState), 'whiteScore': whiteScore, 'blackScore':blackScore}), 200

def convertBoardToString(board):
    string_board = ""
    for row in board:
        for element in row:
            if element == 0:
                string_board += "."
            elif element == 1:
                string_board += "o"
            elif element == 2:
                string_board += "x"
    return string_board

def convertBoardToArray(board):
    array_board = [[] for _ in range(8)]
    for i in range(8):
        for j in range(8):
            array_board[i].append(0 if board[i*8 + j] == "." else 1 if board[i*8 + j] == "o" else 2)
    return array_board

if __name__ == '__main__':
    app.run(host = "0.0.0.0")
