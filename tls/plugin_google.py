import os
import re
import logging

import aiohttp
import aiohttp.web

TEXT_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
NEARBY_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
DETAILS_URL = "https://www.google.com/maps/search/?api=1&query=Google&query_place_id={}"

API_STATUS_CODES = {
    "ZERO_RESULTS": "the search was successful but returned no results. \
            This may occur if the search was passed a latlng in a \
            remote location.",
    "OVER_QUERY_LIMIT": "you are over your quota.",
    "REQUEST_DENIED": "your request was denied, generally because of \
                        lack of an invalid key parameter.",
    "INVALID_REQUEST": "generally indicates that a required query parameter \
            (location or radius) is missing.",
    "UNKNOWN_ERROR": "unknown error"}

DESC_RX = re.compile(r"_(.)")
def build_description(items):
    result = []
    for i in items:
        tmp = i[0].upper() + i[1:]
        tmp = DESC_RX.subn(lambda m: " " + m.group(1).upper(), tmp)[0]
        result.append(tmp)

    return ", ".join(result)

def get_api_key():
    if "GOOGLE_PLACES_API_KEY" not in os.environ:
        raise RuntimeError("GOOGLE_PLACES_API_KEY not defined")

    keyfile = os.environ["GOOGLE_PLACES_API_KEY"]
    if not os.path.exists(keyfile):
        txt = "google places api keyfile '{}' not found"
        raise RuntimeError(txt.format(keyfile))

    with open(keyfile) as f:
        return f.read().strip()

class Plugin(object):
    def __init__(self):
        self.api_key = get_api_key()
        self.log = logging.getLogger("plugin.google")

    async def __call__(self, query, **kwargs):
        params = {"key": self.api_key}
        if "latitude" not in kwargs and "longitude" not in kwargs:
            params["query"] = query
            url = TEXT_URL
        else:
            if "latitude" not in kwargs:
                raise RuntimeError("parameter 'latitude' missing")

            if "longitude" not in kwargs:
                raise RuntimeError("parameter 'longitude' missing")

            params["location"] = "{},{}".format(kwargs.get("latitude"),
                                                kwargs.get("longitude"))
            params["radius"] = kwargs.get("radius", 10000)

            if query:
                params["keyword"] = query

            url = NEARBY_URL

        msg = "query: %s, params: %s"
        self.log.debug(msg, url, params)

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                data = await response.json()
                if data["status"] != "OK":
                    msg = "{}: {}".format(data["status"], 
                                          API_STATUS_CODES[data["status"]])
                    raise RuntimeError(msg)

                result = []
                for location in data["results"]:
                    geo = location["geometry"]["location"]
                    if "formatted_address" in location:
                        address = location["formatted_address"]
                    else:
                        address = location["vicinity"]

                    item = {"provider": "google",
                            "id": location["id"],
                            "name": location["name"],
                            "description": build_description(location["types"]),
                            "location": "{},{}".format(geo["lat"], geo["lng"]),
                            "address": address,
                            "details": DETAILS_URL.format(location["place_id"])}
                    result.append(item)
                return result
