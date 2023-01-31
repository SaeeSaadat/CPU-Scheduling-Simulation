from cpu import CPU
from environment import Environment
from task import Task
import logging

# for final statistics
queue_lens = {
    'pq': [],
    'rr1': [],
    'rr2': [],
    'fcfs': []
}

cpu_busy = []

def main():
    # Preparation
    environment = Environment()
    tasks = environment.create()
    cpu = CPU()
    arrival_checker = arrival_checker_generator(environment)

    # Simulation
    for t in environment.simulate():
        try:
            next(arrival_checker)
        except StopIteration:
            pass

        if should_load_new_tasks(environment):
            task_loader(environment)

        dispatcher(environment, cpu, t)

        queue_lens['pq'].append(len(environment.priorityQueue))
        queue_lens['rr1'].append(len(environment.rrQueue1))
        queue_lens['rr2'].append(len(environment.rrQueue2))
        queue_lens['fcfs'].append(len(environment.fifoQueue))

        cpu_busy.append(1 if cpu.is_busy else 0)


        
    print(Task.tasks[0].queue_times)
    final_results()


def arrival_checker_generator(environment):
    current_job_index = 0
    while current_job_index < len(Task.tasks):
        task = Task.tasks[current_job_index]
        while environment.clock == task.arrival:
            logging.info(f"[{environment.clock}]  [ARRIVAL] Task {task.id} has arrived!")
            environment.load_task(task)
            current_job_index += 1
            if current_job_index >= len(Task.tasks):
                break
            task = Task.tasks[current_job_index]
        yield


def should_load_new_tasks(environment: Environment):
    return len(environment.rrQueue1) + len(environment.rrQueue2) + len(environment.fifoQueue) < environment.k


def task_loader(environment: Environment):
    for _ in range(environment.k):
        if len(environment.priorityQueue) < 1:
            break
        environment.rrQueue1.enqueue(environment.priorityQueue.dequeue())


def dispatcher(environment: Environment, cpu: CPU, simulation_time: int):
    selected_queue = environment.get_second_layer_queue()
    if cpu.is_busy:
        cpu.run_task(simulation_time)
    elif selected_queue is None:
        return
    else:
        task = selected_queue.dequeue()
        execution_time = selected_queue.rrt
        cpu.run_task(simulation_time, task, execution_time)

    if not cpu.is_busy:  # either task has finished or timeout has occurred
        task = cpu.current_task
        if task.is_finished:
            task.exit_time = simulation_time + 1
        else:  # requeue the task
            destination_queue = environment.get_next_queue(selected_queue)
            destination_queue.enqueue(task)


def final_results():
    logging.info("\n\n\n")
    logging.info(Task.tasks)

    for q in ['pq', 'rr1', 'rr2', 'fcfs']:
        logging.info(f'{q} average time: {sum([t.queue_times[q] for t in Task.tasks])/len(Task.tasks)}')
        logging.info(f'{q} average length: {sum(queue_lens[q])/len(queue_lens[q])}')

    logging.info(f'cpu was busy {100*sum(cpu_busy)/len(cpu_busy)}% of the time')


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("simulation.log"),
            logging.StreamHandler()
        ]
    )


if __name__ == '__main__':
    configure_logging()
    main()
