from data_process.database.common.data_utils import get_appliance_list, get_appliance_name
from train_model.trainer import Trainer
import running_param
from utils.common_utils import get_appliance_count, get_engine

meter_name_list = running_param.meter_name_list
batch_size = running_param.batch_size
model_type = running_param.model_type
predict_mode = running_param.predict_mode
epochs = running_param.epochs
input_window_length = running_param.input_window_length
validation_frequency = running_param.validation_frequency
plot = running_param.is_plot
dataset = running_param.dataset
learning_rate = running_param.learning_rate
is_load_model = running_param.is_load_model
engine = get_engine()



def train_model():
    if predict_mode == 'single':
        for meter_name in meter_name_list:
            appliance_id_list = get_appliance_list(meter_name, engine)
            for appliance_id in appliance_id_list:
                if appliance_id is None or '-' in appliance_id:
                    continue
                appliance_name = get_appliance_name(appliance_id, engine)
                training_directory = 'data_process/' + dataset + '/processed_dataset/1min_csv/' + predict_mode + "/" + appliance_name + '_training_.csv'
                validation_directory = 'data_process/' + dataset + '/processed_dataset/1min_csv/' + predict_mode + "/" + appliance_name + '_validation_.csv'
                save_model_dir = "saved_models/" + model_type + "_1min/" + predict_mode + "/" + appliance_name + "_" + model_type + "_model.h5"
                appliance_count = get_appliance_count()
                trainer = Trainer(appliance_name, batch_size, model_type,
                                  training_directory, validation_directory,
                                  save_model_dir, predict_mode, appliance_count,
                                  epochs=epochs, input_window_length=input_window_length,
                                  validation_frequency=validation_frequency, learning_rate=learning_rate, is_load_model=is_load_model, plot=plot)
                trainer.train_model()

    elif predict_mode == 'multiple' or predict_mode == 'multi_label':
        training_directory = 'data_process/' + dataset + '/processed_dataset/1min_csv/' + predict_mode + "/" + 'all' + '_training_.csv'
        validation_directory = 'data_process/' + dataset + '/processed_dataset/1min_csv/' + predict_mode + "/" + 'all' + '_validation_.csv'
        save_model_dir = "saved_models/" + model_type + "_1min/" + predict_mode + "/" + 'all' + "_" + model_type + "_model.h5"
        appliance_count = get_appliance_count()
        trainer = Trainer('all', batch_size, model_type,
                          training_directory, validation_directory,
                          save_model_dir, predict_mode, appliance_count,
                          epochs=epochs, input_window_length=input_window_length,
                          validation_frequency=validation_frequency,learning_rate=learning_rate, is_load_model=is_load_model, plot=plot)
        trainer.train_model()
