#!/usr/bin/env python3

import sys
import time
import subprocess
import sqlalchemy
from configparser import ConfigParser
import pandas as pd

## parsing variables from config.ini
file = 'config.ini'
config = ConfigParser(interpolation=None)
config.read(file)

## define sql engine
def sql(sql_statement):
    username = str(config['credentials']['user'])
    password = str(config['credentials']['password_db']    )
    server_ip = str(config['db']['server_ip'])
    engine = sqlalchemy.create_engine(
    f"mysql+pymysql://{username}:{password}@{server_ip}/Registration")
    return pd.read_sql(str(sql_statement),
                       con=engine
                       )
## if variables are defined, import variables
if len(sys.argv) > 1:
    debug = str(sys.argv[1])
    reg_username = str(sys.argv[2])
    reg_name = str(sys.argv[3])
    reg_mail = str(sys.argv[4])
    #  token = str(sys.argv[5])
    if debug == "debug":
        debug = True
else:
    debug = False

## random number generator
from random import randint

## generate token with a random number generator
#mail = "test@mail.com"
token = randint(1000000, 999999999)

## send token and passing in variables needed by the 'send_token.py' process
send = subprocess.Popen(['python3', 'send_token.py', str(debug),
                                  str(reg_username), str(reg_name),
                                  str(reg_mail), str(token)])
## no response is needed. Wait for the process to finish.
send.wait()
if debug == True:
    print(f"sending token: {token} to {reg_name}")


## wait for response (3 tries in 5 minutes)

######### WIP ######################

## How do we receive the user input?
def dummy_pull_token():
        time.sleep(5)
        return token + 1

def query():
    return sql(f'SELECT token FROM registration WHERE reg_mail = \'{reg_mail}\' ')

def pull_token():
    if query().empty:
        time.sleep(5)
        pull_token()
        ## exit strategy
    else:
        return query()

####################################

trial = 0

timeout = time.time() + 5*60 ## time-out after 5 minutes
while True:
    if trial == 4 or time.time() > timeout: ## time-out after 3 trials
        print('timeout or too many trials')
        print('sending tokern_failed.php message')
        print('execute clean_up.py')
        print('token_failed')
        break ## if breaking conditions are met, break loop
    elif pull_token() == token: ## if token is correct, send token_success
        print('sending success message.php')
        print("continue with registration.py")
        print('token_success')
        break
    else: ## try again basically
        print("token incorrect")
        #  kill_query()
        pull_token()
        time.sleep(5)
        if debug == True:
            print(f"trail: {trial}")
        trial = trial + 1
