#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import random
from gameboard.board import Board
from gameboard.coordinate import Coordinate
import operator
import numpy as np
from math import ceil 

class ShipSinker:
	"""This is the class where all the magic happens. Given a board you should decide on a position to shoot at."""
	def returnHit(self, shots):
		for shot in shots:
			if shot['state'] == 'Seaworthy':
				return [shot['coordinates']['x'], shot['coordinates']['y']]
		return [-1, -1]

	def returnMatrix(self, shots, dimension):
		theBoard = np.zeros((dimension,dimension), dtype=np.int)

		for shot in shots:
			if shot['state'] == 'Missed':
				theBoard[shot['coordinates']['x']][shot['coordinates']['y']] = 1
			if shot['state'] == 'Seaworthy':
				theBoard[shot['coordinates']['x']][shot['coordinates']['y']] = 2
			if shot['state'] == 'Capsized':
				theBoard[shot['coordinates']['x']][shot['coordinates']['y']] = 3
		return theBoard
		
	def returnLengthDirection(self, startX, startY, dirX, dirY, theBoard):
		lengthCounter = 0
		shipCounter = 0
		totCounter = 0
		while True:
			if startX + dirX + (totCounter*dirX) >= self.board.size() or startY + dirY + (totCounter*dirY) >= self.board.size() or startX + dirX + (totCounter*dirX) < 0 or startY + dirY + (totCounter*dirY) < 0 :
				return [lengthCounter,shipCounter] 
			elif theBoard[startX + dirX + (totCounter*dirX)][startY + dirY + (totCounter*dirY)] == 2:
				shipCounter += 1
				totCounter += 1
			elif theBoard[startX + dirX + (totCounter*dirX)][startY + dirY + (totCounter*dirY)] == 0:
				lengthCounter += 1
				totCounter += 1
			else:
				return [lengthCounter, shipCounter]

	def returnWeights(self, x, y, theBoard):
		weights = [0,0,0,0] 
		foo1 = self.returnLengthDirection(x, y, 1, 0, theBoard)
		foo2 = self.returnLengthDirection(x, y, 0, 1, theBoard)
		foo3 = self.returnLengthDirection(x, y, -1, 0, theBoard)
		foo4 = self.returnLengthDirection(x, y, 0, -1, theBoard)


		weights[0] = (foo1[0] + 10*(foo1[1]+foo3[1]))*(foo1[0] != 0)
		weights[1] = (foo2[0] + 10*(foo2[1]+foo4[1]))*(foo2[0] != 0)
		weights[2] = (foo3[0] + 10*(foo1[1]+foo3[1]))*(foo3[0] != 0)
		weights[3] = (foo4[0] + 10*(foo2[1]+foo4[1]))*(foo4[0] != 0)
		return weights

	def weights(self,theBoard,dimension):
		pointsBoard = np.zeros((dimension,dimension))
		for row in range(dimension):
			steps = (theBoard[0][row] ==0)
			for column in range(dimension):
				if column == dimension-1:
					for n in range(int(ceil(steps/2))):
						value = n + 1
						pointsBoard[column-n][row] = value
						pointsBoard[column-steps+1+n][row] = value
				elif theBoard[column+1][row] == 0:
					steps += 1
				else:
					for n in range(int(ceil((steps+1)*0.5))):
						value = n + 1
						pointsBoard[column-n][row] = value
						pointsBoard[column-steps+1+n][row] = value
					steps = 0
		return pointsBoard


	def findSpot(self,theBoard,dimension):

		totWeights = self.weights(theBoard,dimension) + self.weights(theBoard.transpose(),dimension).transpose()
		if self.debug: print self.weights(theBoard,dimension)
		if self.debug: print totWeights
		if self.debug: print theBoard
		
		x = int(np.argmax(totWeights)%dimension )
		y = int(np.argmax(totWeights)//dimension)
		if self.debug: print(x,y)

		return Coordinate(x,y)



	def findLongestShipAlive(self,ships):
		longestShip = 0
		for ship in ships:
			if ship['length'] > longestShip and ship['alive'] == True :
				longestShip = ship['length']
		return longestShip
		


	def make_move(self, board):
		# You get a board-object.



		self.debug = 1
		self.board = board
		theBoard = self.returnMatrix(board.shots(), board.size())

		#if something is sea...
		hit = self.returnHit(board.shots())
		if hit[0] != -1 and hit[1] != -1:
			weights = self.returnWeights(hit[0], hit[1], theBoard)
			if self.debug: print(weights)
			if self.debug: print(hit)
			
			max_index, max_value = max(enumerate(weights), key=operator.itemgetter(1))

			x = hit[0] + (max_index==0)*1 + (max_index==2)*-1
			y = hit[1] + (max_index==1)*1 + (max_index==3)*-1
			
			while theBoard[x][y] == 2:
				x +=  (max_index==0)*1 + (max_index==2)*-1
				y +=  (max_index==1)*1 + (max_index==3)*-1

			if self.debug: print(x,y)
			return Coordinate(x,y)

		else:
			return self.findSpot(theBoard, board.size())

		badCoordinates = True
		while badCoordinates:
			badCoordinates = False
			x = random.randrange(board.size())
			y = random.randrange(board.size())

			for shot in board.shots():
				if shot['coordinates']['x'] == x and shot['coordinates']['y'] == y:
					badCoordinates = True
					break




		if self.debug: print(x,y)

        # Your job is to return a position
		#import pdb; pdb.set_trace()
		return Coordinate(x,y)