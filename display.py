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


# class App(QMainWindow):

#     def __init__(self):
#         super().__init__()
#         self.title = 'Predictive Freq Mapper'

#         self.init_data()
#         self.initUI()

#     def init_data(self):
#         self.read_csv_lines()
#         self.line_counter = 0
#         self.apigee_schema = dict_reduce(sample_input_dict)
#         self.frequency_map = {}
#         self.left = 10
#         self.top = 10
#         self.width = 650
#         self.height = 600
#         self.selected = False
#         self.saved_lines = []
#         self._save_confirmation = False
#         self.freq_map = {}

#     def initUI(self):
#         self.setWindowTitle(self.title)
#         self.setGeometry(self.left, self.top, self.width, self.height)

#         # Create predicted box
#         padding = 20
#         size_x = 600
#         self.predicted_box = QLineEdit(self)
#         self.predicted_box.move(padding, padding)
#         self.predicted_box.resize(size_x, 60)
#         # self.predicted_box.setReadOnly(True)

#         # Create input_box
#         self.input_box = QLineEdit(self)
#         self.input_box.move(
#             self.predicted_box.pos().x(),
#             self.predicted_box.pos().y() + self.predicted_box.height() + padding*2
#         )
#         self.input_box.resize(
#             self.predicted_box.width(),
#             self.predicted_box.height() - padding
#         )

#         # debugger
#         self.debuggers = []
#         self.history_box = QDbgConsole(parent=self, debug=DEBUG)
#         self.current_box = QDbgConsole(parent=self)

#         # label things
#         self.set_label_for(self.predicted_box,'Predicted')
#         self.set_label_for(self.history_box, 'Past')
#         self.set_label_for(self.input_box, 'Line')
#         self.set_label_for(self.current_box, 'Current')

#         self.show()


#     def set_label_for(self, parent, text='No Text', padding=15):
#         label = QLabel(self)
#         label.setText(text)
#         label.move(
#             parent.pos().x(),
#             parent.pos().y() - padding
#         )
#         label.resize(
#             parent.width(),
#             20
#             )

#     @pyqtSlot()
#     def keyPressEvent(self, event):
#         self.current_box.setStyleSheet("")
#         if event.key() == Qt.Key_Escape:
#             self.close()
#         if event.key() == Qt.Key_R:
#             line = self.get_next_line()
#             self.current_box.setText('\n'.join(line))
#         elif event.key() == Qt.Key_Return:
#             self.return_enter_event()
#         elif event.key() == Qt.Key_F:
#             self.write_csv_file()
#             self.current_box.setStyleSheet("border: 3px solid green;")



# # 'a.b.c.d' - 'e.b.f'

# # # f = [d]
# # # abc - eb
# # # b != c


# # def dict_enlarge(input_dict):
# #     key_dict = {}

# #     column = column.split('.')
# #     for i in range(len(column)):
# #         if freq_d.get(key, None) is None:

# #         else:
# #             key_dict[key] = dict_enlarge(input_dict[key])

#     def predict_value(self):
#         line = self.get_current_line()
#         keys = line[1].split('.')[:-1]
#         while len(keys) > 0:
#             key = keys.pop(0)
#             val = self.freq_map.get(key, None)
#             if val is not None:
#                 # predicted
#                 break
#         pdb()
#         # No keys left
#         # cant predic
#         # a.b.c.d
#         # a.b.c = d
#         self.freq_map[key] = line[1].split('.')[-1]
#         self.predicted_box.setText(self.freq_map.get(key))
#         print(self.freq_map)
#     # def update_predictions(self, key, pred_val):
#     #     # abcde = fghi
#     #     # comes in as abcd = fgh
#     #     # freq_fgh
#     #     freq_val = self.freq_map.get(key, None)
#     #     if self.freq_val is not None and freq_val:
#     #     # a.b.c.d = e.f
#     #     # a.b.c.d = e.f
#     #     self.freq_map[key] = pred_val

#     def return_enter_event(self):
#         line = self.get_current_line()
#         delta_val = self.input_box.text()
#         # some_val
#         if self._save_confirmation:
#             line[3] = delta_val
#             # line = [l for l in line]
#             self.saved_lines.append(line)
#             self.line_postprocessor(line)
#             line = self.get_next_line()
#             # reset state to false so it doesnt save next time
#             self.set_save_state()
#             self.input_box.setStyleSheet("")
#             self.input_box.setText("")
#             print('saved val: ', str(line[3]))
#         elif delta_val is not line[3] and delta_val is not '':
#             line[3] = delta_val
#             # set state to true so we can save
#             self.set_save_state()
#             self.input_box.setStyleSheet("border: 3px solid red;")
#         self.current_box.setText('\n'.join(line))

#     def set_save_state(self, state=None):
#         if state is None:
#             self._save_confirmation = not self._save_confirmation
#         else:
#             self._save_confirmation = state

#     def closeEvent(self, event):
#         event.accept()


#     def line_unpack(self, line):
#         key_hierarchy = line.split('.')
#         for key in key_hierarchy:
#             self.frequency_map.get(key, None)
#             # if temp_cursor:

#     def line_postprocessor(self, line):
#         our_key = line[3]
#         source_key = line[1]

#     def get_current_line(self):
#         return self.read_csv_data[self.line_counter]

#     def get_next_line(self):
#         self.history_box.setText('\n'.join(self.get_current_line()))
#         self.predict_value()
#         if self.line_counter < len(self.read_csv_data) - 1:
#             self.line_counter += 1
#             line = self.read_csv_data[self.line_counter]
#             return line
#         return '--==No Line Read==--'


#     def read_csv_lines(self):
#         # self.frequency_map = read_the_csv_files()
#         # print(self.frequency_map)
#         list_of_files = list_all_files()
#         print(list_all_files())
#         for file in list_of_files:
#             if not '.csv' in file:
#                 continue
#             with open(file, newline='') as csvfile:
#                 self.read_csv_data = list(csv.reader(csvfile))

#     def write_csv_file(self):
#         with open('___{0}.csv'.format(str(uuid.uuid4())), 'w') as csvfile:
#             writer = csv.writer(csvfile)
#             writer.writerows(self.saved_lines)


if __name__ == '__main__':
    run_filler()
    # app = QApplication(sys.argv)
    # ex = App()
    # sys.exit(app.exec_())


