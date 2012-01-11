import logging
import unittest

import api
import mock

data = {
    'addon_xml_simple': """
<?xml version="1.0" encoding="utf-8" ?>
<addon id="3615">
  <name>Delicious Bookmarks</name>
</addon>
""",
    'search_xml_simple': """
<?xml version="1.0" encoding="utf-8" ?>
<searchresults total_results="15">
    <addon id="4908">
</searchresults>
"""
}


class Wrapper:
    def __init__(self, data):
        self.content = data


class TestURL(unittest.TestCase):
    def setUp(self):
        self.url = api.URL()

    def test_pass(self):
        for url, kwargs, res in (
                ('http://foo.com', {}, 'http://foo.com'),
                ('http://foo.com/bar/{baz}', {'baz':'foo'},
                 'http://foo.com/bar/foo'),
                ('http://foo.com/bar///', {}, 'http://foo.com/bar/'),
                ('http://foo.com/bar/{optional|baz}/', {},
                 'http://foo.com/bar/'),
                ):
            out = self.url.format(url, **kwargs)
            assert out == res, '%s not equal %s' % (out, res)


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.srv = api.Server('amo')

    @mock.patch('requests.get')
    def test_addon(self, get):
        get.return_value = Wrapper(data['addon_xml_simple'])
        assert data['addon_xml_simple'] == self.srv.addon.get(id=3615)

    def _test_addon_no_mock(self):
        assert '<addon id="3615">' in self.srv.addon.get(id=3615)

    @mock.patch('requests.get')
    def test_search(self, get):
        get.return_value = Wrapper(data['search_xml_simple'])
        assert data['search_xml_simple'] == (
                    self.srv.search.get(searchterm='nasa'))

    def _test_search_no_mock(self):
        assert '<addon id="4908">' in self.srv.search.get(searchterm='nasa')

    def _test_search_type_no_mock(self):
        assert '<addon id="4908">' in self.srv.search.get(searchterm='nasa',
                                                          searchtype='theme')


if __name__ == '__main__':
    log = logging.getLogger('amo.api')
    log.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    log.addHandler(handler)
    unittest.main()
