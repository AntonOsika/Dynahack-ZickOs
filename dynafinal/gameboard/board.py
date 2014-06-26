#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Board:
    """The Sink Shop Game Board"""

    def __init__(self, size, shots, ships):
        self._size = size
        self._shots = shots
        self._ships = ships

    def size(self):
        return self._size;

    def shots(self):
        return self._shots

    def ships(self):
        return self._ships

    @staticmethod
    def parse(json):
        return Board(json["size"], json["shots"], json["ships"])
