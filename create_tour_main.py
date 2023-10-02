import json
import random
from prefix import prefixes
import Distance_finder_using_geopy

# TODO: sort places from closed to farthest = DONE
# TODO: make the number of places in one day, dynamic = DONE
# TODO: Write the phases after Day            -----LAST
# TODO: add (things to do there) after place name  -------- LAST
# TODO: deal with less number of tourist spot (Solution : add some tourist spot of nearby city)   ----- NEXT
# TODO: add validation of ideal (no of day) to visit that city   ---LAST
# TODO: skip the not found location in distance calculator ----------- DONE
# TODO: Sort from previous spot
# TODO: use Threading

with open('IndianJSON.json', 'r') as indian_data:
    data = json.load(indian_data)

no_of_place_in_a_day = 3


def fetch_and_sort(destination):

    destination = destination.title()
    places_ready_to_render = []

    tour_spot = []
    tour_spot_location = []

    nearest_airport = None
    nearest_railway = None

    for state in data['States']:
        for city in state['Cities']:
            if city['CityName'] == destination:
                for spot in city['TouristSpots']:
                    if "NearestAirport" in spot:
                        nearest_airport = spot["NearestAirport"]
                    else:
                        nearest_airport = None
                    if "NearestRailway" in spot:
                        nearest_railway = spot["NearestRailway"]
                    else:
                        nearest_railway = None

                    tour_spot.append(spot['TouristSpotName'])
                    tour_spot_location.append(spot["Location"])

    for ut in data['UnionTerritory']:
        if ut['UnionTerritoryName'] == destination:
            for spot in ut['TouristSpots']:
                tour_spot.append(spot['TouristSpotName'])
                if "NearestAirport" in spot:
                    nearest_airport = spot["NearestAirport"]
                else:
                    nearest_airport = None
                if "NearestRailway" in spot:
                    nearest_railway = spot["NearestRailway"]
                else:
                    nearest_railway = None
                tour_spot_location.append(spot["Location"])

    if len(tour_spot) == 0:
        print('Destination Not Found')

    place_distance_from_air, place_distance_from_rail, not_find =\
        Distance_finder_using_geopy.find_distance(airport=nearest_airport, railway=nearest_railway, tour_spot=tour_spot,
                                                  destination=destination, tour_spot_location=tour_spot_location)

    if place_distance_from_air or place_distance_from_rail or not_find:
        sorted_location = sort_near_to_far(place_distance_from_air)
        for place_name, km in sorted_location.items():
            if km == 0.0:
                pass
            else:
                places_ready_to_render.append(place_name)

        for place_name, km in sorted_location.items():
            if km == 0.0:
                places_ready_to_render.append(place_name)

        return places_ready_to_render
    else:
        return None


def create_personalised_trip(places_ready_to_render, no_of_days):
    global no_of_place_in_one_day
    no_of_place_in_one_day = no_of_place_in_a_day
    personalised_trip_empty = {}
    personalised_trip = personalised_trip_empty.copy()
    places_copy = places_ready_to_render[:]

    total_places_needed = no_of_place_in_one_day * no_of_days
    if len(places_ready_to_render) < total_places_needed:
        while no_of_place_in_one_day >= 2 and len(places_copy) < total_places_needed:
            no_of_place_in_one_day -= 1
            total_places_needed = no_of_place_in_one_day * no_of_days

    try:
        for day in range(1, no_of_days + 1):
            places = random.sample(places_copy, k=no_of_place_in_one_day)
            personalised_trip[f'Day {day}'] = places

            for place in places_copy:
                if place in places:
                    places_copy.remove(place)
        if personalised_trip:
            return personalised_trip
    except Exception as e:
        no_of_place_in_one_day = no_of_place_in_one_day - 1
        if no_of_place_in_one_day >= 2:
            create_personalised_trip(places_ready_to_render, no_of_days)
        else:
            print("More number of days than the number of tourist spots in that city")


def print_personalized_trip(trip, starting_prefixes):
    time = ['09:00 am', '11:00 am', '02:00 pm', '04:00 pm', '06:00 pm']
    try:
        for day, places in trip.items():
            if day == 'Day 1':
                print(f"{day}: Arrival and Explore")
            else:
                print(f'{day}')

            starting_prefixes_to_add = starting_prefixes[:]
            for place in places:
                prefix = random.choice(starting_prefixes_to_add)
                starting_prefixes_to_add.remove(prefix)
                print(f"{time[places.index(place)]}: {prefix} {place}")
            print()
    except Exception as e:
        print('Something Went Wrong', e)

    # remove this line when run console application
    return True

def sort_near_to_far(place_distance_from_air):
    list_for_sorting = []
    for places, dist in place_distance_from_air.items():
        list_for_sorting.append(dist)
    list_for_sorting = sorted(list_for_sorting)

    sorted_location = {}

    for i in list_for_sorting:
        for places, dist in place_distance_from_air.items():
            if i == dist:
                sorted_location[places] = i

    return sorted_location

#
# run_successfully = False
#
# user_choice_city = input("Enter The City name: ")
# no_of_day = int(input("Enter No. of days: "))
#
# all_the_tourist_spot = fetch_and_sort(user_choice_city)
#
# if all_the_tourist_spot:
#     personalised = create_personalised_trip(all_the_tourist_spot, no_of_days=no_of_day)
# else:
#     personalised = None
#     print("ISSUE WITH fetch_and_sort function")
#
# if personalised:
#     print("******************************************************************************************************")
#     print_personalized_trip(personalised, prefixes)
#     print("******************************************************************************************************")
#     run_successfully = True
#
#
# while run_successfully:
#     flag = input("Do you want to change your personalised trip ? Y/N ")
#     flag = flag.lower()
#     if flag == 'y':
#         tourist_spot_to_shuffle = all_the_tourist_spot
#         random.shuffle(tourist_spot_to_shuffle)
#         no_of_day = int(input("Enter No. of days: "))
#         personalised_again = create_personalised_trip(tourist_spot_to_shuffle, no_of_days=no_of_day)
#         print_personalized_trip(personalised_again, prefixes)
#     else:
#         print("Thank For Using TourSarthi")
#         break


def generate_personalized_trip(trip, starting_prefixes):
    time = ['09:00 am', '11:00 am', '02:00 pm', '04:00 pm', '06:00 pm']
    personalized_trip = []

    try:
        for day, places in trip.items():
            day_details = []
            if day == 'Day 1':
                day_details.append(f"{day}: Arrival and Explore")
            else:
                day_details.append(day)

            starting_prefixes_to_add = starting_prefixes[:]
            for place in places:
                prefix = random.choice(starting_prefixes_to_add)
                starting_prefixes_to_add.remove(prefix)
                day_details.append(f"{time[places.index(place)]}: {prefix} {place}")

            personalized_trip.append(day_details)
    except Exception as e:
        print('Something Went Wrong', e)

    return personalized_trip
