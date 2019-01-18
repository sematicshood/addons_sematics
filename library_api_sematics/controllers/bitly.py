from flectra import http
from flectra.http import request
import requests
import json
import urllib.parse
from urllib.parse import urlencode
import socket
import datetime
import sys

class Bitly(http.Controller):
    _link   =   'https://api-ssl.bitly.com/v3'

    def get_access(self):
        options =   request.env['library_api_sematics'].search_read([])

        return options[0]['access_token_bitly']

    @http.route('/sematics_api/bitly/shorten', type='http')
    def shorten(self, **params):
        url         = urllib.parse.quote(params['url'])

        access_token = self.get_access()
        longUrl = url

        response    = requests.get('{}/shorten?access_token={}&longUrl={}&format=json'.format(self._link, access_token, longUrl))

        if response.status_code >= 500:
            print('[!] [{0}] Server Error'.format(response.status_code))
            return None
        elif response.status_code == 404:
            print('[!] [{0}] URL not found: [{1}]'.format(response.status_code,api_url))
            return None
        elif response.status_code == 401:
            print('[!] [{0}] Authentication Failed'.format(response.status_code))
            return None
        elif response.status_code >= 400:
            print('[!] [{0}] Bad Request'.format(response.status_code))
            print(response.content)
            return None
        elif response.status_code >= 300:
            print('[!] [{0}] Unexpected redirect.'.format(response.status_code))
            return None
        elif response.status_code == 200:
            added_key = json.loads(response.content)
            return added_key['data']
        else:
            print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))
            return None