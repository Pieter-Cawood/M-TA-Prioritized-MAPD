"""
Created on Sat Apr 18 12:51:32 2020

@author: Pieter Cawood
"""
from queue import Queue


class Task(object):
    def __init__(self, task_id, release_time, endpoint_pickup, endpoint_delivery, world):
        self.id = task_id
        self.assigned_agent = None
        self.release_time = release_time
        self.pickup_endpoint = world.endpoints[
            endpoint_pickup]  # world endpoints should match the task_file, check offsets if crash
        self.delivery_endpoint = world.endpoints[endpoint_delivery]


# With key of task_id to pair with TaskSequence
class TaskDict(dict):
    def __init__(self, task_file_path, world):
        self.load_file(task_file_path, world)

    # Loads the task file .task to dictionary with task_id : Task()
    def load_file(self, task_file_path, world):
        file = open(task_file_path, "r")
        if not file.mode == 'r':
            print("Could not open " + task_file_path)
        else:
            print("Loading task file")
            task_data = file.readlines()
            task_id = 0
            for line in task_data:
                if line.find("\t") < 1:
                    #Data seperated with spaces
                    data = line.split(" ")
                else:
                    data = line.split("\t")
                release_time = int(data[0])
                endpoint_pickup = int(data[1])
                endpoint_delivery = int(data[2])
                self[task_id] = Task(task_id, release_time, endpoint_pickup, endpoint_delivery, world)
                task_id += 1


# With key of seq id (max is agent count) to load all tasks
# Seq_id is initially agent listed in tour file
class TourDict(dict):
    def __init__(self, tour_file_path, agent_count, tasks_dict):
        self.load_file(tour_file_path, agent_count, tasks_dict)

    def load_file(self, tour_file_path, agent_count, tasks_dict):
        file = open(tour_file_path, "r")
        if not file.mode == 'r':
            print("Could not open " + tour_file_path)
        else:
            print("Loading tour file")
            tour_data = file.readlines()
            tour_section = False
            agent_sequence = None
            agent_number = 1
            for line in tour_data:
                if "-1" in line:  # end of data
                    if agent_sequence.qsize():
                        self[agent_number] = agent_sequence
                        tour_section = False
                if tour_section:
                    line_val = int(line)
                    if line_val <= agent_count:  # line listed an agent number
                        if agent_sequence.qsize():  # Store previous agent queue
                            self[agent_number] = agent_sequence
                            agent_sequence = Queue()  # Create new agent queue
                            agent_number = line_val
                    else:
                        # Line listed as task number, subtract agent count
                        task_id = line_val - agent_count - 1
                        agent_sequence.put(tasks_dict[task_id])
                        # Set initial agent to tsp seq
                        tasks_dict[task_id].seq_id = agent_number
                if "TOUR_SECTION" in line:  # start of data next line
                    tour_section = True
                    agent_sequence = Queue()
