

def test_get_users(client, sample_user):
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert len(data["users"]) == 1
    assert data["users"][0]["name"] == "Test User"


def test_get_user(client, sample_user):
    response = client.get(f"/users/{sample_user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"


def test_get_user_not_found(client):
    response = client.get("/users/999")
    assert response.status_code == 404


def test_get_posts(client, sample_post):
    response = client.get("/posts")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["posts"][0]["title"] == "Test Post"


def test_get_post(client, sample_post):
    response = client.get(f"/posts/{sample_post.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Post"


def test_get_post_not_found(client):
    response = client.get("/posts/999")
    assert response.status_code == 404


def test_get_comments(client, sample_comment):
    response = client.get("/comments")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["comments"][0]["body"] == "Test comment"


def test_get_user_posts(client, sample_user, sample_post):
    response = client.get(f"/users/{sample_user.id}/posts")
    assert response.status_code == 200
    data = response.json()
    assert len(data["posts"]) == 1
    assert data["posts"][0]["title"] == "Test Post"


def test_get_post_comments(client, sample_post, sample_comment):
    response = client.get(f"/posts/{sample_post.id}/comments")
    assert response.status_code == 200
    data = response.json()
    assert len(data["comments"]) == 1
    assert data["comments"][0]["body"] == "Test comment"


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
