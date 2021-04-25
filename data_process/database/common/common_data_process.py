import pandas as pd
import matplotlib.pyplot as plt
from data_process.database.common.data_utils import data_read_database, get_appliance_name


# 生成总功率数据
def generate_mains_common(meter, sample_seconds, plot, engine):
    meter_table_name = 'meter_{}_source'.format(meter)
    sql_query = "select timestamp, KW, centigrade, people, isworkday from {}".format(meter_table_name)
    mains_df = data_read_database(engine, sql_query)
    mains_df.rename(columns={"KW": 'aggregate', "timestamp": "time"}, inplace=True)
    mains_df['time'] = mains_df['time'].astype('str')
    mains_df['aggregate'] = mains_df['aggregate'].astype('float64')
    mains_df['aggregate'] = mains_df['aggregate'] * 1000
    mains_df['time'] = pd.to_datetime(mains_df['time'], unit='ms')
    mains_df.set_index('time', inplace=True)

    mains_df = mains_df.resample(str(sample_seconds) + 'S').fillna(method='backfill', limit=1)
    mains_df.reset_index(inplace=True)

    if plot:
        print("    mains_df:")
        print(mains_df.head())
        plt.plot(mains_df['time'], mains_df['aggregate'])
        plt.show()
    return mains_df


def generate_appliance_common(appliance_name, appliance_id, meter, sample_seconds, engine):
    meter_table_name = 'meter_{}_source'.format(meter)
    sql_query = "select timestamp, KW from {} where model = '{}' or instr(model, '{}') = 1".format(meter_table_name, appliance_id, appliance_id)
    app_df = data_read_database(engine, sql_query)
    app_df.rename(columns={"KW": appliance_name, "timestamp": "time"}, inplace=True)
    app_df['time'] = app_df['time'].astype('str')
    app_df[appliance_name] = app_df[appliance_name].astype('float64')
    app_df[appliance_name] = app_df[appliance_name] * 1000
    app_df['time'] = pd.to_datetime(app_df['time'], unit='ms')
    app_df.set_index('time', inplace=True)
    app_df = app_df.resample(str(sample_seconds) + 'S').fillna(method='backfill', limit=1)
    app_df.reset_index(inplace=True)

    return app_df

