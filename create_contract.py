import csv
import collections
from reader import read_the_csv_files, list_all_files
from FINAL_freq_map_backup import prev_freq_map as FREQ_MAP
import json
import uuid
from datetime import datetime

_input_dict = None

DETAIL_MAP = {}

def dict_reduce(input_dict):
    """Reduce a given dict with random elements into one."""
    output = {}
    for key in input_dict.keys():
        # {'value': 'Apigee', 'keys_value': 'value', 'val_type': 'string', 'extras': []}
        #  get the actual key name value
        lookup_val = input_dict[key]['long_key']
        value = lookup_val.split('.')
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
    # attributes = payload_hierarchy_map.keys()
    for att_k, att_v in payload_hierarchy_map.items():
        create_contract_block(att_v, att_k)


def create_contract_block(value_map, key):
    """
        properties:
            sideQuest:
                type: string
                $ref: '#definitions/{REFERENCE_OBJ}'
    """
    if last_item_in_tier(value_map):
        return write_contract_block(value_map, key)
    for k, v in value_map.items():
        if k and k[0] == '_':
            continue
        # write these into the file block now
        create_contract_block(v, k)
        if key == '':
            import pdb; pdb.set_trace()
        write_contract_block(value_map, key)

def last_item_in_tier(value_map):
    return len(value_map.keys()) == 1 and '_meta' in value_map.keys()
    # return len(value_map.keys()) <= 2 and ('_full_key' in value_map.keys() and '_tier' in value_map.keys())

def write_contract_block(keys_value, key):
    contract_block = ''
    tab = '  '
    tab_count = 1

    type_block = '{tab}type: object\n{tab}properties:'.format(tab=tab)
    if key[-1] == 's':
        type_block = "{tab}type: array\n{tab}items:".format(tab=tab)

    tab_count += 1
    _tab_count = tab_count
    timestamp = str(datetime.now().timestamp()).split('.')[0]
    contract_block += '{key}Object:\n{type_block}\n'.format(
        key=key, type_block=type_block
    )
    _detail_block = ''
    with open('generated_contract_{0}.yaml'.format(timestamp), 'a') as open_file:
        if last_item_in_tier(keys_value):
            value_type = keys_value['_meta'].get('val_type', None)
            if value_type is None:
                # print(keys_value)
                value_type = '===UNKNOWN==='
            contract_block += '{tab}type: {type}\n'.format(tab=tab, type=value_type)
        else:
            for child in keys_value.keys():
                child_block = '{tab}{child}:\n'.format(child=child, tab=tab*tab_count)
                # if child[-1] == 's':
                    # if array
                    # _detail_block = '{tab}type: array\n{tab}items:\n'.format(tab=tab)
                    # tab_count += 1
                contract_block += "{child_block}{tab}$ref: '#/definitions/{child}Object'\n".format(
                    tab=(tab+1)*tab_count, child=child, child_block=child_block
                )
                # contract_block += _detail_block
        open_file.write(contract_block + '\n')

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
    return {long_key[0].lower():create_nested(long_key[1:])}


if __name__ == '__main__':
    updated_freq_map = read_csv_values()
    new_payload_hierarchy = dict_reduce(updated_freq_map)
    create_contract(new_payload_hierarchy)


