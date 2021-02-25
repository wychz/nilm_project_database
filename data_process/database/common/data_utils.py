import pandas as pd
from sklearn.preprocessing import MinMaxScaler, LabelBinarizer
import numpy as np
import configparser

cf = configparser.ConfigParser()
cf.read("temp.conf", encoding='utf-8')


def data_read_database(engine, sql_query):
    df_read = pd.read_sql_query(sql_query, engine)
    return df_read


def single_normalization(df_align, appliance_name):
    aggregate_mean = np.mean(df_align['aggregate'])
    aggregate_std = np.std(df_align['aggregate'])
    appliance_min = np.min(df_align[appliance_name])
    appliance_max = np.max(df_align[appliance_name])

    if cf.has_section('aggregate'):
        cf.remove_section('aggregate')
    cf.add_section('aggregate')
    cf.set('aggregate', 'mean', str(aggregate_mean))
    cf.set('aggregate', 'std', str(aggregate_std))
    if cf.has_section(appliance_name):
        cf.remove_section(appliance_name)
    cf.add_section(appliance_name)
    cf.set(appliance_name, 'min', str(appliance_min))
    cf.set(appliance_name, 'max', str(appliance_max))
    cf.write(open('temp.conf', 'w'))

    df_align['aggregate'] = standardize_data(df_align['aggregate'], aggregate_mean, aggregate_std)
    df_align[appliance_name] = normalize_data(df_align[appliance_name], appliance_min, appliance_max)
    society_normalization(df_align)


def multi_normalization(df_align, appliance_name_list):
    for appliance_name in appliance_name_list:
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
    if cf.has_section('aggregate'):
        cf.remove_section('aggregate')
    cf.add_section('aggregate')
    cf.set('aggregate', 'mean', str(aggregate_mean))
    cf.set('aggregate', 'std', str(aggregate_std))
    cf.write(open('temp.conf', 'w'))
    df_align['aggregate'] = standardize_data(df_align['aggregate'], aggregate_mean, aggregate_std)
    society_normalization(df_align)


def society_normalization(df_align):
    continues = ['centigrade', 'people']
    cs = MinMaxScaler()
    df_align[continues] = cs.fit_transform(df_align[continues])
    lb = LabelBinarizer().fit(df_align['isworkday'])
    df_align['isworkday'] = lb.transform(df_align['isworkday'])


def standardize_data(data, mu=0.0, sigma=1.0):
    data -= mu
    data /= sigma
    return data


def normalize_data(data, min_value=0.0, max_value=1.0):
    data -= min_value
    diff = max_value - min_value
    if diff != 0:
        data /= max_value - min_value
    return data
