import urllib.request
from bs4 import BeautifulSoup

movieList = []
url = "https://wannianrili.bmcx.com/"


def get_html(urls):
    request = urllib.request
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = request.Request(url=urls, headers=headers)
    html = request.urlopen(req).read().decode()
    return html


def parse_html(file):
    soup = BeautifulSoup(file, 'html.parser')
    movie_zone = soup.find('ol', attrs={'class', 'grid_view'})



parse_html(get_html(url))

