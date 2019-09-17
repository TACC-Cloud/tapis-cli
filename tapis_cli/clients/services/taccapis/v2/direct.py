from tapis_cli.main import PKG_NAME, About, VersionInfo
import requests
from agavepy.agave import Agave

__all__ = ['TaccApiDirectClient']


class TaccApiDirectClient(object):
    """Requests client bootstrapped from a Tapis API client

    The intended use is to implement methods not expressed by the
    current Swagger spec and which are thus not accessible in
    AgavePy. Examples include the 'search' function, which relies
    on encoding a POST form of search terms into a GET request. The
    web request is made directly using the ``requests`` library.
    """
    def __init__(self, agave_client):
        ab = About(PKG_NAME)
        vers = VersionInfo(PKG_NAME)
        # TODO - Catch when client is missing properties
        # token = agave_client.token.token_info['access_token']
        token = agave_client._token
        self.headers = {
            'authorization':
            'Bearer {}'.format(token),
            'user-agent':
            '{}/{}#{}'.format(ab.title, vers.version_string(), ab.git_commit)
        }
        self.api_server = agave_client.api_server
        self.service_name = None
        self.service_version = None
        self.api_path = None

    def setup(self, service_name, service_version, api_path=None):
        setattr(self, 'service_version', service_version)
        setattr(self, 'service_name', service_name)
        setattr(self, 'api_path', api_path)

    def build_url(self, *args):
        path_els = [
            self.service_name, self.service_version, self.api_path, *args
        ]
        # TODO - Filter for leading slashes in path_els
        # TODO - Strip trailing slash from api_server
        url_path_els = [self.api_server]
        url_path_els.extend(path_els)
        url_path_els = [u for u in url_path_els if u is not None]
        return '/'.join(url_path_els)

    def get(self, path=None):
        url = self.build_url(path)
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()
        return resp.json().get('result', {})

    def get_data(self, path=None, params={}):
        url = self.build_url(path)
        resp = requests.get(url, headers=self.headers, params=params)
        resp.raise_for_status()
        return resp.json().get('result', {})

    def post(self, path=None, content_type=None):
        url = self.build_url(path)
        post_headers = self.headers
        if content_type is not None:
            post_headers['Content-type'] = content_type
        resp = requests.post(url, headers=post_headers)
        resp.raise_for_status()
        return resp.json().get('result', {})
