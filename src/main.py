import cherrypy
import utils
import haversine
from haversine import Unit

class GetAllItems(object):
    # welcome endpoint
    @cherrypy.expose
    def index(self):
        return "Welcome"


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getsorteddata(self, reverse: bool = False, criteria: str = "price"):
        if reverse:
            reverse = eval(reverse)     #converting from string to bool
        try:
            data = utils.get_data_from_file()
            sorted_data = sorted(data, reverse=reverse, key=lambda x: x[criteria])      #sorting the data in required way
            return {"result": sorted_data}
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
                data: list = utils.get_data_from_file()

                for item in data:
                    if item["id"] == id:
                        return item
                
                # if no item is found
                cherrypy.response.status = 400
                return {"error": f"item with id {id} not found!"}
            except:
                cherrypy.response.status = 500
                return {"error": "error occured during fetching the data"}

        # if only location is provided
        elif id == "" and location != "":
            try:
                parsed_loc = utils.parse_location(location)
                data = utils.get_data_from_file()

                for item in data:
                    if item["loc"] == parsed_loc:
                        return {"result": item}
                    
                # if no item is found
                cherrypy.response.status = 400
                return {"error": f"Not item found with location {location}"}
            
            except ValueError:
                cherrypy.response.status = 400
                return {"error": "Incorrect location format!"}
            except:
                cherrypy.response.status = 500
                return {"error": "Some error occured while fetching data"}
            
        else:
            cherrypy.response.status = 400
            return {"error": "provide id or location of item"}



    # get the list of items based on status or userid
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getitemslist(self, status: str = "", userid: str = ""):
        try:
            data: list = utils.get_data_from_file()
        except:
            cherrypy.response.status = 500
            return {"error": "error occured during fetching the data"}
        
        # if neither userid nor status is provided
        if status == "" and userid == "":
            cherrypy.response.status = 400
            return {"error": "Provide either userid or status"}
        
        item_list: list = []
        
        for item in data:
            if status != "" and userid != "":          
                if item["status"] == status and item["userId"] == userid:   # if both are provided, then consider both the parameters in item
                    item_list.append(item)

            elif status != "":
                if item["status"] == status:
                    item_list.append(item)
            
            else:
                if item["userId"] == userid:
                    item_list.append(item)

        return {"result": item_list}
    


    # to get the items in the given radius
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_items_in_radius(self, radius : float, latitude : float, longitude : float):

        # convert the parameters from string to float and fetch the data
        try:
            latitude = float(latitude)
            longitude = float(longitude)
            radius = float(radius)
            data = utils.get_data_from_file()
        except ValueError:
            cherrypy.response.status = 400
            return {"error" : "All the parameters must be a numeber."}
        except:
            cherrypy.response.status = 500
            return {"error" : "Some error occured while fetching data!"}
        
        item_list = []
        
        for item in data:

            # calculating the great circle distance
            loc1 = (item['loc'][0], item['loc'][1])
            loc2 = (latitude, longitude)
            dis = haversine.haversine(loc1, loc2,unit=Unit.KILOMETERS)

            if dis <= radius:
                item_list.append(item)

        return {"result" : item_list}


cherrypy.quickstart(GetAllItems(), "/")