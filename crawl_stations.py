import os
import requests
import time
import json
import pandas as pd
import warnings

DIR = os.getcwd()
API_PATH = "https://api.publibike.ch/v1/public"

# disable the performance warning since pickle does not like utf-8 strings (i guess)
warnings.simplefilter('ignore', pd.io.pytables.PerformanceWarning)

''' gets station ifos from publibike api '''
def get_station_infos(id):
    info = requests.get(API_PATH + "/stations/" + str(id)).json()
    # remove non stationary part
    del info['vehicles']
    return info

''' cuts fieldname entry out of dict and replaces it with its id
    returns the updated dict as well as a new dict containing the cut out data
'''
def splitAndReplace(input, fieldname, from_id, to_id):
    def replaceItemsWithId(station):
        new_id = station[fieldname][from_id]
        del station[fieldname]
        station[to_id] = new_id
        return station

    out = [s[fieldname] for s in input]
    input_new = [replaceItemsWithId(s) for s in input]
    return input_new, out

''' cuts fieldname entry out of dict and replaces it with its id list
    returns the updated dict as well as a list containing the cut out data
'''
def splitAndReplaceList(input, fieldname, from_id, to_id):

    def replaceListWithIdList(station):
        to_idlist = [sp[from_id] for sp in station[fieldname]]
        del station[fieldname]
        station[to_id] = to_idlist
        return station

    out = [i[fieldname] for i in input]
    out_flat = [item for subitem in out for item in subitem]
    input_new = [replaceListWithIdList(s) for s in input]

    return input_new, out_flat

''' creates a pandas frame and stores it as hdf5 '''
def createAndSaveFrame(input, name):
    frame = pd.DataFrame.from_dict(input)
    # remove duplicates, since all stationary
    frame.set_index('id', inplace=True)
    frame = frame[~frame.index.duplicated(keep='first')]
    frame.sort_index(inplace=True)
    frame.to_hdf(os.path.join(DIR, 'data', 'static_info.h5'), name)


print("dumping station data")

stations = requests.get(API_PATH + "/stations").json()
station_ids = [s['id'] for s in stations]
station_infos = [get_station_infos(id) for id in station_ids]

# take all items containing another dict out of dict
station_infos, networks = splitAndReplace(station_infos, 'network', 'id', 'network_id')
station_infos, state = splitAndReplace(station_infos, 'state', 'id', 'state_id')
station_infos, sponsors = splitAndReplaceList(station_infos, 'sponsors', 'id', 'sponsors_id')

createAndSaveFrame(station_infos, 'stations')    
createAndSaveFrame(networks, 'networks')
createAndSaveFrame(state, 'state')
createAndSaveFrame(sponsors, 'sponsors')
