"""
Created on Sat Apr 18 11:45:41 2020

@author: Pieter Cawood

"""

class Agent(object):
    def __init__(self, _id, parking_location, max_time):
        self.id = _id
        self.parking_location = parking_location
        self.path = {}
        self.max_time = max_time
        self.next_endpoint = None
        self.time_at_goal = 0
