# from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QTextCursor
from io import StringIO
from PyQt5.QtCore import pyqtSlot, Qt

class QDbgConsole(QTextEdit):
    '''
    A simple QTextEdit, with a few pre-set attributes and a file-like
    interface.
    '''
    # Feel free to adjust those
    WIDTH  = 500
    HEIGHT = 140
    PADDING = 20
    hidden = False
    
    def __init__(self, parent=None, w=WIDTH, h=HEIGHT, debug=False):
        super(QDbgConsole, self).__init__(parent)
        
        self._buffer = StringIO()

        self.resize(w, h)
        if debug:
            self.move(20, parent.height - h*2 + self.PADDING)
        else:
            self.move(20, parent.height - h*3 + self.PADDING)
        self.setReadOnly(True)

    ### File-like interface ###
    ###########################

    def write(self, msg):
        '''Add msg to the console's output, on a new line.'''
        self.insertPlainText(msg)
        # Autoscroll
        self.moveCursor(QTextCursor.End)
        self._buffer.write(msg)

    # Most of the file API is provided by the contained StringIO 
    # buffer.
    # You can redefine any of those methods here if needed.

    def toggle_view(self):
        self.hidden = not self.hidden
        if self.hidden:
            self.height = self.height*10
        else:
            self.height = self.height/10

    @pyqtSlot()
    def on_click():
        self.toggle_view()

    def __getattr__(self, attr):
        '''
        Fall back to the buffer object if an attribute can't be found.
        '''
        return getattr(self._buffer, attr)
