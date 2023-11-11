import os
import psutil
from config import settings
from pprint import pprint

key_dict = {
    "coretemp": "core_temp",
    "acpitz": "mb_temp",
    "i350bb": "mb_temp"
}


def handle_sensor(sensor: str, sensor_data: list) -> None:
    temperature = sensor_data[0].current
    temperature_dict = {"sensor": key_dict[sensor], "temperature": temperature}
    zabbix_sender(temperature_dict)


def zabbix_sender(temperature_dict: dict) -> None:
    zabbix_command = f"""zabbix_sender -z {settings.ZABBIX_SERVER} -p {settings.ZABBIX_PORT} -s {settings.ZABBIX_NODE} 
                         -k temperature_{temperature_dict["sensor"]} -o {temperature_dict["temperature"]}"""
    print(zabbix_command)


def main():
    temper_dict = psutil.sensors_temperatures()
    # import pprint
    # pprint.pprint(temper_dict, indent=2)
    for item in temper_dict:
        if item in key_dict:
            handle_sensor(item, temper_dict[item])


if __name__ == "__main__":
    main()