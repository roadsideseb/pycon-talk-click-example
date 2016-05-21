import click

from .pinkbike import find_new_ads


@click.command()
@click.argument('url')
def main(url):
    print('Processing URL:', url)

    new_ads = find_new_ads(url)

    print('Found {} ads!'.format(len(new_ads)))
