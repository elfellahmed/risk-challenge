## Coding Challenge
This Coding Challende is dedicated to applicants for the integration team at xxxx.

### Requirements
Please send these informations and results to xxx

- an estimation how long you'll need to solve this task
- by when we can expect the solution
- your results (including the source code)
- how long you actually needed 

If you have any further questions, please don't hesitate to ask us.

### Development environment
Write the code in a language you feel comfortable with.
What would be the difference, if you run it once or on a regular basis?

### Starting situation
As integration manager for a fraud prevention solution I want to import a customers list of
items, enrich them with a risk score and import them into the fraud prevention solution.

Starting point is a list of items in CSV format.

Remove duplicated entries from this list and transform the CSV entries to JSON objects.

Map categories as follows:

```
1 -> phone
2 -> sim
3 -> supplies
4 -> headphones
```

Please add a risk score of 50 for items of the category 1.

The customer's list of items is available via HTTP interface.
The final JSONs should be uploaded via PUT to an external HTTP-interface.

### Format of the source file
- delimiter: Pipe (|)
- line separator: LF (\n)
- line 1: header / column names
- columns: id|produktId|artikeltyp|name|beschreibung|preis|bestand

### JSON schema of the destination JSON object
```
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "http://example.com/root.json",
  "type": "object",
  "required": [
    "id",
    "productId",
    "category",
    "price",
    "stock"
  ],
  "properties": {
    "id": {
      "$id": "#/properties/id",
      "type": "string",
      "examples": [
        "123abc"
      ]
    },
    "productId": {
      "$id": "#/properties/productId",
      "type": "string",
      "examples": [
        "abc123"
      ]
    },
    "productname": {
      "$id": "#/properties/productname",
      "type": [ "string", "null" ],
      "examples": [
        "iPhone 6"
      ]
    },
    "category": {
      "$id": "#/properties/category",
      "type": "string",
      "enum": [
        "phone",
        "sim",
        "supplies",
        "headphones"
      ]
      "examples": [
        "phone"
      ]
    },
    "comment": {
      "$id": "#/properties/comment",
      "type": [ "string", "null" ],
      "examples": [
        "This is a comment"
      ]
    },
    "price": {
      "$id": "#/properties/price",
      "type": "integer",
      "examples": [
        30.5
      ]
    },
    "stock": {
      "$id": "#/properties/stock",
      "type": "integer",
      "examples": [
        2
      ]
    },
    "risk": {
      "$id": "#/properties/risk",
      "type": "integer",
      "examples": [
        10
      ]
    }
  }
}
```

### API documentation download
- HTTP GET /items
- Response Body: CSV file

### API documentation upload
- HTTP PUT /riskyItems, Content-Type: application/json
- Response Code: 200 if JSON is in a correct structure

### Test Service
- Start: `java -jar coding-challenge.jar`
