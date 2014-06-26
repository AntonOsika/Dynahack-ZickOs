#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from gameboard.board import Board
from gameboard.coordinate import Coordinate

class ShipSinker:
	"""This is the class where all the magic happens. Given a board you should decide on a position to shoot at."""
	def returnHit(self, shots):
		for shot in shots:
			if shot['state'] == 'Seaworthy':
				return shot['coordinates']
		else:
			return 0

	def returnMatrix(self, shots, dimension):
		theBoard = [[0 for x in xrange(dimension)] for x in xrange(dimension)]
		for shot in shots:
			if shot['state'] == 'Missed':
				theBoard[shot['coordinates']['x']][shot['coordinates']['y']] = 1
			if shot['state'] == 'Seaworthy':
				theBoard[shot['coordinates']['x']][shot['coordinates']['y']] = 2
			if shot['state'] == 'Capsized':
				theBoard[shot['coordinates']['x']][shot['coordinates']['y']] = 3
		return theBoard
		

        def findLongestShipAlive(self,ships):
                longestShip = 0
                for ship in ships:
                        if ship['length'] > longestShip and ship['alive'] = True :
                                longestShip = ship['length']
                return longestShip

	def make_move(self, board):
        # You get a board-object.

		print(self.returnMatrix(board.shots(), board.size()))


		badCoordinates = True
		while badCoordinates:
			badCoordinates = False
			x = random.randrange(board.size())
			y = random.randrange(board.size())

			for shot in board.shots():
				if shot['coordinates']['x'] == x and shot['coordinates']['y'] == y:
					badCoordinates = True
					break



        # Your job is to return a position
		#import pdb; pdb.set_trace()
		return Coordinate(x,y)
