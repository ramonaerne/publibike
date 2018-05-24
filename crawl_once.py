# old query:
# station_vehicles = [{'id': id, 'vehicles': get_station_vehicles(id)} for id in station_ids]

# now we have the following information for each station, e.g
# {'id': 108,
#  'vehicles': [{'id': 488, 'name': '101280', 'type': {'id': 1, 'name': 'Bike'}}, ...]}
# let's assume for now that this datastructure remains somewhat the same so we don't
# have to store all data, e.g. we are only interested in timestamp/vehicleid/stationid, the rest
# we can conclude from this, i.e. station name, vehicle type and so on ...

# now a good dataformat to continue working with it a database with entries
# (unique id) timestamp station_id vehicle_id
# this adds some duplication since we store timestamp and station_id more, but now
# we know all the ids and can save only these in the database
import os
import requests
import time
import datetime
import pandas as pd
import warnings, tables

DIR = os.getcwd()
API_PATH = "https://api.publibike.ch/v1/public"

# disable naturalNameWarning in tables module
warnings.simplefilter('ignore', tables.NaturalNameWarning)

# get stations
stations = requests.get(API_PATH + "/stations").json()

# get timestamp and convert to pandas timestamp, as well as readable
current_timestamp = time.time()
pd_t = pd.to_datetime(current_timestamp, unit='s')
readable_t = datetime.datetime.fromtimestamp(current_timestamp).strftime('%Y-%m-%d_%H_%M_%S')
print("crawling vehicles @ ", readable_t)

# prepare datarow in the way that will be saved later
def data_row(id):
    info = requests.get(API_PATH + "/stations/" + str(id)).json()

    # return list including timestamp and station id
    return [{'station_id': id, 'vehicle_id': v['id'], 'timestamp': pd_t} for v in info['vehicles']]

# get entries for all active stations
data_entries = [data_row(s['id']) for s in stations if s['state']['id'] == 1]
# and now flatten the list (we have a list of lists in data_entries
# and store in pd frame
data = [item for subitem in data_entries for item in subitem]
frame = pd.DataFrame.from_dict(data)

# store in same file but with different keys
frame.to_hdf(DIR + '/data/data.h5', key=str(current_timestamp))

# how to read later
#data2 = pd.read_hdf(DIR + '/data/data.h5', key=str(current_timestamp))
#raw = pd.HDFStore(DIR + '/data/data.h5')
# access ith frame with raw[raw.keys()[i]]
