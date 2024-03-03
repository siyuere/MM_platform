import threading, time
import uuid

from celery import shared_task
from redis import Redis
from flask import Flask, render_template, jsonify, request
from config import celery_init_app
from constants import TASK_RUNNING, TASK_COMPLETED, TASK_ERROR
from db.models import Session, Task, Model, ModelTaskResult, Prediction, db_url
from db_utils.task_utils import get_model_info_by_id, get_model_path_by_id
from task_schedule import PeriodicThread
from training import run_training, INPUT_PATH, generate_output_path

app = Flask(__name__)
app.config.from_mapping(
    CELERY=dict(
        broker_url='redis://localhost:6379/0',
        result_backend='redis://localhost:6379/0',
        task_ignore_result=True,
    ),
)
celery_app = celery_init_app(app)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/home/train")
def train():
    return render_template('training.html')

@app.route("/home/predict")
def predict():
    return render_template('predict.html')

@app.route("/create_model", methods=['POST'])
def create_model():
    session = Session()

    try:
        data = request.json
        model_name = data.get("model_name")
        parameters = data.get("parameters")

        new_model = Model(
            model_name=model_name,
            parameters=parameters,
            creat_time=int(time.time()),
        )

        session.add(new_model)
        session.commit()
        return jsonify({"message": "Model created successfully"})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()

@app.route('/create_train_task', methods=['POST'])
def create_train_task():
    data = request.json
    epochs = data.get('epochs')
    model_id = data.get('model_id')
    task_name = data.get('task_name')

    session = Session()
    output_path = generate_output_path(task_name)
    task = Task(model_id=model_id, task_name=task_name, input_path=INPUT_PATH, output_path=output_path, epochs=epochs)
    session.add(task)
    session.commit()
    session.close()

    return jsonify({'code': 200, 'message': 'Success'})


def save_training_result(task_id, accuracy, output_path):
    session = Session()

    try:
        new_result = ModelTaskResult(
            task_id=task_id,
            accuracy=accuracy,
            output_path=output_path
        )
        session.add(new_result)
        session.commit()

        return new_result.id  # or any other confirmation you want to return
    except Exception as e:
        session.rollback()
        print(f"Error occurred: {e}")
    finally:
        session.close()

@app.route('/make_prediction', methods=['POST'])
def make_prediction():
    data = request.json()
    structure = data.get('structure')
    model_id = data.get('model_id')

    session = Session()
    task = Prediction(model_id=model_id, structure=structure)
    session.add(task)
    session.commit()
    task_id = task.id
    session.close()

    prediction_thread = threading.Thread(
        target=prediction_task_wrapper,
        args=(task_id, model_id, structure)
    )
    prediction_thread.start()
    return jsonify({'code': 200, 'message': 'Success'})

def prediction_task_wrapper(task_id, model_id, structure):
    model_path = get_model_path_by_id(model_id)
    result = predict(model_path, structure)
    session = Session()
    try:
        task = session.query(Prediction).filter_by(id=task_id).first()
        if task:
            task.result = result  # Update the entry with the prediction result
            session.commit()
        else:
            print(f"No task found with task_id: {task_id}")
    except Exception as e:
        print(f"Error occurred: {e}")
        session.rollback()
    finally:
        session.close()



redis_client = Redis(host='localhost', port=6379, db=0, decode_responses=True)
@app.route('/test_redis')
def test_redis():
    # Test writing to Redis
    redis_client.set('test_key', 'test_value')

    # Test reading from Redis
    value = redis_client.get('test_key')

    if value == 'test_value':
        return 'Redis is connected and working!'
    else:
        return 'Something went wrong with Redis!'


if __name__ == '__main__':
    # Create an instance of the custom thread class with a 5-minute interval (300 seconds)
    periodic_thread = PeriodicThread(interval=300)

    # Start the thread
    periodic_thread.start()

    app.run(debug=True)



