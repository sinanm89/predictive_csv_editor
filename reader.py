import sys
import csv
from os import walk

_REF = "$ref" 
tab_count = 0
next_tab_count = 0
frequency_map = {}

# def get_properties(tab_count, rest_of_the_lines):
#     def get_referenced_properties():

#     built_object = {}
#     for line in rest_of_the_lines:
#         if (line[:tab_count] == ' ' * tab_count):
#             if does_word_exist(line[:tab_count], _REF):
#                 ref_properties = get_referenced_properties()
#             # elif does_word_exist(line[:tab_count, '')


# def check_case(line, search_word, rest_of_the_lines):
#     tab_found = does_word_exist(line, search_word, True)
#     if not tab_found:
#         return False
#     if search_word == 'definitions':
#         contract_details = {
#             'definitions_tab_number': tab_found
#         }
#     if search_word == 'properties':
#         tab_count = 0
#         for i in line:
#             if i == ' ':
#                 tab_count += 1
#         get_properties(tab_count, rest_of_the_lines)

#     return contract_details

# def parse_contract_to_json(object_name):
#     object_name = 'HotelDetails'
#     path = '/Users/snn/Documents/contract-definitions/enterprise/hotels/profiles.yaml'

#     search_map = {
#         'definitions_found': {},
#         'properties_found': {},
#         'properties_to_check': []
#     }
#     with open(path, newline='') as contract_file:
#         lines_to_read = f.readlines()
#         i = 0
#         while i < len(lines_to_read):
#             check_case(line, 'definitions', rest_of_the_lines[i:])
#             i += 1
            

def does_word_exist(line, search_word, line_number=False):
    if line[0] == ' ':
        return False
    i = 0
    j = 0
    while j < len(search_word):
        if search_word[j] == line[i]:
            j += 1
        i += 1
    if search_word != line[i-j:i-1]:
        return False
    return True if line_number is False else len(line) - i


def breakdown_key(key_list, key_map):
    '''
    Creates a frequency table from the nesting key/val pairs
    '''
    while key_list:
        key = key_list.pop(0)
        if not key_list:
            key_map[key] = key_map.get(key, {})
            return key_map
        key_map[key] = breakdown_key(key_list, key_map.get(key, {}))
    return key_map

def list_all_files(walk_path='.'):
    f = []
    for (dirpath, dirnames, filenames) in walk(walk_path):
        f.extend(filenames)
        break
    return f

def read_the_csv_files():
    list_of_files = list_all_files()
    
    for file in list_of_files:
        if not '.csv' in file:
            continue
        # print('{0}\n{1}\n{2}'.format('-'*90,file,'-'*90)); import pdb; pdb.set_trace()
        with open(file, newline='') as csvfile:
            read_data = csv.reader(csvfile)
            frequency_map = {}
            for row in read_data:
                # print('empty_row')
                if row[1] == '':
                    continue
                # print(row)
                exit = False
                i = 0
                key = row[1]
                val = row[2]
                apigee_key = row[3]
                # (['hotelContent', 'generalPropertyDetails', 'propertySettings', 'timeZone'], {})
                frequency_map = breakdown_key(key.split('.'), frequency_map)
    return frequency_map

def main():
    ee = read_the_csv_files()

if __name__ == '__main__':
    # sys.argv[1]
    main()
    # print(get_files())
