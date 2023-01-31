import math
import logging
from typing import List


class Task:
    tasks: List['Task'] = []

    def __init__(self, arrival, service_time, timeout, priority):
        self.id = len(Task.tasks) + 1
        self.arrival = arrival
        self.service_time = service_time
        self.timeout = timeout
        self.waiting_time = 0
        self.priority = priority
        self.remaining_time = service_time
        self.exit_time = math.inf
        self.current_queue = None
        self.queue_times = {
            'pq': 0,
            'rr1': 0,
            'rr2': 0,
            'fcfs': 0
        }

        Task.tasks.append(self)

    def execute(self):
        self.remaining_time -= 1

        if self.current_queue is not None:
            self.queue_times[self.current_queue.name] = self.queue_times.get(self.current_queue.name, 0) + 1


    def exit(self, time: int):
        self.exit_time = time
        logging.info(f"[{time}]  [Departure] Task {self.id} has left")
        self.waiting_time = time - self.arrival - (self.service_time - self.remaining_time)

    @property
    def is_finished(self) -> bool:
        return self.remaining_time <= 0

    def __repr__(self) -> str:
        return f"\n{self.id}) \n\tArrival: {self.arrival}\n\tservice_time: {round(self.service_time)}\n" \
               f"\ttimeout: {round(self.timeout)}\n\tpriority: {self.priority}\n\twaiting_time: {self.waiting_time}\n" \
               f"\texit time: {self.exit_time}\n" \
               f"\tpq time: {self.queue_times['pq']}\n" \
               f"\trr1 time: {self.queue_times['rr1']}\n" \
               f"\trr2 time: {self.queue_times['rr2']}\n" \
               f"\tfcfs time: {self.queue_times['fcfs']}"

    def __eq__(self, other) -> bool:
        if self is None or other is None:
            return self is None and other is None
        return self.id == other.id

    def __lt__(self, other) -> bool:
        return (self.priority, self.waiting_time) > (other.priority, other.waiting_time)

    @staticmethod
    def remove_for_timed_out_tasks(simulation_time):
        for task in Task.tasks:
            if simulation_time - task.arrival - (task.service_time - task.remaining_time) + 1 > task.timeout:
                logging.warning(f"[TIMEOUT] Task {task.id} timed out and left.")
                task.exit(simulation_time)
                Task.tasks.remove(task)

