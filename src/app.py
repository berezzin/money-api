import uvicorn
from fastapi import APIRouter
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.config import REDIS_HOST, REDIS_PORT
from src.auth.router import router as auth_router
from src.transactions.router import router as transaction_router
from src.tasks.router import router as report_router
from src.pages.router import router as pages_router

app = FastAPI(title='Money API')

app.mount("/src/static", StaticFiles(directory="src/static"), name="static")

main_router = APIRouter()

main_router.include_router(auth_router, prefix='/auth', tags=['Auth'])
main_router.include_router(transaction_router, prefix='/transaction', tags=['Transactions'])
main_router.include_router(report_router, prefix='/report', tags=['Reports'])
main_router.include_router(pages_router, prefix='/pages', tags=['Pages'])

app.include_router(main_router)

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
