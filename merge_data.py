# now a good dataformat to continue working with it a database with entries
# (unique id) timestamp station_id vehicle_id
# this adds some duplication since we store timestamp and station_id more, but now
# we know all the ids and can save only these in the database
import sys, os
import requests
import time
import datetime
import pandas as pd

API_PATH = "https://api.publibike.ch/v1/public"

def merge(path):
    # get stations
    stations = requests.get(API_PATH + "/stations").json()

    # how to read later
    #data2 = pd.read_hdf(DIR + '/data/data.h5', key=str(current_timestamp))
    raw = pd.HDFStore(os.path.join(path, 'data/data.h5'))
    raw_concat = [raw[k] for k in raw.keys()]

    merged = pd.concat(raw_concat)
    print(merged)

def main():
    # get directory of this script
    path = sys.argv[0]
    if os.path.exists(path):
        DIR = os.path.dirname(os.path.abspath(path))
        merge(DIR)

if __name__ == "__main__":
    main()


# access ith frame with raw[raw.keys()[i]]
