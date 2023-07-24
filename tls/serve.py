import re
import logging
import asyncio

import aiohttp
import aiohttp.web

from tls import util

RX_LOCATION = re.compile(r"-?\d+\.\d+")


async def handle(request):
    log = logging.getLogger("handle[{}]".format(request.remote))

    query = request.match_info.get("query", "").strip()
    if not query:
        msg = {"error": "no query"}
        return aiohttp.web.json_response(msg, status=400)

    params = {}
    for p in ("latitude", "longitude"):
        if p in request.query:
            v = request.query[p]
            if not RX_LOCATION.match(v):
                msg = {"error": "bad value for parameter '{}'".format(p)}
                return aiohttp.web.json_response(msg, status=400)

            params[p] = request.query[p]

    unknown = set(request.query.keys()) - set(params.keys())
    if unknown:
        txt = "unknown parameter(s): '{}'".format("', '".join(unknown))
        msg = {"error": txt}
        return aiohttp.web.json_response(msg, status=400)

    service_requests = []
    for service in request.app["services"]:
        service_requests.append(service(query, **params))

    try:
        results = await asyncio.gather(*service_requests)
    except Exception as e:
        log.error("gathering failed: %s", e)
        msg = {"error": str(e)}
        return aiohttp.web.json_response(msg, status=400)

    return aiohttp.web.json_response({"results": results})


def get_app():
    app = aiohttp.web.Application()
    app["services"] = []
    app.add_routes([aiohttp.web.get("/{query}", handle)])
    app.add_routes([aiohttp.web.get("/", handle)])
    return app


def main():
    import argparse

    parser = argparse.ArgumentParser(description="the location service")
    parser.add_argument(
        "--bind-host", type=str, default="0.0.0.0", help="hostname/ip to bind to"
    )

    parser.add_argument("--bind-port", type=int, default="8080", help="port to bind to")

    args = parser.parse_args()

    app = get_app()

    # this is our fancy plugin system ;)
    from tls import plugin_google

    app["services"].append(plugin_google.Plugin())

    import logging

    util.init_logging(level=logging.INFO)

    aiohttp.web.run_app(app, host=args.bind_host, port=args.bind_port)


if __name__ == "__main__":
    main()
