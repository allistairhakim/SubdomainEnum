import requests
import yaml
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
from threading import Lock
import time

s_print_lock = Lock()

def s_print(*a, **b):
    with s_print_lock:
        print(*a, **b)

def scan_url(url, matchers):
    try:
        response = requests.get(url, timeout=3)
        content = str(response.content, 'utf-8', errors='ignore')

        for matcher in matchers:
            flag = False
            for word in matcher['words']:
                if word in content:
                    flag = True
                else:
                    if matcher.get('condition'):
                        flag = False
            if flag:
                s_print("\033[92mTAKEOVER FOUND [" + matcher['name'] + "]\033[0m" + " " + url + "")
                return "[" + matcher['name'] + "]" + " " + url
            else:
                pass

        s_print("\033[94m[No takeover found]\033[0m " + url)
        return ""

    except requests.exceptions.ConnectTimeout:
        s_print("\033[91m[No response]\033[0m " + url)
        return ""
    except requests.exceptions.SSLError:
        s_print("\033[91m[SSL error]\033[0m " + url)
        return ""
    except requests.exceptions.ReadTimeout:
        s_print("\033[91m[Timeout]\033[0m " + url)
        return ""
    except requests.exceptions.ConnectionError:
        s_print("\033[91m[Connection refused]\033[0m " + url)
        return ""
    except requests.exceptions.InvalidURL:
        s_print("\033[91m[Invalid URL]\033[0m " + url)
        return ""

def scan_content(inp, out):
    input = open(inp).read()
    urls = input.split("\n")
    stream = open("subdomain-takeover.yaml", encoding='UTF-8')
    dictionary = yaml.safe_load(stream)
    matchers = dictionary['requests'][0]['matchers']

    if '' in urls:
        urls.remove('')

    with ThreadPoolExecutor(max_workers=5) as pool:
        future = pool.map(scan_url, urls, repeat(matchers))

    output = open(out, "a")

    for takeover_subdomain in future: #TEST IF THIS WORKS BY PRINTING TAKEOVER_SUBDOMAIN
        if not takeover_subdomain.isspace() and takeover_subdomain != "":
            output.write(takeover_subdomain + "\n")

    output.close()
