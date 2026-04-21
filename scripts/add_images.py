import json
import requests
import time

INPUT = "data\fish_data_clean.json"
OUTPUT = "data\fish_data_final.json"

def get_inaturalist_image(name):
    url = 