import uvicorn
from fastapi import FastAPI
from app.routers.tasks import router

api = FastAPI()
api.include_router(router)

if __name__ == '__main__':
	uvicorn.run(api, host='127.0.0.1', port=8080)