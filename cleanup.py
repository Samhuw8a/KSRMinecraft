import sqlalchemy
import pandas as pd
from configparser import ConfigParser

file = 'config.ini'
config = ConfigParser(interpolation=None)
config.read(file)

def main()->None:
    print(str(sql("SELECT * FROM registration")))

def sql(sql_statement :str)->pd.read_sql:
    username = str(config['credentials']['user'])
    password = str(config['credentials']['password_db']    )
    server_ip = str(config['db']['server_ip'])
    engine = sqlalchemy.create_engine(
    f"mysql+pymysql://{username}:{password}@{server_ip}/Registration")
    return pd.read_sql(str(sql_statement),
                       con=engine
                       )
if __name__ == "__main__":
    main()
