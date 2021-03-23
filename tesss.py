from sqlalchemy import create_engine
import running_param
from data_process.database.common.data_utils import data_read_database

username = running_param.username
password = running_param.password
host = running_param.host
port = running_param.port
db = running_param.db

engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(username, password, host, port, db))
sql_test = "select timestamp, KW from meter_160327039_source where meter_160327039_source.model = '{}';".format()
app_df = data_read_database(engine, sql_test)
print('s')

