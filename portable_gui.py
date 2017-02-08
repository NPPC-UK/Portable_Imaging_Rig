#!/usr/bin/python3

"""
This is the GUI application that when ran controls the portable_camera application
For more info contact nah31@aber.ac.uk | nathan1hughes@gmail.com
Or read the documentation on the Wiki or the README.md in this directory
"""


import sys
from datetime import date
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
        self.plants_imaged = []
        self.btn_take_picture.clicked.connect(self.take_picture)
        self.list_plant_order.currentItemChanged.connect(self.select_plant)
        self.list_plants_done.currentItemChanged.connect(
            self.select_imaged_plant)

        self.btn_open_csv.clicked.connect(self.select_csv)
        self.btn_load_csv.clicked.connect(self.load_csv)
        self.btn_quit.clicked.connect(self.quit_program)
        self.show()

    def quit_program(self):
        sys.exit()

    def setup_plant_list(self):
        self.list_plant_order.clear()
        self.list_plants_done.clear()
        for plant in self.plant_queue:
            print(plant)
            item = QListWidgetItem(str(plant))
            self.list_plant_order.addItem(item)

        for plant in reversed(self.plants_imaged):
            item = QListWidgetItem(str(plant))
            self.list_plants_done.addItem(item)

    def select_plant(self):
        self.in_plant_name.setText(self.list_plant_order.currentItem().text())

    def select_imaged_plant(self):
        self.in_plant_name.setText(self.list_plants_done.currentItem().text())
        date_str = '{0}-{1}-{2}'.format(date.today().year,
                                        date.today().month, date.today().day)
        myPixmap = QPixmap(
            'images/{0}/{1}/{0}.jpg'.format(self.list_plants_done.currentItem().text().replace(' ', ''), date_str))

        self.lbl_last_capture.setPixmap(myPixmap)

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
            date_str = '{0}-{1}-{2}'.format(date.today().year,
                                            date.today().month, date.today().day)

            if portable_camera.take_picture(self.in_plant_name.text(), date_str):
                myPixmap = QPixmap(
                    'images/{0}/{1}/{0}.jpg'.format(self.in_plant_name.text().replace(' ', ''), date_str))
                self.lbl_last_capture.setPixmap(myPixmap)
                self.plants_imaged.append(self.in_plant_name.text())
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
                "Looks like you retook a picture! Old image has been overwritten")

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
