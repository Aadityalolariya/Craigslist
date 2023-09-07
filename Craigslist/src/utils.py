import json

def get_data_from_file():
    try:
        with open("./Craigslist/data.json", "r") as f:
            data = json.load(f)
            return data
    except:
        raise FileExistsError()


def parse_location(location):
    try:
        loc = location.split(" ")

        # validating the format of location
        if (
            loc.__len__() != 2
            or not loc[0].startswith("[")
            or not loc[0].endswith(",")
            or not loc[1].endswith("]")
        ):
            raise ValueError()
        
        # creating the list having latitude and longitude
        latitide = float(loc[0].removeprefix("[").removesuffix(","))
        longitude = float(loc[1].removesuffix("]"))
        parsed_loc = [latitide, longitude]

        return parsed_loc
    except:
        raise ValueError()
