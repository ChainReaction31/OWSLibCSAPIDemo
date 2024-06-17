import datetime as dt
import tkinter as tk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from owslib.ogcapi.connectedsystems import Observations
from owslib.util import Authentication

server_url = 'http://34.67.197.57:8585/sensorhub/api'
local_server_url = 'http://localhost:8585/sensorhub/api'
auth = Authentication('auto_test', 'automated_tester24')
local_auth = Authentication('admin', 'admin')
json_headers = {'Content-Type': 'application/json'}
obs_api = Observations(server_url, auth=auth, headers=json_headers)
weather_datastream_id = 'fbmjp5um2cd7u'
local_weather_datastream_id = 'e84l3n755576m'
gyro_datastream_id = 'hjdvcjp6an6ie'

gyro_time = []
gyro_data_x = []
gyro_data_y = []
gyro_data_z = []
accel_data_x = []
accel_data_y = []
accel_data_z = []


def main():
    global root, ax, canvas, temperature_data, timestamp_data
    root = tk.Tk()
    root.title('Weather & Gyroscope Data')
    root.geometry('1920x1080')
    # label = tk.Label(root, text='Weather Data')
    # label.pack()

    temperature_data = []
    timestamp_data = []

    fig, axs = plt.subplots(2, 2, figsize=(20, 20))
    ax = axs[0, 0]
    ax1 = axs[0, 1]
    ax2 = axs[1, 0]
    ax3 = axs[1, 1]

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Gyro Loop
    # fig2, ax2 = plt.subplots()
    # canvas2 = FigureCanvasTkAgg(fig2, master=root)
    # canvas2.draw()
    # canvas2.get_tk_widget().pack()
    #
    # # Accelerometer Loop
    # fig3, ax3 = plt.subplots()
    # canvas3 = FigureCanvasTkAgg(fig3, master=root)
    # canvas3.draw()
    # canvas3.get_tk_widget().pack()

    root.after(2000, update_plot)
    root.after(2000, lambda: update_gyro_plot(plt, ax2, canvas, ax3, canvas))
    root.mainloop()


def fetch_observations(datastream_id):
    latest_obs = obs_api.observations_of_datastream(datastream_id, result_time='latest')['items'][0]
    return latest_obs


def update_plot():
    global temperature_data, timestamp_data
    current_time = dt.datetime.now()
    resp = fetch_observations(weather_datastream_id)
    t_result = resp['result']['temperature']
    time_result = resp['resultTime'].split('T')[1].split('Z')[0]
    temperature_data.append(t_result)
    timestamp_data.append(time_result)
    # if len(temperature_data) > 25 & len(timestamp_data) > 25:
    #     temperature_data.pop(0)
    #     timestamp_data.pop(0)

    temperature_data = temperature_data[-25:]
    timestamp_data = timestamp_data[-25:]

    ax.clear()
    ax.plot(timestamp_data, temperature_data)
    ax.set_title(f'Temperature Data {dt.datetime.now().strftime("%Y-%m-%d")}')
    ax.set_ylabel('Temperature (°C)')
    ax.set_xlabel('Time')
    plt.xticks(rotation=-45)
    ax.tick_params(axis='x', labelsize=6, rotation=-45)

    canvas.draw()
    root.after(2000, update_plot)


def update_gyro_plot(plot, axis, canvas, axis2, canvas2):
    global gyro_time, gyro_data_x, gyro_data_y, gyro_data_z, accel_data_x, accel_data_y, accel_data_z

    resp = fetch_observations(gyro_datastream_id)
    print(resp)
    timestamp = resp['resultTime'].split('T')[1].split('Z')[0]
    gyro_data = resp['result']['gyro-readings']
    accel_data = resp['result']['accelerometer-readings']

    gyro_time.append(timestamp)
    print(gyro_data)

    gyro_data_x.append(gyro_data['x'])
    gyro_data_y.append(gyro_data['y'])
    gyro_data_z.append(gyro_data['z'])

    accel_data_x.append(accel_data['x'])
    accel_data_y.append(accel_data['y'])
    accel_data_z.append(accel_data['z'])

    # Ensure the lists never have more than 25 elements
    gyro_time = gyro_time[-25:]
    gyro_data_x = gyro_data_x[-25:]
    gyro_data_y = gyro_data_y[-25:]
    gyro_data_z = gyro_data_z[-25:]
    accel_data_x = accel_data_x[-25:]
    accel_data_y = accel_data_y[-25:]
    accel_data_z = accel_data_z[-25:]

    axis.clear()
    axis.plot(gyro_time, gyro_data_x, label='X')
    axis.plot(gyro_time, gyro_data_y, label='Y')
    axis.plot(gyro_time, gyro_data_z, label='Z')
    axis.set_title('Gyro Data')
    axis.set_ylabel('Gyro Data')
    axis.set_xlabel('Time')
    axis.legend()
    axis.tick_params(axis='x', labelsize=6, rotation=-45)
    canvas.draw()

    axis2.clear()
    axis2.plot(gyro_time, accel_data_x, label='X')
    axis2.plot(gyro_time, accel_data_y, label='Y')
    axis2.plot(gyro_time, accel_data_z, label='Z')
    axis2.set_title('Accelerometer Data')
    axis2.set_ylabel('Accelerometer Data')
    axis2.set_xlabel('Time')
    axis2.legend()
    axis2.tick_params(axis='x', labelsize=6, rotation=-45)
    canvas2.draw()

    root.after(500, lambda: update_gyro_plot(plot, axis, canvas, axis2, canvas2))


if __name__ == '__main__':
    main()
