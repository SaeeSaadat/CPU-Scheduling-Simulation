from typing import Optional

import numpy as np
from queues import *
from task import Task
import random


class Environment:
    def __init__(self):
        # self.x = int(input("X: "))
        # self.y = int(input("Y: "))
        # self.z = int(input("Z: "))
        # self.num_of_tasks = int(input("Number of tasks: "))
        # self.sim_length = int(input("Simulation time: "))

        self.x = 0.1
        self.y = 10
        self.z = 100
        self.num_of_tasks = 20
        self.sim_length = 300

        self.clock = 0

        # constants:
        self.t1, self.t2 = Environment.get_quantum_times()
        self.k = Environment.get_k()

        self.priority_weights = [0.1, 0.2, 0.7]
        self.priority_population = [1, 2, 3]  # [LOW, NORMAL, HIGH]
        self.priority_weight_queue = [0.8, 0.1, 0.1]

        self.priorityQueue = PriorityQueue('pq')
        self.rrQueue1 = RoundRobinQueue(self.t1, 'rr1')
        self.rrQueue2 = RoundRobinQueue(self.t1, 'rr2')
        self.fifoQueue = FifoQueue('fcfs')

    def load_task(self, task: Task):
        self.priorityQueue.enqueue_with_priority(task.priority * self.sim_length + task.arrival, task)
        # sorting based on priority and then arrival time
        # sim_length >= max(arrival times)

    def get_second_layer_queue(self) -> Optional[TaskQueue]:
        # returns one of the queues from the second layer based on their priority
        if len(self.rrQueue1) + len(self.rrQueue2) + len(self.fifoQueue) == 0:
            return None  # No tasks in second layer!

        second_layer_queues = [self.rrQueue1, self.rrQueue2, self.fifoQueue]
        queues_weights = [
            self.priority_weight_queue[i] * (1 if len(second_layer_queues[i]) > 0 else 0)
            for i in range(len(second_layer_queues))
        ]
        return random.choices(second_layer_queues, queues_weights)[0]

    def simulate(self):
        while self.clock < self.sim_length:
            yield self.clock
            self.clock += 1
        else:
            return None

    def create(self):
        # this is the JobCreator method
        t = 0
        for i in range(self.num_of_tasks):
            interarrival = np.random.exponential(1/self.x) if i > 0 else 0
            t += interarrival
            service_time = round(np.random.exponential(self.y))
            timeout = round(np.random.exponential(self.z))
            priority = random.choices(self.priority_population, self.priority_weights)[0]
            Task(round(t), service_time, timeout, priority)
        return Task.tasks

    def get_next_queue(self, current_queue: TaskQueue):
        if current_queue == self.rrQueue1:
            return self.rrQueue2
        else:
            return self.fifoQueue

    @staticmethod
    def get_quantum_times():
        return 10, 20

    @staticmethod
    def get_k():
        return 10
