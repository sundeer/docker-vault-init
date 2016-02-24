import requests
import base64
from config import settings



KEYBASE_API = settings['keybase']['api']

# Returns public pgp key in ASCII Armor format
def get_pub_key(username):
    url = KEYBASE_API + '/user/lookup.json?usernames={0}'.format(username)

    response = requests.get(url)
    key = response.json()['them'][0]['public_keys']['primary']['bundle']
    return key


def asciiarmor_to_base64(asciarmor):
    asciarmor = asciarmor.splitlines()
    radix64 = asciarmor[4:-2]
    base64 = ''.join(radix64)
    return base64


def base16_to_base64(keys_b16):
    keys_b64 = []
    for key_b16 in keys_b16:
        key_bin = base64.b16decode(key_b16, casefold=True)
        key_b64 = base64.b64encode(key_bin)
        key_b64 = key_b64.decode()
        keys_b64.append(key_b64)
    return keys_b64
