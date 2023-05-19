from httpx import AsyncClient


async def test_register_user(ac: AsyncClient):
    response = await ac.post('/auth/register', json={
        "email": "some_mail@gmail.com",
        "password": "string",
        "is_active": True,
        "is_superuser": True,
        "is_verified": True,
        "username": "some_username"
    })
    response_data = response.json()
    assert response.status_code == 201
    assert response_data.get('email') == "some_mail@gmail.com"
    assert response_data.get('is_active') is True
    assert response_data.get('is_superuser') is False
    assert response_data.get('is_verified') is False
    assert response_data.get('username') == "some_username"


async def test_user_login(ac: AsyncClient):
    response = await ac.post('/auth/jwt/login', data={
        'username': 'some_mail@gmail.com',
        "password": "string"
    })

    assert response.status_code == 204
