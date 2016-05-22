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
@click.argument('url')
@click.option('--email')
@click.option('--reset-cache', default=False, is_flag=True)
@click.pass_context
def main(context, url, email, reset_cache):
    context.obj = {'url': url,
                   'email': email,
                   'reset_cache': reset_cache}


@main.command()
@click.pass_context
def run_once(context):
    process_url(**context.obj)


@main.command()
@click.option('--run-every', default=5, type=int)
@click.pass_context
def run_periodically(context, run_every):
    print('Running as scheduled job, every {} minute(s)'.format(run_every))

    schedule.every(run_every).minutes.do(process_url, **context.obj)

    while True:
        schedule.run_pending()
        time.sleep(1)
