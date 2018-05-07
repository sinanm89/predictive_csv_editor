import csv
import collections
from reader import read_the_csv_files, list_all_files
from FINAL_freq_map_backup import prev_freq_map as FREQ_MAP
import json

example_dict = {
    'hotelContent.rooms.hotelHighlights.roomCounts.nonSmokingRoomCount': 'hotelinfo.profile.nonSmokingRoomCount',
    'hotelContent.generalPropertyDetails.profile.femaNumber': 'hotelinfo.profile.femaNumber',
    'hotelContent.facilities.parking.carParkingAvailable': 'hotelinfo.parking.carParkingAvailable',
    'hotelContent.facilities.parking.valetParkingAvailable': 'hotelinfo.parking.valetParkingAvailable',
    'hotelContent.facilities.parking.dailyValetParkingFee': 'hotelinfo.parking.dailyValetParkingFee',
    'hotelContent.facilities.parking.parkingDescription.value': 'hotelinfo.parking.parkingDescription',
    'hotelContent.generalPropertyDetails.checkOut.lateCheckOutAvailable': 'hotelinfo.parking.lateCheckoutAvailable',
    'hotelContent.generalPropertyDetails.petPolicy.petsAllowed': 'hotelInfo.facilities.petsAllowed',
    'hotelContent.generalPropertyDetails.petPolicy.guideDogsOrServiceAnimalsAllowed': 'hotelInfo.facilities.guideDogsOrServiceAnimalsAllowed',
    'hotelContent.facilities.publicAreas.interiorCorridors': 'hotelinfo.facilities.publicInteriorCorridors',
    'hotelContent.facilities.publicAreas.exteriorCorridors': 'hotelinfo.facilities.publicExteriorCorridors',
    'hotelContent.marketing.marketingText.hotelMajorFeature.value': 'hotelInfo.location.introText or hotelInfo.profile.shortDescription'
}

TAB = ' '

base_definition: ['type: ', 'properties:']
_input_dict = None

DETAIL_MAP = {}

def dict_reduce(input_dict):
    """Reduce a given dict with random elements into one."""
    output = {}
    for key in input_dict.keys():
        # {'value': 'Apigee', 'keys_value': 'value', 'val_type': 'string', 'extras': []}
        #  get the actual key name value
        lookup_val = input_dict[key]['value']
        value = lookup_val.split('.')
        if len(value) <= 2:
            # import pdb; pdb.set_trace()
            continue
        if value == 'MISSING':
            print('------' +key)
            continue
        output = create_hierarchy(output, lookup_val)

    return output

def create_hierarchy(output, long_key):
    keys = long_key.split('.')
    nested_input = create_nested(keys)
    updated_hierarchy = update_or_create_nested(output, nested_input)
    return updated_hierarchy

def get_type(val):
    if type(val) == dict:
        val = 'object'
    elif type(val) == list:
        val = 'array'
    elif type(val) == str:
        val = 'string'
    elif type(val) == int:
        val = 'integer'
    elif type(val) == bool:
        val = 'boolean'
    else:
        import pdb; pdb.set_trace()
    return val

def read_csv_values():
    csv_dir = 'csv_files/'
    file_list = list_all_files(csv_dir)
    updated_freq_map = {}
    for file_name in file_list:
        # file_name.split('.')[-1]
        if not '.csv' in file_name:
            continue
        with open(csv_dir + file_name, newline='') as csvfile:
            reader = csv.reader(csvfile)
            read_csv_data = list(reader)

        for line in read_csv_data:
            key = line[1]
            if key == '':
                continue

            updated_freq_map[key] = {
                'value': FREQ_MAP.get(key),
                'keys_value': line[2],
                'val_type': get_type(line[2]),
                'extras': [],
            }

    return updated_freq_map

def create_contract(u_f_m):
    attributes = u_f_m.keys()

    for att in attributes:
        u_f_m.get(att)

def get_nested(d, key):
    keys = key.split('.')
    for k in keys:
        val = d.get(k, None)
        if val is None:
            return None
    return val

def update_or_create_nested(d, u):
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            d[k] = update_or_create_nested(d.get(k, {}), v)
        else:
            d[k] = v
    return d

def create_nested(long_key):
     # {'a': {'b': {'c': {}}}}
    if len(long_key) == 0:
        return {}
    return {long_key[0].lower():create_nested(long_key[1:])}


if __name__ == '__main__':
    # import pdb; pdb.set_trace()
    updated_freq_map = read_csv_values()
    ee = dict_reduce(updated_freq_map)
    import pdb; pdb.set_trace()

    # calculate tiers
    # create contract based on tiers.
    # tier 1 hotelinfo ; pass
        # tier 2 profiles ; pass




# lookup_val.split('.')
# output={}
# # a.b.c.d
# # b.c.b.a
# tier = 0
# for key in keys:
#     all_vals = lookup_val.split('.')
#     for tiers in all_vals:

#     else:
#         tier += 1



# # e.b.c.f

