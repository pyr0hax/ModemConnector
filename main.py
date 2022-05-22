#!/usr/bin/python
# -*- coding: utf-8 -*-
import serial
import configparser
from datetime import datetime

date_time = datetime.now().strftime('%m/%d/%Y - %H:%M:%S')

try:
    parser = configparser.ConfigParser()
    parser.read('cfg.ini')
    SERIALPORT = parser.get('config', 'SERIALPORT')
    BAUDRATE = parser.get('config', 'BAUDRATE')
except Exception, e:

    with open('logs.txt', 'a') as f:
        f.write(date_time + ' - Config file does not exist: ' + str(e))
    with open('cfg.ini', 'a') as f:
        f.write('''[config]
SERIALPORT = COM2
BAUDRATE = 1200''')
        raise e

ser = serial.Serial(SERIALPORT, int(BAUDRATE))
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.timeout = None
ser.xonxoff = False
ser.rtscts = False
ser.dsrdtr = False
ser.writeTimeout = 0

try:
    ser.isOpen()
except Exception, e:
    print 'Exception: Opening serial port: ' + str(e)
while True:
    print 'waiting for modem'
    ser.write('ats0=1\r\n'.encode('ascii'))
    response = ser.readline().decode('ascii')
    if response == 'RING':
        ser.write('OK\r\n'.encode('ascii'))
