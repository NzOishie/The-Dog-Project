import json
import ssl
import urllib

from flask_caching import Cache

import certifi

from app import app

cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://localhost:6379/0'})


# @cache.cached(timeout=60*60)
def get_json_response(search_url):
    search_response = urllib.request.urlopen(
        search_url, context=ssl.create_default_context(cafile=certifi.where()),
    )
    search_result = search_response.read()
    all_dog = json.loads(search_result)
    return all_dog
