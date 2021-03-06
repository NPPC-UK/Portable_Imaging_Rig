#!/bin/bash

# edit the desktop file first
file_to_edit="$(pwd)/portable_camera.desktop"
sed -i -e "s@{executable}@python3 $(pwd)/portable_gui.py@g" $file_to_edit
sed -i -e "s@{icon}@$(pwd)/icon/camera.png@g" $file_to_edit

# edit the python script to state the working directory to find the UI file
gui_location="$(pwd)/GUI/mainwindow.ui"
python_script_to_edit="$(pwd)/portable_gui.py"

sed -i -e "s@gui_file = 'GUI/mainwindow.ui'@gui_file = '$gui_location'@g" $python_script_to_edit

# move the desktop file to the user share
mkdir ~/.local/share/applications/
cp portable_camera.desktop ~/.local/share/applications/
chmod +x ~/.local/share/applications/portable_camera.desktop
