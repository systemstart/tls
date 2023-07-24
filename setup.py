from distutils.core import setup

setup(
    name="tls",
    version="0.1dev",
    packages=["tls"],
    entry_points={"console_scripts": ["tlsd = tls.serve:main"]},
)
