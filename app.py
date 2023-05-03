import uvicorn
from fastapi import FastAPI
from fastapi import APIRouter
from models import async_session, User

app = FastAPI(title='Money API')

user_router = APIRouter()


@user_router.post('/')
async def create_user(username: str):
    async with async_session() as session:
        session.begin()
        new_user = User(username=username)
        session.add(new_user)
        await session.commit()
        return {'Id': new_user.user_id}


main_router = APIRouter()

main_router.include_router(user_router, prefix='/user', tags=['Users'])
app.include_router(main_router)

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
