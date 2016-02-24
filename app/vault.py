import hvac
from config import settings


VAULT_URL = settings['vault']['url']

client = hvac.Client(url=VAULT_URL)

def is_initialized():
    return client.is_initialized()

def initialize(pgp_keys):
    key_shares = get_key_shares()
    threshold = settings['vault']['threshold']

    print('Initialized - {0}'.format(client.is_initialized()))
    print("Initializing")

    result = client.initialize(key_shares, threshold, pgp_keys)
    root_token = result['root_token']
    keys_b16 = result['keys']

    print('Initialized - {0}'.format(client.is_initialized()))

    return keys_b16, root_token


def get_key_shares():
    users = settings['keybase']['users']

    key_shares = 0
    for user in users:
        key_shares = key_shares + user['key_shares']

    return key_shares
