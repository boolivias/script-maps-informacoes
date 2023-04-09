import googlemaps
import math

class MapsHelper:
    def __init__(self, maps_key) -> None:
        self.__client = googlemaps.Client(key=maps_key)

    def __apply_area_filter(self, param):
        area_filter = "administrative_area_level_4"
        filter_lambda = lambda r: r["types"].count(area_filter) > 0
        filter_object = filter(filter_lambda, param)
        return list(filter_object)[0]

    def getNeighborhood(self, lat, long):
        if not (math.isnan(lat) and math.isnan(long)) and lat != 0 and long != 0:
            maps_response = self.__client.reverse_geocode((lat, long))
            try:
                addr_components = self.__apply_area_filter(maps_response)["address_components"]
                return (False, self.__apply_area_filter(addr_components)["long_name"])
            except:
                return (True, maps_response)
        else:
            return (False, "S/R")
