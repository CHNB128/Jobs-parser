from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    with closing(get(url, stream=True)) as resp:
        if is_good_response(resp):
            return resp.content
        else:
            return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


def get_page_count():
    raw_html = simple_get('https://gamedev.ru/job/forum/?vacancy&page=1')
    html = BeautifulSoup(raw_html, 'html.parser')
    pages_tags = html.select('.pages a')
    count = pages_tags[-2:-1][0].get_text()
    return count


def get_jobs():
    base_url = 'https://gamedev.ru/job/forum/?vacancy&page='
    pages_count = get_page_count()
    # jobs = []
    for page_number in range(1, int(pages_count) - 400):
        raw_html = simple_get(base_url + str(page_number))
        html = BeautifulSoup(raw_html, 'html.parser')
        current_jobs = html.select('.bound div')[1:-2]
        for job in current_jobs:
            link = job.select('a')
            print(link)
            # print(link.get_text())
        # jobs.append(html.select('.bound div')[1:-2])
    # map(print, jobs)


get_jobs()
