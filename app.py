from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:jihan2301@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.Date)  # New field for due date
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Task(id={self.id}, title={self.title})"
    
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
    

#retrieve all tasks
@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    try:
        tasks = Task.query.all()
        task_list = []
        for task in tasks:
            task_list.append({
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'due_date': task.due_date.isoformat() if task.due_date else None,
                'completed': task.completed
            })
        return jsonify(task_list)
    except SQLAlchemyError as e:
        logger.error(str(e))
        return jsonify({'message': 'An error occurred while retrieving tasks'}), 500

#create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    try:
        task_data = request.json
        title = task_data.get('title')
        description = task_data.get('description')
        due_date = task_data.get('due_date')  # New field for due date
        completed = task_data.get('completed', False)

        new_task = Task(title=title, description=description, due_date=due_date, completed=completed)
        db.session.add(new_task)
        db.session.commit()

        return jsonify({'message': 'Task created successfully!', 'id': new_task.id}), 201
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while creating the task'}), 500

#retrieve a specific task
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'message': 'Task not found'}), 404

        task_data = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'due_date': task.due_date.isoformat() if task.due_date else None,
            'completed': task.completed
        }
        return jsonify(task_data)
    except SQLAlchemyError:
        return jsonify({'message': 'An error occurred while retrieving the task'}), 500

#update a specific task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'message': 'Task not found'}), 404

        task_data = request.json
        task.title = task_data.get('title', task.title)
        task.description = task_data.get('description', task.description)
        task.due_date = task_data.get('due_date', task.due_date)  # Update due date
        task.completed = task_data.get('completed', task.completed)

        db.session.commit()

        return jsonify({'message': 'Task updated successfully!'})
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while updating the task'}), 500

#delete a specific task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'message': 'Task not found'}), 404

        db.session.delete(task)
        db.session.commit()

        return jsonify({'message':'Task deleted successfully!'})
    except SQLAlchemyError:
       db.session.rollback()
       return jsonify({'message': 'An error occurred while deleting the task'}), 500

if __name__ == '__main__':
    app.run(debug=True)