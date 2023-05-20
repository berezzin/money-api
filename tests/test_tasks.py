from httpx import AsyncClient


async def test_send_transaction_report(ac: AsyncClient):
    await ac.post('/auth/register', json={
        "email": "another_mail@gmail.com",
        "password": "string",
        "is_active": True,
        "is_superuser": True,
        "is_verified": True,
        "username": "some_username"
    })

    await ac.post('/auth/jwt/login', data={
        'username': 'another_mail@gmail.com',
        "password": "string"
    })

    auth_token = ac.cookies['money']

    response = await ac.get('/report/transactions', headers={'Cookie': f'money={auth_token}'})

    assert response.status_code == 200
    assert response.json() == {
        "Status": 200,
        "data": "Email has been sent",
        "details": None
    }
