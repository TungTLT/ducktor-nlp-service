from enum import Enum


class ConfigType(Enum):
    CALL_JAVA_SERVICE = 0,
    NOT_CALL_JAVA_SERVICE = 1


class AppConfig:
    service_config: ConfigType = ConfigType.NOT_CALL_JAVA_SERVICE
    host = '192.168.1.85'
    port = 5004
