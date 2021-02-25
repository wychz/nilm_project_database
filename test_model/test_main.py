from test_model.tester import Tester
import running_param

meter_name_list = running_param.meter_name_list
batch_size = running_param.batch_size
model_type = running_param.model_type
input_window_length = running_param.input_window_length
predict_mode = running_param.predict_mode
dataset = running_param.dataset


def test_model():
    if predict_mode == 'single':
        for meter_name in meter_name_list:
            test_directory = 'data_process/' + dataset + '/processed_dataset/1min_csv/' + predict_mode + '/' + meter_name + '_test_.csv'
            saved_model_dir = "saved_models/" + model_type + "_1min/" + predict_mode + "/" + meter_name + "_" + model_type + "_model.h5"
            log_file_dir = "saved_models/" + model_type + "_1min/" + predict_mode + "/" + meter_name + "_" + model_type + ".log"
            tester = Tester(meter_name, batch_size, model_type, predict_mode, meter_name_list, test_directory, saved_model_dir,
                            log_file_dir, input_window_length)
            tester.test_model()

    elif predict_mode == 'multiple' or predict_mode == 'multi_label':
        test_directory = 'data_process/' + dataset + '/processed_dataset/1min_csv/' + predict_mode + '/' + 'all' + '_test_.csv'
        saved_model_dir = "saved_models/" + model_type + "_1min/" + predict_mode + "/" + 'all' + "_" + model_type + "_model.h5"
        log_file_dir = "saved_models/" + model_type + "_1min/" + predict_mode + "/" + 'all' + "_" + model_type + ".log"
        tester = Tester('all', batch_size, model_type, predict_mode, meter_name_list, test_directory, saved_model_dir,
                        log_file_dir, input_window_length)
        tester.test_model()
