import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QTextEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt
from reader import read_the_csv_files, list_all_files
import csv
from debug_logger import QDbgConsole
from sample_dict import input_dict as sample_input_dict

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
        if type(val) in [str, int, bool]:
            del_keys.append(key)
            val = type(val)
            # output['{key}.{val}'.format(key=key, val=type(val))] = 'value'
            output['{key}'.format(key=key, val=val)] = type(val)
        else:
            output[key] = val

    # for i in del_keys:
    #     if output.get(i):
    #         del output[i]
    return output

def line_unpack(self, line):
    if type(line) == list:
        line = line[1]
    key_hierarchy = line.split('.')
    for key in key_hierarchy:
        cursor = self.frequency_map.get(key, None)
        if cursor


# def run_me():
    # {'brandInfo': {"chainCode.<class 'str'>": 'value'},
    # "Telecommute.<class 'bool'>": 'value', 'list__contact': {
    # "faxNumber.<class 'str'>": 'value', "reservationsPhoneNumber.<class 'str'>": 'value',
    # "reservationsPhoneNumberMessage.<class 'bool'>": 'value',
    # "frontDeskNumber.<class 'str'>": 'value', "email.<class 'str'>": 'value'}}

#     ii = {
#         "brandInfo": {
#             "chainCode": "IC",
#         },
#         "Telecommute": True,
#         "contact": [
#             {
#                 "faxNumber": "1-404-9469001",
#                 "reservationsPhoneNumber": None,
#                 "reservationsPhoneNumberMessage": False,
#                 "frontDeskNumber": "1-404-9469190",
#                 "email": "icbsales@ihg.com"
#             }
#     ]}  
#     ee = dict_reduce(ii, True)
#     print(ee)
#     return 0


class App(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 textbox'
        self.left = 10
        self.top = 10
        self.width = 800
        self.height = 600
        self.selected = False
        self.init_data()
        self.initUI()
        self.saved_lines = []
 
    def init_data(self):
        self.reduced_dict = dict_reduce(sample_input_dict)
        print(self.reduced_dict)


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        # Create textbox
        self.textbox = MappingTextEditor(self)
        self.textbox.move(20, 160)
        self.textbox.resize(280,60)

        # Create textbox
        self.display_box = QTextEdit(self)
        self.display_box.setReadOnly(True)
        self.display_box.move(20, 20)
        self.display_box.resize(580,40)
        
        # Create read and possible boxes
        self.possible_db = QLineEdit(self)
        self.already_there_db = QLineEdit(self)
        self.dbs = [self.possible_db, self.already_there_db]
        
        # set boxes
        size_x = 300
        i = 0
        move_x = 0
        for _dbi in self.dbs:
            move_x = 20 + (size_x*i + 20*i)
            _dbi.setReadOnly(True)
            _dbi.resize(size_x, 60)
            _dbi.move(move_x, 100)
            i += 1
 
        self.set_text_on_boxes()
        self.line_counter = 0
        
        # debugger 
        self.debugger = QDbgConsole(parent=self)

        self.show()
    

    @pyqtSlot()
    def on_click(self):
        textboxValue = self.textbox.text()
        self.get_next_line()
        # QMessageBox.question(self, 'MESAJ', "You typed: " + textboxValue, QMessageBox.Ok, QMessageBox.Ok)
        self.textbox.setText("")

    @pyqtSlot()
    def keyPressEvent(self, event):
        print(event.key())
        if event.key() == Qt.Key_Escape:
            self.close()

        if event.key() == Qt.Key_R:
            # self.dbs[0].setText("asf"*10)
            # if(self.line_counter == 0):
            line = self.get_next_line()
            self.display_box.setText(line[1] or 'null')
            # search_and_suggest()
            # self.possible_db
            self.already_there_db.setText(line[3] or 'null')
            # self.display_box.setText(lines)
        elif event.key() == Qt.Key_Return:
            line = self.get_next_line()
            line[3] = self.textbox.text()
            self.saved_lines.append(line)
            print(line)

            self.reduced_dict
            self.debugger.setText(str(line))
            # print(dir(self.textbox))
        # elif event.key():
            # import pdb; pdb.set_trace()
        # if event.key() == Qt.Key_Tab:
        #     print('hello')
        #     self.textbox.setFocus()

    def closeEvent(self, event):
        event.accept()

    def get_current_line():
        return self.saved_lines[self.line_counter]

    def get_next_line(self):
        if self.line_counter < len(self.read_csv_data) - 1:
            line = self.read_csv_data[self.line_counter]
            self.line_counter += 1
            self.debugger.setText('\n'.join(line))
            return line
        return '--==No Line Read==--'
 
    def set_text_on_boxes(self):
        # self.frequency_map = read_the_csv_files()
        # print(self.frequency_map)
        list_of_files = list_all_files()
        print(list_all_files())
        for file in list_of_files:
            if not '.csv' in file:
                continue
            with open(file, newline='') as csvfile:
                self.read_csv_data = list(csv.reader(csvfile))



if __name__ == '__main__':
    # run_me()
    app = QApplication(sys.argv)

    ex = App()
    sys.exit(app.exec_())
