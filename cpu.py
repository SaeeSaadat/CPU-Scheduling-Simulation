from math import inf
from task import Task
import logging


class CPUMaxTimeException(Exception):
    pass


class CPU:
    def __init__(self):
        self.time_on_current_task = 0
        self.current_task = None
        self.is_busy = False

    def run_task(self, simulation_time: int, task: Task = None,  max_time: int = inf, is_new_task: bool = False):
        # returns whether or not execution is finished (or reached it's time limit)

        if task is None:
            task = self.current_task

        if is_new_task or (task != self.current_task):
            logging.info(f"[{simulation_time}]  [Execution] task {task.id}")
            self.current_task = task
            self.time_on_current_task = 0
        elif self.time_on_current_task > max_time:
            raise CPUMaxTimeException

        self.time_on_current_task += 1
        self.is_busy = True

        task.execute()

        if task.is_finished:
            task.exit(simulation_time + 1)
            self.is_busy = False
        elif self.time_on_current_task >= max_time:
            self.is_busy = False
