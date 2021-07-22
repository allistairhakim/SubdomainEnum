from dnsdumpster.DNSDumpsterAPI import DNSDumpsterAPI
results = DNSDumpsterAPI({'verbose':True}).search('microsoft.com')

print(results)
