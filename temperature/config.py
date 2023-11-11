from pydantic import BaseSettings


class Settings(BaseSettings):
    ZABBIX_SERVER: str
    ZABBIX_PORT: str
    ZABBIX_NODE: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
