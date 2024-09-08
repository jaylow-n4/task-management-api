from fastapi import APIRouter
from fastapi.responses import (
	PlainTextResponse,
	JSONResponse
)
from logging import getLogger

from app.database.database import db
from app.models.task import RequestTask as ReqTask
from app.models.task import Task

router = APIRouter(prefix='/tasks')
logger = getLogger('uvicorn')


# 全てのタスクを取得する
@router.get('')
async def get_all_tasks():
	response = {'tasks': []}
	try:
		with db.atomic():
			for task in Task.select():
				response['tasks'].append(
					{
						'task_id': task.task_id,
						'title': task.title
					}
				)

	except Exception as e:
		db.rollback()
		logger.error(f'error occured {e}')
		return PlainTextResponse(status_code=500, content='Internal Server Error')

	return JSONResponse(status_code=200, content=response)


# 新しいタスクを作成する
@router.post('')
async def post_task(task: ReqTask):
	response = {'message': 'new task created'}
	try:
		with db.atomic():
			id = Task.select().order_by(Task.task_id.desc()).get().task_id + 1

			if task.title == '':
				db.rollback()
				return PlainTextResponse(status_code=400, content='Bad Request')

			Task.create(
				task_id=id,
				title=task.title,
				description=task.description,
				comleted=False
			)

	except Exception as e:
		db.rollback()
		logger.error(f'error occured {e}')
		return PlainTextResponse(status_code=500, content='Internal Server Error')

	return JSONResponse(status_code=201, content=response)


# 指定したタスクIDのタスクを取得する
@router.get('/{task_id}')
async def get_task(task_id: str):
	try:
		with db.atomic():
			task = Task.select().where(Task.task_id == task_id).get()
			response = {
				'task_id': task.task_id,
				'title': task.title,
				'description': task.description,
				'completed': task.completed
			}

	except Task.DoesNotExist:
		db.rollback()
		return PlainTextResponse(status_code=404, content='Not Found')

	except Exception as e:
		db.rollback()
		logger.error(f'error occured {e}')
		return PlainTextResponse(status_code=500, content='Internal Server Error')

	return JSONResponse(status_code=200, content=response)


# 指定したIDのタスクを更新します
@router.put('/{task_id}')
async def put_task(task_id: str, request_task: ReqTask):
	response = {'message': 'task updated'}
	try:
		with db.atomic():
			task = Task.select().where(Task.task_id == task_id).get()

			title = task.title
			if request_task.title != '':
				title = request_task.title
			else:
				db.rollback()
				return PlainTextResponse(status_code=400, content='Bad Reqest')
			description = task.description
			if request_task.description != '':
				description = request_task.description
			completed = task.completed
			if not request_task.completed:
				completed = request_task.completed

			query = Task.update(
				title=title,
				description=description,
				completed=completed
			).where(Task.task_id == task_id)
			query.execute()

	except Task.DoesNotExist:
		db.rollback()
		return PlainTextResponse(status_code=404, content='Not Found')

	except Exception as e:
		db.rollback()
		logger.error(f'error occured {e}')

	return JSONResponse(status_code=200, content=response)


# 指定したIDのタスクを削除します
@router.delete('/{task_id}')
async def delete_task(task_id: str):
	response = {'message': 'task deleted'}
	try:
		with db.atomic():
			Task.select().where(Task.task_id == task_id).get()
			query = Task.delete().where(Task.task_id == task_id)
			query.execute()

	except Task.DoesNotExist:
		db.rollback()
		return PlainTextResponse(status_code=404, content='Not Found')

	except Exception as e:
		db.rollback()
		logger.error(f'error occured {e}')

	return JSONResponse(status_code=200, content=response)
