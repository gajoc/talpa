import requests


class AllegroProvider(object):

    def __init__(self, token, base_url):
        self.token = token
        self.base_url = base_url
        self.headers = self._prepare_headers()

    def search(self, payload):
        return self._get(endpoint='offers/listing', payload=payload)

    def _prepare_headers(self):
        return {
            'Accept': 'application/vnd.allegro.public.v1+json',
            'content-type': 'application/vnd.allegro.public.v1+json',
            'Authorization': 'Bearer %s' % self.token,
        }

    def _get(self, endpoint, payload):
        r = requests.get(url=requests.compat.urljoin(self.base_url, endpoint),
                         headers=self.headers,
                         params=payload)
        return r.json()
