from data_process.database.common.data_utils import get_appliance_list, get_appliance_name
from test_model.tester import Tester
import running_param
from utils.common_utils import get_appliance_count, get_engine

meter_name_list = running_param.meter_name_list
batch_size = running_param.batch_size
model_type = running_param.model_type
input_window_length = running_param.input_window_length
predict_mode = running_param.predict_mode
plot_to_file = running_param.plot_to_file
dataset = running_param.dataset
engine = get_engine()


def test_model():
    if predict_mode == 'single':
        for meter_name in meter_name_list:
            appliance_id_list = get_appliance_list(meter_name, engine)
            for appliance_id in appliance_id_list:
                if appliance_id is None or '-' in appliance_id:
                    continue
                appliance_name = get_appliance_name(appliance_id, engine)
                test_directory = 'data_process/' + dataset + '/processed_dataset/1min_csv/' + predict_mode + '/' + appliance_name + '_test_.csv'
                saved_model_dir = "saved_models/" + model_type + "_1min/" + predict_mode + "/" + appliance_name + "_" + model_type + "_model.h5"
                log_file_dir = "saved_models/" + model_type + "_1min/" + predict_mode + "/" + appliance_name + "_" + model_type + ".log"
                appliance_count = get_appliance_count()
                tester = Tester(appliance_name, batch_size, model_type, predict_mode, meter_name_list, test_directory, saved_model_dir,
                                log_file_dir, input_window_length, appliance_count, plot_to_file)
                tester.test_model()

    elif predict_mode == 'multiple' or predict_mode == 'multi_label':
        test_directory = 'data_process/' + dataset + '/processed_dataset/1min_csv/' + predict_mode + '/' + 'all' + '_test_.csv'
        saved_model_dir = "saved_models/" + model_type + "_1min/" + predict_mode + "/" + 'all' + "_" + model_type + "_model.h5"
        log_file_dir = "saved_models/" + model_type + "_1min/" + predict_mode + "/" + 'all' + "_" + model_type + ".log"
        appliance_count = get_appliance_count()
        tester = Tester('all', batch_size, model_type, predict_mode, meter_name_list, test_directory, saved_model_dir,
                        log_file_dir, input_window_length, appliance_count, plot_to_file)
        tester.test_model()
