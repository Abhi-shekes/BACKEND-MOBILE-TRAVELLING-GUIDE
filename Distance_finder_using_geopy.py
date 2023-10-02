from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

geolocator = Nominatim(user_agent="place_distance_calculator")

place_distance_from_air = {}
place_distance_from_rail = {}
not_found = []

places_failed_to_find_distance = []


def distance_calculator(place1, place2, destination, place2_location):
    lat1 = None
    lon1 = None
    lat2 = None
    lon2 = None

    tourist_spot_source = str(place1) + f", {destination}"
    location1_with_city_name = geolocator.geocode(tourist_spot_source)
    if location1_with_city_name:

        lat1 = location1_with_city_name.latitude
        lon1 = location1_with_city_name.longitude
    else:
        place1_again = str(place1) + ", India"

        location1_with_india = geolocator.geocode(place1_again)
        if location1_with_india:
            lat1 = location1_with_india.latitude
            lon1 = location1_with_india.longitude
        else:
            print(f"Failed to locate {place1}.")

    tourist_spot_location = str(place2) + f", {place2_location}"
    location2_with_location = geolocator.geocode(tourist_spot_location)
    if location2_with_location:
        print(f"Place {place2} with location = {tourist_spot_location}")
        lat2 = location2_with_location.latitude
        lon2 = location2_with_location.longitude

    elif location2_with_location is None:
        tourist_spot_city = str(place2) + f", {destination}"
        location2_with_city = geolocator.geocode(tourist_spot_city)
        if location2_with_city:
            print(f"Place {place2} with City = {location2_with_city}")
            lat2 = location2_with_city.latitude
            lon2 = location2_with_city.longitude
    else:
        place2_again = str(place2) + ", India"
        location2_with_india = geolocator.geocode(place2_again)
        if location2_with_india:
            print(f"Place {place2} with India = {place2_again}")

            lat2 = location2_with_india.latitude
            lon2 = location2_with_india.longitude
        else:
            places_failed_to_find_distance.append(place2)

    if lat1 and lon1 and lat2 and lon2:
        return lat1, lon1, lat2, lon2

    else:
        return None, None, None, None


def find_distance(airport, railway, destination, tour_spot, tour_spot_location):

    if airport is not None:
        try:
            for i in range(len(tour_spot)):
                place2 = tour_spot[i]
                place2_location = tour_spot_location[i]
                lat1, lon1, lat2, lon2 = distance_calculator(airport, place2, destination, place2_location)
                if lat1 and lon1 and lat2 and lon2:
                    distance_from_air = geodesic((lat1, lon1), (lat2, lon2)).kilometers
                    place_distance_from_air[place2] = distance_from_air
                else:
                    not_found.append(place2)
        except (GeocoderTimedOut, GeocoderUnavailable) as e:
            print(f"Failed to connect to the geocoding service")
            return None, None, None

    # if railway is not None:
    #     try:
    #         for i in range(len(tour_spot)):
    #             place2 = tour_spot[i]
    #             place2_location = tour_spot_location[i]
    #             lat1, lon1, lat2, lon2 = distance_calculator(railway, place2, destination, place2_location)
    #             if lat1 and lon1 and lat2 and lon2:
    #                 distance_from_rail = geodesic((lat1, lon1), (lat2, lon2)).kilometers
    #                 place_distance_from_rail[place2] = distance_from_rail
    #             else:
    #                 not_found.append(place2)
    #     except (GeocoderTimedOut, GeocoderUnavailable) as e:
    #         return None, None, None
    #         print(f"Failed to connect to the geocoding service")

    return place_distance_from_air, place_distance_from_rail, not_found
