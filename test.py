import time
import unittest
from flask import Flask, jsonify, request
from app import app
from unittest.mock import patch
from task_schedule import PeriodicThread


class FlaskCreateTrainTaskTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.Session')  # Mock the Session class
    def test_create_train_task(self, mock_session):
        # Mock data to be sent in POST request
        post_data = {
            'epochs': 10,
            'model_id': 123,
            'task_name': 'test_task'
        }

        # Simulate POST request
        response = self.app.post('/create_train_task', json=post_data)

        # Check if the response is as expected
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'code': 200, 'message': 'Success'})

        # Additional assertions can be made here, such as checking if session.add() and session.commit() were called

    @patch('app.Session')  # Mock the Session class
    def test_create_train_task_data(self, mock_session):
        # Mock data to be sent in POST request
        post_data = {
            'epochs': 10,
            'model_id': 123,
            'task_name': 'test_task'
        }

        # Simulate POST request
        response = self.app.post('/create_train_task', json=post_data)

        # Check if the response is as expected
        self.assertEqual(response.status_code, 200)

        # Assert that the response is in JSON format
        self.assertEqual(response.content_type, "application/json")

        # Load the response data
        response_data = response.json

        # Assert the type of the data in the response
        self.assertIsInstance(response_data, dict)
        self.assertIn('code', response_data)
        self.assertIn('message', response_data)
        self.assertIsInstance(response_data['code'], int)
        self.assertIsInstance(response_data['message'], str)

class TestPeriodicThread(unittest.TestCase):

    @patch('app.Session')
    def test_thread_execution(self, mock_session):
        # Create an instance of the thread
        thread = PeriodicThread(interval=1)

        # Start the thread
        thread.start()

        # Allow some time for the thread to run
        time.sleep(5)

        # Assert that the thread is alive
        self.assertTrue(thread.is_alive())

        # Trigger thread to stop
        thread.terminate()

        # Wait for the thread to finish
        thread.join(timeout=10)

        # Assert that the thread has stopped
        self.assertFalse(thread.is_alive())



if __name__ == '__main__':
    unittest.main()
