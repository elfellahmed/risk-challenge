from urllib import request
import json
import sys

import pandas as pd

#read the CSV from the API endpoint using new column names. Return a Pandas Dataframe.
def read(url):
    csv_data = pd.read_csv(url,delimiter="|",usecols=["id","produktId","artikeltyp","name","beschreibung","preis","bestand"], header=0)
    csv_data.columns = ["id","productId","category","productname","comment","price","stock"]
    return csv_data


def data_manipulation(csv_data):
    csv_data.drop_duplicates(subset ="id", keep = False, inplace = True)
    csv_data = csv_data.dropna(subset=['category'])
    
    #Cast the columns below as Integer & fill empty stock entries with 0
    csv_data['category'] = csv_data.category.astype(int)
    csv_data['price'] = csv_data['price'].multiply(100)
    csv_data['price'] = csv_data.price.astype(int)
    csv_data['stock'] = csv_data['stock'].fillna(0)
    csv_data['stock'] = csv_data.stock.astype(int)
    
    #map artikelTyp with categories
    cat = {1:"phone",2:"sim",3:"supplies",4:"headphones"}
    csv_data['category'] = csv_data['category'].map(cat)
    return csv_data


def add_risk(data):
    #insert Risk as a new column with Value 50 for Cat1 and Value 0 for other Cat.
    risk = {'phone':50,'sim':0,'supplies':0,'headphones':0}
    data['risk'] = data['category'].map(risk)
    return data

def serialize_json(row):
    return row[1].to_json()

def put_json(json_str):
    req = request.Request(url='http://localhost:8080/riskyItems',
                          data = json_str.encode('utf-8'),
                          method='PUT', 
                          headers={'content-type': 'application/json'})
    with request.urlopen(req) as f:
        pass
    print(str(f.status)+" "+f.reason)   #Response code
    pass

def main():
    url = "http://localhost:8080/items"
    try:
        csv_data = read(url)
    except:
        print("Server or Endpoint not responding.")
        sys.exit()
    data = data_manipulation(csv_data)
    enriched_data = add_risk(data)
    #itereate the rows of the dataframe and serialize each one to a JSON String. 
    #Iterrows return a tuple (index,Series)
    for row in enriched_data.iterrows(): 
        json_str = serialize_json(row)
        put_json(json_str)
        continue

main()