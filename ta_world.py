"""
Created on Sat Apr 18 10:49:17 2020

@author: Pieter Cawood

"""
from enum import Enum
from ta_agent import *
from ta_state import *


class MAPNODETYPES(Enum):
    PARKING = 0
    PATH = 1
    WALL = 2
    TASK_ENDPOINT = 3


# Loads map. parking and endpoints are numbered in sequence loaded.
# Task endpoints numbered from agent_number + 1
class World(dict):
    def __init__(self, world_file_path, max_path_time):
        self.agents = dict()
        self.endpoints = dict()
        self.parking_locations = dict()
        self.width = 0  # Map width
        self.height = 0  # Map height
        self.load_file(world_file_path, max_path_time)

    def load_file(self, world_file_path, max_path_time):
        file = open(world_file_path, "r")
        if not file.mode == 'r':
            print("Could not open " + world_file_path)
        else:
            print("Loading map file")
            world_data = file.readlines()
            col = 0
            row = 0
            parking_count = 0
            endpoint_count = 0
            for line in world_data:
                col = 0
                for char in line:
                    node = None
                    if char == '.':
                        node = MAPNODETYPES.PATH
                    elif char == 'r':
                        node = MAPNODETYPES.PARKING
                        # Assign new agent at this parking
                        parking_count += 1
                        self.agents[parking_count] = Agent(parking_count, Location(col, row), max_path_time)
                        self.agents[parking_count].path[0] = Location(col, row)
                        self.parking_locations[parking_count] = Location(col, row)
                    elif char == '@':
                        node = MAPNODETYPES.WALL
                    elif char == 'e':
                        node = MAPNODETYPES.TASK_ENDPOINT
                        self.endpoints[endpoint_count] = Location(col, row)
                        endpoint_count += 1
                    if node is not None:
                        # Add node to this collection
                        self[col, row] = node
                    col += 1
                row += 1
        self.width = col
        self.height = row
        file.close()
