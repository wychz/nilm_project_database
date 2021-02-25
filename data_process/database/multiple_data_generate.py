import matplotlib.pyplot as plt
import time
from data_process.database.common.data_utils import multi_normalization
from data_process.database.common.common_data_process import generate_mains_common, generate_appliance_common
import running_param as param


# 同时训练多个电器 ---- 数据生成
def generate(appliance_name_list, main_meter, save_path, engine):
    start_time = time.time()
    validation_percent = param.validation_percent
    sample_seconds = param.sample_seconds
    test_percent = param.test_percent
    debug = True

    mains_df = generate_mains_common(main_meter, sample_seconds, debug, engine)
    app_df = generate_appliance(appliance_name_list, sample_seconds, debug, engine)
    df_align = generate_mains_appliance(mains_df, app_df, appliance_name_list, sample_seconds, debug)
    multi_normalization(df_align, appliance_name_list)

    # test CSV
    test_len = int((len(df_align) / 100) * test_percent)
    test = df_align.tail(test_len)
    test.reset_index(drop=True, inplace=True)
    df_align.drop(df_align.index[-test_len:], inplace=True)
    test.to_csv(save_path + 'all' + '_test_' + '.csv', index=False, header=False)

    # Validation CSV
    val_len = int((len(df_align) / 100) * validation_percent)
    val = df_align.tail(val_len)
    val.reset_index(drop=True, inplace=True)
    df_align.drop(df_align.index[-val_len:], inplace=True)
    val.to_csv(save_path + 'all' + '_validation_' + '.csv', index=False, header=False)

    df_align.to_csv(save_path + 'all' + '_training_.csv', index=False, header=False)

    print("    Size of total training set is {:.4f} M rows.".format(len(df_align) / 10 ** 6))
    print("    Size of total validation set is {:.4f} M rows.".format(len(val) / 10 ** 6))
    print("    Size of total test set is {:.4f} M rows.".format(len(test) / 10 ** 6))
    print("\nPlease find files in: " + save_path)
    print("Total elapsed time: {:.2f} min.".format((time.time() - start_time) / 60))
    del df_align, val


def generate_appliance(appliance_name_list, sample_seconds, debug, engine):
    app_df_list = []
    for i in range(len(appliance_name_list)):
        meter = appliance_name_list[i]
        app_df = generate_appliance_common(meter, sample_seconds, engine)
        app_df_list.append(app_df)
        app_df_list[i].set_index('time', inplace=True)

    app_df = app_df_list[0]
    for i in range(1, len(app_df_list)):
        app_df = app_df.join(app_df_list[i])
    del app_df_list
    app_df.reset_index(inplace=True)
    app_df.set_index('time', inplace=True)
    app_df = app_df.resample(str(sample_seconds) + 'S').fillna(method='backfill', limit=1)
    app_df.reset_index(inplace=True)
    if debug:
        print("app_df:")
        print(app_df.head())
        for meter in appliance_name_list:
            plt.plot(app_df['time'], app_df[meter])
        plt.show()
    return app_df


def generate_mains_appliance(mains_df, app_df, appliance_name_list, sample_seconds, debug):
    mains_df.set_index('time', inplace=True)
    app_df.set_index('time', inplace=True)
    df_align = mains_df.join(app_df, how='outer').resample(str(sample_seconds) + 'S').fillna(method='backfill', limit=1)
    df_align = df_align.dropna()
    df_align.reset_index(inplace=True)
    df_align['time'] = df_align['time'].astype('str')
    df_align['aggregate'] = df_align['aggregate'].astype('float64')
    for appliance_name in appliance_name_list:
        df_align[appliance_name] = df_align[appliance_name].astype('float64')
    if debug:
        print("df_align_time:")
        print(df_align.head())
    del mains_df, app_df, df_align['time']
    if debug:
        print("df_align:")
        print(df_align.head())
        for appliance_name in appliance_name_list:
            plt.plot(df_align[appliance_name].values)
        plt.show()
    return df_align

