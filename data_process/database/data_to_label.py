import pandas as pd
import numpy as np
import running_param
import configparser

# 将电器功率数据转换为0,1开关状态
meter_name_list = running_param.meter_name_list
data_dir = 'data_process/database/processed_dataset/1min_csv/multiple/'
save_path = 'data_process/database/processed_dataset/1min_csv/multi_label/'
predict_mode = 'multi_label'

cf = configparser.ConfigParser()
cf.read('temp.conf', encoding='gbk')


def data_process_database_multi_label():
    if predict_mode == 'single_label':
        for meter_name in meter_name_list:
            df_test = pd.read_csv(data_dir + meter_name + "_test_.csv", usecols=[0, -1], names=['aggregate', 'test'], dtype={'time': str})
            df_training = pd.read_csv(data_dir + meter_name + "_training_.csv", usecols=[0, -1], names=['aggregate', 'training'], dtype={'time': str})
            df_validation = pd.read_csv(data_dir + meter_name + "_validation_.csv", usecols=[0, -1], names=['aggregate', 'validation'], dtype={'time': str})

            test_array = np.round(np.array(df_test.iloc[:, -1], float), 6)
            training_array = np.round(np.array(df_training.iloc[:, -1], float), 6)
            validation_array = np.round(np.array(df_validation.iloc[:, -1], float), 6)

            # std = appliance_param[appliance_name]["std"]
            appliance_min = cf.getfloat(meter_name, 'std')
            appliance_max = cf.getfloat(meter_name, 'float')
            on_power_threshold = running_param.on_power_threshold
            test_array = (test_array * (appliance_max - appliance_min)) + appliance_min
            training_array = (training_array * (appliance_max - appliance_min)) + appliance_min
            validation_array = (validation_array * (appliance_max - appliance_min)) + appliance_min

            test_array[test_array < on_power_threshold] = 0
            test_array[test_array > 0] = 1

            training_array[training_array < on_power_threshold] = 0
            training_array[training_array > 0] = 1

            validation_array[validation_array < on_power_threshold] = 0
            validation_array[validation_array > 0] = 1

            df_test.loc[:, 'test'] = test_array
            df_training.loc[:, 'training'] = training_array
            df_validation.loc[:, 'validation'] = validation_array

            df_test.to_csv(save_path + meter_name + '_test_.csv', index=False, header=False)
            df_training.to_csv(save_path + meter_name + '_training_.csv', index=False, header=False)
            df_validation.to_csv(save_path + meter_name + '_validation_.csv', index=False, header=False)

    elif predict_mode == 'multi_label':

        names_list = ['mains', 'centigrade', 'people', 'isworkday']
        for meter_name in meter_name_list:
            names_list.append(meter_name)
        names_array = np.array(names_list)

        df_test_all = pd.read_csv(data_dir + 'all' + "_test_.csv", names=names_array)
        df_training_all = pd.read_csv(data_dir + 'all' + "_training_.csv", names=names_array)
        df_validation_all = pd.read_csv(data_dir + 'all' + "_validation_.csv", names=names_array)

        for i, meter_name in enumerate(meter_name_list):
            test_array = np.round(np.array(df_test_all.iloc[:, i + 4], float), 6)
            training_array = np.round(np.array(df_training_all.iloc[:, i + 4], float), 6)
            validation_array = np.round(np.array(df_validation_all.iloc[:, i + 4], float), 6)

            appliance_min = cf.getfloat(meter_name, 'min')
            appliance_max = cf.getfloat(meter_name, 'max')
            on_power_threshold = running_param.on_power_threshold

            test_array = ((test_array * (appliance_max - appliance_min)) + appliance_min)
            training_array = ((training_array * (appliance_max - appliance_min)) + appliance_min)
            validation_array = ((validation_array * (appliance_max - appliance_min)) + appliance_min)

            test_array[test_array < on_power_threshold] = 0
            test_array[test_array > 0] = 1

            training_array[training_array < on_power_threshold] = 0
            training_array[training_array > 0] = 1

            validation_array[validation_array < on_power_threshold] = 0
            validation_array[validation_array > 0] = 1

            df_test_all.loc[:, meter_name] = test_array
            df_training_all.loc[:, meter_name] = training_array
            df_validation_all.loc[:, meter_name] = validation_array

        df_test_all.to_csv(save_path + 'all' + '_test_.csv', index=False, header=False)
        df_training_all.to_csv(save_path + 'all' + '_training_.csv', index=False, header=False)
        df_validation_all.to_csv(save_path + 'all' + '_validation_.csv', index=False, header=False)