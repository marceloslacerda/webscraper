#!/usr/bin/env python3.6

import json
import sys


from io import StringIO
from os.path import join
from urllib.parse import urljoin
from typing import Dict, Any, AnyStr

import requests
from lxml.html import parse


class PageError(ValueError):
    def __init__(self, pname):
        self.pname = pname


def process_page(meta_data: Dict[AnyStr, Any], tree):
    actual_result = tree.xpath(meta_data['xpath_test_query'])
    expected_result = meta_data['xpath_test_result']
    if actual_result != expected_result:
        raise PageError(meta_data['next_page_expected'])
    else:
        return (
            tree.xpath(meta_data['xpath_button_to_click'] + '/@href')[0],
            meta_data['next_page_expected'])


def get_tree(url: AnyStr, name: AnyStr):
    text = requests.get(url, auth=('Thumb', 'Scraper')).text
    with open(join('debug', name), 'w') as f:
        f.write(text)
    return parse(StringIO(text))


def scrape_text(text_input: AnyStr):
    pages = json.loads(text_input)
    base = 'https://yolaw-tokeep-hiring-env.herokuapp.com/'
    next_url = '/'
    next_name = '0'
    for i in range(len(pages)):
        try:
            tree = get_tree(urljoin(base, next_url), next_name)
            next_url, next_name = process_page(pages[next_name], tree)
            print(f"Move to page {next_name}")
        except PageError as err:
            print(
                f'ALERT - Can’t move to page {err.pname}: '
                f'page {next_name} link has been malevolently tampered with!!')
            return


if __name__ == '__main__':
    scrape_text(sys.stdin.read())
