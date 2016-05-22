import dj_email_url

from envelopes import Envelope


def ads_as_list(ads):
    content = []
    for ad in ads:
        content.append('* {ad.id} - {ad.title} - {ad.url}\n\n'.format(ad=ad))
    return ''.join(content)


def send_email(to, subject, content):
    email_config = dj_email_url.config()

    if not email_config:
        return

    smtp_config = {'host': email_config['EMAIL_HOST'],
                   'port': email_config['EMAIL_PORT'],
                   'login': email_config['EMAIL_HOST_USER'],
                   'password': email_config['EMAIL_HOST_PASSWORD'],
                   'tls': email_config['EMAIL_USE_TLS']}

    envelope = Envelope(
        from_addr='seb@roadsi.de',
        to_addr=[to],
        subject=subject,
        text_body=content)

    envelope.send(**smtp_config)
