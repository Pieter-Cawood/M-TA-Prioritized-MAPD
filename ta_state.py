"""
Created on Sat Apr 18 10:45:11 2020

@author: Pieter Cawood

"""


class Location(object):
    def __init__(self, col, row):
        self.col = col
        self.row = row

    def __eq__(self, other):
        return self.col == other.col and self.row == other.row

    def __hash__(self):
        return hash(str(self.col) + str(self.row))

    def __str__(self):
        return str((self.col, self.row))


class State(object):
    def __init__(self, time, location):
        self.time = time
        self.location = location
        self.g = 0
        self.f = 0

    def __eq__(self, other):
        return self.time == other.time and self.location == other.location

    def __hash__(self):
        return hash(str(self.time) + str(self.location.col) + str(self.location.row))

    def __str__(self):
        return str((self.time, self.location.col, self.location.row))

    def __lt__(self, other):
        if self.f < other.f:
            return True
        else:
            return False
