import urllib.request
import requests
import re
import ssl

def check_templating(url):
    url = 'https://' + url # Whoops I was stupid and forgot these much like forms.py require the scheme
    resp = None
    try:
        resp = requests.get(url)
    except:
        return "None"

    # headers = resp.headers # can be used to check decoding type and if its json or text

    mystr = resp.text

    # fp = urllib.request.urlopen(url)
    # mybytes = fp.read()

    # mystr = mybytes.decode("utf8")
    # fp.close()

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

    return "None" # please dear god return something even if its None


if __name__ == "__main__":
    print(check_templating("urbanasacs.com"))
    # print(check_templating("google.com"))
