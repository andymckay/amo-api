import unittest

import api
import mock

data = {
    'addon_xml_simple': """
<?xml version="1.0" encoding="utf-8" ?>
<addon id="3615">
  <name>Delicious Bookmarks</name>
</addon>
"""
}

class Wrapper:
    def __init__(self, data):
        self.content = data


class TestAddon(unittest.TestCase):
    def setUp(self):
        self.srv = api.Server('amo')

    @mock.patch('requests.get')
    def test_addon(self, get):
        get.return_value = Wrapper(data['addon_xml_simple'])
        assert data['addon_xml_simple'] == self.srv.addon(3615)

if __name__ == '__main__':
    unittest.main()
