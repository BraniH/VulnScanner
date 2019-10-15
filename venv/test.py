#! /usr/bin/env python

import requests
import BeautifulSoup
#import urlparse

def make_get_requests(url):
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        pass


target_url = "http://127.0.0.1/mutillidae/index.php?page=dns-lookup.php"
response = make_get_requests(target_url)
print(response.content)
