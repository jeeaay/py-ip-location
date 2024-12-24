#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: Jeay
# Mail: admin@jeay.net
# Created Time:  2024-12-20 15:09:02
#############################################


from setuptools import setup, find_packages
filepath = 'README.md'
setup(
    name = "ip-region",
    version = "1.0.6",
    keywords = ["ip loaction", "ip country", "ip region", "IP address loaction", "IP geographic location"],
    description = "Get geographic location through IP address, support IPv4 and IPv6. Combine IP address library and online API.",
    long_description = open(filepath, encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license = "Apache-2.0 License",

    url = "https://github.com/jeeaay/py-ip-location",
    author = "Jeay",
    author_email = "admin@jeay.net",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["requests"]
)