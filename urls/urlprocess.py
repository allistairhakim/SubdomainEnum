urls = open("unprocessed_urls.txt").read()
output = open("urls.txt", "w")

subdomains = []
unprosub = []

for url in urls.split("\n"):
    if ".com" in url or ".net" in url or ".org" in url:
        spliturl = url.split(".")
        if len(spliturl[len(spliturl) - 1]) != 2:
            rawsuf = spliturl[len(spliturl) - 2]
            domain = spliturl[len(spliturl) - 1]
            suffix = "." + rawsuf + "." + domain
            unprosub.append(suffix)

[subdomains.append(x) for x in unprosub if x not in subdomains]

for subdomain in subdomains:
    output.write(subdomain + "\n")
