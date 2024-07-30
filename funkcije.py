import csv
import os
import requests


def download_url_to_string(url):
    return requests.get(url)
