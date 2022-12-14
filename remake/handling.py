from   configparser import ConfigParser
from   mcrcon import MCRcon
import sqlalchemy
import pandas as pd
from errors import Error
import time

class User():
    def __init__(self,mail:str,username:str,name:str) -> None:
        self.mail:str     = mail 
        self.username:str = username
        self.name:str     = name
        self.token:int     = 0

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

    def mc_call(self,resp:str)->bool:
        # TODO: response als registriet oder falscher username identifizieren.
        return True

class Handler():

    def __init__(self,db_username:str,db_pswrd:str,db_server_ip:str, mc_pswrd:str) -> None:
        self.db_username:str = db_username
        self.db_password:str = db_pswrd
        self.db_ip:str       = db_server_ip
        self.mc_password:str = mc_pswrd
        self.token_limit:int = 3
        self.timeout:int     = 5*60

    def sql_call(self,cmd:str)->pd.DataFrame:
        engine = sqlalchemy.create_engine(
            f"mysql+pymysql://{self.db_username}:{self.db_password}@{self.db_ip}/Registration")
        return pd.read_sql(str(cmd),
                           con=engine
                          )
    def sql_update(self,cmd:str)->pd.DataFrame:
        engine = sqlalchemy.create_engine(
            f"mysql+pymysql://{self.db_username}:{self.db_password}@{self.db_ip}/Registration")
        with engine.connect() as connection:
            connection.execute(sqlalchemy.text(cmd))

    def await_token(self,user:User)->bool:
        timeout_limit = time.time() + self.timeout
        counter       = 0
        ret           = 0

        while counter <=self.token_limit or time.time()>=timeout_limit:
            sql = self.sql_call(f"SELECT token FROM registration WHERE reg_mail = '{user.mail}'")
            if sql.empty:
                raise Error("Es gibt kein user")
            token = sql.split()[-1]

            if token != "None":
                counter +=1
                try: ret = int(token)
                except ValueError: raise Error(f"kein korrekter Token syntax: {token}")
            if ret == user.token:
                return True

            time.sleep(5)

        return False

    def mcrcon_call(self,cmd:str)->str:
        with MCRcon("45.154.49.72", self.mc_password) as mcr:
            resp = mcr.command(cmd)
        return resp

def main()->None:
    p = Parser()
    conf = p.load_config("config.ini")
    h = Handler(conf["db_username"],conf["db_password"],conf["db_server_ip"],conf["mcrcon_password"])
    u = User("samuel.huwiler@gmx.ch","test","samuel")
    u.token= 111_111
    print(h.await_token(u))

if __name__ == "__main__":
    main()
