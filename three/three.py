"""
A new Python wrapper for interacting with the Open311 API.
"""

import os
from collections import defaultdict

import requests
import simplejson as json


class Three(object):
    """The main class for interacting with the Open311 API."""

    def __init__(self, endpoint=None, **kwargs):
        keywords = defaultdict(str)
        keywords.update(kwargs)
        if endpoint:
            keywords['endpoint'] = endpoint
        self._keywords = keywords
        self.configure()

    def _global_api_key(self):
        """
        If a global Open311 API key is available as an environment variable,
        then it will be used when querying.
        """
        if 'OPEN311_API_KEY' in os.environ:
            api_key = os.environ['OPEN311_API_KEY']
        else:
            api_key = ''
        return api_key

    def configure(self, **kwargs):
        """Configure a previously initialized instance of the class."""
        keywords = self._keywords.copy()
        keywords.update(kwargs)
        self.api_key = keywords['api_key'] or self._global_api_key()
        self.endpoint = keywords['endpoint']
        self.format = keywords['format'] or 'json'
        self.jurisdiction = keywords['jurisdiction']
        self.proxy = keywords['proxy']

    def _create_path(self, *args):
        """Create URL path for endpoint and args."""
        if not self.endpoint.endswith('/'):
            self.endpoint += '/'
        args = filter(None, args)
        path = self.endpoint + '/'.join(args) + '.%s' % (self.format)
        return path

    def reset(self):
        """Reset the class back to the original keywords and values."""
        self.configure()

    def convert(self, content):
        """Convert content to Python data structures."""
        if self.format == 'json':
            data = json.loads(content)
        else:
            # XML2Dict the content?
            data = content
        return data

    def get(self, path, **kwargs):
        """Perform a get request."""
        url = self._create_path(path)
        data = requests.get(url, params=kwargs).content
        return data

    def discovery(self, url=None):
        url = self._create_path('discovery')
        data = self.get(url)
        return data

    def services(self, code=None):
        url = self._create_path('services', code)
        data = self.get(url)
        return data