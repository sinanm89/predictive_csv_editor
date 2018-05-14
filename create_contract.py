import csv
import collections
from reader import read_the_csv_files, list_all_files
from FINAL_freq_map_backup import prev_freq_map as FREQ_MAP
import json
import uuid
from datetime import datetime


# =====

# there needs to be a collection of

# taxes:[]
# fees:[]

# added to the hcm attribute yaml file

# update the yaml file

# ======

_input_dict = None

DETAIL_MAP = {}

def dict_reduce(input_dict):
    """Reduce a given dict with random elements into one."""
    output = {}

    for key in input_dict.keys():
        # {'value': 'Apigee', 'keys_value': 'value', 'val_type': 'string', 'extras': []}
        #  get the actual key name value
        lookup_val = input_dict[key]['long_key']
        try:
            value = lookup_val.split('.')
        except:
            import pdb;pdb.set_trace()
        if '' in value:
            print('=====EMPTY VALUE IN INPUT DICT')
        if len(value) <= 2:
            continue
        if value == 'MISSING':
            print('=====MISSING KEY' + key)
            continue
        output = create_hierarchy(output, input_dict[key])

    return output

def create_hierarchy(output, meta):
    keys = meta['long_key'].split('.')
    nested_input = create_nested(keys)
    updated_hierarchy = update_or_create_nested(output, nested_input, meta)
    return updated_hierarchy

def get_type(val):
    if val == None:
        return '===UNKNOWN==='
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
        val = '===UNKNOWN==='
        # import pdb; pdb.set_trace()
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
            if FREQ_MAP.get(key) == None:
                continue
            if FREQ_MAP.get(key) == '':
                continue
            updated_freq_map[key] = {
                'long_key': FREQ_MAP.get(key, ''),
                'keys_value': line[2],
                'val_type': get_type(line[2]),
                'extras': [],
            }

    return updated_freq_map

def create_contract(payload_hierarchy_map):
    # {a:{
    #     b:{e:-,f:-,g:-}
    #     c:-
    #     d:-
    # }}
    import pdb; pdb.set_trace()
    write_contract_block(payload_hierarchy_map['hotelinfo'], 'hotelinfo')
    for att_k, att_v in payload_hierarchy_map.items():
        if att_k == '_meta':
            continue
        create_contract_block(att_v, att_k)

def create_contract_block(value_map, key):
    """
        properties:
            sideQuest:
                type: string
                $ref: '#definitions/{REFERENCE_OBJ}'
    """
    for k, v in value_map.items():
        if k == '_meta':
            continue
        if last_item_in_tier(v):
            continue
        write_contract_block(v, k)
        create_contract_block(v, k)

def last_item_in_tier(value_map):
    return len(value_map.keys()) == 1 and '_meta' in value_map.keys()

def write_contract_block(keys_value, key):

    tab = '  '
    tab_count = 1
    type_block = '{tab}type: object\n{tab}properties:'.format(tab=tab)
    if key[-1] == 's':
        type_block = "{tab}type: array\n{tab}items:".format(tab=tab)
    contract_block = '{key}Object:\n{type_block}\n'.format(
        key=key, type_block=type_block
    )
    tab_count += 1
    _tab_count = tab_count
    timestamp = str(datetime.now().timestamp()).split('.')[0]
    with open('generated_contract_{0}.yaml'.format(timestamp), 'a') as open_file:
        child_block = ''
        if last_item_in_tier(keys_value):
            value_type = keys_value['_meta'].get('val_type', None)
            contract_block = '{key}Object:\n{tab}type: {type}\n'.format(
                tab=tab, type=value_type, key=key
            )
        else:
            for child in keys_value.keys():
                if child == '_meta':
                    continue
                if last_item_in_tier(keys_value[child]):
                    child_block += "{tab}{child}:\n{child_tab}type: {type}\n".format(
                        tab=tab*tab_count, child=child, type=keys_value[child]['_meta']['val_type'], child_tab=tab*(tab_count+1))
                else:
                    child_block += "{tab}{child}:\n{child_tab}$ref: '#/definitions/{child}Object'\n".format(
                        tab=tab*tab_count, child_tab=tab*(tab_count+1), child=child
                    )
        open_file.write(contract_block + child_block + '\n')

def get_nested(d, key):
    keys = key.split('.')
    for k in keys:
        val = d.get(k, None)
        if val is None:
            return None
    return val

def update_or_create_nested(d, u, meta):
    # {'a': {'b': {'c': {'_tier': 4}, 'tier': 3}, '_tier': 2}, '_tier': 1}
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            d[k] = update_or_create_nested(d.get(k, {}), v, meta)
            # d[k]['_tier'] = tier
        if v == {}:
            d[k] = {'_meta': meta}
            # d[k]['_tier'] = tier
    return d

def create_nested(long_key):
     # {'a': {'b': {'c': {}}}}
    if len(long_key) == 0:
        return {}
    return { long_key[0].lower(): create_nested(long_key[1:]) }

def write_payload_hierarchy(payload_map):
    with open('payload_map.json', 'w') as open_file:
        open_file.write(str(payload_map))

def change_facilities(pp_map):
    o = {}
    for k, v in pp_map.items():
        if (
            'facilities' in [e.lower() for e in v['long_key'].split('.')] or
            'facilities' in [e.lower() for e in k.split('.')]
        ):
            ke = []
            for e in k.split('.'):
                if e.lower() == 'hotelcontent':
                    e = 'hotelInfo'
                if e.lower() == 'facilities':
                    continue
                if e.lower() == 'hotelfacilities':
                    e = 'facilities'
                if e.lower() == 'value':
                    continue
                ke.append(e)
            v['long_key'] = '.'.join(ke)
        o[k] = v
    with open('NEW_facilities_map.json', 'w') as open_file:
        open_file.write(str(o))
    return o

if __name__ == '__main__':
    updated_freq_map = read_csv_values()
    # import pdb; pdb.set_trace()
    updated_freq_map = change_facilities(updated_freq_map)
    new_payload_hierarchy = dict_reduce(updated_freq_map)
    write_payload_hierarchy(new_payload_hierarchy)
    create_contract(new_payload_hierarchy)


