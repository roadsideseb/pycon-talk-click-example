import click

from .pinkbike import find_new_ads


@click.command()
@click.argument('url')
@click.option('--reset-cache', default=False, is_flag=True)
def main(url, reset_cache):
    print('Processing URL:', url)

    new_ads = find_new_ads(url, reset_cache)

    print('Found {} ads!'.format(len(new_ads)))
