import cherrypy
import haversine
from haversine import Unit
import utils
import models
from peewee import DoesNotExist


class Craigslist(object):
    # welcome endpoint
    @cherrypy.expose
    def index(self):
        return "Welcome"

    # get all the items sorted as per the given criteria
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getsorteddata(self, reverse: bool = False, criteria: str = "price"):
        if reverse:
            reverse = eval(reverse)  # converting from string to bool
        try:
            # fetching the data as per reverse and criteria parameter
            data = utils.get_data_from_database(reverse, criteria)
            return {"no_of_items": data.__len__(), "result": data}
        except AttributeError:
            cherrypy.response.status = 500
            return {"error": "criteria field is invalid"}
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
                item = models.Craigslist.get_by_id(id)  #  getting the item as per given id
                if item:
                    if location != "":
                        parsed_loc = utils.parse_location(location)

                        # when id is matching but location is not matching
                        if (item.latitude != parsed_loc[0] or item.longitude != parsed_loc[1]):  
                            cherrypy.response.status = 400
                            return {"error": f"item with id {id} and location {location} not found!"}

                    return {
                        "no_of_items": 1,
                        "result": utils.modelObjToDict(item)
                    }
            except DoesNotExist:
                cherrypy.response.status = 400
                return {"error": f"item with id {id} not found!"}
            except ValueError:
                cherrypy.response.status = 400
                return {"error": "Incorrect location format!"}
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
                    "result": utils.modelObjToDict(item)
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

        # if neither status nor userid is provided
        if status == "" and userid == "":
            cherrypy.response.status = 400
            return {"error": "Provide either userid or status"}

        item_list: list = []
        try:
            # only status parameter is provided
            if status != "" and userid == "": 
                items = models.Craigslist.select().where(models.Craigslist.status == status)

            # only userid parameter is provided
            elif status == "" and userid != "":  
                items = models.Craigslist.select().where(models.Craigslist.userId == userid)

            # userid as well as status is provided
            else:  
                items = models.Craigslist.select().where(models.Craigslist.userId == userid, models.Craigslist.status == status)

            # appending the items to the item_list
            for item in items:
                item_list.append(utils.modelObjToDict(item))
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
        except ValueError:          #  invalid parameter type
            cherrypy.response.status = 400
            return {"error": "All the parameters must be a numeber."}
        except:
            cherrypy.response.status = 500
            return {"error": "Some error occured while fetching data!"}

        item_list = []

        # iterating through all the items to get the valid items
        for item in data:
            # calculating the great circle distance
            loc1 = (item["latitude"], item["longitude"])
            loc2 = (latitude, longitude)
            dis = haversine.haversine(loc1, loc2, unit=Unit.KILOMETERS)

            if dis <= radius:  # assuming radius is provided in kilonmeters
                item_list.append(item)
        return {"no_of_items": item_list.__len__(), "result": item_list}


cherrypy.config.update({
    'server.socket_port' : 10001,
})

cherrypy.quickstart(Craigslist(), "/")