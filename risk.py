from urllib import request, response, error
import pandas as pd
import json

#read the CSV from the API endpoint with only the required columns. Return a Pandas Dataframe.
def read(url):
    csv_data = pd.read_csv(url,delimiter="|",usecols=["id","produktId","artikeltyp","preis","bestand"])
    return csv_data


def dataManipulation(csv_data):
    #drop duplicates by ID from the Dataframe and rename the column 'arttikelTyp'
    csv_data.drop_duplicates(subset ="id", keep = False, inplace = True)
    csv_data.rename(columns={'artikeltyp':'category'}, inplace=True)
    csv_data['category'] = csv_data['category'].fillna(0)
    #print(csv_data.describe())
    csv_data['category'] = csv_data.category.astype(int)
    print(csv_data['category'].dtype)
    #Create a dict with the category mapping
    cat = {0:"undefined",1:"phone",2:"sim",3:"supplies",4:"headphones"}
    #map the dict created above with the artikelTyp column values
    csv_data['category'] = csv_data['category'].map(cat)
    return csv_data

def serializeJSON(data):
    #insert Risk as a new column with Value 50 for Cat1 and Value 0 for other Cat.
    risk = {'phone':50,'sim':0,'supplies':0,'headphones':0,'undefined':0}
    data['risk'] = data['category'].map(risk)
    print(data)
    #serialize the Dataframe object to a JSON String
    data.to_json(orient="records",inlines=True)
    return data

#send the PUT request and log the response
#def putJSON():
#    pass

def main():
    url = "/home/melfellah/Python/Risk.ident/risk-challenge/products.csv"
    csv_data = read(url)
    data = dataManipulation(csv_data)
    jsonStr = serializeJSON(data)
    #putJSON()
    print(jsonStr)

main()