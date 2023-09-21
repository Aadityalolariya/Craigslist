# Craigslist API

## Outline

It is an API that provides the data of people have listed for sale on Craigslist.

It is developed in three phases:

### Phase1
API is developed using *cherrypy* framework.
The data of items is stored in data.json file.

### Phase2
*Peewee* library is used for Object-Relational Mapping.
The data of items is stored in data.db file.

### Phase3
API is switched to *fastapi* framework from cherrypy.


## Getting Started:-

1. Clone the repository and open it.

2. Install all the dependencies by running:
   ```pip install -r requirements.txt```

3. To start the server, run the command:
   ```python Craigslist\src\app.py```

The server will be started on `http://127.0.0.1:10001` in phase2 and phase3, while in phase1 it will be started on `http://127.0.0.1:8080`.


## This API contains the following endpoints:

### The entire list sorted by the item’s price (Ascending and Descending based on reverse parameter):
    http://127.0.0.1:10001/getsorteddata?reverse=True&criteria=price

### Any single item by:
    --  By Id :-
        http://127.0.0.1:10001/getitem?id=AAsm
    --  By Location :-
        http://127.0.0.1:10001/getitem?location=AAsm

### List of items by:
    --  Status :-
        http://127.0.0.1:10001/getitemslist?status=AAsm
    --  userId :- 
        http://127.0.0.1:10001/getitemslist?userid=AAsm
    

### An array of items based on radius 
    --  Location specified by coordinate :- 
        http://127.0.0.1:10001/get_items_in_radius?radius=xy&latitude=xx&longitude=yy

**Note: All the above endpoints are GET requests. In *phase1*, use port 8080 instead of 10001.


## API Structure:-

The data is stored in data.json file.

`app.py` file contains all the endpoints.

`utils.py` conatains a couple of utility functions used in data processing.



## Technologies:-

`Fastapi`
`Cherrypy`
`Python`
`Haversine`
