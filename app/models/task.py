from pydantic import BaseModel
from peewee import (
	Model,
	CharField,
	IntegerField,
	BooleanField
)

from app.database.database import db


# リクエスト時のモデル
class RequestTask(BaseModel):
	title: str = ''
	description: str = ''
	completed: bool = False


# データモデル
class Task(Model):
	# 自動生成される1意のID
	task_id = IntegerField(null=False, primary_key=True, unique=True)
	# タスクのタイトル
	title = CharField(max_length=128)
	# タスクの詳細(任意)
	description = CharField(max_length=1024)
	# タスク完了ステータス(default = False)
	completed = BooleanField(null=False, default=False)

	class Meta:
		database = db
		table_name = 'tasks'


db.create_tables([Task])
