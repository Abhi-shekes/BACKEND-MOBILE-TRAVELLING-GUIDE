import json
import random
with open('IndianJSON.json', 'r') as indian_data:
    data = json.load(indian_data)


STATE_IMAGE = {}
for state in data['States']:
    if state["StateName"] in ["Maharashtra", "Madhya Pradesh", "Manipur", "Meghalaya", "Karnataka", "Kerala", "Mizoram",
                              "Nagaland", "Odisha"]:
        state_images = state['StateImage']
        alternative_images = [image for i, image in enumerate(state_images) if i % 2 == 0]
        for stateimage in alternative_images:
            STATE_IMAGE[state["StateName"]] = stateimage.split(".")[0]

CITY_IMAGE = {}
for state in data['States']:
    if state["StateName"] in ["Maharashtra", "Madhya Pradesh", "Manipur", "Meghalaya", "Karnataka", "Kerala", "Mizoram",
                              "Nagaland","Odisha"]:
        for city in state["Cities"]:
            city_image = city["CityImage"]
            alternative_images = [image for i, image in enumerate(city_image) if i % 2 == 0]
            for cityimage in alternative_images:
                CITY_IMAGE[city["CityName"]] = cityimage.split(".")[0]

SPOT_IMAGE = {}
for state in data['States']:
    if state["StateName"] in ["Maharashtra", "Madhya Pradesh", "Manipur", "Meghalaya", "Karnataka", "Kerala", "Mizoram",
                              "Nagaland", "Odisha"]:
        for city in state["Cities"]:
            for spot in city["TouristSpots"]:
                spot_image = spot["Images"]
                alternative_images = [image for i, image in enumerate(spot_image) if i % 2 == 0]
                for spotimage in alternative_images:
                    SPOT_IMAGE[spot["TouristSpotName"]] = spotimage.split(".")[0]

UT_IMAGE = {}
for ut in data["UnionTerritory"]:
    if ut['UnionTerritoryName'] in ["Delhi", "Lakshadweep", "Puducherry"]:
        ut_images = ut["UnionTerritoryImage"]
        alternative_images = [image for i, image in enumerate(ut_images) if i % 2 == 0]
        for images in alternative_images:
            UT_IMAGE[ut["UnionTerritoryName"]] = images.split(".")[0]


SPOT_IMAGE_10 = random.sample(SPOT_IMAGE.items(), 10)
SPOT_IMAGE_10 = dict(SPOT_IMAGE_10)

CITY_IMAGE_10 = random.sample(CITY_IMAGE.items(), 10)
CITY_IMAGE_10 = dict(CITY_IMAGE_10)

STATE_IMAGE_10 = random.sample(STATE_IMAGE.items(), 9)
STATE_IMAGE_10 = dict(STATE_IMAGE_10)

UT_IMAGE_10 = random.sample(UT_IMAGE.items(), 3)
UT_IMAGE_10 = dict(UT_IMAGE_10)


