import threading, time
from flask import Flask, render_template, jsonify, request
from db.models import Session, Task, Model
from training import run_training, INPUT_PATH, generate_output_path

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/home/train")
def train():
    return render_template('training.html')

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

@app.route('/create_task', methods=['POST'])
def create_task():
    data = request.json
    task_name = data.get('task_name')
    epoches = data.get('epoches')
    model_id = data.get('model_id')

    session = Session()
    #training_result = run_training(task_name, parameters, epoches)
    task = Task(input_path=INPUT_PATH, output_path=generate_output_path(task_name))
    session.add(task)
    session.commit()
    session.close()

    training_thread = threading.Thread(
        target=training_task_wrapper,
        args=(task_name, model_id, epoches)
    )
    training_thread.start()
    return jsonify({'code': 200, 'message': 'Success'})

def training_task_wrapper(task_name, model_id, epochs):
    # Run the training and get results
    training_results = run_training(task_name, model_id, epochs)

    # Extract the necessary data for saving results
    accuracy = training_results.get('accuracy', 0)
    loss = training_results.get('loss', 0)

    # Save the training results to the database
    save_training_result(task_id, accuracy)

def save_training_result(task_id, accuracy):
    session = Session()

    try:
        new_result = TrainingResult(
            task_id=task_id,
            accuracy=accuracy,
        )
        session.add(new_result)
        session.commit()

        return new_result.id  # or any other confirmation you want to return
    except Exception as e:
        session.rollback()
        print(f"Error occurred: {e}")
    finally:
        session.close()


if __name__ == '__main__':
    app.run(debug = True)
