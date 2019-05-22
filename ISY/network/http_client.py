#! /usr/bin/env python

import requests
from urllib.parse import urlencode

import logging
logger = logging.getLogger(__name__)

TIMEOUT = 3

class HTTP_Client(object):

    def __init__(self,address,port=None,username='',password='',use_https=False):

        self._address = address
        self._port = port
        self._username = username
        self._password = password

        url = (use_https and 'https://' or 'http://') + self._address
        # add port...
        self._url = url

        self.create_session()

    def create_session(self):
        self._session = requests.Session()
        self._session.auth = (self._username,self._password)

    def compile_request(self, path, query=None):
        url = self._url + '/rest' + '/' + path 
        if query is not None:
            url = url + '?' + query

        return url

    def request(self,path,query=None, timeout=TIMEOUT): #TBD better error handling and logging
        url = self.compile_request(path,query)

        try:
            logger.info('Request: {}'.format(url,timeout=timeout))
            response = self._session.get (url)
            response.raise_for_status()
            return True,response
        
        except requests.exceptions.RequestException as err:
            logger.warn('Request Error: {}'.format(err))
            return None,err
        except requests.exceptions.HTTPError as errh:
            logger.warn('Request HTTP Error: {}'.format(errh))
            return None,errh
        except requests.exceptions.ConnectionError as errc:
            logger.warn('Request Connection Error: {}'.format(errc))
            return None,errc
        except requests.exceptions.Timeout as errt:
            logger.warn('Request Timeout Error: {}'.format(errt))
            return None, errt