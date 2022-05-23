#!/usr/bin/python
# -*- coding: utf-8 -*-
import serial
import configparser
from logger import lognow

# import cfg.ini file
# If import fails, creates template config for useage
try:
    parser = configparser.ConfigParser()
    parser.read('cfg.ini')
    SERIALPORT = parser.get('config', 'SERIALPORT')
    BAUDRATE = parser.get('config', 'BAUDRATE')
except Exception as e:
    with open('logs.txt', 'a') as f:
        f.write(lognow() + str(e))
    with open('cfg.ini', 'a') as f:
        f.write('''[config]
SERIALPORT = COM2
BAUDRATE = 1200''')
        raise e

# Opens up serial communication with imported config. Change config if below code fails.
def modemChatter():
    try:
        ser = serial.Serial(SERIALPORT, int(BAUDRATE))
        ser.bytesize = serial.EIGHTBITS
        ser.parity = serial.PARITY_NONE
        ser.stopbits = serial.STOPBITS_ONE
        ser.timeout = None
        ser.xonxoff = False
        ser.rtscts = False
        ser.dsrdtr = False
        ser.writeTimeout = 0
        ser.isOpen()
    except Exception as e:
        lognow(e)
        raise e
    ser.write('ats0=3\r\n'.encode()) # Tells modem to auto-answer after 3 rings
    print('waiting for modem')
    while True:
        response = ser.readline()[6:].decode().strip() # stores response from Modem via Serial Port in a variable
        if BAUDRATE in response:
            ser.write('This is a TEST\r\n'.encode())
            continue

# starts main function
if __name__ == '__main__':
    modemChatter()