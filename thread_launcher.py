import concurrent.futures
import time

def method(url):
    print("thread-" + str(url))
    time.sleep(2)
    return url + 4

url_list = [1, 2, 3, 4]

############### TODO #################
# read URLs in to url_list
threads = []

with concurrent.futures.ThreadPoolExecutor() as executor:
    threads = [executor.submit(method, url) for url in url_list]

############## TODO ##################
# write to database
for ret in threads:
    print(ret.result())
