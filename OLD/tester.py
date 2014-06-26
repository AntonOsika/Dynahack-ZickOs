#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse, json, urllib, urllib2, httplib, hashlib, copy, random

# Here be cli-stuff

parser = argparse.ArgumentParser(description='Runs a game of Ship Sinker against an API')
parser.add_argument('url', metavar='url', type=str, nargs='?',
                   help='The url to the API running the ShipSinker AI')
parser.add_argument('stress', metavar='stress', type=str, nargs='?',
                   help='Stress-test the API, get a rating')
args = parser.parse_args()

if (not args.url):
    print "Missing url, use:   python tester.py <url>"
    exit()

stress = False
if (args.stress == "stress"):
    stress = True

# Here be classes

class Board:
    """GameBoard"""

    def __init__(self):
        self.size = 10
        board = []
        for x in range(self.size):
            board.append([])
            for y in range(self.size):
                board[x].insert(y, Position(x, y))
        self.board = board
        self._distributeShips()

    def _distributeShips(self):
        first = self._distributeOneShip(1, 3)
        for position in first.positions:
            self.board[position.x][position.y].ship_id = first.ship_id

        second = self._distributeOneShip(2, 2)
        for position in second.positions:
            self.board[position.x][position.y].ship_id = second.ship_id


        third = self._distributeOneShip(4, 4)
        for position in third.positions:
            self.board[position.x][position.y].ship_id = third.ship_id

        fourth = self._distributeOneShip(3, 3)
        for position in fourth.positions:
            self.board[position.x][position.y].ship_id = fourth.ship_id


        self.ships = [first, second, third,fourth]

    def _distributeOneShip(self, ship_id, size):
        for i in range(100): # Only 100 tries
            board = copy.deepcopy(self.board)
            positions = []
            leftToPlace = size-1
            x = random.randrange(self.size)
            y = random.randrange(self.size)
            if (board[x][y].ship_id):
                continue
            board[x][y].ship_id = ship_id
            positions.append(Position(x, y))
            stepX = random.randrange(2)
            stepY = 1 - stepX
            for j in range(100):
                if (leftToPlace == 0):
                    return Ship(ship_id, positions)
                newX = x 
                newY = y
                newStepX = stepX * random.randrange(-1,2, 2)
                newStepY = stepY * random.randrange(-1,2, 2)
                while (newX >= 0 and newX < self.size
                        and newY >= 0 and newY < self.size
                        and board[newX][newY].ship_id == ship_id):
                    newX = newX + newStepX
                    newY = newY + newStepY
                if (newX >= 0 and newX < self.size
                        and newY >= 0 and newY < self.size
                        and not board[newX][newY].ship_id):
                    board[newX][newY].ship_id = ship_id
                    positions.append(Position(newX, newY))
                    leftToPlace -= 1

        print "Could not place ship of size " + str(size)
        print board
        exit()

    def generateShips(self):
        toReturn = []
        for ship in self.ships:
            alive = self._shipIsAlive(ship)
            toReturn.append({
                "id": ship.ship_id, 
                "length": len(ship.positions), 
                "alive": alive
            })
        return toReturn

    def _shipIsAlive(self, ship):
        for position in ship.positions:
            if (self.board[position.x][position.y].shot == False):
                return True
        return False

    def generateShots(self):
        toReturn = []
        for x in range(self.size):
            for y in range(self.size):
                if (self.board[x][y].shot == True):
                    position = {
                        "coordinates": {
                            "x": x,
                            "y": y
                        }
                    }
                    if (self.board[x][y].ship_id == None):
                        position["state"] = "Missed"
                    else:
                        ship = self._getShip(self.board[x][y].ship_id)
                        if (self._shipIsAlive(ship)):
                            position["state"] = "Seaworthy"
                        else:
                            position["state"] = "Capsized"
                            position["shipId"] = ship.ship_id
                    toReturn.append(position);
        return toReturn

    def _getShip(self, ship_id):
        for ship in self.ships:
            if (ship.ship_id == ship_id):
                return ship
        return None

    def toDict(self):
        return {
            "size": self.size, 
            "ships": self.generateShips(), 
            "shots": self.generateShots()
        }

    def toJson(self):
        return json.dumps(self.toDict())

    def shoot(self, x, y):
        self.board[x][y].shot = True

    def hasWon(self):
        for ship in self.ships:
            if (self._shipIsAlive(ship)):
                return False
        return True

    def hash(self):
        return hashlib.md5(self.toJson()).hexdigest()

    def __str__(self):
        board = ""
        for y in range(self.size):
            for x in range(self.size):
                if (self.board[x][y].shot == False):
                    board += "?"
                else:
                    ship_id = self.board[x][y].ship_id
                    if (ship_id):
                        if (self._shipIsAlive(self._getShip(ship_id))):
                            board += "X"
                        else:
                            board += str(ship_id)
                    else:
                        board += "~"
                board += " "
            board += "\n"
        return board

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shot = False
        self.ship_id = None

    def __str__(self):
        return str(self.x) + str(self.y) + str(self.shot) + str(self.ship_id)

class Ship:
    def __init__(self, ship_id, positions):
        self.ship_id = ship_id
        self.positions = positions

def playTheGame(url, silent):
    board = Board()
    counter = 0
    hashes = []
    while not board.hasWon():
        counter += 1
        
        if (not silent):
            print ""
        try:
            response = urllib2.urlopen(urllib2.Request(url, board.toJson(), {"Content-type": "application/json"}))
            position = json.loads(response.read())

            if (not silent):
                print "Round " + str(counter) + ": AI shoots at x: " + str(position["x"]) + " and y: " + str(position["y"])
            board.shoot(position["x"], position["y"])
            noProgressLimit = 100
            if (len(hashes) == noProgressLimit):
                hashes.pop(0)
            hashes.append(board.hash())
            if (hashes.count(board.hash()) == noProgressLimit):
                print "No game board change in " + str(noProgressLimit) + " rounds, bye..."
                exit()
            if (not silent):
                print board
        except urllib2.HTTPError:
            print "AI return status 500 :("
            print board
        except urllib2.URLError:
            print "Cannot find any AI at " + url
            exit()
        except httplib.InvalidURL:
            print "Invalid url: " + url
            exit()

        if (board.hasWon()):
            break
        try:
            if (not silent):
                raw_input("Press enter to shoot again (ctrl+c to exit)")
        except KeyboardInterrupt:
            print ""
            print "Ok, bye!"
            exit()

    if (not silent):
        print ""
        print "AI sank all ships in " + str(counter) + " moves!"
    return counter

# Here be the runner
if (stress):
    total = 0
    games = 50
    for i in range(games):
        rounds = playTheGame(args.url, True)
        print "Game " + str(i + 1) + " done in " + str(rounds) + " rounds"
        total += rounds
    print ""
    print "Total rounds " + str(total) + " in " + str(games) + " games"
    print ""
    print "Avarage of " + str(total / games) + " per game"
else:
    playTheGame(args.url, False)
