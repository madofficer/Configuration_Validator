import os.path
import re
from uuid import UUID

from framework.exception.validation_exception import ValidationException


# General

def validate_int_range(param: str, val, min_val: int, max_val: int) -> bool:
    try:
        num = int(val.strip())
        return min_val <= num <= max_val

    except Exception as err:
        raise ValidationException(
            param,
            val,
            message="Something went wrong"
        ) from err


def validate_bool(param: str, val: str) -> bool:
    try:
        return val.strip().lower() in {"true", "false", "yes", "no"}

    except Exception as err:
        raise ValidationException(
            param,
            val,
            message="Something went wrong"
        ) from err


def validate_path(param: str, val: str) -> bool:
    try:
        path = val.strip().lower()
        return os.path.isabs(path) and os.path.exists(path)

    except Exception as err:
        raise ValidationException(
            param,
            val,
            message="Something went wrong"
        ) from err


def validate_uuid(param: str, val: str) -> bool:
    try:
        UUID(val.strip())
        return True

    except Exception as err:
        raise ValidationException(
            param,
            val,
            message="Something went wrong"
        ) from err


def validate_package_type(param: str, val: str) -> bool:
    try:
        return val.strip().lower() in {"rpm", "deb"}

    except Exception as err:
        raise ValidationException(
            param,
            val,
            message="Something went wrong"
        ) from err


def validate_locale(param: str, val: str) -> bool:
    pattern = r"^[a-z]{2,3}(-[A-Za-z0-9]{2,3})?$"
    try:
        locale_ = val.strip()
        return re.fullmatch(pattern, locale_) is not None

    except Exception as err:
        raise ValidationException(
            param,
            val,
            message="Something went wrong"
        ) from err


# Watchdog

def validate_time_out(param: str, val: str) -> bool:
    try:
        time_out = val.replace(' ', '').lower()
        return (time_out.endswith("m")
                and validate_int_range(param,
                                       time_out[:-1],
                                       1,
                                       120)
                )

    except Exception as err:
        raise ValidationException(
            param,
            val,
            message="Something went wrong"
        ) from err


def validate_memory_value(param: str, val: str) -> bool:
    try:
        val = val.strip().lower()
        try:
            return 0 < float(val) <= 100
        except ValueError as err:
            return val in {"off", "auto"}

    except Exception as err:
        raise ValidationException(
            param,
            val,
            message="Something went wrong"
        ) from err
