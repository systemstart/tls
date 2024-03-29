[![Build Status](https://travis-ci.org/systemstart/tls.svg?branch=master)](https://travis-ci.org/systemstart/tls)

The Location Service(TLS)
=========================

This is a simple REST service to query location services. It was build as a 
coding challenge, not as a real life product.

It's built for Python 3.6

Setup
-----

* (Optional) Create a virtual environment and activate it.
* Install dependencies: Run `pip install -r requirements.txt`.
* Install TLS: Run `pip install .`
* Make sure you have a API-Key file for Google Places
* Start TLS: Run `GOOGLE_PLACES_API_KEY=/path/to/key/file tlsd`

Note: The service will bind to "0.0.0.0:8080" by default, check `tlsd -h`
about how to change that.

Tests
-----

* Install development dependencies: Run `pip install -r requirements-dev.txt`
* Run `PYTHON_PATH=. pytest -v`

Some tests will be skipped as they require a API key. If you have one, 
you can run the tests like this: `GOOGLE_PLACES_API_KEY=/path/to/key/file PYTHON_PATH=. pytest -v`
