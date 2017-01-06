#!/usr/bin/python3

import sys
from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import portable_camera

gui_file = 'GUI/mainwindow.ui'
Ui_MainWindow, QtBaseClass = uic.loadUiType(gui_file)

# Where 0 is the plant name and 1 is the date
plant_save_location = 'images/{0}/{1}'


class PlantCaptureGui(QMainWindow, Ui_MainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.plant_queue = []
        self.btn_take_picture.clicked.connect(self.take_picture)
        self.list_plant_order.currentItemChanged.connect(self.select_plant)

        self.btn_open_csv.clicked.connect(self.select_csv)
        self.btn_load_csv.clicked.connect(self.load_csv)
        self.show()

    def setup_plant_list(self):
        self.list_plant_order.clear()
        for plant in self.plant_queue:
            print(plant)
            item = QListWidgetItem(str(plant))
            self.list_plant_order.addItem(item)

    def select_plant(self):
        self.in_plant_name.setText(self.list_plant_order.currentItem().text())

    def load_csv(self):
        try:
            with open(self.in_csv_file.text()) as f:
                self.plant_queue = [p.replace('\n', '') for p in f.readlines()]
                self.setup_plant_list()
                self.btn_load_csv.setEnabled(False)
        except:
            self.show_dialog(
                "Try making sure that you've selected a valid CSV")

    def select_csv(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Open file', '.', "CSV Files (*.csv)")
        self.in_csv_file.setText(fname)
        self.btn_load_csv.setEnabled(True)

    def take_picture(self):
        try:
            # TODO Fix this arbitrary dates
            if portable_camera.take_picture(self.in_plant_name.text(), '2015-06-14'):
                myPixmap = QPixmap('images/{0}/2015-06-14/{0}.jpg'.format(
                    self.in_plant_name.text()).replace(' ', ''))
                self.lbl_last_capture.setPixmap(myPixmap)
                self.plant_queue.remove(self.in_plant_name.text())
                if self.plant_queue is not None:
                    self.in_plant_name.setText(self.plant_queue[0])
                    self.setup_plant_list()
                else:
                    self.show_dialog("You're out of plants to image")
            else:
                self.show_dialog(
                    "The picture did not take sucessfully, check camera is connected and try again")
        except Exception as e:
            print(e)
            self.show_dialog(
                "Looks like you did something bad with the image naming")

    def show_dialog(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PlantCaptureGui()
    sys.exit(app.exec_())
