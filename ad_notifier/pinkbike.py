import click
import requests

from collections import namedtuple

from bs4 import BeautifulSoup


Ad = namedtuple('Ad', ['id', 'title', 'url', 'image'])


def find_ads(url):
    response = requests.get(url)

    if not response.ok:
        raise click.ClickException("couldn't get search result page")

    soup = BeautifulSoup(response.content, 'html.parser')

    ads = []
    for bsitem in soup.select('.bsitem'):
        item_id = bsitem['id']
        elem = bsitem.select('td > div > a')[0]

        ad = Ad(id=item_id,
                title=elem.text.strip(),
                url=elem.get('href', ''),
                image='')

        ads.append(ad)

    return ads
