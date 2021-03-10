import configparser
import requests

config = configparser.RawConfigParser()
config.read('config.properties')
host = config.get('Connection', 'connection.host_test')
# host = config.get('Connection', 'connection.host')
port = config.get('Connection', 'connection.port')


def get_scheme_test():
    request = host + port + config.get('ManipulatorAPI', 'api.get_scheme_test')
    print('getting ', request)
    return requests.get(request).json()


def get_scheme():
    request = host + port + config.get('ManipulatorAPI', 'api.get_scheme')
    return requests.get(request)


def load():
    request = config.get('ManipulatorAPI', 'api.load')
    requests.post(host + port + request)


def unload():
    config.read('config.properties')
    request = config.get('ManipulatorAPI', 'api.unload')



