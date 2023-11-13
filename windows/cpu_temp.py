import clr
import os

from config import settings

hwtypes = ['Mainboard','SuperIO','CPU','RAM','GpuNvidia','GpuAti','TBalancer','Heatmaster','HDD']


class GetTemerature:
    def initialize_openhardwaremonitor(self):
        file = rf'{os.getcwd()}\OpenHardwareMonitorLib'
        clr.AddReference(file)

        from OpenHardwareMonitor import Hardware

        handle = Hardware.Computer()
        handle.MainboardEnabled = True
        handle.CPUEnabled = True
        handle.RAMEnabled = True
        handle.GPUEnabled = True
        handle.HDDEnabled = True
        handle.Open()
        self.cpu_temp = []
        return handle

    def fetch_stats(self, handle):
        for i in handle.Hardware:
            i.Update()
            for sensor in i.Sensors:
                self.parse_sensor(sensor)
            for j in i.SubHardware:
                j.Update()
                for subsensor in j.Sensors:
                    self.parse_sensor(subsensor)

    def parse_sensor(self, sensor):
        if sensor.Value:
            if str(sensor.SensorType) == 'Temperature':
                if hwtypes[sensor.Hardware.HardwareType].strip() == "CPU":
                    self.cpu_temp.append(sensor.Value)

    def send_zabbix_message(self, cpu_temp: float) -> None:
        zabbix_command = f"""zabbix_sender -z {settings.ZABBIX_SERVER} -p {settings.ZABBIX_PORT} -s {settings.ZABBIX_NODE}\
                         -k {"cpu_temp"} -o {cpu_temp}"""
        print(zabbix_command)
        os.system(zabbix_command)

    def main(self):
        HardwareHandle = self.initialize_openhardwaremonitor()
        self.fetch_stats(HardwareHandle)
        self.send_zabbix_message(max(self.cpu_temp))
        return max(self.cpu_temp)


if __name__ == "__main__":
    temp_status = GetTemerature().main()
    # print(f"CPU temperature: {temp_status}")
    