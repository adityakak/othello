from OthelloAB import findNextMoveAB, findPossibleMoves, newBoardState
#from OthelloNN import findNextMoveNN
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
import multiprocessing

app = Flask(__name__)
CORS(app)


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

def addPossibleMovesToBoard(stringBoard, possibleMoves, opponent):
    for coordinate in possibleMoves:
        stringBoard = stringBoard[:coordinate] + 'b' + stringBoard[coordinate + 1:] if opponent == 'x' else stringBoard[:coordinate] + 'w' + stringBoard[coordinate + 1:]
    return stringBoard

def findNextMoveABWithTimeout(stringBoard, player, depth, duration):
    manager = multiprocessing.Manager()
    move = manager.Value(int, -1)
    process = multiprocessing.Process(target=findNextMoveAB, args=(stringBoard, player, depth, move))

    process.start()
    process.join(duration)

    if process.is_alive():
        process.terminate()
        process.join()

    return move.value

@app.route('/minimax', methods=['POST', 'OPTIONS']) # Returns JSON with the new board, white score, black score, and game over status
                                                    # Game over status: 0 = game not over, 1 = keep turn because opponent cannot move but we can, 2 = game over and no more moves
def get_moveAB():
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = jsonify({'status': 'success'})
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
    
    duration = 2
    board = request.json['board']
    player = request.json['player']
    currentMove = request.json['move']
    stringBoard = convertBoardToString(board)

    opponent = 'x' if player == 'o' else 'o'

    currentBoardPlayerPossibleMoves = findPossibleMoves(stringBoard, player)
    if len(currentBoardPlayerPossibleMoves) == 0:
        whiteScore, blackScore = parseScore(stringBoard)
        currentBoardOpponentPossibleMoves = findPossibleMoves(stringBoard, opponent)
        if len(currentBoardOpponentPossibleMoves) == 0:
            return jsonify({'board': convertBoardToArray(stringBoard), 'whiteScore': whiteScore, 'blackScore': blackScore, 'gameOver': 2, 'move': currentMove}), 200
        else:
            stringBoard = addPossibleMovesToBoard(stringBoard, currentBoardOpponentPossibleMoves, opponent)
            return jsonify({'board': convertBoardToArray(stringBoard), 'whiteScore': whiteScore, 'blackScore': blackScore, 'gameOver': 0, 'move': currentMove}), 200
        
    endTime = time.time() + duration
    depth = 1
    move = None
    # while time.time() < endTime:
    #     move = findNextMoveAB(stringBoard, player, depth)
    #     depth += 1
    while time.time() < endTime:
        moveFound = findNextMoveABWithTimeout(stringBoard, player, depth, endTime - time.time())
        if moveFound != -1:
            move = moveFound
        depth += 1
        print(move)


    newState = newBoardState(stringBoard, player, move)

    whiteScore, blackScore = parseScore(newState)

    newBoardOpponentPossibleMoves = findPossibleMoves(newState, opponent)
    newBoardPlayerPossibleMoves = findPossibleMoves(newState, player)

    if len(newBoardOpponentPossibleMoves) == 0 and len(newBoardPlayerPossibleMoves) == 0:
        return jsonify({'board': convertBoardToArray(newState), 'whiteScore': whiteScore, 'blackScore':blackScore, 'gameOver': 2, 'move': currentMove + 1}), 200
    elif len(newBoardOpponentPossibleMoves) == 0:
        return jsonify({'board': convertBoardToArray(newState), 'whiteScore': whiteScore, 'blackScore':blackScore, 'gameOver': 1, 'move': currentMove + 1}), 200
    newState = addPossibleMovesToBoard(newState, newBoardOpponentPossibleMoves, opponent)
    return jsonify({'board': convertBoardToArray(newState), 'whiteScore': whiteScore, 'blackScore':blackScore, 'gameOver': 0, 'move': currentMove + 1}), 200

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
    currentMove = request.json['move']

    position = (coordinate[0] * 8) + coordinate[1]

    stringBoard = convertBoardToString(board)
    possible_moves = findPossibleMoves(stringBoard, player)
    oldWhiteScore, oldBlackScore = parseScore(stringBoard)
    if position not in possible_moves:
        return jsonify({'valid': False, 'board': data['board'], 'whiteScore': oldWhiteScore, 'blackScore': oldBlackScore, 'move': currentMove}), 200
    newState = newBoardState(stringBoard, player, position)
    whiteScore, blackScore = parseScore(newState)
    return jsonify({'valid': True, 'board': convertBoardToArray(newState), 'whiteScore': whiteScore, 'blackScore':blackScore, 'move': currentMove + 1}), 200

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
            else:
                string_board += "."
    return string_board

def convertBoardToArray(board):
    array_board = [[] for _ in range(8)]
    for i in range(8):
        for j in range(8):
            if board[i*8 + j] == ".":
                array_board[i].append(0)
            elif board[i*8 + j] == "o":
                array_board[i].append(1)
            elif board[i*8 + j] == "x":
                array_board[i].append(2)
            elif board[i*8 + j] == "w":
                array_board[i].append(3)
            elif board[i*8 + j] == "b":
                array_board[i].append(4)
            # array_board[i].append(0 if board[i*8 + j] == "." else 1 if board[i*8 + j] == "o" else 2)
    return array_board

if __name__ == '__main__':
    app.run(host = "0.0.0.0")
