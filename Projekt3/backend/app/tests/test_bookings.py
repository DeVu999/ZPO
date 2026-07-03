from datetime import datetime, timedelta


def _create_room(client, admin_token, name="Sala Testowa", capacity=10):
    res = client.post(
        "/api/rooms",
        json={"name": name, "capacity": capacity, "description": "Test"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert res.status_code == 200
    return res.json()


def test_create_room(client, admin_token):
    room = _create_room(client, admin_token)
    assert room["name"] == "Sala Testowa"
    assert room["capacity"] == 10


def test_create_room_requires_auth(client):
    res = client.post(
        "/api/rooms",
        json={"name": "Sala X", "capacity": 10},
    )
    assert res.status_code == 401


def test_create_booking(client, user_token, admin_token):
    room = _create_room(client, admin_token)
    now = datetime.utcnow()
    start = (now + timedelta(hours=1)).isoformat()
    end = (now + timedelta(hours=2)).isoformat()

    res = client.post(
        "/api/bookings",
        json={"room_id": room["id"], "start_time": start, "end_time": end, "title": "Test"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["room_id"] == room["id"]
    assert data["title"] == "Test"


def test_booking_time_conflict(client, user_token, admin_token):
    room = _create_room(client, admin_token)
    now = datetime.utcnow()
    start1 = (now + timedelta(hours=1)).isoformat()
    end1 = (now + timedelta(hours=3)).isoformat()
    start2 = (now + timedelta(hours=2)).isoformat()
    end2 = (now + timedelta(hours=4)).isoformat()

    headers = {"Authorization": f"Bearer {user_token}"}
    r1 = client.post(
        "/api/bookings",
        json={"room_id": room["id"], "start_time": start1, "end_time": end1},
        headers=headers,
    )
    assert r1.status_code == 200

    r2 = client.post(
        "/api/bookings",
        json={"room_id": room["id"], "start_time": start2, "end_time": end2},
        headers=headers,
    )
    assert r2.status_code == 409


def test_cancel_booking(client, user_token, admin_token):
    room = _create_room(client, admin_token)
    now = datetime.utcnow()
    start = (now + timedelta(hours=1)).isoformat()
    end = (now + timedelta(hours=2)).isoformat()

    headers = {"Authorization": f"Bearer {user_token}"}
    res = client.post(
        "/api/bookings",
        json={"room_id": room["id"], "start_time": start, "end_time": end},
        headers=headers,
    )
    assert res.status_code == 200
    booking_id = res.json()["id"]

    res2 = client.delete(
        f"/api/bookings/{booking_id}",
        headers=headers,
    )
    assert res2.status_code == 204


def test_get_available_rooms(client, user_token, admin_token):
    room1 = _create_room(client, admin_token, "Sala 1", 10)
    room2 = _create_room(client, admin_token, "Sala 2", 20)
    now = datetime.utcnow()

    start = (now + timedelta(hours=1)).isoformat()
    end = (now + timedelta(hours=2)).isoformat()

    headers = {"Authorization": f"Bearer {user_token}"}
    client.post(
        "/api/bookings",
        json={"room_id": room1["id"], "start_time": start, "end_time": end},
        headers=headers,
    )

    res = client.get(
        f"/api/bookings/available?start_time={start}&end_time={end}",
        headers=headers,
    )
    assert res.status_code == 200
    available = res.json()
    available_ids = [r["id"] for r in available]
    assert room1["id"] not in available_ids
    assert room2["id"] in available_ids


def test_booking_requires_auth(client, admin_token):
    room = _create_room(client, admin_token)
    now = datetime.utcnow()
    start = (now + timedelta(hours=1)).isoformat()
    end = (now + timedelta(hours=2)).isoformat()

    res = client.post(
        "/api/bookings",
        json={"room_id": room["id"], "start_time": start, "end_time": end},
    )
    assert res.status_code == 401


def test_create_room_as_user_forbidden(client, user_token):
    res = client.post(
        "/api/rooms",
        json={"name": "Sala X", "capacity": 10},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert res.status_code == 403
