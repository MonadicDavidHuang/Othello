import functools as ft

from itertools import chain

import sys

baseNum = 10

class Othello:
    
    def __init__(self):
        # self.gameMap = [['N' for i in range(baseNum)] for j in range (baseNum)]
        self.gameMap = [['S', '.', '.', '.', '.', '.', '.', '.'],
                        ['.', '.', '.', '.', '.', '.', '.', '.'],
                        ['.', '.', '.', '.', '.', '.', '.', '.'],
                        ['.', '.', '.', 'B', 'W', '.', '.', '.'],
                        ['.', '.', '.', 'W', 'B', '.', '.', '.'],
                        ['.', '.', '.', '.', '.', '.', '.', '.'],
                        ['.', '.', '.', '.', '.', '.', '.', '.'],
                        ['.', '.', '.', '.', '.', '.', '.', '.']]

    def showGameMap(self):
        gridsStr = "    ".join(list(map(lambda x: str(x), range(baseNum))))
        print("   ", gridsStr, "   ")
        for i, line in enumerate(self.gameMap):
            showLine = "  " + "    ".join(line) + "  "
            print(i, showLine, i)
        print("   ", gridsStr, "   ")


def traverse(gTuple, direction, mC, othelloObj):
    if mC == "W":
        advC = "B"
    elif mC == "B":
        advC = "W"
    else:
        raise ValueError("Invalid collor")

    if direction == "R":
        dTuple = (1, 0)
    elif direction == "RD":
        dTuple = (1, -1)
    elif direction == "D":
        dTuple = (0, -1)
    elif direction == "LD":
        dTuple = (-1, -1)
    elif direction == "L":
        dTuple = (-1, 0)
    elif direction == "LU":
        dTuple = (-1, 1)
    elif direction == "U":
        dTuple = (0, 1)
    elif direction == "RU":
        dTuple = (1, 1)
    else:
        raise ValueError("Invalid direction")

    stackedGridList = []
    validation = False

    x, y = gTuple[0] + dTuple[0], gTuple[1] + dTuple[1] # Set grid which player choose to put stone.

    while (x < baseNum  and 0 <= x and y < baseNum and 0 <= y):
        curEnt = othelloObj.gameMap[y][x]
        if curEnt == advC:
            stackedGridList.append((x, y))
        elif curEnt == mC and len(stackedGridList) > 0:
            validation = True
            break
        elif curEnt == ".":
            stackedGridList = []
            break

        x += dTuple[0]
        y += dTuple[1]

    return [validation, stackedGridList]

def proceedGame(gTuple, mC, othelloObj):
    if not othelloObj.gameMap[gTuple[1]][gTuple[0]] == '.':
        print("This grid had already taken!")
        res =  False
    else:
        travIns = lambda x: traverse(gTuple, x, mC, othelloObj)
        directionList = ["R", "RD", "D", "LD", "L", "LU", "U", "RU"]
        resultList = list(map(travIns, directionList))

        validList = [i for i, j in resultList]

        # Check indicated grid able or not.
        if ft.reduce(lambda a, b: a or b, validList):
            print(":)")
            targetList = list(chain.from_iterable([j for i, j in resultList]))

            for tup in targetList:
                x, y = tup[0], tup[1]
                othelloObj.gameMap[y][x] = mC
            othelloObj.gameMap[gTuple[1]][gTuple[0]] = mC
            res = True
        else:
            print("This grid is not able now :/")
            res = False

    return res

if __name__ == '__main__':
    """
    othelloObj = Othello()
    othelloObj.showGameMap()
    proceedGame((5, 3), "B", othelloObj)
    othelloObj.showGameMap()
    proceedGame((5, 4), "W", othelloObj)
    othelloObj.showGameMap()
    proceedGame((5, 3), "B", othelloObj)
    """
    othelloObj = Othello()
    othelloObj.showGameMap()

    userList = ['B', 'W']
    i = 0

    while True:
        try:
            curStone = userList[i % 2]
            sys.stdout.write(curStone + ":")
            userInput = input()
            if userInput == "exit":
                print("Leaving")
                sys.exit(0)

            userInputList = list(map(int, userInput.split(" ")))
            res = proceedGame((userInputList[0], userInputList[1]), curStone, othelloObj)
            othelloObj.showGameMap()
            if not res:
                continue
            else:
                i += 1

        except ValueError:
            print("Please input 'exit' or 'hoge hoge' with hoge take grid index")
