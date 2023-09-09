# import cherrypy
# import utils
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
        data = utils.get_data_from_database(reverse, criteria)
        return {"no_of_items": data.__len__(), "result": data}
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="error occured during fetching the data",
        )


# --------------- getting single item by id or location ---------------
@app.get("/getitem")
def getItem(id: str = "", location: str = ""):
    if (location == "" and id != "") or (id != "" and location != ""):
        try:
            item = models.Craigslist.get_by_id(id)
            if item:
                return {"no_of_items": 1, "result": utils.modelObjToDict(item)}
        except DoesNotExist:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, f"item with id {id} not found!"
            )
        except:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "error occured during fetching the data",
            )

    # if only location is provided
    elif id == "" and location != "":
        try:
            parsed_loc = utils.parse_location(location)
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
    if status == "" and userid == "":
        raise HTTPException(400, "Provide either userid or status")

    item_list: list = []
    try:
        if status != "" and userid == "":  # only status parameter is provided
            items = models.Craigslist.select().where(models.Craigslist.status == status)
            for item in items:
                item_list.append(utils.modelObjToDict(item))
            return {"no_of_items": item_list.__len__(), "result": item_list}

        elif status == "" and userid != "":  # only userid parameter is provided
            items = models.Craigslist.select().where(models.Craigslist.userId == userid)
            for item in items:
                item_list.append(utils.modelObjToDict(item))
            return {"no_of_items": item_list.__len__(), "result": item_list}

        else:  # userid as well as status is provided
            items = models.Craigslist.select().where(
                models.Craigslist.userId == userid,
                models.Craigslist.status == status,
            )
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

    for item in data:
        # calculating the great circle distance
        loc1 = (item["latitude"], item["longitude"])
        loc2 = (latitude, longitude)
        dis = haversine.haversine(loc1, loc2, unit=Unit.KILOMETERS)

        if dis <= radius:  # assuming radius is provided in kilonmeters
            item_list.append(item)
    return {"no_of_items": item_list.__len__(), "result": item_list}


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=10001, reload=True)
