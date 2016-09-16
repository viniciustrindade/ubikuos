#!/usr/bin/python

import serial
import time

ser = serial.Serial('/dev/ttyACM1', 9600)
while True:
    ser.write('acende')
    time.sleep(3)
    ser.write('apaga')
    time.sleep(3)
    ser.write('pisca')
    time.sleep(4)
    ser.write('pisca')
    time.sleep(4)
