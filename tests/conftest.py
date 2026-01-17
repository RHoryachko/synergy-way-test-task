import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app
from app.models import User, Post, Comment

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_user(db):
    user = User(
        external_id=1,
        name="Test User",
        username="testuser",
        email="test@example.com",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def sample_post(db, sample_user):
    post = Post(
        external_id=1,
        user_id=sample_user.id,
        title="Test Post",
        body="Test body",
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@pytest.fixture
def sample_comment(db, sample_user, sample_post):
    comment = Comment(
        external_id=1,
        post_id=sample_post.id,
        user_id=sample_user.id,
        body="Test comment",
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment
