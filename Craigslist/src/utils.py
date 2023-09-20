import models


def get_data_from_database(reverse: bool = False, criteria: str = "price"):
    try:
        data = []
        # ordering the items by the price (by default) in ascending order
        cursor = models.Craigslist.select().order_by(models.Craigslist.price)

        for item in cursor:
            data.append(
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

    except:
        raise FileExistsError()

    # if reversed data is required or some other criteria for ordering is given
    if reverse != False or criteria != "price":
        try:
            sorted_data = sorted(data, reverse=reverse, key=lambda x: x[criteria])
            return sorted_data
        except:
            raise AttributeError()  # invalid criteria is provided
    return data


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


def modelObjToDict(item):
    return {
        "id": item.id,
        "latitude": item.latitude,
        "longitude": item.longitude,
        "userId": item.userId,
        "description": item.description,
        "price": item.price,
        "status": item.status,
    }