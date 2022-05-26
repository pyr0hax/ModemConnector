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
    SERIALPORT = parser.get('serialconf', 'SERIALPORT')
    BAUDRATE = parser.get('serialconf', 'BAUDRATE')
except Exception as e:
    lognow(e)
    with open('cfg.ini', 'a') as f:
        f.write('''[serialconf]
SERIALPORT = COM2
BAUDRATE = 1200\n''')
        raise e
cmd = "ATS0=2\r"
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
    ser.write(cmd.encode()) # Tells modem to auto-answer after 3 rings
    print('waiting for modem')
    while True:
        response = ser.readline()[6:].decode().strip() # stores response from Modem via Serial Port in a variable
        if BAUDRATE in response:
            ser.write('''Welcome to Pyro BBS.\r
This was written in Python by Jaco van Zyl\r
Please note that this is just a test service\r\n'''.encode())

            
# starts main function
if __name__ == '__main__':
    modemChatter()