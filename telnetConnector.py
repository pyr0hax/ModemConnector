import getpass
import telnetlib
import configparser
from logger import lognow

try:
    parser = configparser.ConfigParser()
    parser.read('cfg.ini')
    HOST = parser.get('telnetconf', 'HOST')
    PORT = parser.get('telnetconf', 'PORT')
except Exception as e:
    lognow(e)
    with open('cfg.ini', 'a') as f:
        f.write('''\n[telnetconf]
HOST = bbs.vcgsa.co.za
PORT = 23''')
        raise e

def telnetconnector():
    hostname = HOST, PORT
    user = input("Enter your remote account: ")
    password = getpass.getpass()
    tn = telnetlib.Telnet(hostname)
    tn.read_until(b"login: ")
    tn.write(user.encode('ascii') + b"\n")
    if password:
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")
    tn.write(b"ls\n")
    tn.write(b"exit\n")
    print(tn.read_all().decode('ascii'))