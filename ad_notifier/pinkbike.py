import os
import click
import requests

from hashlib import sha1
from collections import namedtuple

from bs4 import BeautifulSoup


Ad = namedtuple('Ad', ['id', 'title', 'url', 'image'])


def get_cache_filename(url, reset=False):
    filename = '.{}.cache'.format(sha1(url.encode('utf-8')).hexdigest())

    if reset and os.path.exists(filename):
        os.remove(filename)

    return filename


def find_new_ads(url, reset_cache=False):
    """
    Extracts a list of new ads at the URL in *url*.
    """
    response = requests.get(url)

    if not response.ok:
        raise click.ClickException("couldn't get search result page")

    cache_file = get_cache_filename(url, reset=reset_cache)

    soup = BeautifulSoup(response.content, 'html.parser')

    old_ads = []
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as cache:
            old_ads = [l.strip() for l in cache]

    new_ads = []
    with open(cache_file, 'a+') as cache:
        for bsitem in soup.select('.bsitem'):
            item_id = bsitem['id']

            if item_id in old_ads:
                continue

            elem = bsitem.select('td > div > a')[0]

            ad = Ad(id=item_id,
                    title=elem.text.strip(),
                    url=elem.get('href', ''),
                    image='')

            new_ads.append(ad)
            cache.write('{}\n'.format(item_id))

    return new_ads
