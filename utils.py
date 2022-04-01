import json
import ssl
import urllib

import certifi
import redis

r = redis.Redis(host='localhost', port=6379, db=0)


def get_json_response(search_url):
    if r.exists(search_url):
        search_result = r.get(search_url)
    else:
        search_response = urllib.request.urlopen(
            search_url, context=ssl.create_default_context(cafile=certifi.where()),
        )
        search_result = search_response.read()
        r.set(search_url,search_result)
    all_dog = json.loads(search_result)
    return all_dog
