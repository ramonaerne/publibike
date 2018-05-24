# now a good dataformat to continue working with it a database with entries
# (unique id) timestamp station_id vehicle_id
# this adds some duplication since we store timestamp and station_id more, but now
# we know all the ids and can save only these in the database
import requests
import time
import datetime
import pandas as pd

DIR = "/nas/raerne/Work/publibike"
API_PATH = "https://api.publibike.ch/v1/public"

# get stations
stations = requests.get(API_PATH + "/stations").json()

# how to read later
#data2 = pd.read_hdf(DIR + '/data/data.h5', key=str(current_timestamp))
raw = pd.HDFStore(DIR + '/data/data.h5')
raw_concat = [raw[k] for k in raw.keys()]

merged = pd.concat(raw_concat)
print(merged)



# access ith frame with raw[raw.keys()[i]]
