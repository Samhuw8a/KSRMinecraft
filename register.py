#!/usr/bin/env python3
## register process

import sys
from configparser import ConfigParser
import sqlalchemy
import pandas as pd
from sqlalchemy.sql import text
from mcrcon import MCRcon

debug = sys.argv[1]

reg_username = str(sys.argv[2])
reg_name = sys.argv[3]
reg_mail = str(sys.argv[4])

file = 'config.ini'
config = ConfigParser(interpolation=None)
config.read(file)

if debug == "True":
    debug = True
else:
    debug = False

if debug == True:
    print("register starting")

#  username = str(config['credentials']['user'])
#  password = str(config['credentials']['password'])
#  server_ip = str(config['db']['server_ip'])
mcpassword = str(config['credentials']['mcpassword'])
#  engine = sqlalchemy.create_engine(f"mysql+pymysql://{username}:{password}@{server_ip}/Registration")
#  query = f"INSERT INTO Registration.`user` (email, name, username, comment, `timestamp`) VALUES('{reg_mail}', '{reg_name}', '{reg_username}', NULL, current_timestamp());"

#  with engine.connect() as con:
    #  con.execute(query)
#
#  def sql(sql_statement):
#      username = str(config['credentials']['user'])
#      password = str(config['credentials']['password']    )
#      server_ip = str(config['db']['server_ip'])
#      engine = sqlalchemy.create_engine(
#      f"mysql+pymysql://{username}:{password}@{server_ip}/Registration")
#      return pd.read_sql(str(sql_statement),
#                         con=engine
#                         )
if debug == True:
    print(sql("SELECT * FROM user"))
else:
    pass

with MCRcon("45.154.49.72", mcpassword) as mcr:
    resp = mcr.command(f"/whitelist add [{reg_username}]")

print('registration_successful')


