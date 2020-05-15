"""
Created on Sat Apr 18 11:11:10 2020

@author: Pieter Cawood
"""
import time
from ta_world import *
from ta_task import *
from ta_astar import AStar
from queue import Queue
from itertools import combinations
import mesa_server

GLOBAL_MAX_AGENT_TIME = 1500


def load_files():
    world = World("instances//small//kiva-10-500-5.map", GLOBAL_MAX_AGENT_TIME)
    tasks = TaskDict("instances//small//kiva-1.task", world)
    agent_tour_dict = TourDict("tour//10-1.tour", len(world.agents), tasks)
    return world, tasks, agent_tour_dict


def copy_queue(queue):
    result = Queue()
    for entry in queue.queue:
        result.put(entry)
    return result


def find_agent_path(world, agent, time_step, release_time=0, find_step=0):
    a_star = AStar(world)
    other_agent_paths = []
    parking_locations = []

    # Add other agent paths
    for agent_id in world.agents:
        if agent_id != agent.id:
            other_agent_paths.append(world.agents[agent_id].path)
            parking_locations.append(world.agents[agent_id].parking_location)
    start_location = agent.path[time_step]
    goal_location = agent.next_endpoint

    # Non dummy path, add release time to hold pickup
    new_path = a_star.search(time_step, start_location, goal_location, other_agent_paths, world, parking_locations,
                             agent, release_time, find_step)
    # Could not find path
    if not new_path:
        return False

    # Update agent path
    for state in new_path:
        world.agents[agent.id].path[state.time] = state.location

    world.agents[agent.id].time_at_goal = time_step + len(new_path) - 1
    return world.agents[agent.id].time_at_goal


def test_paths(world):
    for agent_1, agent_2 in combinations(world.agents, 2):
        for time_step in world.agents[agent_1].path:
            if time_step > max(world.agents[agent_2].path):
                break
            # Vertex collision between any two agents
            if world.agents[agent_1].path[time_step] == world.agents[agent_2].path[time_step]:
                print("Agent #" + str(agent_1) + ",#" + str(agent_2) + " vertex collision at " +
                      str(world.agents[agent_1].path[time_step]) + " t:" + str(time_step))
                return False
            # Edge collision between any two agents
            elif (time_step + 1 in world.agents[agent_1].path) and (time_step + 1 in world.agents[agent_2].path):
                if (world.agents[agent_1].path[time_step] == world.agents[agent_2].path[time_step + 1]) and \
                        (world.agents[agent_2].path[time_step] == world.agents[agent_1].path[time_step + 1]):
                    print("Agent #" + str(agent_1) + ",#" + str(agent_2) + " edge collision at " +
                          str(world.agents[agent_1].path[time_step]) + "-" +
                          str(world.agents[agent_2].path[time_step]) + " t:" + str(time_step))
                    return False
    return True


def main():
    world, tasks, tsp_seqs = load_files()
    make_span = 0
    last_sim_step = 0
    closed_list = {}
    time_start = time.perf_counter()
    for next_agent in world.agents:
        time_agent_start = time.perf_counter()
        max_len = 0
        priority_id = -1
        print("Determining execution times", end='')
        '''
        Calculate agents execution time for their paths
        Initialise path to parking position once complete
        '''
        for agent_id in world.agents:
            if agent_id not in closed_list:
                print(".", end='')
                time_step = 0
                new_start_step = -1
                while True:
                    new_start_step += 1
                    time_step = new_start_step
                    seq = copy_queue(tsp_seqs[agent_id])
                    path_failed = False
                    for seq_task in range(seq.qsize()):
                        task = seq.get()
                        # To pickup position
                        world.agents[agent_id].next_endpoint = task.pickup_endpoint
                        time_step = find_agent_path(world, world.agents[agent_id], time_step, task.release_time, 1)
                        if not time_step:
                            path_failed = True
                            break
                        # To delivery position
                        world.agents[agent_id].next_endpoint = task.delivery_endpoint
                        time_step = find_agent_path(world, world.agents[agent_id], time_step, 0, 2)
                        if not time_step:
                            path_failed = True
                            break
                    if not path_failed:
                        break
                # Move agent path back to parking position
                for t_step in range(GLOBAL_MAX_AGENT_TIME):
                    world.agents[agent_id].path[t_step] = world.agents[agent_id].parking_location
                if priority_id == -1 or (time_step > max_len):
                    # Highest execution time so far
                    max_len = time_step
                    priority_id = agent_id
        print("")
        # Expand _id: highest execution time
        closed_list[priority_id] = True
        '''
        Calculate actual prioritized agent path
        '''
        new_start_step = -1
        while True:
            new_start_step += 1
            time_step = new_start_step
            seq = copy_queue(tsp_seqs[priority_id])
            path_failed = False
            for next_task in range(tsp_seqs[priority_id].qsize()):
                task = seq.get()
                # To pickup position
                world.agents[priority_id].next_endpoint = task.pickup_endpoint
                time_step = find_agent_path(world, world.agents[priority_id], time_step, task.release_time, 3)
                if not time_step:
                    path_failed = True
                    break
                # To delivery position
                world.agents[priority_id].next_endpoint = task.delivery_endpoint
                time_step = find_agent_path(world, world.agents[priority_id], time_step, 0, 4)
                if not time_step:
                    path_failed = True
                    break
            if not path_failed:
                break
        # Record make_span before parking travel
        make_span = max(make_span, world.agents[priority_id].time_at_goal)
        time_agent_stop = time.perf_counter()
        print("Agent #" + str(priority_id) + " execution time: " + str(
            world.agents[priority_id].time_at_goal) + " (calc :" + str(
            round(((time_agent_stop - time_agent_start) / 60), 1)) + " mins)")
        # End - Travel back to parking
        world.agents[priority_id].next_endpoint = world.agents[priority_id].parking_location
        find_agent_path(world, world.agents[priority_id], time_step)
        last_sim_step = max(last_sim_step, world.agents[priority_id].time_at_goal)

    time_stop = time.perf_counter()

    print("Testing solution for collisions")
    if test_paths(world):
        print("Success, no collisions found")
        print("Make_span of :" + str(make_span))
        print("Runtime of :" + str(round(((time_stop - time_start) / 60), 1)) + " minutes")
        # Simulate results
        mesa_server.simulate_scenario(world, tsp_seqs, last_sim_step)


if __name__ == '__main__':
    main()
