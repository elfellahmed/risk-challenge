from urllib import request, response, error
import pandas as pd
import json

#read the CSV from the API endpoint with only the required columns. Return a Pandas Dataframe.
def read(url):
    csv_data = pd.read_csv(url,delimiter="|",usecols=["id","produktId","artikeltyp","name","beschreibung","preis","bestand"], header=0)
    csv_data.columns = ["id","productId","category","productname","comment","price","stock"]
    return csv_data


def dataManipulation(csv_data):
    #drop duplicates by ID from the Dataframe and rename the column 'arttikelTyp'
    csv_data.drop_duplicates(subset ="id", keep = False, inplace = True)
    csv_data = csv_data.dropna(subset=['category'])
    #print(csv_data.describe())
    csv_data['category'] = csv_data.category.astype(int)
    csv_data['price'] = csv_data.price.astype(int)
    csv_data['stock'] = csv_data['stock'].fillna(-1)
    csv_data['stock'] = csv_data.stock.astype(int)
    #Create a dict with the category mapping
    cat = {0:"undefined",1:"phone",2:"sim",3:"supplies",4:"headphones"}
    #map the dict created above with the artikelTyp column values
    csv_data['category'] = csv_data['category'].map(cat)
    return csv_data

def serializeJSON(data):
    #insert Risk as a new column with Value 50 for Cat1 and Value 0 for other Cat.
    risk = {'phone':50,'sim':0,'supplies':0,'headphones':0,'undefined':0}
    data['risk'] = data['category'].map(risk)
    #serialize the Dataframe object to a JSON String
    jsonStr = data.to_json(orient="records")
    return jsonStr

#send the PUT request and log the response
def putJSON(jsonStr):
    req = request.Request(url='http://localhost:8080/riskyItems', 
                          data=jsonStr,
                          method='PUT', 
                          headers={'content-type': 'application/json'})
    with request.urlopen(req) as f:
        pass
    print(f.status)
    print(f.reason)
    pass

def main():
    url = "http://localhost:8080/items"
    csv_data = read(url)
    data = dataManipulation(csv_data)
    jsonStr = serializeJSON(data)
    putJSON(jsonStr)
    
main()