import httpx

from app.config import settings


class APIClient:
    @staticmethod
    def get_users():
        with httpx.Client(timeout=30.0) as client:
            response = client.get(f"{settings.jsonplaceholder_url}/users")
            response.raise_for_status()
            return response.json()

    @staticmethod
    def get_posts(limit: int = 10, skip: int = 0):
        with httpx.Client(timeout=30.0) as client:
            response = client.get(
                f"{settings.dummyjson_url}/posts",
                params={"limit": limit, "skip": skip}
            )
            response.raise_for_status()
            data = response.json()
            return data.get("posts", [])

    @staticmethod
    def get_comments(limit: int = 10, skip: int = 0):
        with httpx.Client(timeout=30.0) as client:
            response = client.get(
                f"{settings.dummyjson_url}/comments",
                params={"limit": limit, "skip": skip}
            )
            response.raise_for_status()
            data = response.json()
            return data.get("comments", [])
