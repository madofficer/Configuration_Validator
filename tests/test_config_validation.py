import os
from io import StringIO, BytesIO


import pytest
from dotenv import load_dotenv

from framework.config import read_config
from framework.exception.validation_exception import ValidationException
from framework.validators import (
    validate_int_range,
    validate_bool,
    validate_path,
    validate_uuid,
    validate_package_type,
    validate_locale,
    validate_time_out,
    validate_memory_value,
)

load_dotenv()

general_fields = {
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
}

watchdog_fields = {"ConnectTimeout", "MaxVirtualMemory", "MaxMemory", "PingInterval"}


@pytest.fixture
def valid_config():
    return read_config()


# valid tests on temp config.ini


@pytest.mark.parametrize("param", ("General", "Watchdog"))
def test_required_sections(valid_config, param):
    assert param in valid_config


@pytest.mark.parametrize("param", general_fields)
def test_general_fields(valid_config, param):
    general = valid_config["General"]
    assert param in general
    assert len(general) == len(general_fields)


@pytest.mark.parametrize("param", watchdog_fields)
def test_watchdog_fields(valid_config, param):
    watchdog = valid_config["Watchdog"]
    assert param in watchdog
    assert len(watchdog) == len(watchdog_fields)


@pytest.mark.parametrize(
    "param,min_val,max_val",
    [
        ("ScanMemoryLimit", 1024, 8192),
        ("ExecArgMax", 10, 100),
        ("ExecEnvMax", 10, 100),
        ("MaxInotifyWatches", 1000, 1_000_000),
        ("MaxInotifyInstances", 1024, 8192),
    ],
)
def test_int_range_validation_g(valid_config, param, min_val, max_val):
    general = valid_config["General"]
    assert validate_int_range(param, general[param], min_val, max_val)


@pytest.mark.parametrize("param,min_val,max_val", [("PingInterval", 100, 10_000)])
def test_int_range_validation_wd(valid_config, param, min_val, max_val):
    watchdog = valid_config["Watchdog"]
    assert validate_int_range(param, watchdog[param], min_val, max_val)


@pytest.mark.parametrize(
    "param",
    [
        "AdditionalDNSLookup",
        "CoreDumps",
        "RevealSensitiveInfoInTraces",
        "UseFanotify",
        "KsvlaMode",
        "StartupTraces",
    ],
)
def test_bool_validation(valid_config, param):
    general = valid_config["General"]
    assert validate_bool(param, general[param])


@pytest.mark.parametrize("param", ["CoreDumpsPath"])
@pytest.mark.xfail(
    condition=lambda: not os.path.exists(valid_config["General"]["CoreDumpsPath"]),
    reason="Test path does not exist",
    strict=False,
)
def test_path_validation(valid_config, param):
    general = valid_config["General"]
    assert not validate_path(param, general[param])


@pytest.mark.parametrize("param", ["MachineId"])
def test_uuid_validation(valid_config, param):
    general = valid_config["General"]
    assert validate_uuid(param, general[param])


@pytest.mark.parametrize("param", ["PackageType"])
def test_package_type_validation(valid_config, param):
    general = valid_config["General"]
    assert validate_package_type(param, general[param])


@pytest.mark.parametrize("param", ["Locale"])
def test_locale_validation(valid_config, param):
    general = valid_config["General"]
    assert validate_locale(param, general[param])


@pytest.mark.parametrize("param", ["ConnectTimeout"])
def test_time_out_validation(valid_config, param):
    watchdog = valid_config["Watchdog"]
    assert validate_time_out(param, watchdog[param])


@pytest.mark.parametrize("param", ["MaxVirtualMemory", "MaxMemory"])
def test_memory_value_validation(valid_config, param):
    watchdog = valid_config["Watchdog"]
    assert validate_memory_value(param, watchdog[param])


# invalid tests for General section


@pytest.mark.parametrize(
    "param,val,min_val,max_val",
    [
        ("ScanMemoryLimit", "1023", 1024, 8192),
        ("ScanMemoryLimit", "8193", 1024, 8192),
        ("ExecArgMax", "09", 10, 100),
        ("ExecArgMax", " 101 ", 10, 100),
        ("ExecEnvMax", "9", 10, 100),
        ("ExecEnvMax", "101", 10, 100),
        ("MaxInotifyWatches", "999", 1000, 1_000_000),
        ("MaxInotifyWatches", " 1000001", 1000, 1_000_000),
        ("MaxInotifyInstances", "1023 ", 1024, 8192),
        ("MaxInotifyInstances", "8193", 1024, 8192),
    ],
)
def test_int_range_validation_g_invalid(param, val, min_val, max_val):
    assert not validate_int_range(param, val, min_val, max_val)


@pytest.mark.parametrize(
    "param,val",
    [
        ("AdditionalDNSLookup", "enabled"),
        ("CoreDumps", "disabled"),
        ("RevealSensitiveInfoInTraces", "1"),
        ("UseFanotify", "0"),
        ("KsvlaMode", ""),
        ("StartupTraces", "ye s"),
    ],
)
def test_bool_validation_invalid(param, val):
    assert not validate_bool(param, val)


@pytest.mark.parametrize(
    "param,val",
    [
        ("CoreDumpsPath", "fake_path/path"),
        ("CoreDumpsPath", "/random_path/path"),
    ],
)
def test_path_validation_invalid(param, val):
    assert not validate_path(param, val)


@pytest.mark.parametrize(
    "param,val",
    [
        ("MachineId", "not-a-uuid"),
        ("MachineId", "12345678-1234-1234-1234-1234567890"),
    ],
)
def test_uuid_validation_invalid(param, val):
    assert not validate_uuid(param, val)


@pytest.mark.parametrize(
    "param,val",
    [
        ("PackageType", "msi"),
        ("PackageType", "tar"),
    ],
)
def test_package_type_validation_invalid(param, val):
    assert not validate_package_type(param, val)


@pytest.mark.parametrize(
    "param,val",
    [
        ("Locale", "rus/iso8859"),
        ("Locale", "en-US-utf8"),
        ("Locale", "123 "),
    ],
)
def test_locale_validation_invalid(param, val):
    assert not validate_locale(param, val)


# invalid tests for Watchdog section
@pytest.mark.parametrize(
    "param,val,min_val,max_val",
    [
        ("PingInterval", "99", 100, 10_000),
        ("PingInterval", "10001", 100, 10_000),
    ],
)
def test_int_range_validation_wd_invalid(param, val, min_val, max_val):
    assert not validate_int_range(param, val, min_val, max_val)


@pytest.mark.parametrize(
    "param,val",
    [
        ("ConnectTimeout", "0m"),
        ("ConnectTimeout", "121m"),
        ("ConnectTimeout", "10"),
        ("ConnectTimeout", "10s"),
    ],
)
def test_time_out_validation_invalid(param, val):
    assert not validate_time_out(param, val)


@pytest.mark.parametrize(
    "param,val",
    [
        ("MaxVirtualMemory", "0"),
        ("MaxVirtualMemory", "101"),
        ("MaxVirtualMemory", "on"),
        ("MaxMemory", "0"),
        ("MaxMemory", "101"),
        ("MaxMemory", "on"),
    ],
)
def test_memory_value_validation_invalid(param, val):
    assert not validate_memory_value(param, val)


# test section with exceptions raised


@pytest.mark.parametrize(
    "param,val,min_val,max_val",
    [
        ("ScanMemoryLimit", 2048, 1024, 8192),
        ("ScanMemoryLimit", "", 1024, 8192),
        ("ExecArgMax", "_090", 10, 100),
        ("ExecArgMax", "101-50", 10, 100),
        ("ExecEnvMax", "12 .9", 10, 100),
        ("ExecEnvMax", None, 10, 100),
        ("MaxInotifyWatches", "199n9", 1000, 1_000_000),
        ("MaxInotifyWatches", "100 009", 1000, 1_000_000),
        ("MaxInotifyInstances", "0b100000000000", 1024, 8192),
        ("MaxInotifyInstances", "0b1000000000000", 1024, 8192),
    ],
)
def test_int_range_validation_g_exception(param, val, min_val, max_val):
    with pytest.raises(ValidationException):
        validate_int_range(param, val, min_val, max_val)


@pytest.mark.parametrize(
    "param,val",
    [
        ("AdditionalDNSLookup", None),
        ("CoreDumps", False),
        ("RevealSensitiveInfoInTraces", True),
        ("UseFanotify", 0),
        ("KsvlaMode", 1),
        ("StartupTraces", ...),
    ],
)
def test_bool_validation_exception(param, val):
    with pytest.raises(ValidationException):
        validate_bool(param, val)


@pytest.mark.parametrize(
    "val",
    [
        StringIO("file-like object"),
        BytesIO(b"binary data"),
    ],
)
def test_validate_path_exception(val):
    with pytest.raises(ValidationException):
        validate_path("test_param", val)


@pytest.mark.parametrize(
    "param,val",
    [
        ("MachineId", None),
        ("MachineId", True),
    ],
)
def test_uuid_validation_exception(param, val):
    with pytest.raises(ValidationException):
        validate_uuid(param, val)


@pytest.mark.parametrize(
    "param,val",
    [
        ("PackageType", 123),
        ("PackageType", None),
    ],
)
def test_package_type_validation_exception(param, val):
    with pytest.raises(ValidationException):
        validate_package_type(param, val)


@pytest.mark.parametrize(
    "param,val",
    [
        ("Locale", None),
        ("Locale", True),
        ("Locale", 124),
    ],
)
def test_locale_validation_exception(param, val):
    with pytest.raises(ValidationException):
        validate_locale(param, val)


@pytest.mark.parametrize(
    "param,val,min_val,max_val",
    [
        ("PingInterval", 1000, 100, 10_000),
        ("PingInterval", 100.75, 100, 10_000),
        ("PingInterval", " 125.", 100, 10_000),
    ],
)
def test_int_range_validation_wd_exception(param, val, min_val, max_val):
    with pytest.raises(ValidationException):
        validate_int_range(param, val, min_val, max_val)


@pytest.mark.parametrize(
    "param,val",
    [
        ("ConnectTimeout", 0),
        ("ConnectTimeout", (100, "m")),
        ("ConnectTimeout", [50, "m"]),
        ("ConnectTimeout", None),
    ],
)
def test_time_out_validation_exception(param, val):
    with pytest.raises(ValidationException):
        validate_time_out(param, val)


@pytest.mark.parametrize(
    "param,val",
    [
        ("MaxVirtualMemory", 0.1),
        ("MaxVirtualMemory", 90.5),
        ("MaxVirtualMemory", None),
    ],
)
def test_memory_value_validation_exception(param, val):
    with pytest.raises(ValidationException):
        validate_memory_value(param, val)
