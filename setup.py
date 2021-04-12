from setuptools import setup, find_packages

NAME = "frontend"
VERSION = "1.0.0"

REQUIRES = ["pygame", "qrcode"]

setup(
    name=NAME,
    version=VERSION,
    description="Frontend for FerryTix Vending Machines written in PyGame.",
    author_email="hendrik.lankers.hl@googlemail.com",
    url="https://github.com/ferrytix/frontend",
    keywords=["Frontend", "FerryTix"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description=open('README.md').read()
)
