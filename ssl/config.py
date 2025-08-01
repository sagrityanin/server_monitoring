from pydantic import BaseSettings


class Settings(BaseSettings):
    ZABBIX_SERVER: str
    ZABBIX_PORT: str
    ZABBIX_NODE: str
    HOSTS: dict = {
            "task.info66.ru": 443,
            "pm1.info66.ru": 8006,
            "pm2.info66.ru": 8006,
            "pm3.info66.ru": 8006,
            "pm4.info66.ru": 8006,
            "loki.info66.ru": 3000,
            "loki.vtkl.ru": 3000,
            "fssys.ru": 443
    }


    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
