#!/usr/bin/env python3
#coding: utf8
## observe db

from socket import SO_SNDLOWAT
import sqlalchemy
import pandas as pd
import time
from configparser import ConfigParser
import subprocess
import asyncio
import websockets
import threading


file = 'config.ini'
config = ConfigParser(interpolation=None)
config.read(file)

def sql_no_resp(sql_statement :str)->pd.read_sql:
    username = str(config['credentials']['user'])
    password = str(config['credentials']['password_db']    )
    server_ip = str(config['db']['server_ip'])
    engine = sqlalchemy.create_engine(
    f"mysql+pymysql://{username}:{password}@{server_ip}/Registration")
    with engine.connect() as connection:
        result = connection.execute(sqlalchemy.text(sql_statement))

def sql(sql_statement :str)->pd.read_sql:
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
    try:
        if sql('SELECT * FROM registration WHERE reg_done is Null').empty:
            #if debug == True:
                #print("que is empty" + "\n" + "going to sleep")
            que = False
        else:
            #if debug == True:
                #print("df is not empty" +"\n" + "going to work!")
            que = True
    except:
        return "ERROR"

#  def fetch_first():
#      return sql('SELECT * FROM registration LIMIT 1')

class user:
    def __init__(self, username, name, mail, comment, timestamp):
        self.username = username
        self.name = name
        self.mail = mail
        self.comment = comment
        self.timestamp = timestamp
    def __str__(self):
        return f"{self.username}\n{self.mail}\n{self.timestamp}\n"
    
def fetch_first(is_repeat=False)->None:
    global user1
    if is_repeat:
        check_str='SELECT reg_username, reg_mail, reg_name, reg_comment, reg_timestamp FROM registration Where reg_done = 2.0 LIMIT 1'
    else:
        check_str='SELECT reg_username, reg_mail, reg_name, reg_comment, reg_timestamp FROM registration Where reg_done is Null LIMIT 1'
    try:
        username = str(sql(check_str)['reg_username']).strip("0 ").partition('\n')[0]
        mail = str(sql(check_str)['reg_mail']).strip("0 ").partition('\n')[0]
        name =  str(sql(check_str)['reg_name']).strip("0 ").partition('\n')[0]
        comment = str(sql(check_str)['reg_comment']).strip("0 ").partition('\n')[0]
        timestamp = str(sql(check_str)['reg_timestamp']).strip("0 ").partition('\n')[0]
    except:
        return "ERROR"
    mail.strip()
    #name = conv_name(name)
    username.strip()
    try:
        print(name)
    except:
        print("ERROR with charcter in the text:")
        print(mail)
        sql_no_resp(f"UPDATE registration SET reg_done = 2.0 WHERE reg_mail='{mail}'")
    #name = name.lower().replace("??","ae").replace("??","oe").replace("??","ue")
        return "Text_ERROR"
    #for i in name:
        #print(i)

    user1 = user(username, name, mail, comment, timestamp)
    #if debug:
        #print(username,name,mail,comment,timestamp)
        #print("asgf")
    

def main()->None:
    #fetch_first()
    
    res_que=check_que()
    if res_que == "ERROR" :
        print("Error while acssesing the database")
        time.sleep(6)
        return
    if que == True:
        res=fetch_first()

        if debug == True:
            print("start registering...")
            if res == "ERROR" :
                print("Error while acssesing the database")
                time.sleep(6)
                return
            if res == "Text_ERROR":
                time.sleep(6)
                return
            print(user1)
        if str(user1.mail)[-8:] == "@sluz.ch":
            if debug == True:
                print('is sluz')
            p = subprocess.check_output(['python3', 'auth_token.py', str(debug), str(user1.username), str(user1.name), str (user1.mail)])
            p = p.decode('ascii')
            token_state = p.splitlines()[-1]
            if token_state == "token_success":
                r = subprocess.check_output(['python3', 'register.py', str(debug),
                                  str(user1.username), str(user1.name),
                                  str(user1.mail)])
                r = r.decode('ascii')
                #r = p
                registration_state = r.splitlines()[-1]
                print(r)
                print(f"/Whitelist {user1.username}")
                if registration_state == "registration_successful":
                    print("sending success notification")
                    # send_message(...)
                    #set_reg_satus()
                    sql_no_resp(f"UPDATE registration SET reg_done = 1.0 WHERE reg_mail='{user1.mail}'")
                else:
                    print('sending error')                
                    sql_no_resp(f"UPDATE registration SET reg_done = 2.0 WHERE reg_mail='{user1.mail}'")
                    # send_message(...)
                
            elif token_state == "token_failed":
                print("send token error")
                    # Websocket_send(...)

                sql_no_resp(f"UPDATE registration SET reg_done = 2.0 WHERE reg_mail='{user1.mail}'")
                print('startin with clean_up')
		
                
        else:
            if debug == True:
                print('not an sluz mail!')
            sql_no_resp(f"UPDATE registration SET reg_done = 2.0 WHERE reg_mail='{user1.mail}'")
        print("subprocess done!")

    else:
        #if debug == True:
            #print("going to sleep for 5 seconds")
        time.sleep(5)

if __name__ == '__main__':
    debug=False
    while True:
        main()
