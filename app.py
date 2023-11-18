from flask import Flask, jsonify, request
from typing import TypedDict, Dict
import uuid
from datetime import datetime

app = Flask(__name__)

class Task(TypedDict):
    id: str
    name: str
    description: str
    completion_status: bool
    due_date: str

tasks: Dict[str, Task] = {}

def generate_unique_id() -> str:
    """ Generate a unique ID for each task """
    return str(uuid.uuid4())

def is_valid_date(date_str):
    """ Validate if the date string is in ISO format (YYYY-MM-DD) """
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def sort_tasks_by_due_date(tasks_list, reverse=False):
    """ Sort tasks by their due date """
    # Handling tasks without a due date by placing them at the end or start based on the sort order
    no_date = datetime.max if not reverse else datetime.min
    return sorted(tasks_list, key=lambda x: datetime.strptime(x['due_date'], '%Y-%m-%d') if x['due_date'] else no_date, reverse=reverse)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    limit = request.args.get('limit', default=None, type=int)
    sort_by_date = request.args.get('sort_by_date', default='asc')

    if limit is not None and limit < 1:
        return jsonify({'message': 'Invalid limit value. It must be a positive integer.'}), 400

    tasks_list = list(tasks.values())
    if sort_by_date == 'desc':
        tasks_list = sort_tasks_by_due_date(tasks_list, reverse=True)
    else:
        tasks_list = sort_tasks_by_due_date(tasks_list)

    if limit is not None and limit > 0:
        tasks_list = tasks_list[:limit]

    return jsonify({'tasks': tasks_list})

@app.route('/tasks/<string:task_id>', methods=['GET'])
def get_task(task_id):
    task = tasks.get(task_id)
    if task:
        return jsonify(task)
    return jsonify({'message': 'Task not found'}), 404

@app.route('/tasks', methods=['POST'])
def create_task():
    request_data = request.get_json()
    name = request_data.get('name')
    description = request_data.get('description')
    due_date = request_data.get('due_date', '')

    if not name or not description:
        return jsonify({'message': 'Missing required fields (name, description).'}), 400

    if due_date and not is_valid_date(due_date):
        return jsonify({'message': 'Invalid due date format. Please use YYYY-MM-DD.'}), 400

    task_id = generate_unique_id()
    tasks[task_id] = Task(
        id=task_id,
        name=name,
        description=description,
        completion_status=False,
        due_date=due_date
    )
    return jsonify(tasks[task_id]), 201

@app.route('/tasks/<string:task_id>', methods=['PUT'])
def update_task(task_id):
    if task_id not in tasks:
        return jsonify({'message': 'Task not found'}), 404

    request_data = request.get_json()
    due_date = request_data.get('due_date')

    if due_date is not None and not is_valid_date(due_date):
        return jsonify({'message': 'Invalid due date format. Please use YYYY-MM-DD.'}), 400

    for key in request_data.keys():
        if key in tasks[task_id]:
            tasks[task_id][key] = request_data[key]

    return jsonify(tasks[task_id])

@app.route('/tasks/<string:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if task_id in tasks:
        del tasks[task_id]
        return jsonify({'message': 'Task deleted'})
    return jsonify({'message': 'Task not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
