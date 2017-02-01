#!/usr/bin/python3

"""
This program requires numpy and the PIL python3 libraries

It takes a CSV file as an argument and iterates through each item
taking pictures saving an image with the name given
"""

import sys
import os
from subprocess import Popen, PIPE, STDOUT


def take_picture(plant_name, date, experiment_name='TR008'):
    cmd = 'gphoto2 --capture-image-and-download --force-overwrite'
    Popen((cmd), shell=True, stdin=PIPE,
          stdout=PIPE, stderr=STDOUT, close_fds=True).wait()

    #naming_convention = '00_VIS_TV_000_0-0-0'

    try:

        # Check if the path where we want to save the image to exists and make
        # it if it doesn't
        if not os.path.exists('images/{0}/{1}/{2}'.format(experiment_name, plant_name, date).replace(' ', '')):
            os.makedirs(
                'images/{0}/{1}/{2}'.format(experiment_name, plant_name, date).replace(' ', ''))

        os.rename('capt0000.nef', 'images/{0}/{1}/{2}/{3}.nef'.format(
            experiment_name, plant_name, date, naming_convention).replace(' ', ''))

        os.rename('capt0000.jpg', 'images/{0}/{1}/{2}/{3}.jpg'.format(
            experiment_name, plant_name, date, naming_convention).replace(' ', ''))

        return True

    except:
        print('There was a problem capturing this image')
        return False


def is_this_your_plant(plant):
    """Returns true if user enters Y"""
    ans = input(
        'The next plant to be imaged is: {0}\nIs this the correct plant? '.format(plant))
    while(ans != 'Y' and ans != 'N' and ans != 'Q'):
        ans = input('Please answer Y/N/Q ')
    if ans == 'Q':
        sys.exit()
    return True if ans == 'Y' else False


def main():
    """
    Main entry point for this program, main comments coming soon
    """
    plant_queue = []
    with open(sys.argv[1]) as f:
        plant_queue = [p.replace('\n', '') for p in f.readlines()]

    print('This is the order of plants to be imaged:\n{0}'.format(
        plant_queue))

    while plant_queue:
        # Check if plant at top of stack is your plant
        if is_this_your_plant(plant_queue[0]):
            # if it is then proceed to image
            if take_picture(plant_queue[0], '2014'):
                # remove plant from queue
                plant_queue.pop(0)
            else:
                continue
        else:
            # if it isn't the right plant then move this plant to the end of the queue
            # and move the named plant to the start i.e. position [0]
            alt_plant = input('What plant is next? ')

            while alt_plant not in plant_queue:
                alt_plant = input(
                    'Sorry {0} is not in the list, try again '.format(alt_plant))

            # move the previous plant to the end of the list
            plant_queue += [plant_queue.pop(0)]

            plant_queue.insert(0, plant_queue.pop(
                plant_queue.index(alt_plant)))

    print('Finished')

if __name__ == "__main__":
    sys.exit(main())
