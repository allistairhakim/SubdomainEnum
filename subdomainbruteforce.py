import requests
import sys
import threading
from concurrent.futures import ThreadPoolExecutor

subdomains = []

SUFFIX = ".google.com"
VALID_STATUS_CODES = [200]
MAX_WORKER_THREADS = 10
PREFIX_WORDLIST_URL = 'https://raw.githubusercontent.com/rbsec/dnscan/master/subdomains-10000.txt'

def evaluateSubdomain(prefix, i):
    if prefix != "":
        potsubdomain = "https://" + prefix + SUFFIX
        response = requests.get(potsubdomain)
        print(str(i) + " - " + str(response.status_code) + " - " + potsubdomain + " - " + prefix)
        if response.status_code in VALID_STATUS_CODES:
            subdomains.append(str(i) + " - " + str(response.status_code) + " - " + potsubdomain + " - " + prefix)

def validResults():
    print("\nVALID SUBDOMAINS\n======================\n")
    for subdomain in subdomains:
        print(subdomain)

if __name__ == "__main__":
    rawPrefixResponse = requests.get(PREFIX_WORDLIST_URL)
    rawPrefixs = rawPrefixResponse.text
    prefixs = rawPrefixs.split("\n")

    with ThreadPoolExecutor(max_workers=MAX_WORKER_THREADS) as pool:
        future = pool.map(evaluateSubdomain, prefixs, range(len(prefixs)))

    validResults()
