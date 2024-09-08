from datetime import datetime
import requests
import json

ENDPOINT = 'http://localhost:8080'


def test_get_tasks():
	response = requests.get(
		f'{ENDPOINT}/tasks'
	)

	if response.status_code != 200:
		raise Exception


def test_post_tasks():
	request_body = {
		'title': 'this is test_post_tasks',
		'description': f'now {datetime.now()}'
	}
	response = requests.post(
		f'{ENDPOINT}/tasks',
		data=request_body,
		headers={'Content-Type': 'application/json'}
	)

	if response.status_code != 200:
		raise Exception


def test_get_tasks_task():
	new_task = get_new_task()
	response = requests.get(
		f'{ENDPOINT}/tasks/{new_task['task_id']}'
	)
	if response.status_code != 200:
		raise Exception


def test_put_tasks_task():
	request_body = {
		'title': 'this is test_put_tasks_task',
		'description': 'test_body put_tasks_task'
	}
	new_task = get_new_task()
	response = requests.put(
		f'{ENDPOINT}/tasks{new_task['task_id']}',
		data=request_body,
		headers={'Content-Type': 'application/json'}
	)
	if response.status_code != 200:
		raise Exception


def test_delete_tasks_task():
	new_task = get_new_task()
	response = requests.delete(
		f'{ENDPOINT}/tasks/{new_task['task_id']}'
	)
	if response.status_code != 200:
		raise Exception


def get_new_task():
	response = requests.get(
		f'{ENDPOINT}/tasks'
	)
	tasks = json.loads(response.content.decode('utf-8'))
	tasks['tasks'].sort(key=lambda task: task['task_id'])
	return tasks['tasks'][-1]


def main():
	try:
		test_get_tasks()
		test_post_tasks()
		test_get_tasks_task()
		test_put_tasks_task()
		test_delete_tasks_task()
	except Exception:
		print('test is failed.')
