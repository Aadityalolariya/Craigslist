# Craigslist Server

It is an API that provides the data of people have listed for sale on Craigslist.

## This API contains the following endpoints:

### The entire list sorted by the item’s price (Ascending and Descending based on reverse parameter) -
    getsorteddata?reverse=True&criteria=price

### Any single item by:
    --  By Id :- getitem?id=AAsm
    --  By Location - getitem?location=AAsm
    If both are provided, then only id is considered.

### List of items by:
    --  Status - getitemslist?status=AAsm
    --  userId - getitemslist?userid=AAsm
    if both are provided, then both of the parameters are simultaneously considered.

### An array of items based on radius 
    --  Location specified by coordinate - get_items_in_radius?radius=xy&latitude=xx&longitude=yy

**Note: All the above endpoints are GET requests.



## Getting Started:-

### Open the command prompt. Requirements are specified in requirements.txt file.
So, to install all the dependencies, run the command
`pip install -r requirements.txt`

### To start the server, in repository itself, run app.py file by running the command
`python Craigslist\src\app.py`

The server will be started on [http://127.0.0.1:10001](http://127.0.0.1:10001).

Apply the above mentioned endpoints to test the API.



## API Structure:-

The data is stored in data.json file.

`app.py` file contains all the endpoints.

`utils.py` conatains a couple of utility functions used in data processing.



## Technologies:-

`Python`
`Fastapi`
`Haversine`