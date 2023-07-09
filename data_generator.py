import utils
import config_data
import os 

def dump_data(fpath_output='./'):
    os.makedirs(fpath_output,exist_ok=True)
    synthetic_data = utils.generate_synthetic_data(num_users = config_data.num_users, places_by_tag = config_data.places_by_tag, num_transactions_per_user = config_data.num_transactions_per_user)
    synthetic_data.to_csv(fpath_output,index=False)




