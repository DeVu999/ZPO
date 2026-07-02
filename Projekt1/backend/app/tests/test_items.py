def test_create_item(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    res = client.post(
        "/api/items",
        json={"name": "TestItem", "description": "Opis testowy"},
        headers=headers,
    )
    assert res.status_code == 201
    data = res.json()
    assert data["name"] == "TestItem"
    assert data["description"] == "Opis testowy"
    assert data["owner_id"] == 1


def test_get_items(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    client.post(
        "/api/items", json={"name": "Item1", "description": "Desc1"}, headers=headers
    )
    client.post(
        "/api/items", json={"name": "Item2", "description": "Desc2"}, headers=headers
    )
    res = client.get("/api/items", headers=headers)
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_get_item_by_id(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    created = client.post(
        "/api/items",
        json={"name": "Target", "description": "Find me"},
        headers=headers,
    ).json()
    res = client.get(f"/api/items/{created['id']}", headers=headers)
    assert res.status_code == 200
    assert res.json()["name"] == "Target"


def test_update_item(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    created = client.post(
        "/api/items",
        json={"name": "Old", "description": "Old desc"},
        headers=headers,
    ).json()
    res = client.patch(
        f"/api/items/{created['id']}",
        json={"name": "Updated"},
        headers=headers,
    )
    assert res.status_code == 200
    assert res.json()["name"] == "Updated"
    assert res.json()["description"] == "Old desc"


def test_delete_item(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    created = client.post(
        "/api/items", json={"name": "DeleteMe"}, headers=headers
    ).json()
    res = client.delete(f"/api/items/{created['id']}", headers=headers)
    assert res.status_code == 204
    res = client.get("/api/items", headers=headers)
    assert len(res.json()) == 0


def test_search_items(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    client.post(
        "/api/items", json={"name": "Alpha", "description": "first"}, headers=headers
    )
    client.post(
        "/api/items", json={"name": "Beta", "description": "second"}, headers=headers
    )
    res = client.get("/api/items/search?keyword=alp", headers=headers)
    assert res.status_code == 200
    assert len(res.json()) == 1
    assert res.json()[0]["name"] == "Alpha"


def test_character_count(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    client.post(
        "/api/items",
        json={"name": "A", "description": "12345"},
        headers=headers,
    )
    client.post(
        "/api/items",
        json={"name": "B", "description": "678"},
        headers=headers,
    )
    res = client.get("/api/items/character-count", headers=headers)
    assert res.status_code == 200
    assert res.json() == 8


def test_items_require_auth(client):
    res = client.get("/api/items")
    assert res.status_code == 401
