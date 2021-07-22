import requests
import sys
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
from tqdm import tqdm
from treq import get
from twisted.internet import reactor
from threading import Lock

s_print_lock = Lock()

def s_print(*a, **b):
    with s_print_lock:
        print(*a, **b)

subdomains = []

SUFFIX = ".google.com"
VALID_STATUS_CODES = [200]
MAX_WORKER_THREADS = 10

spaces = " " * 10
def evaluateSubdomain(suf, prefix, i):
    if prefix != "":
        potsubdomain = "https://" + prefix + suf
        try:
            response = requests.head(potsubdomain, timeout=1)
            if response.status_code != 403 and response.status_code != 301:
                s_print("\r\033[96m[" + str(response.status_code) + "]\033[0m" + potsubdomain + spaces, end="")
                subdomains.append(potsubdomain + "\n")
        except:
            s_print("\r\033[96m[Refused to connect]\033[0m " + potsubdomain, end="")


def checkSuffix(suf, pre, out):
    subdomains = []
    rawPrefixResponse = requests.get(pre)
    rawPrefixs = rawPrefixResponse.text
    prefixs = rawPrefixs.split("\n")

    with ThreadPoolExecutor(max_workers=MAX_WORKER_THREADS) as pool:
        future = list((pool.map(evaluateSubdomain, repeat(suf), prefixs, range(len(prefixs)))))

    output = open(out, "w")
    for subdomain in subdomains:
        output.write(subdomain)

    print(str(len(subdomains)) + " subdomains found")
    output.close()
