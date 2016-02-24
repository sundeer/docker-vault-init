import sys
import time
import boto3
import string
import os
import mail
import crypto
import vault
from   config import settings



if vault.is_initialized():
    print('Vault in already initialized')
    sys.exit()
else:
    users = settings['keybase']['users']
    threshold = settings['vault']['threshold']

    pgp_keys = []
    shares = 0
    for user in users:
        key_asciiarmor = crypto.get_pub_key(user['name'])
        key_base64 = crypto.asciiarmor_to_base64(key_asciiarmor)
        for _ in range(user['key_shares']):
            pgp_keys.append(key_base64)
            shares = shares + 1

    unseal_keys_b16, root_token = vault.initialize(pgp_keys)

    unseal_keys_b64 = crypto.base16_to_base64(unseal_keys_b16)

    mail.send_user_keys(unseal_keys_b64, root_token)


# s3 = boto3.resource('s3')
# for bucket in s3.buckets.all():
#     print(bucket.name)

# bucket = s3.Bucket('test-vault-unseal-234857187')
# response = bucket.create(ACL='private')
#
# for bucket in s3.buckets.all():
#     print(bucket.name)
#
# time.sleep(5)
#
# response = bucket.delete()
# xinput = open("freeformatter-output", mode='rb')
# output = open("output", mode='bw')
# base64.encode(xinput, output)

# send_simple_message(key[0])
# unseal with individual keys
# client.unseal(keys[0])
# client.unseal(keys[1])
# client.unseal(keys[2])
#
# time.sleep(5)
#
# # unseal with multiple keys until threshold met
# client.unseal_multi(keys)
#
# print(client.is_sealed())
#
# time.sleep(5)
# client.seal()
#
# print(client.is_sealed())
