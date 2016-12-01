import sys
from PyQt4 import QtGui, uic
from PyQt4.QtCore import Qt
import portable_camera

gui_file = 'GUI/mainwindow.ui'

Ui_MainWindow, QtBaseClass = uic.loadUiType(gui_file)


class MyWindow(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.btn_take_picture.clicked.connect(self.take_picture)
        self.show()

    def take_picture(self):
        portable_camera.take_picture('test1')
        myPixmap = QtGui.QPixmap('test1.jpg')
        self.lbl_last_capture.setPixmap(myPixmap)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
