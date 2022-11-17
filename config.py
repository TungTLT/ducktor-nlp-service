from enum import Enum


class ConfigType(Enum):
    CALL_JAVA_SERVICE = 0,
    NOT_CALL_JAVA_SERVICE = 1


class AppConfig:
    currentConfig: ConfigType = ConfigType.CALL_JAVA_SERVICE
