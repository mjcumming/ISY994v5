import requests
from requests.auth import HTTPBasicAuth
import json
from urllib.parse import urlencode
from urllib.parse import quote
import sys


class Connection(object):

    def __init__(self,address,port=None,username='',password='',use_https=False):

        self._address = address
        self._port = port
        self._username = username
        self._password = password

        url = (use_https and 'https://' or 'http://') + self._address
        # add port...
        self._url = url

        self._session = requests.Session()
        self._session.auth = (self._username,self._password)

    def compile_request(self, path, query=None):
        url = self._url + '/rest' + '/' + path #.join([quote(item) for item in path])
        if query is not None:
            url += '?' + urlencode(query)

        return url

    def request(self,path,query=None):
        url = self.compile_request(path,query)

        try:
            #print (url)
            response = self._session.get (url)
        
        except requests.ConnectionError as err:
            print ('connection error {}'.format(err))

        except requests.exceptions.Timeout:
            print ('Timed out waiting for response from the ISY device.')        
        
        except:
            print("Oops!",sys.exc_info()[0],"occured.")
            #401 not auth
            #403 forbidden
            #404 not found

        return response



