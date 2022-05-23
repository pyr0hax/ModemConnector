from datetime import datetime

def lognow(errormsg):
    date_time = datetime.now().strftime('%m/%d/%Y - %H:%M:%S - ')
    with open('logs.txt', 'a') as f:
        f.write(date_time + str(errormsg) +'\n')