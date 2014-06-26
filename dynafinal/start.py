#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dependencies.bottle import post, run, request, response
from gameboard.board import Board
from shipsinker import ShipSinker
import argparse, json

parser = argparse.ArgumentParser(description='Starts the Ship Sinker.')
parser.add_argument('port', metavar='port', type=int, nargs='?',
                   help='the port to listen to')
args = parser.parse_args()

port = 8080
if (args.port):
    port = args.port

@post('/make-move')
def make_move_request():
    if (request.json):
        board = Board.parse(request.json)
        position = ShipSinker().make_move(board)
        return {'x':position.x,'y':position.y}
    else:
        print "Not a json request."
        return {'error':"Not a json request"}

run(host='0.0.0.0', port=port, debug=True)
