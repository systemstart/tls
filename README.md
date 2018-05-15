The Location Service(TLS)
=========================

This is a simple REST service to query location services. It was build as a 
coding challenge, not as a real life product.

It's build for Python 3.6

Setup
-----

* Create a virtual environment and activate it(OPTIONAL)
* Install dependencies: Run `pip install -r requirements.txt`.
* Install TLS: Run `pip install .`
* Start TLS: Run `tlsd`

Note: The service will bind to "0.0.0.0:8080" by default, check `tlsd -h`
about how to change that.

Tests
-----

* Install development dependencies: Run `pip install -r requirements-dev.txt`
* Run `pytest -v`
