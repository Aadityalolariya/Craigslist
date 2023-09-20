import haversine
from haversine import Unit
import utils
import models
from peewee import DoesNotExist
from fastapi import HTTPException, FastAPI, Response, status
import uvicorn

app = FastAPI()


@app.get("/")
def welcome():
    return "Welcome"


# --------------- getting all the items in sorted form ---------------
@app.get("/getsorteddata")
def getSortedData(reverse: bool = False, criteria: str = "price"):
    try:
        # fetching the data as per reverse and criteria parameter
        data = utils.get_data_from_database(reverse, criteria)
        return {"no_of_items": data.__len__(), "result": data}
    except AttributeError:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "criteria field is invalid"
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="error occured during fetching the data",
        )


# --------------- getting single item by id or location ---------------
@app.get("/getitem")
def getItem(id: str = "", location: str = ""):
    # only id is given or id as well as location is given
    if (location == "" and id != "") or (id != "" and location != ""):
        try:
            item = models.Craigslist.get_by_id(id)  # get the item by id
            if item:
                # if location is also provided, we will check location of the item too
                if location != "":
                    parsed_loc = utils.parse_location(location)
                    #  if location is matching
                    if (parsed_loc[0] == item.latitude and parsed_loc[1] == item.longitude):
                        return {"no_of_items": 1, "result": utils.modelObjToDict(item)}
                    
                    #  if location is not matching
                    else:       
                        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"item with id {id} and location {location} not found!")
                
                # if location is not provided
                return {"no_of_items": 1, "result": utils.modelObjToDict(item)}
        except DoesNotExist:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, f"item with id {id} not found!")
        except ValueError:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Incorrect location format!")

    # if only location is provided
    elif id == "" and location != "":
        try:
            parsed_loc = utils.parse_location(location)     # parse the location from string to list

            # get the item matching the given location
            item = models.Craigslist.get(
                models.Craigslist.latitude == parsed_loc[0],
                models.Craigslist.longitude == parsed_loc[1],
            )
            return {"no_of_items": 1, "result": utils.modelObjToDict(item)}
        except ValueError:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "Incorrect location format!"
            )

        except DoesNotExist:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, f"Not item found with location {location}"
            )
        except:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Some error occured while fetching data",
            )

    # if no parameter is provided
    else:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "provide id or location of item"
        )


# --------------- getting the list of items based on the given status or userid ---------------
@app.get("/getitemslist")
def getItemsList(status: str = "", userid: str = ""):

    # if neither status not userid is provided
    if status == "" and userid == "":
        raise HTTPException(400, "Provide either userid or status")

    item_list: list = []
    try:
        if status != "" and userid == "":  # only status parameter is provided
            items = models.Craigslist.select().where(models.Craigslist.status == status)

        elif status == "" and userid != "":  # only userid parameter is provided
            items = models.Craigslist.select().where(models.Craigslist.userId == userid)

        else:  # userid as well as status is provided
            items = models.Craigslist.select().where(
                models.Craigslist.userId == userid,
                models.Craigslist.status == status,
            )

        #  append all the required items in item_list
        for item in items:
            item_list.append(utils.modelObjToDict(item))

        return {"no_of_items": item_list.__len__(), "result": item_list}

    except:
        raise HTTPException(500, "Some error occured while fetching the data!")


# --------------- getting the items in the radius of given latitude and longitude ---------------
@app.get("/get_items_in_radius")
def getItemsInRadius(radius: float, latitude: float, longitude: float):
    # fetching the data
    try:
        data = utils.get_data_from_database()
    except:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Some error occured while fetching data!",
        )
    
    item_list = []

    #  iterating through all the items to get the valid items
    for item in data:
        # calculating the great circle distance
        loc1 = (item["latitude"], item["longitude"])
        loc2 = (latitude, longitude)
        dis = haversine.haversine(loc1, loc2, unit=Unit.KILOMETERS)

        if dis <= radius:  # assuming radius is provided in kilonmeters
            item_list.append(item)

    return {"no_of_items": item_list.__len__(), "result": item_list}


if __name__ == "__main__":
    # hosting the server on ip address of the pc rather than localhost so that the systems in same network can also access the server.
    uvicorn.run("app:app", host="192.168.189.117", port=10001, reload=True)