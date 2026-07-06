import httpx

from app.core.config import settings


class CircleClient:

    def __init__(self):

        self.base_url = settings.CIRCLE_BASE_URL

        self.headers = {

            "Authorization": f"Bearer {settings.CIRCLE_API_KEY}",

            "Content-Type": "application/json"

        }

        self.client = httpx.Client(
            base_url=self.base_url,
            headers=self.headers,
            timeout=30
        )

    def get(self, endpoint):

        return self.client.get(endpoint)

    def post(self, endpoint, data):

        return self.client.post(endpoint, json=data)