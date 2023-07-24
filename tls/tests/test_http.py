async def test_query(aiohttp_client, loop):
    from tls import serve

    app = serve.get_app()
    client = await aiohttp_client(app)
    resp = await client.get("/hello")
    assert resp.status == 200
    msg = await resp.json()
    assert "error" not in msg


async def test_no_query(aiohttp_client, loop):
    from tls import serve

    app = serve.get_app()
    client = await aiohttp_client(app)
    resp = await client.get("/ ")
    assert resp.status == 400


async def test_query_param(aiohttp_client, loop):
    from tls import serve

    app = serve.get_app()
    client = await aiohttp_client(app)
    resp = await client.get("/hello?latitude=12.34")
    assert resp.status == 200
    msg = await resp.json()
    assert "error" not in msg


async def test_query_bad_param(aiohttp_client, loop):
    from tls import serve

    app = serve.get_app()
    client = await aiohttp_client(app)
    resp = await client.get("/hello?latitude=ouch")
    assert resp.status == 400
    msg = await resp.json()
    assert "error" in msg
