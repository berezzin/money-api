import uvicorn
from fastapi import APIRouter
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from .config import REDIS_HOST, REDIS_PORT
from .auth.router import router as auth_router
from .transactions.router import router as transaction_router
from .tasks.router import router as report_router

app = FastAPI(title='Money API')

main_router = APIRouter()

main_router.include_router(auth_router, prefix='/auth', tags=['Auth'])
main_router.include_router(transaction_router, prefix='/transaction', tags=['Transactions'])
main_router.include_router(report_router, prefix='/report', tags=['Reports'])

app.include_router(main_router)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
