import logging
import re
import string
import urlparse

import requests

from config import servers, urls


remove = re.compile('//+')
log = logging.getLogger('amo.api')


class URL(string.Formatter):

    def get_value(self, name, args, kwargs):
        try:
            return super(URL, self).get_value(name, args, kwargs)
        except KeyError:
            if name.startswith('optional|'):
                name = name.split('|')[1]
                try:
                    return super(URL, self).get_value(name, args, kwargs)
                except KeyError:
                    pass

        return ''

    def format(self, format_string, *args, **kwargs):
        res = super(URL, self).format(format_string, *args, **kwargs)
        parsed = urlparse.urlsplit(res)
        url = parsed[0:2] + (remove.sub('/', parsed.path),) + parsed[3:]
        return urlparse.urlunsplit(url)


class ResourceLookup(object):
    def __getattr__(self, name):
        log.debug('Making resource: %s' % name)
        return Resource(name, self._server)


class Resource(ResourceLookup):
    def __init__(self, name, _server):
        self._server = _server
        url = name
        if name in urls:
            url = urls[name]['url']
        self._url = urls['api'] + url

    def get(self, **kwargs):
        data = self._server._data.copy()
        data.update(**kwargs)
        url = URL().format(self._url, **data)
        log.debug('Calling URL: %s' % url)
        return requests.get(url).content


class Server(ResourceLookup):
    def __init__(self, server, locale='en-US'):
        self._locale = locale
        self._data = {'server': servers[server],
                      'locale': self._locale,
                      'version': 1.5}
        self._server = self


if __name__=='__main__':
    srv = Server('amo')
    print srv.addon.get(3615)
