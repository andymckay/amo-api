servers = {
    'amo': 'addons.mozilla.org',
}

urls = {
    'api': 'https://services.{server}/{locale}/api/1.5',
    'addon': {'url': '/addon/{id}'},
    'search': {'url': '/search/{searchterm}/{optional|searchtype}/'
                      '{optional|maxresults}/{optional|search_os}/'
                      '{optional|search_version}',
               'pre': 'search_args'}
}


