import time
import datetime as dt

from owslib.ogcapi.connectedsystems import Systems, Datastreams, Observations
from owslib.util import Authentication
import matplotlib.pyplot as plt

server_url = 'http://34.67.197.57:8585/sensorhub/api'
local_server_url = 'http://localhost:8585/sensorhub/api'
auth = Authentication('auto_test', 'automated_tester24')
local_auth = Authentication('admin', 'admin')
json_headers = {'Content-Type': 'application/json'}
obs_api = Observations(server_url, auth=auth, headers=json_headers)
weather_datastream_id = 'fbmjp5um2cd7u'
local_weather_datastream_id = 'e84l3n755576m'


def main():
    temperature_data = []
    timestamp_data = []

    # do stuff
    while True:
        current_time = dt.datetime.now()
        resp = fetch_observations()
        t_result = resp['result']['temperature']
        time_result = resp['resultTime'].split('T')[1].split('Z')[0]
        temperature_data.append(t_result)
        timestamp_data.append(time_result)
        if len(temperature_data) > 100 & len(timestamp_data) > 100:
            temperature_data.pop(0)
            timestamp_data.pop(0)
        plt.plot(timestamp_data, temperature_data)
        plt.title('Temperature Data')
        plt.ylabel('Temperature')
        plt.xlabel('Time')
        plt.xticks(rotation=-45)
        plt.show()
        time.sleep(2)


def fetch_observations():
    latest_obs = obs_api.observations_of_datastream(weather_datastream_id, result_time='latest')['items'][0]
    print(latest_obs)
    return latest_obs


if __name__ == '__main__':
    main()
