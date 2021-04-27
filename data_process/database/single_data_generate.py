import matplotlib.pyplot as plt
import time
import running_param as param

from data_process.database.common.common_data_process import generate_appliance_common, generate_mains_common
from data_process.database.common.data_utils import single_normalization, get_appliance_list, get_appliance_name


# 训练单个电器 ---- 数据生成
def generate(meter_name_list, main_meter, save_path, engine, plot):
    start_time = time.time()
    validation_percent = param.validation_percent
    sample_seconds = param.sample_seconds
    test_percent = param.test_percent
    is_plot = plot

    for meter_name in meter_name_list:
        appliance_id_list = get_appliance_list(meter_name, engine)
        for appliance_id in appliance_id_list:
            if appliance_id is None or '-' in appliance_id:
                continue
            appliance_name = get_appliance_name(appliance_id, engine)
            print('\n' + meter_name + ': ' + appliance_name)
            mains_df = generate_mains_common(main_meter, sample_seconds, is_plot, engine)
            app_df = generate_appliance(appliance_name, appliance_id, meter_name, sample_seconds, is_plot, engine)
            df_align = generate_mains_appliance(mains_df, app_df, appliance_name, sample_seconds, is_plot)
            df_align = single_normalization(df_align, appliance_name, 'database')
            df_align['isworkday'] = 1           # 数据库数据有问题，后期删除这个

            # test CSV
            test_len = int((len(df_align) / 100) * test_percent)
            test = df_align.tail(test_len)
            test.reset_index(drop=True, inplace=True)
            df_align.drop(df_align.index[-test_len:], inplace=True)
            test.to_csv(save_path + meter_name + '_' + appliance_name + '_test_' + '.csv', index=False, header=False)

            # Validation CSV
            val_len = int((len(df_align) / 100) * validation_percent)
            val = df_align.tail(val_len)
            val.reset_index(drop=True, inplace=True)
            df_align.drop(df_align.index[-val_len:], inplace=True)
            val.to_csv(save_path + meter_name + '_' + appliance_name + '_validation_' + '.csv', index=False, header=False)

            # Training CSV
            df_align.to_csv(save_path + meter_name + '_' + appliance_name + '_training_.csv', index=False, header=False)

            print("    Size of total training set is {:.4f} M rows.".format(len(df_align) / 10 ** 6))
            print("    Size of total validation set is {:.4f} M rows.".format(len(val) / 10 ** 6))
            print("    Size of total test set is {:.4f} M rows.".format(len(test) / 10 ** 6))
            print("\nPlease find files in: " + save_path)
            print("Total elapsed time: {:.2f} min.".format((time.time() - start_time) / 60))
            del df_align, val


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
