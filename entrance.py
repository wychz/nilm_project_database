import argparse
from utils.common_utils import remove_space
from train_model.train_main import train_model
from test_model.test_main import test_model
from data_process.database.data_main import database_data_process
from data_process.database.data_to_label import data_process_database_multi_label

parser = argparse.ArgumentParser(description="Train sequence-to-point learning for energy disaggregation. ")

# train, test, data_process
parser.add_argument("--step", type=remove_space, default="train", help="The name of the appliance to train the network with. Default is kettle. Available are: kettle, fridge, washing machine, dishwasher, and microwave. ")

arguments = parser.parse_args()

# mode = arguments.step
mode = 'all'


if mode == 'train':
    train_model()
elif mode == 'test':
    test_model()
elif mode == 'data_process':
    database_data_process()
elif mode == 'data_process_database_multi_label':
    data_process_database_multi_label()
elif mode == 'all':
    database_data_process()
    train_model()
    test_model()
