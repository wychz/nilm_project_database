from data_process.database import single_data_generate, single_data_generate_file
from data_process.database import multiple_data_generate
import running_param
from sqlalchemy import create_engine

# 主程序： 指定参数，进行数据生成
meter_name_list = running_param.meter_name_list
predict_mode = running_param.predict_mode
save_path = running_param.save_path + predict_mode + "/"
main_meter = running_param.main_meter
plot = running_param.is_plot

username = running_param.username
password = running_param.password
host = running_param.host
port = running_param.port
db = running_param.db

engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(username, password, host, port, db))


def database_data_process():
    if predict_mode == 'single':
        single_data_generate.generate(meter_name_list, main_meter, save_path, engine, plot)
    if predict_mode == 'single_file':
        single_data_generate_file.generate(meter_name_list, main_meter, save_path, engine, plot)
    elif predict_mode == 'multiple':
        multiple_data_generate.generate(meter_name_list, main_meter, save_path, engine, plot)
