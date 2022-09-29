#!/usr/bin/env python3
## observe db

from socket import SO_SNDLOWAT
import sqlalchemy
import pandas as pd
import time
from configparser import ConfigParser
import subprocess


file = 'config.ini'
config = ConfigParser(interpolation=None)
config.read(file)


def sql(sql_statement)->pd.read_sql:
    username = str(config['credentials']['user'])
    password = str(config['credentials']['password_db']    )
    server_ip = str(config['db']['server_ip'])
    engine = sqlalchemy.create_engine(
    f"mysql+pymysql://{username}:{password}@{server_ip}/Registration")
    return pd.read_sql(str(sql_statement),
                       con=engine
                       )

def check_que()->None:
    global que
    if sql('SELECT * FROM registration').empty:
        if debug == True:
            print("que is empty" + "\n" + "going to sleep")
        que = False
    else:
        if debug == True:
            print("df is not empty" +"\n" + "going to work!")
        que = True

#  def fetch_first():
#      return sql('SELECT * FROM registration LIMIT 1')

class user:
  def __init__(self, username, name, mail, comment, timestamp):
    self.username = username
    self.name = name
    self.mail = mail
    self.comment = comment
    self.timestamp = timestamp

def fetch_first()->None:
    global user1
    username = str(sql('SELECT * FROM registration LIMIT 1')['reg_username']).strip("0 ").partition('\n')[0]
    mail = str(sql('SELECT * FROM registration LIMIT 1')['reg_mail']).strip("0 ").partition('\n')[0]
    name =  str(sql('SELECT * FROM registration LIMIT 1')['reg_name']).strip("0 ").partition('\n')[0]
    comment = str(sql('SELECT * FROM registration LIMIT 1')['reg_comment']).strip("0 ").partition('\n')[0]
    timestamp = str(sql('SELECT * FROM registration LIMIT 1')['reg_timestamp']).strip("0 ").partition('\n')[0]

    user1 = user(username, name, mail, comment, timestamp)
    

def main()->None:
    fetch_first()
    
    check_que()
    if que == True:
        if debug == True:
            print("start registering...")
            print(fetch_first())
        if str(user1.mail)[-8:] == "@sluz.ch":
            if debug == True:
                print('is sluz')
            p = subprocess.check_output(['python', 'auth_token.py', str(debug), str(user1.name)])
            p = p.decode('ascii')
            token_state = p.splitlines()[-1]
            if token_state == "token_success":
                r = subprocess.check_output(['python', 'register.py', str(debug),
                                  str(user1.username), str(user1.name),
                                  str(user1.mail)])
                r = p.decode('ascii')
                registration_state = r.splitlines()[-1]
                if registration_state == "registraion_successful":
                    print("sending success notification")
                    # Websocket_send(...)
                else:
                    print('sending error')                
                    # Websocket_send(...)
                
            elif token_state == "token_failed":
                print("send token error")
                    # Websocket_send(...)
                print('startin with clean_up')
                
        else:
            if debug == True:
                print('not an sluz mail!')
        print("subprocess done!")

    else:
        if debug == True:
            print("going to sleep for 5 seconds")
        time.sleep(5)

if __name__ == '__main__':
    debug = True
    main()
