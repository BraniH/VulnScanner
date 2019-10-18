#! /usr/bin/env python

"""Scanner controller"""

import requests
import re
from urllib import parse
from bs4 import BeautifulSoup
import os


class ScannerController:
    def __init__(self, url):
        self.session = requests.Session()
        self.target_url = url
        self.target_links = []

    def extract_links(self, url):
        response = self.session.get(url)
        return re.findall('(?:href=")(.*?)"', str(response.content))

    def crawler(self, url=None):
        if url is None:
            url = self.target_url
        href_links = self.extract_links(url)
        for link in href_links:
            link = parse.urljoin(url, link)

            if "#" in link:
                link = link.split("#")[0]

            if self.target_url in link and link not in self.target_links:
                if "logout" not in link:
                    self.target_links.append(link)
                    self.crawler(link)
        return self.target_links

    def extract_forms(self, url):
        response = self.session.get(url)
        # find all forms
        parsed_html = BeautifulSoup(response.content, features="html.parser", from_encoding="iso-8859-1")

        if len(parsed_html) != 0:
            return parsed_html.findAll("form")
        else:
            return False

    def submit_form(self, form, value, url):
        action = form.get("action")
        request_url = parse.urljoin(url, action)
        method = form.get("method")

        # find all inputs from forms
        inputs_list = form.findAll("input")
        post_data = {}
        for input_from_html in inputs_list:
            input_name = input_from_html.get("name")
            input_type = input_from_html.get("type")
            input_value = input_from_html.get("value")
            if input_type == "text":
                input_value = value

            post_data[input_name] = input_value

        if method == "post":
            return self.session.post(request_url, data=post_data)
        else:
            return self.session.get(request_url, params=post_data)

    def start_scan(self):
        for link in self.target_links:
            forms = self.extract_forms(link)
            for form in forms:
                print("[+] Testing form in " + link)

            if "=" in link:
                print("[+] Testing " + link)

    def xss_in_forms(self, url, form):
        result = []
        for payload in self.payloads_from_file():
            response = self.submit_form(form, payload, url)
            if url not in result:
                if payload in str(response.content):
                    result.append(str("[+] XSS found in form: " + url + "\n Used payload: " + payload + "\n"))

        return result

    def test_xss_link(self, url):
        result = []
        for payload in self.payloads_from_file():
            prepared_url = url.replace("=", "=" + payload)
            response = self.session.get(prepared_url)
            if payload in str(response.content):
                if url not in result:
                    result.append(str("[+] XSS found in url: " + prepared_url + "\nUsed payload: " + payload + "\n"))

        return result

    def payloads_from_file(self):
        path = os.getcwd() + "\\payloads.txt"
        xss_payloads = []
        with open(path, "r") as payloads:
            all_payloads = payloads.readlines()
            for payload in all_payloads:
                xss_payloads.append(payload.replace("\n", ""))

        return xss_payloads
