import click

from .pinkbike import find_new_ads
from .mailer import send_email


@click.command()
@click.argument('url')
@click.option('--email')
@click.option('--reset-cache', default=False, is_flag=True)
def main(url, email, reset_cache):
    print('Processing URL:', url)

    new_ads = find_new_ads(url, reset_cache)

    print('Found {} ads!'.format(len(new_ads)))

    if email and new_ads:
        send_email(email,
                   subject='New ads available',
                   content='Found {} new ads for {}'.format(len(new_ads), url))
