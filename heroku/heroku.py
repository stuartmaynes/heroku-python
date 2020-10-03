import json, os
import requests

class Heroku:

    def __init__(self, api_key=None, headers={}):
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = os.getenv('HEROKU_API_KEY')

        self.session = requests.Session()

        self.session.headers.update({
            'Accept': 'application/vnd.heroku+json; version=3',
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        })

        self.session.headers.update(headers)

    def delete(self, endpoint):
        """Return the result of making a DELETE
        request to the Heroku Platform API"""

        return self.session.delete(endpoint)

    def get(self, endpoint, *args, **kwargs):
        """Return the result of making a GET
        request to the Heroku Platform API"""

        return self.session.get(endpoint, *args, **kwargs)

    def patch(self, endpoint, *args, **kwargs):
        """Return the result of making a PATCH
        request to the Heroku Platform API"""

        return self.session.patch(endpoint, *args, **kwargs)

    def put(self, endpoint, *args, **kwargs):
        """Return the result of making a PUT
        request to the Heroku Platform API"""

        return self.session.put(endpoint, *args, **kwargs)

    def post(self, endpoint, *args, **kwargs):
        """Return the result of making a POST
        request to the Heroku Platform API"""

        return self.session.post(endpoint, *args, **kwargs)

