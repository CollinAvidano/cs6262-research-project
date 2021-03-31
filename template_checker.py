import urllib.request
import re

def check_templating(url):
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()

    mystr = mybytes.decode("utf8")
    fp.close()

    metacheck = re.search('<meta\\s+name="generator"\\s+content=.*>', mystr);

    if metacheck is not None:
        content_part = re.search('content=.*', metacheck.group(0))
        return content_part.group(0)[8:-2]

    if "<!-- This is Squarespace. -->" in mystr:
        return "Squarespace"

    if "var Shopify = Shopify" in mystr:
        return "Shopify"

    if '_W.configDomain = "www.weebly.com";' in mystr:
        return "Weebly"

    # print(mystr)

print (check_templating("https://urbanasacs.com/"))
