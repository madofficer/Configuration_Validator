import pytest

from framework.config import read_config
from framework.validators import validate_int_range, validate_bool, validate_path, validate_uuid, validate_package_type, \
    validate_locale, validate_time_out, validate_memory_value

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
    "Locale"
}

watchdog_fields = {
    "ConnectTimeout",
    "MaxVirtualMemory",
    "MaxMemory",
    "PingInterval"
}


@pytest.fixture
def valid_config():
    return read_config()


@pytest.mark.parametrize("param", ("General", "Watchdog"))
def test_required_sections(valid_config, param):
    assert param in valid_config


@pytest.mark.parametrize("param", general_fields)
def test_general_fields(valid_config, param):
    assert param in valid_config["General"]


@pytest.mark.parametrize("param", watchdog_fields)
def test_watchdog_fields(valid_config, param):
    assert param in valid_config["Watchdog"]


@pytest.mark.parametrize(
    "param,min_val,max_val",
    [
        ("ScanMemoryLimit", 1024, 8192),
        ("ExecArgMax", 10, 100),
        ("ExecEnvMax", 10, 100),
        ("MaxInotifyWatches", 1000, 1_000_000),
        ("MaxInotifyInstances", 1024, 8192)
    ]
)
def test_int_range_validation_g(valid_config, param, min_val, max_val):
    general = valid_config["General"]
    assert validate_int_range(param, general[param], min_val, max_val)


@pytest.mark.parametrize(
    "param,min_val,max_val",
    [("PingInterval", 100, 10_000)]
)
def test_int_range_validation_wd(valid_config, param, min_val, max_val):
    watchdog = valid_config["Watchdog"]
    assert validate_int_range(param, watchdog[param], min_val, max_val) == True


@pytest.mark.parametrize(
    "param", [
        "AdditionalDNSLookup",
        "CoreDumps",
        "RevealSensitiveInfoInTraces",
        "UseFanotify",
        "KsvlaMode",
        "StartupTraces"
    ]
)
def test_bool_validation(valid_config, param):
    general = valid_config["General"]
    assert validate_bool(param, general[param]) == True


@pytest.mark.parametrize(
    "param", ["CoreDumpsPath"]
)
def test_path_validation(valid_config, param):
    general = valid_config["General"]
    assert validate_path(param, general[param]) == False


@pytest.mark.parametrize(
    "param", ["MachineId"]
)
def test_uuid_validation(valid_config, param):
    general = valid_config["General"]
    assert validate_uuid(param, general[param]) == True


@pytest.mark.parametrize(
    "param", ["PackageType"]
)
def test_package_type_validation(valid_config, param):
    general = valid_config["General"]
    assert validate_package_type(param, general[param]) == True


@pytest.mark.parametrize(
    "param", ["Locale"]
)
def test_locale_validation(valid_config, param):
    general = valid_config["General"]
    assert validate_locale(param, general[param]) == True


@pytest.mark.parametrize(
    "param", ["ConnectTimeout"]
)
def test_time_out_validation(valid_config, param):
    watchdog = valid_config["Watchdog"]
    assert validate_time_out(param, watchdog[param]) == True


@pytest.mark.parametrize(
    "param", ["MaxVirtualMemory", "MaxMemory"]
)
def test_memory_value_validation(valid_config, param):
    watchdog = valid_config["Watchdog"]
    assert validate_memory_value(param, watchdog[param]) == True
