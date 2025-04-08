import pytest

from framework.config import read_config


@pytest.fixture
def valid_config():
    return read_config(r"E:\pets\KasperskyValidate\config\config.ini")

def test_required_sections(valid_config):
    assert "General" in valid_config
    assert "Watchdog" in valid_config