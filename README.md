# Simple RESTful API for a To-Do List for ZenPoint

## Overview
This RESTful API, built using Flask, manages a to-do list. It allows creating, retrieving, updating, and deleting tasks. Each task includes a unique identifier, name, description, completion status, and an optional due date in ISO format (`YYYY-MM-DD`). The API uses a dictionary to store tasks. This approach allows for efficient retrieval, updating, and deletion of tasks by their unique identifiers, compared to a list where each element might need to be iterated over to find a specific task.

## Endpoints

### GET /tasks
Retrieves a list of all tasks, with optional parameters to limit the number of tasks and sort by due date.

| Aspect          | Details                                                                                   |
|-----------------|-------------------------------------------------------------------------------------------|
| **URL Params**  | `limit=[integer]`: Limits the number of tasks returned.<br>`sort_by_date=[asc|desc]`: Sorts tasks by due date in ascending or descending order. |
| **Success Response** | Code: `200 OK`<br>Content: List of tasks                                                   |
| **Error Response**   | Code: `400 Bad Request`<br>Content: `{'message': 'Invalid limit value. It must be a positive integer.'}` |

### GET /tasks/:id
Retrieves a specific task by its unique identifier.

| Aspect          | Details                                                                                   |
|-----------------|-------------------------------------------------------------------------------------------|
| **URL Params**  | `task_id=[string]`: Unique identifier of the task.                                        |
| **Success Response** | Code: `200 OK`<br>Content: Task details                                                    |
| **Error Response**   | Code: `404 Not Found`<br>Content: `{'message': 'Task not found'}`                          |

### POST /tasks
Creates a new task with provided details.

| Aspect          | Details                                                                                   |
|-----------------|-------------------------------------------------------------------------------------------|
| **Data Params** | `name=[string]`<br>`description=[string]`<br>`due_date=[string]` (Optional, must be in ISO format) |
| **Success Response** | Code: `201 Created`<br>Content: Created task details                                       |
| **Error Responses**  | Missing Required Fields:<br>- Code: `400 Bad Request`<br>- Content: `{'message': 'Missing required fields (name, description).'}`<br>Invalid Due Date Format:<br>- Code: `400 Bad Request`<br>- Content: `{'message': 'Invalid due date format. Please use YYYY-MM-DD.'}` |

### PUT /tasks/:id
Updates an existing task identified by its unique identifier.

| Aspect          | Details                                                                                   |
|-----------------|-------------------------------------------------------------------------------------------|
| **URL Params**  | `task_id=[string]`: Unique identifier of the task.                                        |
| **Data Params** | Same as `POST /tasks`.                                                                    |
| **Success Response** | Code: `200 OK`<br>Content: Updated task details                                            |
| **Error Responses**  | Task Not Found:<br>- Code: `404 Not Found`<br>- Content: `{'message': 'Task not found'}`<br>Invalid Due Date Format:<br>- Code: `400 Bad Request`<br>- Content: `{'message': 'Invalid due date format. Please use YYYY-MM-DD.'}` |

### DELETE /tasks/:id
Deletes a task by its unique identifier.

| Aspect          | Details                                                                                   |
|-----------------|-------------------------------------------------------------------------------------------|
| **URL Params**  | `task_id=[string]`: Unique identifier of the task.                                        |
| **Success Response** | Code: `200 OK`<br>Content: `{'message': 'Task deleted'}`                                   |
| **Error Response**   | Code: `404 Not Found`<br>Content: `{'message': 'Task not found'}`                          |

## Additional Features
- **Due Date in ISO Format:** To maintain a standard and internationally recognized date format.
- **Sorting by Due Date:** Enhances usability by allowing users to view tasks in order of their deadlines.
- **Limiting Task Retrieval:** Provides control over data load, useful in scenarios with many tasks.

## Running and Testing the To-Do List API

### Setting Up and Running the API

1. Make sure you have Python and Flask installed on your system. 
2. Navigate to the directory containing your Flask application file, app.py, and run the application via ```python app.py```. This will start the Flask server on `http://localhost:5000`.

### Running Unit Tests

The `app_test.py` script contains unit tests for the Flask To-Do List API. To run these tests, execute the test script using Python's unittest module via the command ```python -m unittest app_test``` or ```python3 -m unittest app_test``` depending on your version.

Test Script Details
* `app_test.py` includes tests for creating tasks (both valid and invalid due dates), retrieving tasks, updating tasks, and deleting tasks.
* The script utilizes the Flask testing client to simulate requests to the API and assert the responses.
  
### Testing the API with curl Commands
1. Get a List of All Tasks:
```
curl -X GET http://localhost:5000/tasks
```
2. Get a Specific Task by Its Unique Identifier:

Replace <task_id> with the actual ID of the task:
```
curl -X GET http://localhost:5000/tasks/<task_id>
```
3. Create a New Task:
```
curl -X POST http://localhost:5000/tasks \
-H "Content-Type: application/json" \
-d '{"name": "New Task", "description": "New Task Description", "due_date": "2023-01-01"}'
```
4. Update an Existing Task:
   
Replace <task_id> with the ID of the task:
```
curl -X PUT http://localhost:5000/tasks/<task_id> \
-H "Content-Type: application/json" \
-d '{"name": "Updated Task", "description": "Updated Description", "completion_status": true, "due_date": "2023-01-05"}'
```
5. Delete a Task by Its Unique Identifier:
   
Replace <task_id> with the ID of the task:
```
curl -X DELETE http://localhost:5000/tasks/<task_id>
```
6. Get Tasks with Sorting by Due Date (Ascending/Descending):
   
  For ascending order:

```
curl -X GET "http://localhost:5000/tasks?sort_by_date=asc"
```

  For descending order:

```
curl -X GET "http://localhost:5000/tasks?sort_by_date=desc"
```

7. Get Tasks with a Limit on the Number of Results:
Replace <number> with the number of tasks you want to retrieve:
```
curl -X GET "http://localhost:5000/tasks?limit=<number>"
```

## Areas for Improvement
The To-Do List API works well for basic operations but can be enhanced in several ways:

Database Integration
* Current State: Tasks are stored in a Python dictionary.
* Improvement: Implement a database like SQLite or PostgreSQL for persistent and scalable data storage.
  
User Authentication and Authorization
* Need: To secure the API and allow user-specific task management.
* Solution: Implement authentication mechanisms and access controls.
