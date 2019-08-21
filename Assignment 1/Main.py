#!/usr/bin/env python3

from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.button import Button
from time import sleep
from ev3dev2.motor import LargeMotor
from ev3dev2.motor import SpeedDPS, SpeedRPM, SpeedRPS, SpeedDPM
from ev3dev2.sound import Sound
import time
from ev3dev2.sensor.lego import UltrasonicSensor

tank_pair = MoveTank(OUTPUT_B, OUTPUT_C)

# Connect an EV3 color sensor to any sensor port.
drive = MoveTank(OUTPUT_B , OUTPUT_C)
cl = ColorSensor()
ts=TouchSensor()
sound = Sound()
us = UltrasonicSensor()


#Global colour intensities
BLACK = 25
WHITE = BLACK + 25
speed = 15


def is_black():
    return cl.reflected_light_intensity <= BLACK

def is_white():
    return cl.reflected_light_intensity >= WHITE

def is_gray():
    return BLACK < cl.reflected_light_intensity < WHITE


#Move off tile onto track of small track
def move_onto_track():
    tank_pair.on(left_speed=speed*2.5, right_speed=speed*2.5)
    while not(is_gray()):
        time.sleep(0.05)
    while is_gray():
        time.sleep(0.05)
    time.sleep(10/speed)
    tank_pair.on_for_rotations(left_speed=speed, right_speed=-speed, rotations = 0.5)
    sound.beep()


def recolor():
    if cl.reflected_light_intensity<50:
        BLACK=cl.reflected_light_intensity+5
        WHITE = BLACK + 25


def part1():

    black_tiles = 0

    state = True
    on_track = True
    tank_pair.on(left_speed=speed, right_speed=speed)
    dir_right = True
    while black_tiles < 14:
        if is_gray() and on_track:
            #move forward a bit- because you might be on a seam, then try again.
            tank_pair.on_for_rotations(left_speed=speed, right_speed=speed, rotations=0.2)
            if is_gray():
                dir_right = True #assume you need to turn right, then update it later
                #turn right and see if the tile is there
                tank_pair.on_for_rotations(left_speed=speed, right_speed=-speed,rotations=0.4)
                if is_gray():# if the tile isn't there
                    dir_right = False#update what direction you turned
                    #overturn the other way
                    tank_pair.on_for_rotations(left_speed=-speed, right_speed=speed, rotations=0.8)

                if not(is_gray()):
                    #path found, move back on
                    tank_pair.on_for_rotations(left_speed=speed, right_speed=speed, rotations=0.3)

                #once on path, correct for the way you turned previosly, and then some
                if dir_right:
                    tank_pair.on_for_rotations(left_speed=-speed, right_speed=speed, rotations=0.38)
                else:
                    tank_pair.on_for_rotations(left_speed=speed, right_speed=-speed, rotations=0.38)

                tank_pair.on_for_rotations(left_speed=-speed, right_speed=-speed, rotations=0.25)
                on_track=False

        if is_black() and not(state):#black
            black_tiles+=1
            sound.beep()
            state=True
            on_track = True

        if is_white() and state:#white
            state=False
            on_track = True

        tank_pair.on(left_speed=speed, right_speed=speed)


def sweep():

    # turn left quater turn and begin to sweep for tower
    tank_pair.on_for_rotations(left_speed=-speed * 2, right_speed=speed * 2, rotations=0.5)

    sound.beep()
    tank_pair.on(left_speed=10, right_speed=-10)
    # 180 deg sweep to the right if it detects tower stop
    while us.distance_centimeters > 150:
        time.sleep(0.1)

    # Need to slightly over correct as the sonar picks up the edge of the tower
    time.sleep(0.2)
    tank_pair.off()
    time.sleep(0.5)
    # Drive foreward should be on course to the tower
    tank_pair.on_for_rotations(left_speed=15, right_speed=15, rotations=3.2)

def back_up():
    tank_pair.on_for_rotations(left_speed=-15, right_speed=-15, rotations=0.5)

def part2():
    #set to use CM
    us.mode = 'US-DIST-CM'

    #Turns 90 deg right
    tank_pair.on_for_rotations(left_speed=speed*2.5, right_speed=-speed*2.5, rotations=0.5)

    #Blindly drive 2/3 way to the tower
    tank_pair.on_for_rotations(left_speed=speed*2, right_speed=speed*2, rotations=9)

    #Two sweeps to ensure more accurate heading
    sweep()

    sweep()

    #If contact is made with the tower increase motor speed to ensure pushes off finishing tile

    #tank_pair.on_for_rotations(left_speed=100, right_speed=100, rotations=4)

    #go slow
    for i in range(2):
        back_up()
        tank_pair.on_for_rotations(left_speed=15, right_speed=15, rotations=3)
        back_up()
        tank_pair.on_for_rotations(left_speed=75, right_speed=75, rotations=3)

    #Make sound to signify tower has been pushed off tile
    sound.beep()


#Main calls
move_onto_track()
#recolor()
part1()
part2()
