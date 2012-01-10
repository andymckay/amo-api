from config import servers, urls
import requests

class Client(object):
    def get(self, url):
        return requests.get(url).content

class Server(object):
    def __init__(self, server, locale='en-US'):
        self.server = servers[server]
        self.locale = locale
        self.data = {'server': self.server,
                     'locale': self.locale,
                     'version': 1.5}
        self.client = Client()

    def addon(self, addon_id):
        data = self.data.copy()
        data.update(addon_id=addon_id)
        url = urls['api'] + urls['addon']
        url = url.format(**data)
        return self.client.get(url)

    addon.format = 'xml'

if __name__=='__main__':
    srv = Server('amo')
    print srv.addon(3615)
