import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QTextEdit, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt, pyqtRemoveInputHook
from reader import read_the_csv_files, list_all_files
import csv
from debug_logger import QDbgConsole
from sample_dict import input_dict as sample_input_dict

DEBUG = True

def pdb(*args, **kwargs):
    pyqtRemoveInputHook()
    import pdb
    pdb.set_trace()


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
        if type(val) in [str, int, bool, float]:
            del_keys.append(key)
            val = type(val)
            # output['{key}.{val}'.format(key=key, val=type(val))] = 'value'
            output['{key}'.format(key=key, val=val)] = '__val'
        else:
            output[key] = val

    return output


class App(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.title = 'Predictive Freq Mapper'
        
        self.init_data()
        self.initUI()
 
    def init_data(self):
        self.read_csv_lines()
        self.line_counter = 0
        self.apigee_schema = dict_reduce(sample_input_dict)
        self.frequency_map = {}
        self.left = 10
        self.top = 10
        self.width = 650
        self.height = 600
        self.selected = False
        self.saved_lines = []


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        # Create predicted box
        padding = 20
        size_x = 600
        self.predicted_box = QLineEdit(self)
        self.predicted_box.move(padding, padding)
        self.predicted_box.resize(size_x, 60)
        self.predicted_box.setReadOnly(True)

        # Create input_box
        self.input_box = QLineEdit(self)
        self.input_box.move(
            self.predicted_box.pos().x(),
            self.predicted_box.pos().y() + self.predicted_box.height() + padding*2
        )
        self.input_box.resize(
            self.predicted_box.width(),
            self.predicted_box.height() - padding
        )

        # Create Current box 
        self.current_box = QLineEdit(self)        
        self.current_box.move(
            self.input_box.pos().x(),
            self.input_box.pos().y() + self.input_box.height() + padding*2
        )
        self.current_box.resize(
            size_x,
            self.predicted_box.height()
        )
        self.current_box.setReadOnly(True)

    
        # debugger 
        self.debuggers = []
        self.debugger_box = QDbgConsole(parent=self, debug=DEBUG)
        self.history_box = QDbgConsole(parent=self)

        # label things
        self.set_label_for(self.predicted_box,'Predicted')
        self.set_label_for(self.current_box, 'Current')
        self.set_label_for(self.history_box, 'Past')
        self.set_label_for(self.input_box, 'Line')
        self.set_label_for(self.debugger_box, 'debugger')
    
        self.show()
    

    def set_label_for(self, parent, text='No Text', padding=15):
        label = QLabel(self)
        label.setText(text)
        label.move(
            parent.pos().x(), 
            parent.pos().y() - padding
        )
        label.resize(
            parent.width(),
            20
            )

    @pyqtSlot()
    def keyPressEvent(self, event):
        pyqtRemoveInputHook()

        if event.key() == Qt.Key_Escape:
            self.close()

        if event.key() == Qt.Key_R:
            # self.dbs[0].setText("asf"*10)
            # if(self.line_counter == 0):
            line = self.get_next_line()
            # self.display_box.setText(line[1] or 'null')
            # search_and_suggest()
            # self.possible_db
            self.current_box.setText(line[3] or 'null')
            # self.display_box.setText(lines)
        elif event.key() == Qt.Key_Return:
            self.return_enter_event()

    def return_enter_event(self):
        line = self.get_next_line()
        self.history_box.setText('\n'.join(line))
        line[3] = self.input_box.text()
        self.saved_lines.append(line)
        self.line_postprocessor(line)
        self.debugger_box.setText('\n'.join(line))



    def closeEvent(self, event):
        event.accept()


    def line_unpack(self, line):
        key_hierarchy = line.split('.')
        for key in key_hierarchy:
            self.frequency_map.get(key, None)
            # if temp_cursor:

    def line_postprocessor(self, line):
        our_key = line[3]
        source_key = line[1]

    def get_current_line(self):
        return self.read_csv_data[self.line_counter]

    def get_next_line(self):
        self.get_current_line()
        if self.line_counter < len(self.read_csv_data) - 1:
            line = self.read_csv_data[self.line_counter]
            self.line_counter += 1
            self.debugger_box.setText('\n'.join(line))
            self.line_postprocessor(line)
            return line
        return '--==No Line Read==--'
 
    def read_csv_lines(self):
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
