import requests
import sys
import time


def dnsRecords(url, out):
    output = open(out, "a") #change to a if bruteforcing
    input = url.split(".")[1] + "." + url.split(".")[2]

    burp0_url = "https://hackertarget.com:443/find-dns-host-records/"
    burp0_headers = {"Connection": "close", "Accept": "text/html, */*; q=0.01", "X-Requested-With": "XMLHttpRequest", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "Origin": "https://hackertarget.com", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://hackertarget.com/find-dns-host-records/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9"}
    burp0_data = {"theinput": input, "thetest": "hostsearch", "name_of_nonce_field": "4cee43d305", "_wp_http_referer": "/find-dns-host-records/"}
    response = requests.post(burp0_url, headers=burp0_headers, data=burp0_data)

    raw1 = response.text.split("<pre id=\"formResponse\">")
    raw2 = raw1[1].split("</pre>")[0]

    domips = raw2.split("\n")
    domains = [domip.split(",")[0] for domip in domips]

    if "API " in domains[0]:
        print("\033[96m[API rate limit exceeded, sleeping...]\033[0m")
        time.sleep(60 * 60)
        response = requests.post(burp0_url, headers=burp0_headers, data=burp0_data)

        raw1 = response.text.split("<pre id=\"formResponse\">")
        raw2 = raw1[1].split("</pre>")[0]

        domips = raw2.split("\n")
        domains = [domip.split(",")[0] for domip in domips]

    for domain in domains:
        output.write("https://" + domain + "\n")

    print(str(len(domains)) + " subdomains found")

    output.close()
