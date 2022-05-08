"""
Created on Sat Mar 09 16:33:01 2020

@author: Pieter Cawood

"""

from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa_agents import Parking, Wall, Space, Robot
from ta_world import MAPNODETYPES
import mesa_sceduler

class Warehouse(Model):
    def __init__(self, world, tsp_seqs, last_sim_step):
        self.schedule = mesa_scheduler.RandomActivation(self)
        self.world = world
        self.tsp_seq = tsp_seqs
        self.last_sim_step = last_sim_step
        self.time_step = 0
        self.task_count = 0
        self.grid = MultiGrid(world.width, world.height, torus=False)
        self.data_collector = DataCollector(
            {"task_count": "task_count"}
        )
        self.robot_count = 0
        # Set up MultiGrid from csv map
        for element in world:
            if world[element] == MAPNODETYPES.WALL:
                # Wall
                agent = Wall(element, self)
                self.grid.place_agent(agent, element)
                self.schedule.add(agent)
                # Task endpoint
            elif world[element] == MAPNODETYPES.TASK_ENDPOINT:
                agent = Space(element, self)
                self.grid.place_agent(agent, element)
                self.schedule.add(agent)
                # Robot spawn endpoint
            elif world[element] == MAPNODETYPES.PARKING:
                # Parking location
                agent = Parking(element, self)
                self.grid.place_agent(agent, element)
                self.schedule.add(agent)
                # Robot location (At park initially)
                self.robot_count += 1
                agent = Robot(element, self, world.agents[self.robot_count].path)
                self.grid.place_agent(agent, element)
                self.schedule.add(agent)
        self.running = True

    def step(self):
        new_task_count = 0
        # Update tasks counter
        for seq_id in self.tsp_seq:
            if self.tsp_seq[seq_id].qsize() > 0:
                if self.time_step >= self.tsp_seq[seq_id].queue[0].release_time:
                    if self.time_step in self.world.agents[seq_id].path:
                        if self.tsp_seq[seq_id].queue[0].delivery_endpoint == \
                                self.world.agents[seq_id].path[self.time_step]:
                            self.tsp_seq[seq_id].get()
            new_task_count += self.tsp_seq[seq_id].qsize()
        self.task_count = new_task_count
        # Stop running once finished
        if self.time_step >= self.last_sim_step:
            self.running = False
        # Next step
        self.time_step += 1
        self.schedule.step()
        self.data_collector.collect(self)
