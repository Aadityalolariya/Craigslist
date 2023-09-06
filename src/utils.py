import json


def get_data_from_file():
    try:
        with open("./data.json", "r") as f:
            data = json.load(f)
            return data
    except:
        raise FileExistsError()


def parse_location(location):
    try:
        loc = location.split(" ")
        if (
            loc.__len__() != 2
            or not loc[0].startswith("[")
            or not loc[0].endswith(",")
            or not loc[1].endswith("]")
        ):
            raise ValueError()
        latitide = float(loc[0].removeprefix("[").removesuffix(","))
        longitude = float(loc[1].removesuffix("]"))
        parsed_loc = [latitide, longitude]
        return parsed_loc
    except:
        raise ValueError()
