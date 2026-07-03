def test_create_movie(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    res = client.post(
        "/api/movies",
        json={"title": "Incepcja", "description": "Film o snach", "genre": "Sci-Fi"},
        headers=headers,
    )
    assert res.status_code == 201
    data = res.json()
    assert data["title"] == "Incepcja"
    assert data["genre"] == "Sci-Fi"


def test_get_movies(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    client.post(
        "/api/movies",
        json={"title": "M1", "description": "D1", "genre": "Horror"},
        headers=headers,
    )
    client.post(
        "/api/movies",
        json={"title": "M2", "description": "D2", "genre": "Komedia"},
        headers=headers,
    )
    res = client.get("/api/movies")
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_get_movie_by_id(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    created = client.post(
        "/api/movies",
        json={"title": "Target", "description": "Find me", "genre": "Dramat"},
        headers=headers,
    ).json()
    res = client.get(f"/api/movies/{created['id']}")
    assert res.status_code == 200
    assert res.json()["title"] == "Target"


def test_rate_movie(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    created = client.post(
        "/api/movies",
        json={"title": "Do oceny", "genre": "Akcja"},
        headers=headers,
    ).json()
    res = client.post(
        f"/api/movies/{created['id']}/rate",
        json={"score": 4},
        headers=headers,
    )
    assert res.status_code == 200
    assert res.json()["score"] == 4


def test_rate_movie_invalid_score(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    created = client.post(
        "/api/movies",
        json={"title": "Zla ocena", "genre": "Akcja"},
        headers=headers,
    ).json()
    res = client.post(
        f"/api/movies/{created['id']}/rate",
        json={"score": 6},
        headers=headers,
    )
    assert res.status_code == 400


def test_average_rating(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    created = client.post(
        "/api/movies",
        json={"title": "Średnia", "genre": "Akcja"},
        headers=headers,
    ).json()

    res = client.get(f"/api/movies/{created['id']}")
    assert res.json()["average_rating"] is None

    client.post(
        f"/api/movies/{created['id']}/rate",
        json={"score": 5},
        headers=headers,
    )
    res = client.get(f"/api/movies/{created['id']}")
    assert res.json()["average_rating"] == 5.0
    assert res.json()["rating_count"] == 1


def test_top_movies(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    m1 = client.post(
        "/api/movies",
        json={"title": "Top1", "genre": "Akcja"},
        headers=headers,
    ).json()
    m2 = client.post(
        "/api/movies",
        json={"title": "Top2", "genre": "Akcja"},
        headers=headers,
    ).json()

    client.post(f"/api/movies/{m1['id']}/rate", json={"score": 5}, headers=headers)
    client.post(f"/api/movies/{m2['id']}/rate", json={"score": 3}, headers=headers)

    res = client.get("/api/movies/top?genre=Akcja&limit=5")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 2
    assert data[0]["avg"] == 5.0
    assert data[1]["avg"] == 3.0


def test_search_by_genre(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    client.post(
        "/api/movies",
        json={"title": "SciFi1", "genre": "Sci-Fi"},
        headers=headers,
    )
    client.post(
        "/api/movies",
        json={"title": "Horror1", "genre": "Horror"},
        headers=headers,
    )

    res = client.get("/api/movies/top?genre=Sci-Fi&limit=5")
    assert res.status_code == 200
    assert len(res.json()) == 0


def test_movies_require_auth_for_create(client):
    res = client.post(
        "/api/movies",
        json={"title": "Test", "genre": "Test"},
    )
    assert res.status_code == 401
