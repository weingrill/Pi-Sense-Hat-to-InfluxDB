#!/usr/bin/python

import argparse
from sense_hat import SenseHat
from influxdb import InfluxDBClient


def send_to_influx(host, port, user, password, database, room, house, data):
    """
    send the data to InfluxDB
    :param host: Hostname/IP of the InfluxDB server. Default localhost
    :param port: Port of InfluxDB http API. Default 8086
    :param user: User to use for the InfluxDB connection. By default not needed
    :param password: Password to use for the InfluxDB connection. By default not needed
    :param database: database name to store the data.
    :param room: Name of the room to serve as an InfluxDB tag name. Required
    :param house: Name of the house/apartment to serve as an InfluxDB tag name. Optional, default My House
    :param data: data dictionary that sends
    :return:
    """
    client = InfluxDBClient(host, port, user, password, database)
    json_body = [
        {
            "measurement": "sensors",
            "tags": {
                "room": room,
                "house": house
            },
            "fields": {
                "temperature": data['temperature'],
                "pressure": data['pressure'],
                "humidity": data['humidity'],
                "temperature_h": data['temperature_h'],
                "temperature_p": data['temperature_p'],
                "magnetometer_x": data['magnetometer_x'],
                "magnetometer_y": data['magnetometer_y'],
                "magnetometer_z": data['magnetometer_z'],
                "gyroscope_x": data['gyroscope_x'],
                "gyroscope_y": data['gyroscope_y'],
                "gyroscope_z": data['gyroscope_z'],
                "accelerometer_x": data['accelerometer_x'],
                "accelerometer_y": data['accelerometer_y'],
                "accelerometer_z": data['accelerometer_z']
            }
        }
    ]
    print(client.write_points(json_body))


def get_sensors(precision):
    """
    get temp, pressure, humidity from the Sense HAT
    :param precision: Decimal point round precision, e.g. with 3 the results will be 24.054. Default 2
    :return: returns a data dictionary
    """
    sense = SenseHat()
    data = {}
    data['temperature'] = round(sense.get_temperature(), precision)
    data['pressure'] = round(sense.get_pressure(), precision)
    data['humidity'] = round(sense.get_humidity(), precision)
    data['temperature_h'] = round(sense.get_temperature_from_humidity(), precision)
    data['temperature_p'] = round(sense.get_temperature_from_pressure(), precision)
    magnetometer_raw = sense.get_compass_raw()
    data['magnetometer_x'] = magnetometer_raw['x']
    data['magnetometer_y'] = magnetometer_raw['y']
    data['magnetometer_z'] = magnetometer_raw['z']
    gyroscope_raw = sense.get_gyroscope_raw()
    data['gyroscope_x'] = gyroscope_raw['x']
    data['gyroscope_y'] = gyroscope_raw['y']
    data['gyroscope_z'] = gyroscope_raw['z']
    accelerometer_raw = sense.get_accelerometer_raw()
    data['accelerometer_x'] = accelerometer_raw['x']
    data['accelerometer_y'] = accelerometer_raw['y']
    data['accelerometer_z'] = accelerometer_raw['z']

    return data


def parse_args():
    parser = argparse.ArgumentParser(description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False, default='localhost',
                        help='Hostname/IP of the InfluxDB server. Default localhost')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='Port of InfluxDB http API. Default 8086')
    parser.add_argument('--user', type=str, required=False, default='admin',
                        help='User to use for the InfluxDB connection. By default not needed')
    parser.add_argument('--password', type=str, required=False, default='password',
                        help='Password to use for the InfluxDB connection. By default not needed')
    parser.add_argument('--database', type=str, required=False, default='sensorhat',
                        help='database name to store the data.')
    parser.add_argument('--house', type=str, required=False, default='My House',
                        help='Name of the house/apartment to serve as an InfluxDB tag name. Optional, default My House')
    parser.add_argument('--room', type=str, required=True,
                        help='Name of the room to serve as an InfluxDB tag name. Required')
    parser.add_argument('--precision', type=int, required=False, default='2',
                        help='Decimal point round precision, e.g. with 3 the results will be 24.054. Default 2')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    sensors = get_sensors(precision=args.precision)
    send_to_influx(host=args.host, port=args.port,
                   user=args.user,
                   password=args.password,
                   database=args.database,
                   room=args.room,
                   house=args.house,
                   data=sensors)
