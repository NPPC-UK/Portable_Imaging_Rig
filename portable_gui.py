import sys
from PyQt4 import QtGui, uic
from PyQt4.QtCore import Qt
import portable_camera

gui_file = 'GUI/mainwindow.ui'

Ui_MainWindow, QtBaseClass = uic.loadUiType(gui_file)

plant_queue = []
with open('example.csv') as f:
    plant_queue = [p.replace('\n', '') for p in f.readlines()]


class PlantCaptureGui(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # start the custom stuff here
        self.btn_take_picture.clicked.connect(self.take_picture)
        self.setup_plant_list()
        self.list_plant_order.currentItemChanged.connect(self.select_plant)
        self.show()

    def setup_plant_list(self):
        for plant in plant_queue:
            item = QtGui.QListWidgetItem(str(plant))
            self.list_plant_order.addItem(item)

    def select_plant(self):
        self.in_plant_name.setText(self.list_plant_order.currentItem().text())

    def take_picture(self):
        portable_camera.take_picture('test1')
        myPixmap = QtGui.QPixmap('test1.jpg')
        self.lbl_last_capture.setPixmap(myPixmap)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = PlantCaptureGui()
    sys.exit(app.exec_())
