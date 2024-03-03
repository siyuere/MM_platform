import threading
from collections import deque
import time
from concurrent.futures import ThreadPoolExecutor

from constants import TASK_COMPLETED, TASK_WAITING, TASK_RUNNING, TASK_ERROR
from db.models import Session, Task, ModelTaskResult
from db_utils.task_utils import get_model_info_by_id
from training import run_training

QUEUE_MAX_SIZE = 5

# Define a custom thread class
class PeriodicThread(threading.Thread):
    def __init__(self, interval):
        super().__init__()
        self.interval = interval
        self.daemon = True
        self.queue = deque()
        self.terminate_flag = threading.Event()
        self.executor = ThreadPoolExecutor(max_workers=5)

    def run(self):
        while not self.terminate_flag.is_set():  # Check the flag
            self.schedule()  # Call the function
            if self.terminate_flag.is_set():
                break
            self.terminate_flag.wait(self.interval)

    def terminate(self):
        self.terminate_flag.set()
        self.executor.shutdown(wait=False)

    def schedule(self):
        if self.terminate_flag.is_set():
            return
        print("Start schedule")
        self.check_current_task()
        waiting_tasks = self.list_waiting_task()
        self.run_tasks(waiting_tasks)
        for task in waiting_tasks:
            self.queue.append(task.id)

    def check_current_task(self):
        running_tasks = []
        session = Session()

        while self.queue:
            task_id = self.queue.popleft()
            task = session.query(Task).filter(Task.id == task_id).one()
            if task.status != TASK_RUNNING:
                continue
            running_tasks.append(task.id)
        session.close()
        self.queue.extend(running_tasks)

    def list_waiting_task(self):
        waiting_tasks = []
        session = Session()
        tasks = session.query(Task).filter(Task.status == TASK_WAITING).limit(QUEUE_MAX_SIZE - len(self.queue))
        for task in tasks:
            waiting_tasks.append(task)
        return waiting_tasks

    def run_tasks(self, waiting_tasks):
        for task in waiting_tasks:
            self.executor.submit(self.training_task, task.id, task.model_id, task.epochs, task.output_path)
    def training_task(self, task_id, model_id, epochs, output_path):
        session = Session()
        task = None
        try:
            # Update status to 'In Progress'
            task = session.query(Task).filter(Task.id == task_id).one()

            if task == None:
                print(f"Task with id {task_id} not found.")
                return

            task.status = TASK_RUNNING
            session.commit()

            # Run the training and get results
            model_name, parameters = get_model_info_by_id(model_id)
            accuracy = run_training(task_id, model_name, parameters, epochs, output_path)

            # Save the training results to the database
            result = ModelTaskResult(task_id=task_id, accuracy=accuracy, output_path=output_path)
            task.status = TASK_COMPLETED
            session.add(result)
            session.commit()

        except Exception as e:
            # Update status to 'Failed' upon failure
            session.rollback()
            if task is not None:
                task.status = TASK_ERROR
                session.commit()
            raise e

        finally:
            session.close()
