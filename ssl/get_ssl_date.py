from cryptography import x509
from datetime import datetime
import os
import socket
import ssl
import sys
from config import settings

class GetSsl:
    def __init__(self):

        # create default context
        self.context = ssl.create_default_context()

        # override context so that it can get expired cert
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE

    def get_date(self, hostname):
        print(hostname, settings.HOSTS[hostname])
        with socket.create_connection((hostname, settings.HOSTS[hostname])) as sock:
            with self.context.wrap_socket(sock, server_hostname=hostname) as ssock:
                print("SSL/TLS version:", ssock.version())
                # print()

                # get cert in DER format
                data = ssock.getpeercert(True)
                # print("Data:", data)
                # print()

                # convert cert to PEM format
                pem_data = ssl.DER_cert_to_PEM_cert(data)
                # print("PEM cert:", pem_data)

                # pem_data in string. convert to bytes using str.encode()
                # extract cert info from PEM format
                cert_data = x509.load_pem_x509_certificate(str.encode(pem_data))

                # show cert expiry date
                ssl_date = cert_data.not_valid_after_utc
                return ssl_date

    def zabbix_send(self, zabbix_key: str, zabbix_value: float|int) -> bool:
        zabbix_command = f"""zabbix_sender -z {settings.ZABBIX_SERVER} -p {settings.ZABBIX_PORT}\
                             -s {settings.ZABBIX_NODE} -k {zabbix_key} -o {zabbix_value}"""
        os.system(zabbix_command)
        return True

    def main(self):
        for hostname in settings.HOSTS:
            ssl_date = self.get_date(hostname)
            if ssl_date:
                self.zabbix_send(hostname, int(ssl_date.timestamp() - datetime.now().timestamp()))
            else:
                self.zabbix_send(hostname, 0)
            print("Expiry date:", ssl_date)
            if ssl_date.timestamp() < datetime.now().timestamp():
                print("DANGER________DANGER_______DANGER_______DANGER")
            else: 
                print("Ok")
            print()


if __name__ == "__main__":
    GetSsl().main()
