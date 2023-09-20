import cherrypy
import utils
import haversine
from haversine import Unit

class GetAllItems(object):
    # ---------------------- welcome endpoint ---------------------- 
    @cherrypy.expose
    def index(self):
        return "Welcome"


    #  ---------------------- get all the items in sorted order as per the given criteria ---------------------- 
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getsorteddata(self, reverse: bool = False, criteria: str = "price"):
        if reverse:
            reverse = eval(reverse)     #converting from string to bool
        try:
            data = utils.get_data_from_file()           #  fetching the data from file
            sorted_data = sorted(data, reverse=reverse, key=lambda x: x[criteria])      #sorting the data as per criteria in required order
            return {"no_of_items": sorted_data.__len__(), "result": sorted_data}
        except:
            cherrypy.response.status = 500
            return {"error": "error occured during fetching the data"}



    #  ---------------------- get the item based on location or id ---------------------- 
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getitem(self, id: str = "", location: str = ""):

        # if only id is provided or location as well as id is provided
        if (location == "" and id != "") or (id != "" and location != ""):
            try:
                data: list = utils.get_data_from_file()         # fetching all the items 
                
                # searching and returning the item with given id
                for item in data:
                    if item["id"] == id:
                        #  if location is provided the we will check location too
                        if location != "":          
                            parsed_loc = utils.parse_location(location)     #  parsing the location string to list
                            if item['loc'] == parsed_loc:
                                return item
                            else:                   # id is matching but the location is not matching
                                cherrypy.response.status = 400
                                return {"error": f"item with id {id} and location {location} not found!"}
                        
                        return item
                
                # if no item is found
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
                parsed_loc = utils.parse_location(location)     #  parsing the location from string to list
                data = utils.get_data_from_file()               #  fetching all the items

                #  iterating over all the items to find and return the item with the specified location
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
            
        #  if neither id nor location is provided
        else:
            cherrypy.response.status = 400
            return {"error": "provide id or location of item"}


    #  ---------------------- get the list of items based on status or userid  ---------------------- 
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getitemslist(self, status: str = "", userid: str = ""):
        #  fetching all the items
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
        
        # iterating through all the items to append the items satisfying the provided parameters
        for item in data:
            if status != "" and userid != "":           #  status as well as userid is provided
                if item["status"] == status and item["userId"] == userid:   # if both are provided, then consider both the parameters in item
                    item_list.append(item)

            elif status != "":                          #  only status is provided
                if item["status"] == status:
                    item_list.append(item)
            
            else:                                       #  only userid is provided
                if item["userId"] == userid:
                    item_list.append(item)

        return {"no_of_items": item_list.__len__(), "result": item_list}
    

    #  ---------------------- get the items in the given radius around the given location ---------------------- 
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_items_in_radius(self, radius : float, latitude : float, longitude : float):

        # convert the parameters from string to float and fetch the all the items
        try:
            latitude = float(latitude)
            longitude = float(longitude)
            radius = float(radius)
            data = utils.get_data_from_file()
        except ValueError:              #  invalid parameter is given
            cherrypy.response.status = 400
            return {"error" : "All the parameters must be a numeber."}
        except:
            cherrypy.response.status = 500
            return {"error" : "Some error occured while fetching data!"}
        
        item_list = []
        
        #  iterate through all the items of find the items falling in the given radius around the given location
        for item in data:
            # calculating the great circle distance
            loc1 = (item['loc'][0], item['loc'][1])
            loc2 = (latitude, longitude)
            dis = haversine.haversine(loc1, loc2,unit=Unit.KILOMETERS)

            if dis <= radius:
                item_list.append(item)

        return {"no_of_items": item_list.__len__() ,"result" : item_list}

cherrypy.quickstart(GetAllItems(), "/")