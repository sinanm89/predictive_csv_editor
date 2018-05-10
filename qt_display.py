

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
        self._save_confirmation = False
        self.freq_map = {}

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create predicted box
        padding = 20
        size_x = 600
        self.predicted_box = QLineEdit(self)
        self.predicted_box.move(padding, padding)
        self.predicted_box.resize(size_x, 60)
        # self.predicted_box.setReadOnly(True)

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

        # debugger
        self.debuggers = []
        self.history_box = QDbgConsole(parent=self, debug=DEBUG)
        self.current_box = QDbgConsole(parent=self)

        # label things
        self.set_label_for(self.predicted_box,'Predicted')
        self.set_label_for(self.history_box, 'Past')
        self.set_label_for(self.input_box, 'Line')
        self.set_label_for(self.current_box, 'Current')

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
        self.current_box.setStyleSheet("")
        if event.key() == Qt.Key_Escape:
            self.close()
        if event.key() == Qt.Key_R:
            line = self.get_next_line()
            self.current_box.setText('\n'.join(line))
        elif event.key() == Qt.Key_Return:
            self.return_enter_event()
        elif event.key() == Qt.Key_F:
            self.write_csv_file()
            self.current_box.setStyleSheet("border: 3px solid green;")



# 'a.b.c.d' - 'e.b.f'

# # f = [d]
# # abc - eb
# # b != c


# def dict_enlarge(input_dict):
#     key_dict = {}

#     column = column.split('.')
#     for i in range(len(column)):
#         if freq_d.get(key, None) is None:

#         else:
#             key_dict[key] = dict_enlarge(input_dict[key])

    def predict_value(self):
        line = self.get_current_line()
        keys = line[1].split('.')[:-1]
        while len(keys) > 0:
            key = keys.pop(0)
            val = self.freq_map.get(key, None)
            if val is not None:
                # predicted
                break
        pdb()
        # No keys left
        # cant predic
        # a.b.c.d
        # a.b.c = d
        self.freq_map[key] = line[1].split('.')[-1]
        self.predicted_box.setText(self.freq_map.get(key))
        print(self.freq_map)
    # def update_predictions(self, key, pred_val):
    #     # abcde = fghi
    #     # comes in as abcd = fgh
    #     # freq_fgh
    #     freq_val = self.freq_map.get(key, None)
    #     if self.freq_val is not None and freq_val:
    #     # a.b.c.d = e.f
    #     # a.b.c.d = e.f
    #     self.freq_map[key] = pred_val

    def return_enter_event(self):
        line = self.get_current_line()
        delta_val = self.input_box.text()
        # some_val
        if self._save_confirmation:
            line[3] = delta_val
            # line = [l for l in line]
            self.saved_lines.append(line)
            self.line_postprocessor(line)
            line = self.get_next_line()
            # reset state to false so it doesnt save next time
            self.set_save_state()
            self.input_box.setStyleSheet("")
            self.input_box.setText("")
            print('saved val: ', str(line[3]))
        elif delta_val is not line[3] and delta_val is not '':
            line[3] = delta_val
            # set state to true so we can save
            self.set_save_state()
            self.input_box.setStyleSheet("border: 3px solid red;")
        self.current_box.setText('\n'.join(line))

    def set_save_state(self, state=None):
        if state is None:
            self._save_confirmation = not self._save_confirmation
        else:
            self._save_confirmation = state

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
        self.history_box.setText('\n'.join(self.get_current_line()))
        self.predict_value()
        if self.line_counter < len(self.read_csv_data) - 1:
            self.line_counter += 1
            line = self.read_csv_data[self.line_counter]
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

    def write_csv_file(self):
        with open('___{0}.csv'.format(str(uuid.uuid4())), 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(self.saved_lines)
