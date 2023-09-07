import cherrypy
import utils
import haversine
from haversine import Unit
import models
from peewee import DoesNotExist


class Craigslist(object):
    # welcome endpoint
    @cherrypy.expose
    def index(self):
        return "Welcome"

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getsorteddata(self, reverse: bool = False, criteria: str = "price"):
        if reverse:
            reverse = eval(reverse)  # converting from string to bool
        try:
            data = utils.get_data_from_database(reverse, criteria)
            return {"no_of_items": data.__len__(), "result": data}
        except:
            cherrypy.response.status = 500
            return {"error": "error occured during fetching the data"}

    # get the item based on location or id
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getitem(self, id: str = "", location: str = ""):
        # if only id is provided or location as well as id is provided
        if (location == "" and id != "") or (id != "" and location != ""):
            try:
                item = models.Craigslist.get_by_id(id)
                if item:
                    return {
                        "no_of_items": 1,
                        "res": {
                            "id": item.id,
                            "latitude": item.latitude,
                            "longitude": item.longitude,
                            "userId": item.userId,
                            "description": item.description,
                            "price": item.price,
                            "status": item.status,
                        },
                    }
            except DoesNotExist:
                cherrypy.response.status = 400
                return {"error": f"item with id {id} not found!"}
            except:
                cherrypy.response.status = 500
                return {"error": "error occured during fetching the data"}

        # if only location is provided
        elif id == "" and location != "":
            try:
                parsed_loc = utils.parse_location(location)
                item = models.Craigslist.get(
                    models.Craigslist.latitude == parsed_loc[0],
                    models.Craigslist.longitude == parsed_loc[1],
                )
                return {
                    "no_of_items": 1,
                    "result": {
                        "id": item.id,
                        "latitude": item.latitude,
                        "longitude": item.longitude,
                        "userId": item.userId,
                        "description": item.description,
                        "price": item.price,
                        "status": item.status,
                    },
                }
            except ValueError:
                cherrypy.response.status = 400
                return {"error": "Incorrect location format!"}
            except DoesNotExist:
                cherrypy.response.status = 400
                return {"error": f"Not item found with location {location}"}
            except:
                cherrypy.response.status = 500
                return {"error": "Some error occured while fetching data"}

        # if no parameter is provided
        else:
            cherrypy.response.status = 400
            return {"error": "provide id or location of item"}

    # get the list of items based on status or userid
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getitemslist(self, status: str = "", userid: str = ""):
        if status == "" and userid == "":
            cherrypy.response.status = 400
            return {"error": "Provide either userid or status"}

        item_list: list = []
        try:
            if status != "" and userid == "":  # only status parameter is provided
                items = models.Craigslist.select().where(
                    models.Craigslist.status == status
                )
                for item in items:
                    item_list.append(
                        {
                            "id": item.id,
                            "latitude": item.latitude,
                            "longitude": item.longitude,
                            "userId": item.userId,
                            "description": item.description,
                            "price": item.price,
                            "status": item.status,
                        }
                    )
                return {"no_of_items": item_list.__len__(), "result": item_list}

            elif status == "" and userid != "":  # only userid parameter is provided
                items = models.Craigslist.select().where(
                    models.Craigslist.userId == userid
                )
                for item in items:
                    item_list.append(
                        {
                            "id": item.id,
                            "latitude": item.latitude,
                            "longitude": item.longitude,
                            "userId": item.userId,
                            "description": item.description,
                            "price": item.price,
                            "status": item.status,
                        }
                    )
                return {"no_of_items": item_list.__len__(), "result": item_list}

            else:  # userid as well as status is provided
                items = models.Craigslist.select().where(
                    models.Craigslist.userId == userid,
                    models.Craigslist.status == status,
                )
                for item in items:
                    item_list.append(
                        {
                            "id": item.id,
                            "latitude": item.latitude,
                            "longitude": item.longitude,
                            "userId": item.userId,
                            "description": item.description,
                            "price": item.price,
                            "status": item.status,
                        }
                    )
                return {"no_of_items": item_list.__len__(), "result": item_list}

        except:
            cherrypy.response.status = 500
            return {"error": "Some erro occured while fetching the data!"}

    # to get the items in the given radius
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_items_in_radius(self, radius: float, latitude: float, longitude: float):
        # convert the parameters from string to float and fetch the data
        try:
            latitude = float(latitude)
            longitude = float(longitude)
            radius = float(radius)
            data = utils.get_data_from_database()
        except ValueError:
            cherrypy.response.status = 400
            return {"error": "All the parameters must be a numeber."}
        except:
            cherrypy.response.status = 500
            return {"error": "Some error occured while fetching data!"}

        item_list = []

        for item in data:
            # calculating the great circle distance
            loc1 = (item["latitude"], item["longitude"])
            loc2 = (latitude, longitude)
            dis = haversine.haversine(loc1, loc2, unit=Unit.KILOMETERS)

            if dis <= radius:  # assuming radius is provided in kilonmeters
                item_list.append(item)
        return {"no_of_items": item_list.__len__(), "result": item_list}


cherrypy.quickstart(Craigslist(), "/")
