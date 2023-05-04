import requests
import Constants

GITHUB_API_URL = "https://api.github.com"


class HttpSession:
    def __init__(self, token) -> None:
        self.session = requests.Session()
        self.headers = {
            "Accept": f"{Constants.HEADER_ACCEPT}",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": f"{Constants.HEADER_API_VERSION}"
        }

    def create_request(self, method, url, headers=None, data=None, json=None):
        self.method = method
        self.url = url
        self.headers = self.headers | headers if headers is not None else self.headers
        self.data = data
        self.json = json

    def get_response(self):
        method = getattr(self.session, self.method.lower())
        request_url = f"{GITHUB_API_URL}{self.url}"

        return method(request_url, headers=self.headers, data=self.data, json=self.json)
