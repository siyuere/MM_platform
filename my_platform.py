from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # Path to the database file
db = SQLAlchemy(app)

# define the database model
class TrainingTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='pending')
    parameters = db.Column(db.JSON)  # You can store parameters as JSON

    def __repr__(self):
        return '<TrainingTask %r>' % self.id

class TrainingResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    accuracy = db.Column(db.Float, nullable=True)
    precision = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return '<TrainingResult %r>' % self.id

def create_training_task(parameters):
    """
    Business Logic:
    Create a new training task with the given parameters.

    :param parameters: A dictionary containing the parameters for the training task.
    :return: The created TrainingTask instance.
    """
    new_task = TrainingTask(parameters=parameters)
    db.session.add(new_task)
    db.session.commit()
    return new_task

@app.route('/create_task', methods=['POST'])
def create_task_endpoint():
    data = request.json
    parameters = data.get('parameters')
    new_task = create_training_task(parameters)
    return jsonify({"message": "Task created", "task_id": new_task.id}), 201

def train_task(id):


@app.route('/start_training_task', methods=['POST'])
def start_training():
    data = request.json
    parameters = data.get('parameters', {})
    # Create and start the training task
    new_task = create_training_task(parameters)
    train_task(new_task.id)  # Function to start the training process
    return jsonify({"message": "Training started", "task_id": new_task.id}), 201





@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug = True)