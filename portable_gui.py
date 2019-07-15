#!/usr/bin/python3

"""
This is the GUI application that when ran controls the portable_camera application
For more info contact nah31@aber.ac.uk | nathan1hughes@gmail.com
Or read the documentation on the Wiki or the README.md in this directory
"""


"""
             _|\ _/|_,
           ,((\\``-\\\\_
         ,(())      `))\
       ,(()))       ,_ \
      ((())'   |        \
      )))))     >.__     \
      ((('     /    `-. .c|
              /        `-`'

"""



import sys
import os
from subprocess import Popen, PIPE, STDOUT
from datetime import date
from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *


image_save_directory = '/media/ubuntu/usbdata/'
#image_save_directory = '/home/nathan/'

class gphoto2_exception(Exception):
    """Doesn't do anything, just keeps things rolling"""
    pass



def check_camera():
    #check type of camera being used
    cmd = 'gphoto2 --auto-detect'
    proc = Popen((cmd), shell=True, stdin=PIPE,
                 stdout=PIPE, stderr=STDOUT)
    tmp = proc.stdout.read()
    
    if "Coolpix" in tmp.decode():
        cam_type = 'coolpix'
    else:
        cam_type = 'dslr'
    return cam_type


def take_picture(plant_name, date_taken, experiment_name='TR008'):
    """
    Given a plant_name, date and experiment_name (optional)
    Will take the photo and save it accordingly
    """


    if 'coolpix' in check_camera():

        cmd = 'gphoto2 --capture-image-and-download --force-overwrite --filename capt0000.jpg'
        Popen((cmd), shell=True, stdin=PIPE,
              stdout=PIPE, stderr=STDOUT, close_fds=True).wait()
        
    else:
        cmd = 'gphoto2 --capture-image-and-download --force-overwrite'
        Popen((cmd), shell=True, stdin=PIPE,
              stdout=PIPE, stderr=STDOUT, close_fds=True).wait()


    #naming_convention = '00_VIS_TV_000_0-0-0'

    # little fail safe to replace the saving directory to be in the user space
    os.chdir(image_save_directory)

    try:
        # Check if the path where we want to save the image to exists and make
        # it if it doesn't
        if not os.path.exists('images/{0}/{1}/{2}'.
                              format(experiment_name, plant_name, date_taken).replace(' ', '')):
            os.makedirs('images/{0}/{1}/{2}'.
                        format(experiment_name, plant_name, date_taken).replace(' ', ''))

        os.rename(
            'capt0000.jpg', 'images/{0}/{1}/{2}/{1}.jpg'.
            format(experiment_name, plant_name, date_taken).replace(' ', ''))

        return True

    except gphoto2_exception:
        print('There was a problem capturing this image')
        return False


gui_file = 'GUI/mainwindow.ui' # modified per machine

Ui_MainWindow, QtBaseClass = uic.loadUiType(gui_file)

# Where 0 is the plant name and 1 is the date
plant_save_location = 'images/{0}/{1}'

# This generates the date string used in naming
date_str = '{0}-{1}-{2}'.format(date.today().year,
                                date.today().month, date.today().day)


class PlantCaptureGui(QMainWindow, Ui_MainWindow):
    """
    This is the main class which controls the entire GUI
    A command-line tool exists called "portable_camera.py
    But its functionality exists in this file too
    and therfore is independant!
    """

    def __init__(self):
        """
        Here all of the on-screen objects are assigned to this script for control
        anything, widget-wise which is added in the future must be connected up
        here or else it will not be found by any of the following functions
        """
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # These are the lists of plants processed and
        # plants to be processed
        self.plant_queue = []
        self.plants_imaged = []

        # These buttons allow the user to interact with the program
        self.btn_take_picture.clicked.connect(self.take_picture)
        self.btn_open_csv.clicked.connect(self.select_csv)
        self.btn_test_image.clicked.connect(self.take_test_image)
        self.btn_quit.clicked.connect(self.closeEvent)

        # These are the lists which show the plants' names to be used
        self.list_plant_order.currentItemChanged.connect(self.select_plant)
        self.list_plants_done.currentItemChanged.connect(
            self.select_imaged_plant)

        self.btn_skip.clicked.connect(self.skip_image)
        # Calling show must be at the end of this setup if we want everything previous to it to
        # be rendered
        self.show()

    def keyPressEvent(self, e):
        """This now triggers on hitting return/enter to take pictures!!"""
        if e.key() == Qt.Key_Return:
            self.take_picture()

    def skip_image(self):
        """Skips over the currently selected image"""
        try:
            # take note of the index of given to skip
            idx = self.plant_queue.index(self.in_plant_name.text())
            self.plants_imaged.append(self.in_plant_name.text())
            self.plant_queue.remove(self.in_plant_name.text())
            self.setup_plant_list()

            # set the next entry to be that of the previous (if possible)
            self.in_plant_name.setText(self.plant_queue[idx])
            self.list_plant_order.setCurrentRow(idx)
        except:
            self.show_dialog("Couldn't skip this image, maybe you've already?!")

            
            
    
    def take_test_image(self):
        """Takes a test image"""
        self.take_picture(test_image=True)

    def closeEvent(self, event):
        """Exits the program, completely"""
        quit_msg = "Are you sure you want to exit the program?"
        reply = QMessageBox.question(self, 'Message',
                                           quit_msg, QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            # Could perform any additional clean-up here
            # possibly exporting of images if a connection is available
            sys.exit()
        else:
            try:
                event.ignore()
            except AttributeError:
                pass

    def setup_plant_list(self):
        """
        This is ran each time a picture is taken
        here the list of plants imaged and to be imaged
        is rearranged and displayed to the user
        """

        # Clears the current lists
        self.list_plant_order.clear()
        self.list_plants_done.clear()

        # Loop over the contents of both lists and add them back
        # to their display
        for plant in self.plant_queue:
            #print(plant)
            item = QListWidgetItem(str(plant))
            self.list_plant_order.addItem(item)

        for plant in reversed(self.plants_imaged):
            item = QListWidgetItem(str(plant))
            self.list_plants_done.addItem(item)

    def select_plant(self):
        """Makes a selection of a plant, in the not-yet-imaged section"""
        self.in_plant_name.setText(self.list_plant_order.currentItem().text())

    def select_imaged_plant(self):
        """Makes a selection of a plant from the just taken selection"""
        self.in_plant_name.setText(self.list_plants_done.currentItem().text())

        # Takes the plant name and puts in on display
        imgDisplay = QPixmap(
            'images/{0}/{1}/{2}/{1}.jpg'.format(self.in_experimentID.text().replace('\n', ''),
                                                self.list_plants_done.currentItem().text().replace(' ', ''), date_str))
        self.lbl_last_capture.setPixmap(imgDisplay)

    def load_csv(self):
        """Loads a given CSV of names"""
        try:
            with open(self.in_csv_file.text()) as f:
                self.in_experimentID.setText(f.readline().replace(' ', ''))
                self.plant_queue = [p.replace('\n', '') for p in f.readlines()]
                self.setup_plant_list()
                self.in_plant_name.setText(self.plant_queue[0])

        except:
            self.show_dialog(
                "Try making sure that you've selected a valid CSV")

    def select_csv(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Open file', '.', "CSV Files (*.csv)")
        self.in_csv_file.setText(fname)
        self.load_csv()

    def take_picture(self, test_image=False):
        try:
            # Take a note of the plant index
            idx = 0
            try:
                idx = self.plant_queue.index(self.in_plant_name.text())
            except:
                idx = 0
            if take_picture(self.in_plant_name.text() if test_image is False else 'test_image',
                            date_str, experiment_name=self.in_experimentID.text().replace('\n', '')):

                imgDisplay = QPixmap(
                    'images/{0}/{1}/{2}/{1}.jpg'.format(self.in_experimentID.text().replace('\n', ''),
                                                        self.in_plant_name.text().replace(' ', '')
                                                        if test_image is False else 'test_image', date_str))

                self.lbl_last_capture.setPixmap(imgDisplay)
                if test_image:
                    return

                #if self.plant_name.text() not in self.plants_imaged:

                self.plants_imaged.append(self.in_plant_name.text())
                try:
                    self.plant_queue.remove(self.in_plant_name.text())
                except:
                    pass
                if self.plant_queue is not None:
                    self.setup_plant_list()
                    self.list_plant_order.setCurrentRow(idx)
                else:
                    self.show_dialog("You're out of plants to image")
            else:
                self.show_dialog(
                    "The picture did not take sucessfully, check camera is connected and try again")

        except IndexError:
            self.show_dialog(
                "All plants have been processed, no new pictures to be taken!")

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
    # little fail safe to replace the saving directory to be in the user space
    os.chdir(image_save_directory)
    app = QApplication(sys.argv)
    window = PlantCaptureGui()
    sys.exit(app.exec_())
