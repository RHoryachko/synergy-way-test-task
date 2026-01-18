import pytest
from unittest.mock import patch, MagicMock

try:
    from app.tasks import fetch_users, fetch_posts, fetch_comments
except ImportError:
    pytest.skip("Celery not available", allow_module_level=True)

from app.models import User, Post, Comment


@pytest.fixture
def mock_users_response():
    return [
        {
            "id": 1,
            "name": "Leanne Graham",
            "username": "Bret",
            "email": "Sincere@april.biz",
            "phone": "1-770-736-8031",
            "website": "hildegard.org",
        }
    ]


@pytest.fixture
def mock_posts_response():
    return {
        "posts": [
            {
                "id": 1,
                "userId": 1,
                "title": "Test Title",
                "body": "Test Body",
            }
        ],
        "total": 1,
        "skip": 0,
        "limit": 10
    }


@pytest.fixture
def mock_comments_response():
    return {
        "comments": [
            {
                "id": 1,
                "postId": 1,
                "body": "Test Comment",
                "user": {
                    "id": 1,
                    "username": "testuser"
                }
            }
        ],
        "total": 1,
        "skip": 0,
        "limit": 10
    }


def test_fetch_users(db, mock_users_response):
    with patch("app.services.api_client.APIClient.get_users") as mock_get_users:
        mock_get_users.return_value = mock_users_response

        mock_self = MagicMock()
        mock_self._db = db
        type(mock_self).db = property(lambda self: db)

        result = fetch_users(mock_self)

        assert "Processed" in result
        user = db.query(User).filter(User.external_id == 1).first()
        assert user is not None
        assert user.name == "Leanne Graham"


def test_fetch_posts(db, sample_user, mock_posts_response):
    with patch("app.services.api_client.APIClient.get_posts") as mock_get_posts:
        mock_get_posts.return_value = mock_posts_response["posts"]

        mock_self = MagicMock()
        mock_self._db = db
        type(mock_self).db = property(lambda self: db)

        result = fetch_posts(mock_self, limit=10, skip=0)

        assert "Processed" in result
        post = db.query(Post).filter(Post.external_id == 1).first()
        assert post is not None
        assert post.title == "Test Title"


def test_fetch_comments(db, sample_user, sample_post, mock_comments_response):
    with patch("app.services.api_client.APIClient.get_comments") as mock_get_comments:
        mock_get_comments.return_value = mock_comments_response["comments"]

        mock_self = MagicMock()
        mock_self._db = db
        type(mock_self).db = property(lambda self: db)

        result = fetch_comments(mock_self, limit=10, skip=0)

        assert "Processed" in result
        comment = db.query(Comment).filter(Comment.external_id == 1).first()
        assert comment is not None
        assert comment.body == "Test Comment"
