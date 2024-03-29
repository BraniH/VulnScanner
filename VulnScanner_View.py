#! /usr/bin/env python

"""Calls functionality"""

import VulnScanner_Controller as ScanControl
import Login_Controller as LoginControl


def save_outputs(results):
    write = input("[?] Do you want to save the results (y/n)? ")
    temp = ["y", "n"]
    while write not in temp:
        print("[!] Bad input!")
        write = input("[?] Do you want to save the results (y/n)?")
        write = write.replace(" ", "")

    if write == "y":
        file_name = input("File name: ")
        file_name += ".txt"
        with open(file_name, 'w') as results_to_be_saved:
            for result in results:
                print(result, file=results_to_be_saved)
            print("\n[+] Finished! {0} results found. File name: {1}.".format(str(len(results)), file_name))

    elif write == "n":
        print("\n [+] Back to the main menu...")


def url_and_credentials():
    tar_url = input("[?] Add url to test: ")
    log_url = input("[?]  If you want to login, add login url else, leave empty: ")
    tar_url, log_url = edit_url(tar_url, log_url)
    u_name = input("[?] Add username: ")
    u_password = input("[?] Add password: ")

    return tar_url, log_url, u_name, u_password


# get rid of unecessary spaces
def edit_url(i_url, l_url):
    i_url = i_url.replace(" ", "")
    l_url = l_url.replace(" ", "")
    return i_url, l_url


target_url, login_url, username, user_password = url_and_credentials()
login_control = LoginControl.LoginController()

if ".php" in login_url:
    target_url, scan_call = login_control.login_php(username, user_password, target_url, login_url)
    print(target_url, scan_call)
else:
    target_url, scan_call = login_control.login_aspx(username, user_password, target_url, login_url)
    print(target_url, scan_call)


while True:
    print('\n[?] Press "U" if you want to change url for scanning')
    print("[?] Press 1. Full Scan")
    print("[?] Press 2. XSS Scan")
    print("[?] Press 3. Crawler")
    print("[?] Press X  Turn off program")

    program_option = input("\nYour choice: ")

    if program_option == "1":
        print("full_scan")
    elif program_option == "2":

        print("[*] In progress...")

        crawled_urls = scan_call.crawler(target_url)
        xss_result_forms = []
        xss_result_url = []
        xss_results = []
        cleaned_xss_results = []
        results_count = 1

        for crawled_url in range(0, len(crawled_urls)):
            form = scan_call.extract_forms(crawled_urls[crawled_url])
            try:
                if len(scan_call.xss_in_forms(crawled_urls[crawled_url], form[0])) > 0:
                    xss_result_forms = scan_call.xss_in_forms(crawled_urls[crawled_url], form[0])
                    xss_results.append(xss_result_forms)
                    print(f"\r[+] {results_count} possible vulnerabilities found!", end="")
                    results_count += 1

                if len(scan_call.test_xss_link(crawled_urls[crawled_url])) > 0:
                    xss_result_url = scan_call.test_xss_link(crawled_urls[crawled_url])
                    xss_results.append(xss_result_url)
                    print(f"\r[+] {results_count} possible vulnerabilities found!", end="")
                    results_count += 1

            except IndexError:
                pass

        for xss_site_results in xss_results:
            cleaned_xss_results.append(xss_site_results[0])
            print(xss_site_results[0])

        save_outputs(cleaned_xss_results)

    elif program_option == "3":
        print("[*] In progress... ")
        crawled_urls = scan_call.crawler(target_url)

        for crawled_url in range(0, len(crawled_urls)):
            print(crawled_urls[crawled_url])

        save_outputs(crawled_urls)

    elif program_option == "test":
        print(scan_call.payloads_from_file())

    elif program_option == "U" or program_option == "u":
        target_url, login_url, username, user_password = url_and_credentials()
    elif program_option == "X" or program_option == "x":
        print("[+] program is closing")
        break
    else:
        print("[!] Bad input!")
