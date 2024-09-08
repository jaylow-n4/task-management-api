import os
from dotenv import load_dotenv
from peewee import MySQLDatabase

load_dotenv(f'{os.path.dirname(__file__)}/.env')

DATABASE = os.getenv('DATABASE')
DB_ENDPOINT = os.getenv('DB_ENDPOINT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')


db = MySQLDatabase(
	DATABASE,
	user=DB_USER,
	password=DB_PASSWORD,
	host=DB_ENDPOINT,
	port=3306
)

db.connect()
