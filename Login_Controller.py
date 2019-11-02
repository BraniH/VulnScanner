#! /usr/bin/env python

"""Login controller"""

import requests
from bs4 import BeautifulSoup
import VulnScanner_Controller as ScanControl


class LoginController:

    def login_php(self, username, user_password, input_url, login_url):
        controller_setting = ScanControl.ScannerController(input_url)
        print(controller_setting)
        try:
            if login_url != "":
                data_dict = {"username": username, "password": user_password, "Login": "submit"}
                response = controller_setting.session.post(login_url, data=data_dict)
        except TypeError:
            print["! Bad login url"]

        return input_url, controller_setting

    # ------ asp.net ---------
    def create_session(self, input_url):
        new_session = ScanControl.ScannerController(input_url)
        return new_session

    def attributes_for_session(self, u_name, u_pass, login_url, input_url):
        setup_session = self.create_session(input_url)
        response = setup_session.session.get(login_url)
        soup = BeautifulSoup(response.content, features="html.parser")

        # print(soup)
        states = ["__RequestVerificationToken", "Email", "RememberMe"]
        login_data = {"username": u_name, "password": u_pass, "Login": "submit"}

        for state in states:  # search for existing aspnet states and get its values
            result = soup.find('input', {'name': state})
            if not (result is None):  # when existent (some may not be needed!)
                if state == "Email":
                    login_data.update({state: login_data["username"]})
                else:
                    login_data.update({state: result['value']})
        return login_data, setup_session

    def login_aspx(self, u_name, u_pass, input_url, login_url):
        # call request
        data, crafted_session = self.attributes_for_session(u_name, u_pass, login_url, input_url)
        post_request = crafted_session.session.post(login_url, data=data)
        # if there is redirection stop it
        if post_request.history:
            data, crafted_session = self.attributes_for_session(u_name, u_pass, login_url, input_url)
            post_request = crafted_session.session.post(login_url, data=data, allow_redirects=False)

        cookies = {'__RequestVerificationToken': data.get('__RequestVerificationToken'),
                   '.AspNet.ApplicationCookie': post_request.headers.get('Set-Cookie')}

        get_request = crafted_session.session.get(input_url, cookies=cookies)

        return input_url, crafted_session


