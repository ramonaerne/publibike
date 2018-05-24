
import requests
import time
import json
import sched

API_PATH = "https://api.publibike.ch/v1/public"
s = sched.scheduler(time.time, time.sleep)

def crawl_vehicles(sc):

    def get_station_vehicles(id):
        info = requests.get(API_PATH + "/stations/" + str(id)).json()
        return info['vehicles']

    # restart scheduler for next iteration
    s.enter(10*60, 1, crawl_vehicles, (sc,))

    print("crawling ...")

    stations = requests.get(API_PATH + "/stations").json()
    # get ids if stations are active
    station_ids = [s['id'] for s in stations if s['state']['id'] == 1]

    # get timestamp
    current_timestamp = time.time()
    station_vehicles = [{'id': id, 'vehicles': get_station_vehicles(id)} for id in station_ids]

    with open('data/{}.json'.format(current_timestamp), 'w') as outfile:
        json.dump(station_vehicles, outfile)

    print("done, sleep")


# setup scheduler task and run
s.enter(0, 1, crawl_vehicles, (s,))
s.run()


