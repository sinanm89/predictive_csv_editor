from _FIXED_attribute_map import prev_freq_map

with open('test_contract.yaml', 'r') as yaml_file:
    reader = yaml_file.read()
    read_csv_data = reader.split('\n')
    for k,v in prev_freq_map.items():
        if not k.split('.')[-1] in read_csv_data:
            import pdb; pdb.set_trace()
            print(k)
