def test_register_user(client):
    res = client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "Test1234!",
        },
    )
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["username"] == "testuser"
    assert data["user"]["role"] == "user"
    assert data["user"]["is_active"] is True


def test_register_duplicate_username(client):
    client.post(
        "/api/auth/register",
        json={"username": "dup", "email": "a@a.pl", "password": "Test1234!"},
    )
    res = client.post(
        "/api/auth/register",
        json={"username": "dup", "email": "b@b.pl", "password": "Test1234!"},
    )
    assert res.status_code == 400
    assert "zajeta" in res.json()["detail"]


def test_login_success(client):
    client.post(
        "/api/auth/register",
        json={
            "username": "logintest",
            "email": "login@test.pl",
            "password": "Pass1234!",
        },
    )
    res = client.post(
        "/api/auth/login",
        data={"username": "logintest", "password": "Pass1234!"},
    )
    assert res.status_code == 200
    assert "access_token" in res.json()


def test_login_wrong_password(client):
    client.post(
        "/api/auth/register",
        json={
            "username": "wrongpass",
            "email": "wp@test.pl",
            "password": "Pass1234!",
        },
    )
    res = client.post(
        "/api/auth/login",
        data={"username": "wrongpass", "password": "badpassword"},
    )
    assert res.status_code == 401


def test_get_me(client, user_token):
    res = client.get(
        "/api/auth/me", headers={"Authorization": f"Bearer {user_token}"}
    )
    assert res.status_code == 200
    assert res.json()["user"]["username"] == "testuser"


def test_get_me_unauthorized(client):
    res = client.get("/api/auth/me")
    assert res.status_code == 401
