from scripts.bruteforce import checkSuffix
from scripts.subrecord import dnsRecords
from scripts.subscan import scan_content
from colorama import init
import os

init()
URL_LIST = open("urls/urls.txt").read().split("\n")

def removeDupes():
    file = open("subdomains.txt").read()
    origlist = file.split("\n")
    res = []
    [res.append(x) for x in origlist if x not in res]
    file.close()
    output = open("subdomains.txt", "w")
    for r in res:
        output.write(r)

def numOfSubs():
    file = open("subdomains.txt").read()
    origlist = file.split("\n")
    print(str(len(origlist)) + " subdomains found")

for url in URL_LIST:
    print("\nBruteforcing " + url)
    checkSuffix(url, "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1million-5000.txt", "subdomains.txt")
    print("Checking subdomain records")
    dnsRecords(url, "subdomains.txt")
    numOfSubs()
    print("Scanning for takeovers")
    scan_content("subdomains.txt", "outputs\\output.txt")
    print("Saving to file")
