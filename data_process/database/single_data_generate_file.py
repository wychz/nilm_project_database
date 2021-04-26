import matplotlib.pyplot as plt
import time
import running_param as param
import os

from data_process.database.common.common_data_process import generate_appliance_common, generate_mains_common, \
    generate_mains_common_file, generate_appliance_common_file
from data_process.database.common.data_utils import single_normalization, single_normalization_test


# 训练单个电器 ---- 数据生成
def generate(meter_name_list, main_meter, save_path, engine, plot):
    start_time = time.time()
    validation_percent = param.validation_percent
    sample_seconds = param.sample_seconds
    is_plot = plot
    experiment_id = param.experiment_id

    # 产生训练集数据
    file_dir = "./database_files/" + experiment_id + "/train_data/"
    file_list = os.listdir(file_dir)
    mains_file_dir = None
    for cur_file in file_list:
        if cur_file.endswith('总电表.csv'):
            mains_file_dir = file_dir + cur_file
    for cur_file in file_list:
        if not cur_file.endswith('总电表.csv'):
            cur_file_dir = file_dir + cur_file
            appliance_name = cur_file.split('-')[1].split('.')[0]
            meter_name = cur_file.split('-')[0]
            mains_df = generate_mains_common_file(mains_file_dir, sample_seconds, is_plot)
            app_df = generate_appliance_file(cur_file_dir, appliance_name, sample_seconds, is_plot)
            train_df_align = generate_mains_appliance(mains_df, app_df, appliance_name, sample_seconds, is_plot)
            train_df_align = single_normalization(train_df_align, appliance_name, 'file')
            train_df_align['isworkday'] = 1
            # 产生验证集数据
            val_len = int((len(train_df_align) / 100) * validation_percent)
            val = train_df_align.tail(val_len)
            val.reset_index(drop=True, inplace=True)
            train_df_align.drop(train_df_align.index[-val_len:], inplace=True)
            val.to_csv(save_path + meter_name + '_' + appliance_name + '_validation_' + '.csv', index=False,
                       header=False)
            train_df_align.to_csv(save_path + meter_name + '_' + appliance_name + '_training_.csv', index=False, header=False)
            print("    Size of total training set is {:.4f} M rows.".format(len(train_df_align) / 10 ** 6))
            print("    Size of total validation set is {:.4f} M rows.".format(len(val) / 10 ** 6))
            del train_df_align, val

    # 产生测试集数据
    file_dir = "./database_files/" + experiment_id + "/test_data/"
    file_list = os.listdir(file_dir)
    mains_file_dir = None
    for cur_file in file_list:
        if cur_file.endswith('总电表.csv'):
            mains_file_dir = file_dir + cur_file
    for cur_file in file_list:
        if not cur_file.endswith('总电表.csv'):
            cur_file_dir = file_dir + cur_file
            appliance_name = cur_file.split('-')[1].split('.')[0]
            meter_name = cur_file.split('-')[0]
            mains_df = generate_mains_common_file(mains_file_dir, sample_seconds, is_plot)
            app_df = generate_appliance_file(cur_file_dir, appliance_name, sample_seconds, is_plot)
            test_df_align = generate_mains_appliance(mains_df, app_df, appliance_name, sample_seconds, is_plot)
            test_df_align = single_normalization_test(test_df_align, appliance_name)
            test_df_align['isworkday'] = 1
            test_df_align.reset_index(drop=True, inplace=True)
            test_df_align.to_csv(save_path + meter_name + '_' + appliance_name + '_test_' + '.csv', index=False, header=False)
            print("    Size of total test set is {:.4f} M rows.".format(len(test_df_align) / 10 ** 6))
            del test_df_align

    print("\nPlease find files in: " + save_path)
    print("Total elapsed time: {:.2f} min.".format((time.time() - start_time) / 60))


def generate_mains(meter, sample_seconds, plot, engine):
    return generate_mains_common(meter, sample_seconds, plot, engine)


# 生成单一电器数据
def generate_appliance(appliance_name, appliance_id, meter, sample_seconds, plot, engine):
    app_df = generate_appliance_common(appliance_name, appliance_id, meter, sample_seconds, engine)
    if plot:
        print("app_df:")
        print(app_df.head())
        plt.plot(app_df['time'], app_df[appliance_name])
        plt.show()
    return app_df


def generate_appliance_file(cur_file_dir, appliance_name, sample_seconds, plot):
    app_df = generate_appliance_common_file(cur_file_dir, appliance_name, sample_seconds)
    if plot:
        print("app_df:")
        print(app_df.head())
        plt.plot(app_df['time'], app_df[appliance_name])
        plt.show()
    return app_df


# 拼装总功率和单一电器的功率
def generate_mains_appliance(mains_df, app_df, appliance_name, sample_seconds, plot):
    mains_df.set_index('time', inplace=True)
    app_df.set_index('time', inplace=True)
    df_align = mains_df.join(app_df, how='outer').resample(str(sample_seconds) + 'S').fillna(method='backfill', limit=1)
    df_align = df_align.dropna()
    df_align.reset_index(inplace=True)
    df_align['time'] = df_align['time'].astype('str')
    df_align['aggregate'] = df_align['aggregate'].astype('float64')
    df_align[appliance_name] = df_align[appliance_name].astype('float64')
    df_align = df_align[~df_align['isworkday'].isin(['\\N'])]

    if plot:
        print("df_align_time:")
        print(df_align.head())
    del mains_df, app_df, df_align['time']
    if plot:
        print("df_align:")
        print(df_align.head())
        plt.plot(df_align['aggregate'].values)
        plt.plot(df_align[appliance_name].values)
        plt.show()
    return df_align
