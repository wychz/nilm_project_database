import configparser

cf = configparser.ConfigParser()
cf.read('config.ini', encoding='utf-8')

username = cf.get('mysql', 'username')
password = cf.get('mysql', 'password')
host = cf.get('mysql', 'host')
port = int(cf.get('mysql', 'port'))
db = cf.get('mysql', 'db')

dataset = cf.get('data_process', 'dataset')

save_path = cf.get('data_process', 'save_path')
main_meter = cf.get('data_process', 'main_meter')

epochs = int(cf.get('train', 'epochs'))
validation_frequency = int(cf.get('train', 'validation_frequency'))
meter_name_list = eval(cf.get('train', 'meter_name_list'))
predict_mode = cf.get('train', 'predict_mode')
model_type = cf.get('train', 'model_type')
batch_size = int(cf.get('train', 'batch_size'))
validation_percent = int(cf.get('train', 'validation_percent'))
test_percent = int(cf.get('train', 'test_percent'))
sample_seconds = int(cf.get('train', 'sample_seconds'))
learning_rate = float(cf.get('train', 'learning_rate'))
is_load_model = cf.getboolean('train', 'is_load_model')

is_plot = cf.getboolean('other', 'plot')
plot_to_file = cf.getboolean('other', 'plot_to_file')

input_window_length = int(cf.get('window', 'common'))
fig_length = cf.getint("other", "fig_length")

experiment_id = cf.get('data', 'experiment_id')

mqtt_host = cf.get('mqtt', 'host')
mqtt_port = cf.getint('mqtt', 'port')
