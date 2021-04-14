from setuptools import setup, find_packages

NAME = "frontend"
VERSION = "0.2.1"

REQUIRES = ["pygame", "qrcode"]

setup(
    name=NAME,
    version=VERSION,
    description="Frontend for FerryTix Vending Machines written in PyGame.",
    author_email="leon-pascal.thierschmidt@outlook.de",
    url="https://github.com/ferrytix/frontend",
    keywords=["Frontend", "FerryTix"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description=open('README.md').read()
)
