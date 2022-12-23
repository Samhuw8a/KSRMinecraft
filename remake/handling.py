from   configparser import ConfigParser
from   mcrcon import MCRcon
import sqlalchemy
import pandas as pd
import time
import random

class User():
    def __init__(self,mail:str,username:str,name:str) -> None:
        self.mail:str     = mail 
        self.username:str = username
        self.name:str     = name

    def __repr__(self) -> str:
        return f"User({self.mail},{self.username},{self.name})"

class Parser():
    def __init__(self) -> None:
        pass

    def load_config(self,path:str)->dict:
        config=ConfigParser(interpolation=None)
        config.read(path)
        return {
        "db_username"     : str(config['credentials']['user']),
        "db_password"     : str(config['credentials']['password_db']),
        "db_server_ip"    : str(config['db']['server_ip']),
        "db_database"     : str(config['db']['db']),
        "db_table"        : str(config['db']['table']),
        "mail_password"   : str(config['credentials']['password_web']),
        "mcrcon_password" : str(config['credentials']['mcpassword']),
        }

    def get_user(self, dbframe:pd.DataFrame)->User:
        mail     = str(dbframe["reg_mail"])    .strip("0 ").partition('\n')[0]
        username = str(dbframe["reg_username"]).strip("0 ").partition('\n')[0]
        name     = str(dbframe["reg_name"])    .strip("0 ").partition('\n')[0]
        return User(mail,username,name)

class Handler():

    def __init__(self,db_username:str,db_pswrd:str,db_server_ip:str, mc_pswrd:str) -> None:
        self.db_username:str = db_username
        self.db_password:str = db_pswrd
        self.db_ip:str       = db_server_ip
        self.mc_password:str = mc_pswrd

    def sql_call(self,cmd:str)->pd.DataFrame:
        engine = sqlalchemy.create_engine(
            f"mysql+pymysql://{self.db_username}:{self.db_password}@{self.db_ip}/Registration")
        return pd.read_sql(str(cmd),
                           con=engine
                          )
    def mcrcon_call(self,cmd:str)->str:
        pass

def main()->None:
    p = Parser()
    conf = p.load_config("config.ini")
    h = Handler(conf["db_username"],conf["db_password"],conf["db_server_ip"],conf["mcrcon_password"])
    rs=h.sql_call("SELECT * FROM registration")
    print(str(rs))
    u = p.get_user(rs)
    print(u)

if __name__ == "__main__":
    main()
