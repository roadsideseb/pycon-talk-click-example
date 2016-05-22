import time
import click
import schedule

from .pinkbike import find_new_ads
from .mailer import send_email, ads_as_list


def process_url(url, email, reset_cache):
    print('Processing URL:', url)

    new_ads = find_new_ads(url, reset_cache)

    print('Found {} ads!'.format(len(new_ads)))

    if email and new_ads:
        send_email(email,
                   subject='New ads available',
                   content=ads_as_list(new_ads))


@click.group()
def main():
    pass


@main.command()
@click.argument('url')
@click.option('--email')
@click.option('--reset-cache', default=False, is_flag=True)
def run_once(url, email, reset_cache):
    process_url(url, email, reset_cache)


@main.command()
@click.argument('url')
@click.option('--email')
@click.option('--reset-cache', default=False, is_flag=True)
@click.option('--run-every', default=5, type=int)
def run_periodically(url, email, reset_cache, run_every):
    print('Running as scheduled job, every {} minutes'.format(run_every))

    schedule.every(run_every).minutes.do(
        process_url,
        url=url,
        email=email,
        reset_cache=reset_cache)

    while True:
        schedule.run_pending()
        time.sleep(1)
