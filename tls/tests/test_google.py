import os
import tempfile

import pytest

KEYFILE_DEFINED = "GOOGLE_PLACES_API_KEY" in os.environ

def test_without_keyfile_var(monkeypatch):
    from tls import plugin_google
    monkeypatch.delenv("GOOGLE_PLACES_API_KEY")
    with pytest.raises(RuntimeError):
        plugin_google.Plugin()

def test_without_keyfile(monkeypatch):
    from tls import plugin_google
    monkeypatch.setenv("GOOGLE_PLACES_API_KEY", "/does/not/exist")
    with pytest.raises(RuntimeError):
        plugin_google.Plugin()

def test_keyfile_load(monkeypatch):
    from tls import plugin_google
    key = "jadddaada"
    with tempfile.TemporaryDirectory() as tmp_dir:
        keyfile = os.path.join(tmp_dir, "the_key")
        with open(keyfile, "w") as f:
            f.write(key)

        monkeypatch.setenv("GOOGLE_PLACES_API_KEY", keyfile)
        p = plugin_google.Plugin()
        assert p.api_key == key

def test_description():
    from tls.plugin_google import build_description
    assert build_description(["point_of_interest"]) == "Point Of Interest"
    assert build_description(["restaurant"]) == "Restaurant"
    assert build_description(["bad", "restaurant"]) == "Bad, Restaurant"

@pytest.mark.skipif(KEYFILE_DEFINED is False, 
                    reason="GOOGLE_PLACES_API_KEY not defined")
@pytest.mark.asyncio
async def test_text_query(debug_log):
    from tls import plugin_google
    p = plugin_google.Plugin()
    data = await p("hamburg food")
    assert isinstance(data, list)
    assert len(data) > 1

    d0 = data[0]
    assert "id" in d0
    assert "provider" in d0
    assert d0["provider"] == "google"

@pytest.mark.skipif(KEYFILE_DEFINED is False, 
                    reason="GOOGLE_PLACES_API_KEY not defined")
@pytest.mark.asyncio
async def test_location_query(debug_log):
    from tls import plugin_google
    p = plugin_google.Plugin()
    data = await p("food", latitude="53.5", longitude="10.0")
    assert isinstance(data, list)
    assert len(data) > 1

    d0 = data[0]
    assert "id" in d0
    assert "provider" in d0
    assert d0["provider"] == "google"
