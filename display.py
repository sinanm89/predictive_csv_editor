import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QTextEdit, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt, pyqtRemoveInputHook
from reader import read_the_csv_files, list_all_files
import csv
from debug_logger import QDbgConsole
from sample_dict import input_dict as sample_input_dict
import uuid

from PP_freq_map_backup import prev_freq_map


# USEFUL COMMANDS

# SAVEFILE # with open('05__backup_f.py', 'w') as tf: tf.write('prev_freq_map = {freq_map}'.format(freq_map=str(freq_map)))
# AUTO EDIT # pr[3]='hotelinfo.{0}'.format(pr[1].lstrip('hotelContent.'));print('\n|===> '+pr[3] + '\n>>' + pr[2])

DEBUG = True

def get_old_backups(file_name):
    file_name.split('.')[-1]
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile)
        read_csv_data = list(reader)
    return derive_freq_map(read_csv_data)

def pdb(*args, **kwargs):
    pyqtRemoveInputHook()
    import pdb;pdb.set_trace()

def derive_freq_map(saved_lines):
    derived_freq_map = {}
    for i in saved_lines:
        if i[3] is '' or None:
            print('===CORRUPT LINE #{index}'.format(index=i))
            continue
        # if f_map.get(i[1], None) is None:
        derived_freq_map[i[1]] = i[3]
    return derived_freq_map

def do_tests():
    with open('tests/T____output_test.csv', 'w') as temp_file:
        writer = csv.writer(temp_file)
        writer.writerows(['1','2','3'])
    print('~~~Wrote test file: T____output_test.csv')

    with open("tests/T___freq_map_test.py", 'w') as temp_file:
        temp_file.write('T___prev_freq_map = {freq_map}'.format(freq_map=str({'hello':'world'})))

    print('~~~Wrote test file: freq_map_test.py')

def run_filler():
    file_list = list_all_files('csv_files')
    for file_name in file_list:
        if '.csv' in file_name:
            write_csv_from_freq_map(file_name)
    import pdb; pdb.set_trace()

def write_csv_from_freq_map(file_name):

    with open('csv_files/' + file_name, newline='') as csvfile:
        reader = csv.reader(csvfile)
        read_csv_data = list(reader)

    saved_rows = []
    # try:
    for line in read_csv_data:
        key = line[1]
        val = prev_freq_map.get(key, None)
        if line == ['', '', '', '', '', '', '']:
            print(line)
            continue
        # elif val is None:
            # import pdb; pdb.set_trace()

        line[3] = val
        saved_rows.append(line)

    with open('OUTPUT_{}'.format(file_name), 'w') as temp_file:
        writer = csv.writer(temp_file)
        writer.writerows(saved_rows)

    # except Exception:
        # import pdb; pdb.set_trace()

def run_derivation():

    do_tests()

    freq_map = prev_freq_map
    file_name = sys.argv[1]

    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile)
        read_csv_data = list(reader)

    saved_rows = []

    while len(read_csv_data) > 0:
        pr = read_csv_data.pop(0)
        if pr[1] is '':
            continue
        item = freq_map.get(pr[1], None)
        if item:
            k = pr[1]
            v = pr[3]
            pr[3] = freq_map.get(pr[1], 'MISSING')
            print('~~~Saved {0}\t-\t{1}'.format(pr[1], pr[3]))
            saved_rows.append(pr)
        else:
            print('~~~!OOPS COULDNT FIND!~~~')
            print(pr)
            import pdb;pdb.set_trace()
            freq_map[pr[1]] = pr[3]
            saved_rows.append(pr)

    print('====================={0}'.format('WRITE FILE???'))
    import pdb; pdb.set_trace()
    file_name = file_names[-1]
    try:
        with open('XX_output__{0}.csv'.format(file_name), 'w') as temp_file:
            writer = csv.writer(temp_file)
            writer.writerows(saved_rows)
        print('~~~Wrote: ', 'XX_output__{0}.csv'.format(file_name))

        with open("PP_freq_map__{0}.py".format(file_name), 'w') as temp_file:
            temp_file.write('prev_freq_map = {freq_map}'.format(freq_map=str(freq_map)))
    except Exception:
        print('!!!!!!!!!{0}'.format('WRITE FAILED'))

        import pdb; pdb.set_trace()


    print('~~~Wrote: ', "PP_freq_map__{0}.py".format(file_name))

def dict_reduce(input_dict, top_level=False):
    """Reduce a given dict with random elements into one."""
    output = {}
    if type(input_dict) != dict:
        return input_dict
    old_keys = list(input_dict.keys())
    if len(old_keys) < 1:
        return '{key}.{val}'.format(
            key=list(input_dict.keys())[0], val=input_dict[key]
        )
    del_keys = []
    for key in old_keys:
        val = input_dict[key]
        if val is None:
            val = 'no_value'
        if type(val) == dict:
            val = dict_reduce(val)
        elif type(val) == list:
            val = dict_reduce(val[0])
            key = "list__{0}".format(key)
            output[key] = val
        elif type(val) in [str, int, bool, float]:
            del_keys.append(key)
            val = type(val)
            # output['{key}.{val}'.format(key=key, val=type(val))] = 'value'
            output['{key}'.format(key=key, val=val)] = '__val'
        else:
            pdb()
            output[key] = val

    return output


if __name__ == '__main__':
    run_filler()
    # app = QApplication(sys.argv)
    # ex = App()
    # sys.exit(app.exec_())


