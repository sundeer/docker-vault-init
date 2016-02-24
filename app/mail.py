import mandrill
import os
import vault
from   config import settings



MANDRILL_APIKEY = os.getenv('MANDRILL_APIKEY')
KEYBASE_USERNAME = os.getenv('KEYBASE_USERNAME')


def send_user_keys(keys, root_token):
    users = settings['keybase']['users']
    threshold = settings['vault']['threshold']
    mail_from = settings['vault']['domain']

    share_number = 0
    for user in users:
        attachments = []
        for _ in range(user['key_shares']):
            attachment = {'key'   : keys[share_number],
                          'number': share_number + 1}
            attachments.append(attachment)
            share_number = share_number + 1

        mail_to = user['email']
        send_mail(mail_from, mail_to, attachments, root_token, threshold)


def send_mail(mail_from, recipient, keys, root_token, threshold):
    mandrill_client = mandrill.Mandrill(MANDRILL_APIKEY)
    tot_keys = vault.get_key_shares()

    text = []
    text.append('Vault initialized with {0} key(s) and a key threshold of {1}.'.format(tot_keys, threshold))
    text.append(' ')
    text.append('Root token:')
    text.append(root_token)
    text = '\n'.join(text)

    attachments = []
    i = 0
    for key in keys:
        i = i + 1
        attachment = {'content': key['key'],
                      'name'   : 'unseal-key-{0}.dat'.format(key['number']),
                      'type'   : 'application/octet-stream'}
        attachments.append(attachment)

    message = {
     'to'         : [{'email': recipient}],
     'from_name'  : 'Production Vault Server',
     'from_email' : 'noreply@{0}'.format(mail_from),
     'subject'    : 'Vault Initialized',
     'attachments': attachments,
     'text'       : text
     }

    result = mandrill_client.messages.send(message=message, async=False)
    print(result)
