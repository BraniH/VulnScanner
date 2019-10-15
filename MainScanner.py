#! /usr/bin/env python

"Call functionality"

import FunctionalityOfScanner as FnOfScan
import time
import requests


def save_resulst(results):
    write = input("[?] Do you want to save results (y/n)? ")
    temp = ["y", "n"]
    while write not in temp:
        print("[!] Bad input!")
        write = input("[?] Do you want to save results (y/n)?")
        write = write.replace(" ", "")

    if write == "y":
        name_of_file = input("File name: ")
        name_of_file += ".txt"
        with open(name_of_file, 'w') as results_to_be_saved:
            for result in results:
                print(result, file=results_to_be_saved)
            print("\n[+] Finished! {0} results found. File name: {1}.".format(str(len(results)), name_of_file))

    elif write == "n":
        print("\n [+] Back to main menu...")


def url_for_testing():
    target_url_function = input("[?] Add url to test: ")
    target_url_function = target_url_function.replace(" ", "")
    vuln_scanner_function = FnOfScan.FunctionalityOfScan(target_url_function)
    login_url = input("[?]  If you want to login, add login url else, leave empty: ")
    login_url = login_url.replace(" ", "")

    try:
        if login_url != "":
            data_dict = {"username": "admin", "password": "password", "Login": "submit"}
            response = vuln_scanner_function.session.post(login_url, data=data_dict)
    except TypeError:
        print["! Bad login url"]

    return target_url_function, vuln_scanner_function


target_url, vuln_scanner = url_for_testing()

while True:
    print('\n[?] Type "url" if you want to change url for scanning')
    print("[?] Press 1. Full Scan")
    print("[?] Press 2. XSS Scan")
    print("[?] Press 3. Crawler")
    print("[?] Press X  Turn off program")

    type_of_scan = input("\nYour choice: ")

    if type_of_scan == "1":
        print("full_scan")
    elif type_of_scan == "2":

        print("[*] In progress...")

        crawled_urls = vuln_scanner.crawler(target_url)
        xss_result_forms = []
        xss_result_url = []
        xss_results = []
        cleaned_xss_results = []
        counter = 1

        for b in range(0, len(crawled_urls)):
            form = vuln_scanner.extract_forms(crawled_urls[b])
            try:
                if len(vuln_scanner.xss_in_foms(crawled_urls[b], form[0])) > 0:
                    xss_result_forms = vuln_scanner.xss_in_foms(crawled_urls[b], form[0])
                    xss_results.append(xss_result_forms)
                    print(f"\r[+] {counter} possible vulnerabilities found!", end="")
                    counter += 1

                if len(vuln_scanner.test_xss_link(crawled_urls[b])) > 0:
                    xss_result_url = vuln_scanner.test_xss_link(crawled_urls[b])
                    xss_results.append(xss_result_url)
                    print(f"\r[+] {counter} possible vulnerabilities found!", end="")
                    counter += 1

            except IndexError:
                pass

        print("\n\n[+] All xss results:\n\n")
        time.sleep(1)
        for xss_site_results in xss_results:
            cleaned_xss_results.append(xss_site_results[0])
            print(xss_site_results[0])

        save_resulst(cleaned_xss_results)

    elif type_of_scan == "3":
        print("[*] In progress... ")
        crawled_urls = vuln_scanner.crawler(target_url)
        for a in range(0, len(crawled_urls)):
            print(crawled_urls[a])

        save_resulst(crawled_urls)

    elif type_of_scan == "url":
        target_url, vuln_scanner = url_for_testing()
    elif type_of_scan == "X" or type_of_scan == "x":
        print("[+] program is closing")
        break
    else:
        print("[!] Bad input!")
