import unittest
import json
from app import app

class app_test(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def create_task(self, name, description, due_date):
        return self.app.post('/tasks', data=json.dumps({
            'name': name, 
            'description': description, 
            'due_date': due_date
        }), content_type='application/json')

    def test_create_task_valid(self):
        response = self.create_task('New Task', 'New Description', '2023-01-01')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data.decode())
        self.assertEqual(data['due_date'], '2023-01-01')

    def test_create_task_invalid_date(self):
        response = self.create_task('New Task', 'New Description', '01-01-2023')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data.decode())
        self.assertIn('Invalid due date format', data['message'])

    def test_get_tasks(self):
        response = self.app.get('/tasks')
        self.assertEqual(response.status_code, 200)

    def test_get_task(self):
        create_response = self.create_task('Sample Task', 'Sample Description', '2023-01-01')
        task_id = json.loads(create_response.data.decode())['id']

        response = self.app.get(f'/tasks/{task_id}')
        self.assertEqual(response.status_code, 200)
    
    def test_update_task(self):
        create_response = self.create_task('Update Task', 'Update Description', '2023-01-01')
        task_id = json.loads(create_response.data.decode())['id']

        update_data = {
            'name': 'Updated Task',
            'status': True
        }
        response = self.app.put(f'/tasks/{task_id}', data=json.dumps(update_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete_task(self):
        create_response = self.create_task('Delete Task', 'Delete Description', '2023-01-01')
        task_id = json.loads(create_response.data.decode())['id']

        response = self.app.delete(f'/tasks/{task_id}')
        self.assertEqual(response.status_code, 200)    