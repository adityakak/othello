""" This file is the code for the alpha-beta pruning engine for Othello"""

neighbors = {}
neighborsUp = {}
neighborsUpRight = {}
neighborsUpLeft = {}
neighborsDown = {}
neighborsDownRight = {}
neighborsDownLeft = {}
neighborsLeft = {}
neighborsRight = {}
quickDirection = {
    0: neighborsUp,
    1: neighborsUpRight,
    2: neighborsRight,
    3: neighborsDownRight,
    4: neighborsDown,
    5: neighborsDownLeft,
    6: neighborsLeft,
    7: neighborsUpLeft}
totalTimeHolder = 0

'''
ADVANCED
Below are two dictionaries mapping board states to other board states. With this when the AI receives a state which is
kept within this "book" it knows immediately what board state it would want to play next
'''

openingBookWhite = \
    {
        # Diagonal Opening
        '..........................xxx......xo...........................': '..................o.......xox......xo...........................',
        '..................ox......xxx......xo...........................': '..................ox......oxx.....ooo...........................',
        '..................ox.....xxxx.....ooo...........................': '...........o......oo.....xxox.....ooo...........................',
        '..................ox......oxx.....oxo......x....................': '..................ox......oooo....oxo......x....................',
        '..................ox......ooxo....oxxx.....x....................': '...........o......oo......ooxo....oxxx.....x....................',
        '..................ooo.....xxxx.....xo...........................': '..................ooo.....ooxx....ooo...........................',
        '............x.....oox.....ooxx....ooo...........................': '............x.....oox.....ooox....oooo..........................',
        '..................ooo.....xoxx.....xx......ox...................': '..................ooo....oooxx.....xx......ox...................',

        # Perpendicular Opening
        '....................o.....xxo......xxx..........................': '....................o....oooo......xxx..........................',
        '....................o.....xxo......xx........x..................': '....................o....oooo......xx........x..................',
        '....................o.....xxo......xxx......ox..................': '....................o.....xxo......xxo......ooo.................',
        '....................o.....xxxx....oxxx......ox..................': '....................o.....xxxx....oxxx......ooo.................',
        '....................o.....xxxx....oxxx......xxo......x..........': '...................oo.....xxox....oxxo......xxo......x..........',
        '...................x.......xx......xo...........................': '...................x.......xx.....ooo...........................',
        '...................x.......xx.....oox.......x...................': '...........o.......o.......ox.....oox.......x...................',
        '...........o.......o.......ox.....oxx.....x.x...................': '...........o.......o.......ox.....oox.....xox...................',
        '...................x.......xx.....oox........x..................': '...................x.......xx.....oooo.......x..................',
        '...................x.......xx.....ooxo......xx..................': '...................xo......ox.....ooxo......xx..................',
        '...................xo......xx.....oxxo.....xxx..................': '...................xo......xx.....oxxo.....xxo.......o..........',

        # Extraneous
        '.................xxx......oxx.....ooo...........................': '.................xxx.o....oxo.....ooo...........................',
        '...........o......oo......ooxxx...oxxx.....x....................': '...........o......oo......ooxxx...ooxx.....o.......o............',
        '..................ox......ooxo....oxxx....xxo...................': '..................ox......ooxo....ooxx....xoo......o............',
        '..................ooo.....ooox....ooox....x..x..................': '..................ooo.....oooo....ooooo...x..x..................',
        '..................ox......oxx.....oox........x..................': '..................ox......oxx.....oooo.......x..................',
        '..................o.......xox......xx.......x...................': '..................o.......oox.....oxx.......x...................',
        '..................o.......xox......xxx..........................': '..................o.......oox.....oxxx..........................',
        '....................o.....xoxx....oox......x....................': '....................o.....xoox....ooo......xo...................',
        '...................xoo....xxox....oxx......x....................': '..................oooo....oxox....oxx......x....................',
        '..................oxoo....oxox....oxx......xx...................': '............o.....oooo....oxox....oxx......xx...................',
        '............o.....oooo....oxox...xxxx......xx...................': '............o.....oooo....oxoo...xxxxo.....xx...................',
        '..........xxo.....xxoo...xxxoo...xxxoo.....xoo......o...........': '..........xxo.....xxoo...xxxoo...xxxoo.....ooo....o.o...........',
        '............o.....oooo....oxox....xxx....x.xx...................': '............o.....oooo....oxoo....xxxo...x.xx...................',
        '............o.....oooo...xxooo....xxxxx..x.xxo..................': '............o.....oooo...xxooo....xoxxx..x.oxo.....o............',
        '............o.....oooo....oxoo....xxxxx..x.xx...................': '............o.....oooo....oooo....xxoox..x.xxo..................',
        '....................oo....xoox....oxx......xx...................': '....................oo....xoox....oox.....oxx...................',
        '............x.......xx...oooxx.....oxxx....xoo..................': '............x.......xx...oooxx.....oxxx...oooo..................',
        '....................o.....xoxx....oxxx....oox........x..........': '....................oo....xoox....ooxx....oox........x..........',
        '..................x.o.....xxo.....oxxx......ox..................': '..................x.o....oooo.....oxxx......ox..................',

    }
openingBookBlack = \
    {
        # Diagonal Opening
        '...........................ox......xo...........................': '..........................xxx......xo...........................',
        '..................o.......xox......xo...........................': '..................ox......xxx......xo...........................',
        '..................ox......oxx.....ooo...........................': '..................ox.....xxxx.....ooo...........................',
        '...........o......oo.....xxox.....ooo...........................': '...........o......oo.....xxox.....xoo......x....................',
        '..................ox......oooo....oxo......x....................': '..................ox......ooxo....oxxx.....x....................',
        '...........o......oo......ooxo....oxxx.....x....................': '...........o......oo......ooxo...xxxxx.....x....................',
        '..................ooo.....xxo......xo...........................': '..................ooo.....xxxx.....xo...........................',
        '..................ooo.....ooxx....ooo...........................': '............x.....oox.....ooxx....ooo...........................',
        '..................ooo.....xoxx.....oo......o....................': '..................ooo.....xoxx.....xx......ox...................',

        # Parallel Opening Only Favorable for Black so it is only in its book
        '..........................xxx.....ooo...........................': '..........................xxx.....oxo......x....................',

        # Perpendicular Opening
        '....................o.....xxo......xo...........................': '....................o.....xxo......xxx..........................',
        '....................o....oooo......xxx..........................': '....................ox...ooox......xxx..........................',
        '....................o....oooo......xx........x..................': '....................ox...ooox......xx........x..................',
        '....................o.....xxo......xo.......ox..................': '....................o.....xxo......xxx......ox..................',
        '....................o.....xoo.....oxxx......ox..................': '....................o.....xxxx....oxxx......ox..................',
        '....................o.....xxxx....oxxx......ooo.................': '....................o.....xxxx....oxxx......xxo......x..........',
        '....................o.....xxo......xox......o...................': '....................o.....xxo......xxx......ox..................',

        # Extraneous
        '.................xxx.....oxooo...xooo.....xo....................': '.................xxx.....oxoxo...xxxxx....xo....................',
        '..........xo......xx.....xxxxo....xxxx....ooo...................': '..........xo......xx.....xxxxo....xxxx....oox........x..........',
        '..................ox.....xoooo...xooo....oox....................': '.................xxx.....xoooo...xooo....oox....................',
        '..........x......oxoo...oxoooo..ooxoo...oxxx....................': '..........xx.....oxxo...oxoxoo..ooxxo...oxxx....................',
        '..................ooo....xoooo....xxo......x....................': '.................xooo....xxooo....xxo......x....................',
        '..................ox......ooxo....ooxx.....xo...................': '..................ox......ooxo....ooxx.....xxx..................',
        '............o.....oo......oxx.....oox........x..................': '............o.....oo......oxx.....oxx.....x..x..................',
        '....................oo....xoox....oox......x....................': '....................oo....xoox....xox.....xx....................',
        '............o.....oooo....oxox....oxx......xx...................': '............o.....oooo....oxox...xxxx......xx...................',
        '............o.....oooo....oxoo...xxxxo.....xx...................': '............o....xoooo....xxoo...xxxxo.....xx...................',
        '............o.....oooo....oxoo....xxxo...x.xx...................': '............o.....oooo....oxoo....xxxxx..x.xx...................',
        '....................o.....xoxo....ooooo...oox........x..........': '....................o.....xoxo....oooxo...oox.x......x..........',
        '..................ooo....oooxx.....xx......ox...................': '..................ooo....oooxx.....xx.....xxx...................',
    }

cornerMultiplier = 115
cornerAdjacent = 30
movesMultiplier = 15
finalMultiplier = 12
closeToEndMultiplier = 6
cornerConnectedEdge = 8
earlyGame = 15
middleGame = 48


def printBoard(board):
    output = ''
    row = 0
    for num in range(len(board[0])):
        if num != 0 and num % 8 == 0:
            output += '\n'
            row += 1
        output += board[0][num] + '   '
    print(output)


def createSets(board):
    x = set()
    o = set()
    for count, value in enumerate(board):
        if value == 'o':
            o.add(count)
        elif value == 'x':
            x.add(count)
    return x, o


def isClear(board, value):
    if value not in board[1] and value not in board[2]:
        return True
    return False


def inBounds(x, y):
    if x < 0 or x >= 8 or y < 0 or y >= 8:
        return None
    return x + (y * 8)


def createNeighbors():
    for value in range(64):
        x, y = value % 8, value // 8
        neighborsUp[value] = inBounds(x, (y - 1))
        neighborsDown[value] = inBounds(x, (y + 1))
        neighborsRight[value] = inBounds((x + 1), y)
        neighborsLeft[value] = inBounds((x - 1), y)
        neighborsUpLeft[value] = inBounds((x - 1), (y - 1))
        neighborsUpRight[value] = inBounds((x + 1), (y - 1))
        neighborsDownLeft[value] = inBounds((x - 1), (y + 1))
        neighborsDownRight[value] = inBounds((x + 1), (y + 1))
        neighbors[value] = {
            neighborsUp[value],
            neighborsDown[value],
            neighborsRight[value],
            neighborsLeft[value],
            neighborsUpLeft[value],
            neighborsUpRight[value],
            neighborsDownLeft[value],
            neighborsDownRight[value]}


def whichGroup(spots, value):
    if spots == neighborsUp[value]:
        return 0
    if spots == neighborsUpRight[value]:
        return 1
    if spots == neighborsRight[value]:
        return 2
    if spots == neighborsDownRight[value]:
        return 3
    if spots == neighborsDown[value]:
        return 4
    if spots == neighborsDownLeft[value]:
        return 5
    if spots == neighborsLeft[value]:
        return 6
    if spots == neighborsUpLeft[value]:
        return 7


def canFlip(board, value, token):
    if token == 'o':
        opp = 'x'
    else:
        opp = 'o'
    # Up, UpRight, Right, DownRight, Down, DownLeft, Left, UpLeft
    directions = [False for x in range(0, 8)]
    contPossible = set()
    for spots in neighbors[value]:
        if spots is not None and board[0][spots] == opp:
            contPossible.add(spots)
            directions[whichGroup(spots, value)] = True
    for count, spots in enumerate(directions):
        if spots:
            direct = quickDirection[count]
            dup = value
            while direct[dup] is not None and board[0][direct[dup]] == opp:
                dup = direct[dup]
            if direct[dup] is None and board[0][dup] != opp:
                continue
            if direct[dup] is not None and board[0][direct[dup]] == token:
                return True
    return False


def possibleMoves(board, token):
    possibleSpots = set()
    for value in (board[1].union(board[2])):
        if isClear(board, neighborsUp[value]):
            possibleSpots.add(neighborsUp[value])
        if isClear(board, neighborsDown[value]):
            possibleSpots.add(neighborsDown[value])
        if isClear(board, neighborsRight[value]):
            possibleSpots.add(neighborsRight[value])
        if isClear(board, neighborsLeft[value]):
            possibleSpots.add(neighborsLeft[value])
        if isClear(board, neighborsUpLeft[value]):
            possibleSpots.add(neighborsUpLeft[value])
        if isClear(board, neighborsUpRight[value]):
            possibleSpots.add(neighborsUpRight[value])
        if isClear(board, neighborsDownRight[value]):
            possibleSpots.add(neighborsDownRight[value])
        if isClear(board, neighborsDownLeft[value]):
            possibleSpots.add(neighborsDownLeft[value])
    if None in possibleSpots:
        possibleSpots.remove(None)
    returnSpots = possibleSpots.copy()
    for value in possibleSpots:
        if canFlip(board, value, token) is False:
            returnSpots.remove(value)
    return sorted(list(returnSpots))


def verifyDirections(board, directionList, position, token, opp):
    savePos = position
    for count, value in enumerate(directionList):
        position = savePos
        if value:
            makeFalse = False
            dirList = quickDirection[count]
            position = dirList[position]
            while board[position] != token:
                if board[position] != opp:
                    makeFalse = True
                    break
                position = dirList[position]
                if position is None:
                    makeFalse = True
                    break
            if makeFalse:
                directionList[count] = False
    return directionList


def move(board, token, position):
    if token == 'o':
        opp = 'x'
    else:
        opp = 'o'
    if token == 'x':
        use = 1
    else:
        use = 2
    # Up, UpRight, Right, DownRight, Down, DownLeft, Left, UpLeft
    directions = [False for x in range(0, 8)]
    possible = set()
    for value in neighbors[position]:
        if value is not None and board[0][value] == opp:
            possible.add(value)
            groupNum = whichGroup(value, position)
            directions[groupNum] = True
    directions = verifyDirections(board[0], directions, position, token, opp)
    original = position
    newBoard = [board[0], board[1].copy(), board[2].copy()]
    newBoard[0] = newBoard[0][:position] + token + newBoard[0][position + 1:]
    newBoard[use].add(position)
    if use == 1:
        notUse = 2
    else:
        notUse = 1
    while any(directions):
        position = original
        saveIndex = directions.index(True)
        direct = quickDirection[saveIndex]
        position = direct[position]
        while newBoard[0][position] != token:
            if newBoard[0][position] == opp:
                newBoard[notUse].remove(position)
            newBoard[0] = newBoard[0][:position] + \
                token + newBoard[0][position + 1:]
            newBoard[use].add(position)
            position = direct[position]
        directions[saveIndex] = False
    return newBoard


def possibleNextBoard(board, possibleSpots, token):
    newBoards = []
    for locations in possibleSpots:
        newBoards.append(move(board.copy(), token, locations))
    return newBoards


def countScore(board, token):
    blackScore = len(board[1])
    whiteScore = len(board[2])
    if blackScore == whiteScore:
        return 0
    if token == 'x' and blackScore > whiteScore:
        return 10000
    elif token == 'x' and whiteScore > blackScore:
        return -10000
    if token == 'o' and whiteScore > blackScore:
        return -10000
    if token == 'o' and blackScore > whiteScore:
        return 10000


def countScore2(board, token):
    if token == 'x':
        return len(board[1])
    else:
        return len(board[2])


def gameOver(board, token):
    if token == 'x':
        oppToken = 'o'
    else:
        oppToken = 'x'
    if len(
        possibleMoves(
            board,
            token)) == 0 and len(
            possibleMoves(
                board,
                oppToken)):
        score = countScore(board, token)
        return score
    return float('inf')


def cornerAdjacentTest(board, token):
    count = 0
    if token == 'x':
        use = 1
    else:
        use = 2
    cornersList = [board[0][0], board[0][7], board[0][56], board[0][63]]
    if 1 in board[use]:
        if cornersList[0] == token:
            count -= 1
        else:
            count += 1
    if 6 in board[use]:
        if cornersList[1] == token:
            count -= 1
        else:
            count += 1
    if 8 in board[use]:
        if cornersList[0] == token:
            count -= 1
        else:
            count += 1
    if 9 in board[use]:
        if cornersList[0] == token:
            count -= 1
        else:
            count += 1
    if 14 in board[use]:
        if cornersList[1] == token:
            count -= 1
        else:
            count += 1
    if 15 in board[use]:
        if cornersList[1] == token:
            count -= 1
        else:
            count += 1
    if 48 in board[use]:
        if cornersList[2] == token:
            count -= 1
        else:
            count += 1
    if 49 in board[use]:
        if cornersList[2] == token:
            count -= 1
        else:
            count += 1
    if 54 in board[use]:
        if cornersList[3] == token:
            count -= 1
        else:
            count += 1
    if 55 in board[use]:
        if cornersList[3] == token:
            count -= 1
        else:
            count += 1
    if 57 in board[use]:
        if cornersList[2] == token:
            count -= 1
        else:
            count += 1
    if 62 in board[use]:
        if cornersList[3] == token:
            count -= 1
        else:
            count += 1
    return count


def cornerTest(board, token):
    count = 0
    if token == 'x':
        use = 1
    else:
        use = 2
    if 0 in board[use]:
        count += 1
    if 7 in board[use]:
        count += 1
    if 56 in board[use]:
        count += 1
    if 63 in board[use]:
        count += 1
    return count


def centerTest(board, token):
    if token == 'x':
        use = 1
    else:
        use = 2
    averageX = averageY = 0
    for value in board[use]:
        x, y = value % 8, value // 8
        averageX += x
        averageY += y
    if(len(board[use]) != 0):
        averageX /= len(board[use])
    if(len(board[use]) != 0):
        averageY /= len(board[use])
    average = int((averageX + (averageY * 8)))
    if average not in {
            18,
            19,
            20,
            21,
            26,
            27,
            28,
            29,
            34,
            35,
            36,
            37,
            42,
            43,
            44,
            45}:
        return -70
    if average in {18, 21, 42, 45}:
        return 0
    if average in {19, 20, 26, 27, 28, 29, 34, 35, 36, 37, 43, 44}:
        return 45


'''
ADVANCED
First Part of Edge Building/Play
This function helps in maintaining proper edge structures and avoid unbalanced edges which can be taken advantage of and
result in steep losses of large swaths of edge space. Checks to see if pieces on the edge are "balanced" meaning they have
equal distance on either side while being connected
'''


def balanceEdges(board, token):
    edgeBalance = [False, False, False, False]
    cornersList = [board[0][0], board[0][7], board[0][56], board[0][63]]
    leftMost = 0
    rightMost = 0
    for i in range(0, 8):  # TopEdge
        if board[0][i] == token:
            leftMost = i
            break
    for i in range(7, -1, -1):
        if board[0][i] == token:
            rightMost = i
    if rightMost != leftMost:
        connected = True
        for i in range(leftMost, rightMost + 1):
            if board[0][i] != token:
                connected = False
                break
        if (7 - rightMost ==
                leftMost and connected) or cornersList[0] == token or cornersList[1] == token:
            edgeBalance[0] = True
    else:
        edgeBalance[0] = 0

    leftMost = 0
    rightMost = 0
    for i in range(54, 64):  # Bottom Edge
        if board[0][i] == token:
            leftMost = i
            break
    for i in range(63, 53, -1):
        if board[0][i] == token:
            rightMost = i
    if rightMost != leftMost:
        connected = True
        for i in range(leftMost, rightMost + 1):
            if board[0][i] != token:
                connected = False
                break
        if (7 - rightMost ==
                leftMost and connected) or cornersList[2] == token or cornersList[3] == token:
            edgeBalance[1] = True
    else:
        edgeBalance[1] = 0

    UpperMost = 0
    DownMost = 0
    for i in range(0, 64, 8):  # Left Edge
        if board[0][i] == token:
            UpperMost = i
            break
    for i in range(56, -8, -8):
        if board[0][i] == token:
            DownMost = i
    if UpperMost != DownMost:
        connected = True
        for i in range(UpperMost, DownMost + 8, 8):
            if board[0][i] != token:
                connected = False
                break
        if (7 - (DownMost // 8) == (UpperMost // 8)
                and connected) or cornersList[0] == token or cornersList[2] == token:
            edgeBalance[2] = True
    else:
        edgeBalance[2] = 0

    UpperMost = 0
    DownMost = 0
    for i in range(7, 71, 8):  # Right Edge
        if board[0][i] == token:
            UpperMost = i
            break
    for i in range(63, -1, -8):
        if board[0][i] == token:
            DownMost = i
    if UpperMost != DownMost:
        connected = True
        for i in range(UpperMost, DownMost + 8, 8):
            if board[0][i] != token:
                connected = False
                break
        if (7 - (DownMost // 8) == (UpperMost // 8)
                and connected) or cornersList[1] == token or cornersList[3] == token:
            edgeBalance[3] = True
    else:
        edgeBalance[3] = 0

    scoreCalc = 0
    for item in edgeBalance:
        if item != 0:
            if item:
                scoreCalc += 35
            else:
                scoreCalc -= 50
    return scoreCalc


'''
ADVANCED
Second Part of Edge Building/Play
This function weights edges which are connected to corners higher as that condition guarantees stability and is a
more powerful position on the board
'''


def edgeTest(board, token):
    cornersList = [board[0][0], board[0][7], board[0][56], board[0][63]]
    count = 0
    done = set()
    if cornersList[0] == token:
        for i in range(1, 7):
            if board[0][i] == token:
                count += cornerConnectedEdge
                done.add(i)
            else:
                break
        for i in range(8, 64, 8):
            if board[0][i] == token:
                count += cornerConnectedEdge
                done.add(i)
            else:
                break
    if cornersList[2] == token:
        for i in range(57, 63):
            if board[0][i] == token:
                count += cornerConnectedEdge
                done.add(i)
            else:
                break
        for i in range(48, 0, -8):
            if board[0][i] == token and i not in done:
                count += cornerConnectedEdge
                done.add(i)
            else:
                break
    if cornersList[1] == token:
        for i in range(6, 0, -1):
            if board[0][i] == token and i not in done:
                count += cornerConnectedEdge
                done.add(i)
            else:
                break
        for i in range(15, 63, 8):
            if board[0][i] == token and i not in done:
                count += cornerConnectedEdge
                done.add(i)
            else:
                break
    if cornersList[3] == token:
        for i in range(62, 56, -1):
            if board[0][i] == token and i not in done:
                count += cornerConnectedEdge
                done.add(i)
            else:
                break
        for i in range(55, 7, -8):
            if board[0][i] == token and i not in done:
                count += cornerConnectedEdge
                done.add(i)
            else:
                break
    return count


def minStep(board, alpha, beta, currentDepth, depthLimit):
    xMoves = possibleMoves(board, 'x')
    oMoves = possibleMoves(board, 'o')
    gameState = gameOver(board, 'o')
    if currentDepth == depthLimit or isinstance(gameState, int):
        score = 0
        position = len(board[1]) + len(board[2])
        if isinstance(gameState, int):
            return gameState + \
                ((countScore2(board, 'o') - countScore2(board, 'x'))
                 * -1 * finalMultiplier)
        if position < earlyGame:  # CHANGES For early game, mobility is valued highly, but after we exit the start it
            # matters a bit less and is reflected in a drop to the weighting
            # score += len(oMoves) * -1 * myMoves * 2
            # score += len(xMoves) * oppMoves
            score += (len(oMoves) - len(xMoves)) * movesMultiplier * -1
        else:
            # score += int(len(oMoves) * -1 * myMoves / 1.4) * 2
            # score += int(len(xMoves) * oppMoves / 1.4)
            score += (len(oMoves) - len(xMoves)) * \
                (movesMultiplier / 1.25) * -1
        if position < middleGame:  # CHANGES From the start to middle of the game tokens adjacent to the corner are
            # penalized at a certain amount, as we reach towards endgame that value is disregarded slight more and
            # finally completely ignored
            # score += cornerAdjacentTest(board, 'o') * cornerAdjacent
            # score += cornerAdjacentTest(board, 'x') * cornerAdjacent * -1
            score += (cornerAdjacentTest(board, 'o') -
                      cornerAdjacentTest(board, 'x')) * cornerAdjacent
        elif position < 57:
            # score += cornerAdjacentTest(board, 'o') * cornerAdjacent / 3
            # score += cornerAdjacentTest(board, 'x') * (cornerAdjacent / 3) * -1
            score += (cornerAdjacentTest(board, 'o') -
                      cornerAdjacentTest(board, 'x')) * cornerAdjacent / 2
        # score += edgeTest(board, 'o') * -1
        # score += edgeTest(board, 'x')
        score += (edgeTest(board, 'o') - edgeTest(board, 'x')) * -1
        score += (balanceEdges(board, 'o') - balanceEdges(board, 'x')) * -1
        if position < middleGame:  # CHANGES Decrease the value of the corners as the game progresses to stop the AI
            # from favoring corners over potential piece differential or other more important endgame characteristics
            # score += cornerTest(board, 'o') * -1 * cornerMultiplier
            # score += cornerTest(board, 'x') * cornerMultiplier
            score += (cornerTest(board, 'o') -
                      cornerTest(board, 'x')) * -1 * cornerMultiplier
        elif position < 57:  # CHANGES Decrease the value of the corners as the game progresses to stop the AI
            # from favoring corners over potential piece differential or other more important endgame characteristics
            # score += cornerTest(board, 'o') * -1 * cornerMultiplier / 4
            # score += cornerTest(board, 'x') * cornerMultiplier / 4
            score += ((cornerTest(board, 'o') - cornerTest(board, 'x'))
                      * -1 * cornerMultiplier) / 2
        if position < earlyGame:  # CHANGES Try to keep the AI within the 4x4 Square in the start of the game to
            # provide a more stable opening, disregarded after early game is complete
            # score += centerTest(board, 'o') * -1
            # score += centerTest(board, 'x')
            score += (centerTest(board, 'o') - centerTest(board, 'x')) * -1
        # score += (pieceStabilityCount(board, 'o') - pieceStabilityCount(board, 'x')) * -1 * stableDiskMultiplier
        if position > 57:  # CHANGES Start caring about piece differential as the game reaches its end
            score += (countScore2(board, 'o') -
                      countScore2(board, 'x')) * closeToEndMultiplier * -1
        return score
    if gameState != float('inf'):
        return gameState
    results = list()
    possibleNewBoards = possibleNextBoard(board, oMoves, 'o')
    if len(possibleNewBoards) == 0:
        return maxStep(board, alpha, beta, currentDepth + 1, depthLimit)
    for nextBoard in possibleNewBoards:
        value = maxStep(nextBoard, alpha, beta, currentDepth + 1, depthLimit)
        results.append(value)
        if not isinstance(value, str) and beta > value:  # PRUNING
            beta = value
        if alpha >= beta:
            return min(results)
    return min(results)


def maxStep(board, alpha, beta, currentDepth, depthLimit):
    xMoves = possibleMoves(board, 'x')
    oMoves = possibleMoves(board, 'o')
    gameState = gameOver(board, 'x')
    if currentDepth == depthLimit or isinstance(gameState, int):
        score = 0
        position = len(board[1]) + len(board[2])
        if isinstance(gameState, int):
            return gameState + (countScore2(board, 'x') -
                                countScore2(board, 'o')) * finalMultiplier
        if position < earlyGame:  # CHANGES For early game, mobility is valued highly, but after we exit the start it
            # matters a bit less and is reflected in a drop to the weighting
            # score += len(oMoves) * -1 * oppMoves
            # score += len(xMoves) * myMoves * 2
            score += (len(xMoves) - len(oMoves)) * movesMultiplier
        else:
            # score += len(oMoves) * -1 * oppMoves / 2
            # score += len(xMoves) * myMoves
            score += (len(xMoves) - len(oMoves)) * (movesMultiplier / 1.25)
        if position < middleGame:  # CHANGES From the start to middle of the game tokens adjacent to the corner are
            # penalized at a certain amount, as we reach towards endgame that value is disregarded slight more and
            # finally completely ignored
            # score += cornerAdjacentTest(board, 'x') * -1 * cornerAdjacent
            # score += cornerAdjacentTest(board, 'o') * cornerAdjacent
            score += (cornerAdjacentTest(board, 'x') -
                      cornerAdjacentTest(board, 'o')) * -1 * cornerAdjacent
        elif position < 57:
            # score += cornerAdjacentTest(board, 'x') * -1 * cornerAdjacent / 3
            # score += cornerAdjacentTest(board, 'o') * (cornerAdjacent / 3)
            score += (cornerAdjacentTest(board, 'x') -
                      cornerAdjacentTest(board, 'o')) * cornerAdjacent / -2
        # score += edgeTest(board, 'x')
        # score += edgeTest(board, 'o') * -1
        score += (edgeTest(board, 'x') - edgeTest(board, 'o'))
        score += (balanceEdges(board, 'x') - balanceEdges(board, 'o'))
        if position < middleGame:  # CHANGES Decrease the value of the corners as the game progresses to stop the AI
            # from favoring corners over potential piece differential or other more important endgame characteristics
            # score += cornerTest(board, 'x') * cornerMultiplier
            # score += cornerTest(board, 'o') * cornerMultiplier * -1
            score += (cornerTest(board, 'x') -
                      cornerTest(board, 'o')) * cornerMultiplier
        elif position < 57:
            # score += cornerTest(board, 'x') * cornerMultiplier / 4
            # score += cornerTest(board, 'o') * cornerMultiplier * -1 / 4
            score += ((cornerTest(board, 'x') - cornerTest(board, 'o'))
                      * cornerMultiplier) / 2
        if position < earlyGame:  # CHANGES Try to keep the AI within the 4x4 Square in the start of the game to
            # provide a more stable opening, disregarded after early game is complete
            # score += centerTest(board, 'x')
            # score += centerTest(board, 'o') * -1
            score += (centerTest(board, 'x') - centerTest(board, 'o'))
        # score += (pieceStabilityCount(board, 'x') - pieceStabilityCount(board, 'o')) * stableDiskMultiplier
        if position > 57:  # CHANGES Start caring about piece differential as the game reaches its end
            score += (countScore2(board, 'x') -
                      countScore2(board, 'o')) * closeToEndMultiplier
        return int(score)
    if gameState != float('inf'):
        return gameState
    results = list()
    possibleNewBoards = possibleNextBoard(board, xMoves, 'x')
    if len(possibleNewBoards) == 0:
        return minStep(board, alpha, beta, currentDepth + 1, depthLimit)
    for nextBoard in possibleNextBoard(board, xMoves, 'x'):
        value = minStep(nextBoard, alpha, beta, currentDepth + 1, depthLimit)
        results.append(value)
        if not isinstance(value, str) and value > alpha:  # PRUNING
            alpha = value
        if alpha >= beta:
            return max(results)
    return max(results)


def maxMove(board, depthLimit):
    gameState = gameOver(board, 'x')
    if gameState != float('inf') and gameState != 'pass':
        return gameState
    results = list()
    resultsPos = list()
    dictionary = {}
    possibles = possibleMoves(board, 'x')
    alpha = float('-inf')
    beta = float('inf')
    # ADVANCED The AI Looks for which move results in the board state held
    # within the opening book dictionary
    if board[0] in openingBookBlack:
        lookingFor = openingBookBlack[board[0]]
        possibleBoard = possibleNextBoard(board, possibles, 'x')
        possibleBoardNew = []
        for items in possibleBoard:
            possibleBoardNew.append(items[0])
        position1 = possibleBoardNew.index(lookingFor)
        return possibles[position1], 0
    for position, nextBoard in enumerate(
            possibleNextBoard(board, possibles, 'x')):
        # results.append(minStep(nextBoard, float('-inf'), float('inf'), 0, depthLimit))
        value = minStep(nextBoard, alpha, beta, 0, depthLimit)
        results.append(value)
        if alpha < value:  # PRUNING
            alpha = value
        resultsPos.append(possibles[position])
        dictionary[possibles[position]] = nextBoard
        # print("Moving at", possibles[position], "results in a score %s" % results[len(results) - 1])
    number = max(results)
    number2 = results.index(number)
    number3 = resultsPos[number2]
    # print()
    # print("I choose space %s" % number3)
    # print()
    return number3, number


def minMove(board, depthLimit):
    gameState = gameOver(board, 'o')
    if gameState != float('inf') and gameState != 'pass':
        return gameState
    results = list()
    resultsPos = list()
    dictionary = {}
    possibles = possibleMoves(board, 'o')
    alpha = float('-inf')
    beta = float('inf')
    # ADVANCED The AI Looks for which move results in the board state held
    # within the opening book dictionary
    if board[0] in openingBookWhite:
        lookingFor = openingBookWhite[board[0]]
        possibleBoard = possibleNextBoard(board, possibles, 'o')
        possibleBoardNew = []
        for items in possibleBoard:
            possibleBoardNew.append(items[0])
        position1 = possibleBoardNew.index(lookingFor)
        return possibles[position1], 0
    for position, nextBoard in enumerate(
            possibleNextBoard(board, possibles, 'o')):
        # results.append(maxStep(nextBoard, float('-inf'), float('inf'), 0, depthLimit))
        value = maxStep(nextBoard, alpha, beta, 0, depthLimit)
        results.append(value)
        if beta > value:  # PRUNING
            beta = value
        resultsPos.append(possibles[position])
        dictionary[possibles[position]] = nextBoard
        # print("Moving at", position, "results in a %s" % results[len(results) - 1])
    number = min(results)
    number2 = results.index(number)
    number3 = resultsPos[number2]
    # print()
    # print("I choose space %s" % number3)
    # print()
    return number3, number


def findNextMoveAB(board, token, depth):
    setX, setO = createSets(board)
    createNeighbors()
    state = [board, setX, setO]
    # printBoard(state)
    if token == 'o':
        move, score = minMove(state, depth)
    if token == 'x':
        move, score = maxMove(state, depth)
    return move
    
def findPossibleMoves(board, token):
    setX, setO = createSets(board)
    createNeighbors()
    return possibleMoves([board, setX, setO], token)

def newBoardState(board, token, position):
    setX, setO = createSets(board)
    createNeighbors()
    return move([board, setX, setO], token, position)[0]


'''
ADVANCED
This Is what I used to generate the board states for the global opening book above, I used a combination of the website
http://samsoft.org.uk/reversi/openings.htm and the Othello Engine WZebra to generate responses to many of the popular openings
This function takes an input of player notation eg.(C4, E3, E5) and generates the board state that would be created after the list of moves
(Saves a bunch of time in creating the book)
'''


def wordsToBoard(letters):
    startString = '...........................ox......xo...........................'
    setX, setO = createSets(startString)
    createNeighbors()
    state = [startString, setX, setO]
    letterTranslate = {
        'A': 0,
        'B': 1,
        'C': 2,
        'D': 3,
        'E': 4,
        'F': 5,
        'G': 6,
        'H': 7,
        'I': 8,
        'J': 9,
        'K': 10,
        'L': 11,
        'M': 12,
        'N': 13,
        'O': 14,
        'P': 15,
        'Q': 16,
        'R': 17,
        'S': 18,
        'T': 19,
        'U': 20,
        'V': 21,
        'W': 22,
        'X': 23,
        'Y': 24,
        'Z': 25}
    breakdown = []
    startSubstring = 0
    letters = letters.strip()
    for number, items in enumerate(letters):
        if items.isnumeric():
            breakdown.append(letters[startSubstring: number + 1])
            startSubstring = number + 1
    currentToken = ''
    for numbers, items in enumerate(breakdown):
        if numbers % 2 == 0:
            currentToken = 'x'
        elif numbers % 2 == 1:
            currentToken = 'o'
        position = letterTranslate[items[:1].upper()] + \
            ((int(items[1:]) - 1) * 8)
        state = move(state, currentToken, position)
    if currentToken == 'x':
        print('Black')
    elif currentToken == 'o':
        print('White')
    printBoard(state)
    print(state)


"""class Strategy:
    logging = True

    def best_strategy(self, board, player, best_move, still_running):
        depth = 1
        print(board)
        for i in range(15):
            best_move.value = findNextMove(board, player, depth)
            print(depth)
            depth += 1"""

