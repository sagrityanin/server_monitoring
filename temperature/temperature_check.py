import os
import psutil
from pprint import pprint

ZABBIX_SERVER = "192.168.13.6"
key_dict = {
    "coretemp": "core_temp",
    "acpitz": "mb_temp"
}

def handle_sensor(sensor: str, sensor_data: list) -> None:
    temperature = sensor_data[0].current
    temperature_dict = {"Sensor": key_dict[sensor], "temperature": temperature}
    print(temperature_dict)


def zabbix_sender(temperature_dict: dict) -> None:
    pass


def main():
    temper_dict = psutil.sensors_temperatures()
    for item in key_dict:
        handle_sensor(item, temper_dict[item])



if __name__ == "__main__":
    main()