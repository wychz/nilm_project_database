import running_param
from sqlalchemy import create_engine

from data_process.database.common.data_utils import get_appliance_list

meter_name_list = running_param.meter_name_list

username = running_param.username
password = running_param.password
host = running_param.host
port = running_param.port
db = running_param.db


def remove_space(string):
    return string.replace(" ", "")


def get_appliance_count():
    engine = get_engine()
    count = 0
    for meter_name in meter_name_list:
        appliance_id_list = get_appliance_list(meter_name, engine)
        for appliance_id in appliance_id_list:
            if appliance_id is None or '-' in appliance_id:
                continue
            count += 1
    return count


def get_engine():
    engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(username, password, host, port, db))
    return engine
