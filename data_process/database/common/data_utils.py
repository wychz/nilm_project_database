import pandas as pd
from sklearn.preprocessing import MinMaxScaler, LabelBinarizer
import numpy as np
import configparser

cf = configparser.ConfigParser()


def data_read_database(engine, sql_query):
    df_read = pd.read_sql_query(sql_query, engine)
    return df_read


def data_read_csv(csv_path):
    df_read = pd.read_csv(csv_path, names=["timestamp", "KW", "centigrade", "people", "isworkday"])


def get_appliance_list(meter, engine):
    meter_table_name = 'meter_{}_source'.format(meter)
    sql_query = "select model from {}".format(meter_table_name)
    temp_df = data_read_database(engine, sql_query)
    appliance_id_list = list(set(temp_df['model']))
    appliance_id_list = list(filter(None, appliance_id_list))
    appliance_id_list.sort()
    return appliance_id_list


def get_appliance_list_file(meter, experiment_id):
    csv_path = "./database_files/" + experiment_id + "/train_data/" + meter + "-总电表.csv"
    temp_df = pd.read_csv(csv_path, index_col=False)
    appliance_id_list = list(set(temp_df['model']))
    appliance_id_list = list(filter(None, appliance_id_list))
    appliance_id_list.sort()
    return appliance_id_list


def get_appliance_name(appliance_id, engine):
    meter_table_name = 'model'
    sql_query = "select id, name from {}".format(meter_table_name)
    name_id_df = data_read_database(engine, sql_query)
    name_id_df['id'] = name_id_df['id'].astype(str)
    for index, row in name_id_df.iterrows():
        if row['id'] == appliance_id:
            return row['name']


def single_normalization(df_align, appliance_name, mode):
    cf.read("temp.conf", encoding='gbk')
    aggregate_mean = np.mean(df_align['aggregate'])
    aggregate_std = np.std(df_align['aggregate'])
    appliance_min = np.min(df_align[appliance_name])
    appliance_max = np.max(df_align[appliance_name])

    section_name = 'aggregate_' + appliance_name
    if cf.has_section(section_name):
        cf.remove_section(section_name)
    cf.add_section(section_name)
    cf.set(section_name, 'mean', str(aggregate_mean))
    cf.set(section_name, 'std', str(aggregate_std))
    if cf.has_section(appliance_name):
        cf.remove_section(appliance_name)
    cf.add_section(appliance_name)
    cf.set(appliance_name, 'min', str(appliance_min))
    cf.set(appliance_name, 'max', str(appliance_max))
    if mode == 'file':
        with open('temp_file.conf', 'w') as f:
            cf.write(f)
    elif mode == 'database':
        with open('temp.conf', 'w') as f:
            cf.write(f)
    df_align['aggregate'] = standardize_data(df_align['aggregate'], aggregate_mean, aggregate_std)
    df_align[appliance_name] = normalize_data(df_align[appliance_name], appliance_min, appliance_max)
    df_align = society_normalization(df_align)
    return df_align


def single_normalization_test(df_align, appliance_name):
    cf.read("temp_file.conf", encoding='gbk')
    section_name = 'aggregate_' + appliance_name
    aggregate_mean = cf.getfloat(section_name, "mean")
    aggregate_std = cf.getfloat(section_name, 'std')
    appliance_min = cf.getfloat(appliance_name, 'min')
    appliance_max = cf.getfloat(appliance_name, 'max')
    df_align['aggregate'] = standardize_data(df_align['aggregate'], aggregate_mean, aggregate_std)
    df_align[appliance_name] = normalize_data(df_align[appliance_name], appliance_min, appliance_max)
    df_align = society_normalization(df_align)
    return df_align


def multi_normalization(df_align, meter_name_list, engine):
    cf.read("temp.conf", encoding='gbk')
    for meter_name in meter_name_list:
        appliance_id_list = get_appliance_list(meter_name, engine)
        for appliance_id in appliance_id_list:
            if appliance_id is None or '-' in appliance_id:
                continue
            appliance_name = get_appliance_name(appliance_id, engine)
            appliance_min = np.min(df_align[appliance_name])
            appliance_max = np.max(df_align[appliance_name])
            if cf.has_section(appliance_name):
                cf.remove_section(appliance_name)
            cf.add_section(appliance_name)
            cf.set(appliance_name, 'min', str(appliance_min))
            cf.set(appliance_name, 'max', str(appliance_max))
            df_align[appliance_name] = normalize_data(df_align[appliance_name], appliance_min, appliance_max)
    aggregate_mean = np.mean(df_align['aggregate'])
    aggregate_std = np.std(df_align['aggregate'])
    if cf.has_section('aggregate_all'):
        cf.remove_section('aggregate_all')
    cf.add_section('aggregate_all')
    cf.set('aggregate_all', 'mean', str(aggregate_mean))
    cf.set('aggregate_all', 'std', str(aggregate_std))
    with open('temp.conf', 'w') as f:
        cf.write(f)
    df_align['aggregate'] = standardize_data(df_align['aggregate'], aggregate_mean, aggregate_std)
    df_align = society_normalization(df_align)
    return df_align


def society_normalization(df_align):
    # continues = ['centigrade', 'people']
    # cs = MinMaxScaler()
    # df_align[continues] = cs.fit_transform(df_align[continues])   # 这三句是正常的，原始数据有问题，后期可放开注释
    df_align = df_align.astype({'centigrade': 'int', 'people': 'int'})
    max_cen = df_align['centigrade'].max()
    max_peo = df_align['people'].max()
    df_align['centigrade'] = df_align['centigrade'] / max_cen
    df_align['people'] = df_align['people'] / max_peo
    lb = LabelBinarizer().fit(df_align['isworkday'])
    df_align['isworkday'] = lb.transform(df_align['isworkday'])
    return df_align


def standardize_data(data, mu=0.0, sigma=1.0):
    data -= mu
    data /= sigma
    return data


def normalize_data(data, min_value=0.0, max_value=1.0):
    data -= min_value
    diff = max_value - min_value
    if diff != 0:
        data /= diff
    return data
