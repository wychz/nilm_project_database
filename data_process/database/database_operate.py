import pandas as pd
from sklearn.preprocessing import MinMaxScaler, LabelBinarizer
import numpy as np
from data_process.database.common.data_utils import data_read_database
import configparser

cf = configparser.ConfigParser()
cf.read("temp.conf", encoding='utf-8')


def model_name_to_id(name, engine):
    meter_table_name = 'model'
    sql_query = "select id, name from {}".format(meter_table_name)
    name_id_df = data_read_database(engine, sql_query)
    for index, row in name_id_df.iterrows():
        if row['name'] == name:
            return row[id]


