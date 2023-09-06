import cherrypy
import utils
import math
class GetAllItems(object):
    @cherrypy.expose
    def index(self):
        return "Welcome"

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getsorteddata(self, reverse: bool = False, criteria: str = "price"):
        if reverse:
            reverse = eval(reverse)
        try:
            data = utils.get_data_from_file()
            sorted_data = sorted(data, reverse=reverse, key=lambda x: x[criteria])
            return {"result": sorted_data}
        except:
            cherrypy.response.status = 500
            return {"error": "error occured during fetching the data"}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getitem(self, id: str = "", location: str = ""):
        if (location == "" and id != "") or (id != "" and location != ""):
            try:
                data: list = utils.get_data_from_file()
                for item in data:
                    if item["id"] == id:
                        return item
                cherrypy.response.status = 400
                return {"error": f"item with id {id} not found!"}
            except:
                cherrypy.response.status = 500
                return {"error": "error occured during fetching the data"}

        elif id == "" and location != "":
            try:
                parsed_loc = utils.parse_location(location)
                data = utils.get_data_from_file()
                for item in data:
                    if item["loc"] == parsed_loc:
                        return {"result": item}
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

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getitemslist(self, status: str = "", userid: str = ""):
        try:
            data: list = utils.get_data_from_file()
        except:
            cherrypy.response.status = 500
            return {"error": "error occured during fetching the data"}
        if status == "" and userid == "":
            cherrypy.response.status = 400
            return {"error": "Provide either userid or status"}
        item_list: list = []
        for item in data:
            if status != "" and userid != "":
                if item["status"] == status and item["userId"] == userid:
                    item_list.append(item)
            elif status != "":
                if item["status"] == status:
                    item_list.append(item)
            else:
                if item["userId"] == userid:
                    item_list.append(item)

        return {"result": item_list}
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_items_in_radius(self, radius : float, latitude : float, longitude : float):
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
            item_latitude = item['loc'][0]
            item_longitude = item['loc'][1]
            dis : float = math.sqrt((item_latitude - latitude)**2 + (item_longitude - longitude)**2)
            if dis <= radius:
                item_list.append(item)
        return {"result" : item_list}


cherrypy.quickstart(GetAllItems(), "/")