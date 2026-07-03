def test_create_class(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    res = client.post(
        "/api/classes",
        json={
            "name": "Nowe Zajecia",
            "description": "Opis",
            "instructor": "Trener",
            "datetime": "2026-07-10T12:00:00",
            "capacity": 15,
        },
        headers=headers,
    )
    assert res.status_code == 201
    data = res.json()
    assert data["name"] == "Nowe Zajecia"
    assert data["instructor"] == "Trener"
    assert data["capacity"] == 15
    assert data["free_spots"] == 15


def test_create_class_requires_admin(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    res = client.post(
        "/api/classes",
        json={
            "name": "Bez admina",
            "description": "Opis",
            "instructor": "Trener",
            "datetime": "2026-07-10T12:00:00",
            "capacity": 10,
        },
        headers=headers,
    )
    assert res.status_code == 403


def test_get_all_classes(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    client.post(
        "/api/classes",
        json={
            "name": "Zajecia A",
            "instructor": "Inst A",
            "datetime": "2026-07-10T12:00:00",
            "capacity": 10,
        },
        headers=headers,
    )
    client.post(
        "/api/classes",
        json={
            "name": "Zajecia B",
            "instructor": "Inst B",
            "datetime": "2026-07-11T12:00:00",
            "capacity": 20,
        },
        headers=headers,
    )
    res = client.get("/api/classes")
    assert res.status_code == 200
    assert len(res.json()) >= 2


def test_get_available_classes(client, admin_token, user_token, user2_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    c1 = client.post(
        "/api/classes",
        json={
            "name": "Available Test",
            "instructor": "Inst A",
            "datetime": "2026-07-10T12:00:00",
            "capacity": 1,
        },
        headers=headers,
    ).json()

    ht = {"Authorization": f"Bearer {user_token}"}
    client.post(f"/api/classes/{c1['id']}/signup", headers=ht)

    c2 = client.post(
        "/api/classes",
        json={
            "name": "Empty Class",
            "instructor": "Inst B",
            "datetime": "2026-07-11T12:00:00",
            "capacity": 10,
        },
        headers=headers,
    ).json()

    res = client.get("/api/classes/available")
    assert res.status_code == 200
    data = res.json()
    ids = [c["id"] for c in data]
    assert c2["id"] in ids
    assert c1["id"] not in ids


def test_signup_to_class(client, sample_class, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    res = client.post(f"/api/classes/{sample_class['id']}/signup", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["class_id"] == sample_class["id"]
    assert data["is_waitlisted"] is False


def test_signup_full_goes_to_waitlist(client, full_class, user_token, user2_token):
    h1 = {"Authorization": f"Bearer {user_token}"}
    h2 = {"Authorization": f"Bearer {user2_token}"}

    client.post("/api/auth/register", json={
        "username": "extra", "email": "extra@test.pl", "password": "Extra123!"
    })
    login_res = client.post(
        "/api/auth/login",
        data={"username": "extra", "password": "Extra123!"},
    )
    extra_token = login_res.json()["access_token"]
    h3 = {"Authorization": f"Bearer {extra_token}"}

    res = client.post(f"/api/classes/{full_class['id']}/signup", headers=h3)
    assert res.status_code == 200
    data = res.json()
    assert data["is_waitlisted"] is True


def test_cancel_promotes_from_waitlist(client, full_class, user_token, user2_token):
    client.post("/api/auth/register", json={
        "username": "extra2", "email": "extra2@test.pl", "password": "Extra123!"
    })
    login_res = client.post(
        "/api/auth/login",
        data={"username": "extra2", "password": "Extra123!"},
    )
    extra_token = login_res.json()["access_token"]
    h3 = {"Authorization": f"Bearer {extra_token}"}

    client.post(f"/api/classes/{full_class['id']}/signup", headers=h3)

    ht = {"Authorization": f"Bearer {user_token}"}
    client.delete(f"/api/classes/{full_class['id']}/signup", headers=ht)

    waitlist = client.get(f"/api/classes/{full_class['id']}/waitlist")
    wl_data = waitlist.json()
    assert len(wl_data) == 0

    h2 = {"Authorization": f"Bearer {user2_token}"}
    my_classes = client.get("/api/classes/my-classes", headers=h3)
    mc_data = my_classes.json()
    extra_signup = [c for c in mc_data if c["signup_id"] is not None]
    assert len(extra_signup) == 1
    assert extra_signup[0]["is_waitlisted"] is False


def test_get_waitlist(client, full_class, user_token, user2_token):
    client.post("/api/auth/register", json={
        "username": "wluser", "email": "wl@test.pl", "password": "Wl12345!"
    })
    login_res = client.post(
        "/api/auth/login",
        data={"username": "wluser", "password": "Wl12345!"},
    )
    wl_token = login_res.json()["access_token"]
    h3 = {"Authorization": f"Bearer {wl_token}"}

    client.post(f"/api/classes/{full_class['id']}/signup", headers=h3)

    res = client.get(f"/api/classes/{full_class['id']}/waitlist")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 1
    assert data[0]["user"]["username"] == "wluser"


def test_get_my_classes(client, sample_class, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    client.post(f"/api/classes/{sample_class['id']}/signup", headers=headers)

    res = client.get("/api/classes/my-classes", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 1
    assert data[0]["class_name"] == sample_class["name"]


def test_classes_require_auth_for_create(client):
    res = client.post(
        "/api/classes",
        json={
            "name": "Test",
            "instructor": "Test",
            "datetime": "2026-07-10T12:00:00",
            "capacity": 10,
        },
    )
    assert res.status_code == 401


def test_signup_requires_auth(client, sample_class):
    res = client.post(f"/api/classes/{sample_class['id']}/signup")
    assert res.status_code == 401


def test_delete_class(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    created = client.post(
        "/api/classes",
        json={
            "name": "Do usuniecia",
            "instructor": "Test",
            "datetime": "2026-07-10T12:00:00",
            "capacity": 10,
        },
        headers=headers,
    ).json()

    res = client.delete(f"/api/classes/{created['id']}", headers=headers)
    assert res.status_code == 204

    res = client.get(f"/api/classes/{created['id']}")
    assert res.status_code == 404
