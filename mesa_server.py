"""
Created on Sat Mar 09 16:33:55 2020

@author: Pieter Cawood

"""

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, TextElement
from mesa_model import Warehouse
from mesa_agents import Parking, Wall, Space, Robot


class TaskElement(TextElement):
    def __init__(self):
        pass

    def render(self, model):
        return "Tasks remaining: " + str(model.task_count)


def warehouse_draw(agent):
    if agent is None:
        return
    portrayal = {}

    if type(agent) is Parking:
        # https://icons8.com/icons/set/flag
        portrayal["Color"] = ["#FF8C00", "#FF8C00", "#FF8C00"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1
    elif type(agent) is Wall:
        portrayal["Color"] = ["#000000", "#000000", "#000000"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 1
        portrayal["w"] = 1
        portrayal["h"] = 1
    elif type(agent) is Space:
        portrayal["Color"] = ["#4FA1FF", "#4FA1FF", "#4FA1FF"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1
    elif type(agent) is Robot:
        # https://icons8.com/icons/set/robot
        portrayal["Shape"] = "resources/agent.png"
        portrayal["scale"] = 1
        portrayal["Layer"] = 1
    return portrayal


def simulate_scenario(world, tsp_seqs, last_sim_step):
    model_params = {"world": world, "tsp_seqs": tsp_seqs, "last_sim_step": last_sim_step}
    task_element = TaskElement()
    canvas_element = CanvasGrid(warehouse_draw, world.width, world.height, 700, 420)
    server = ModularServer(Warehouse, [canvas_element, task_element], "MAPD simulation", model_params)
    server.launch()
