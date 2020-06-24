from urllib import request, response, error
import csv
import json

def read(url):
    response = urllib.urlopen(url)
    file_reader = csv.reader(response)
    for row in file_reader:
        print(row)
    pass

url = "http://localhost:8080/items"

read(url)