import os.path
import re
from configparser import ConfigParser
from typing import TypeGuard
from uuid import UUID

from framework.exception.validation_exception import ValidationException

REQUIRED_SECTIONS = {
    "General": {
        "ScanMemoryLimit",
        "PackageType",
        "ExecArgMax",
        "AdditionalDNSLookup",
        "CoreDumps",
        "RevealSensitiveInfoInTraces",
        "ExecEnvMax",
        "MaxInotifyWatches",
        "CoreDumpsPath",
        "UseFanotify",
        "KsvlaMode",
        "MachineId",
        "StartupTraces",
        "MaxInotifyInstances",
        "Locale",
    },
    "Watchdog": {
        "ConnectTimeout",
        "MaxVirtualMemory",
        "MaxMemory",
        "PingInterval",
    },
}

# Check config structure


def validate_config_sections(config: ConfigParser) -> TypeGuard[ConfigParser]:
    return (
        len(config.sections()) == len(REQUIRED_SECTIONS)
        and set(config.sections()) == REQUIRED_SECTIONS.keys()
    )


def validate_config_params(config: ConfigParser) -> TypeGuard[ConfigParser]:
    print(config.sections())
    for section in config.sections():
        print(set(config[section]))
        if len(config[section]) == len(REQUIRED_SECTIONS[section]):
            for param in REQUIRED_SECTIONS[section]:
                if param not in config[section]:
                    return False
        else:
            return False
    return True


# General


def validate_int_range(param: str, val, min_val: int, max_val: int) -> TypeGuard[int]:
    try:
        num = int(val.strip())
        return min_val <= num <= max_val

    except Exception as err:
        raise ValidationException(param, val, message="Something went wrong") from err


def validate_bool(param: str, val: str) -> TypeGuard[bool]:
    try:
        return val.strip().lower() in {"true", "false", "yes", "no"}

    except Exception as err:
        raise ValidationException(param, val, message="Something went wrong") from err


def validate_path(param: str, val: str) -> TypeGuard[str]:
    try:
        path = val.strip().lower()
        return os.path.isabs(path) and os.path.exists(path)

    except Exception as err:
        raise ValidationException(param, val, message="Something went wrong") from err


def validate_uuid(param: str, val: str) -> TypeGuard[UUID]:
    try:
        try:
            UUID(val.strip())
            return True
        except ValueError:
            return False

    except Exception as err:
        raise ValidationException(param, val, message="Something went wrong") from err


def validate_package_type(param: str, val: str) -> TypeGuard[str]:
    try:
        return val.strip().lower() in {"rpm", "deb"}

    except Exception as err:
        raise ValidationException(param, val, message="Something went wrong") from err


def validate_locale(param: str, val: str) -> TypeGuard[str]:
    pattern = r"^[a-z]{2,3}(_[A-Z]{2})(\.[A-Za-z0-9\-]+)?(@[a-z0-9]+)?$"
    try:
        locale_ = val.strip()
        return re.fullmatch(pattern, locale_) is not None

    except Exception as err:
        raise ValidationException(param, val, message="Something went wrong") from err


# Watchdog


def validate_time_out(param: str, val: str) -> TypeGuard[str]:
    try:
        time_out = val.replace(" ", "").lower()
        return time_out.endswith("m") and validate_int_range(
            param, time_out[:-1], 1, 120
        )

    except Exception as err:
        raise ValidationException(param, val, message="Something went wrong") from err


def validate_memory_value(param: str, val: str) -> TypeGuard[str | float]:
    try:
        val = val.strip().lower()
        try:
            return 0 < float(val) <= 100
        except ValueError:
            return val in {"off", "auto"}

    except Exception as err:
        raise ValidationException(param, val, message="Something went wrong") from err
