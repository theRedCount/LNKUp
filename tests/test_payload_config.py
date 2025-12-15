"""
Tests for payload configuration and validation
"""

import pytest
from pydantic import ValidationError
from generate_new import PayloadConfig, EvasionConfig, ExfiltrationMethod


class TestPayloadConfig:
    """Test payload configuration validation"""

    def test_valid_ntlm_config(self, ntlm_payload_config):
        """Test valid NTLM payload configuration"""
        assert ntlm_payload_config.ntlm_capture is True
        assert len(ntlm_payload_config.additional_vars) == 0
        assert len(ntlm_payload_config.exfil_methods) > 0

    def test_valid_env_exfil_config(self, env_exfil_payload_config):
        """Test valid environment exfiltration configuration"""
        assert env_exfil_payload_config.ntlm_capture is False
        assert len(env_exfil_payload_config.additional_vars) > 0
        assert "USERNAME" in env_exfil_payload_config.additional_vars

    def test_empty_command_validation(self, basic_evasion_config, basic_exfil_method):
        """Test that empty command is rejected"""
        with pytest.raises(ValidationError):
            PayloadConfig(
                target_command=[],  # Empty command
                exfil_methods=[basic_exfil_method],
                evasion=basic_evasion_config,
                additional_vars=["USERNAME"],
                ntlm_capture=False
            )

    def test_empty_exfil_methods_validation(self, basic_evasion_config):
        """Test that empty exfiltration methods are rejected"""
        with pytest.raises(ValidationError):
            PayloadConfig(
                target_command=["whoami"],
                exfil_methods=[],  # Empty
                evasion=basic_evasion_config,
                additional_vars=["USERNAME"],
                ntlm_capture=False
            )

    def test_no_vars_and_no_ntlm_validation(self, basic_evasion_config, basic_exfil_method):
        """Test that config without vars or NTLM is rejected"""
        with pytest.raises(ValidationError):
            PayloadConfig(
                target_command=["whoami"],
                exfil_methods=[basic_exfil_method],
                evasion=basic_evasion_config,
                additional_vars=[],  # No vars
                ntlm_capture=False  # No NTLM
            )

    def test_ntlm_without_vars_allowed(self, basic_evasion_config, basic_exfil_method):
        """Test that NTLM-only config is valid"""
        config = PayloadConfig(
            target_command=["whoami"],
            exfil_methods=[basic_exfil_method],
            evasion=basic_evasion_config,
            additional_vars=[],
            ntlm_capture=True
        )
        assert config.ntlm_capture is True

    def test_vars_without_ntlm_allowed(self, basic_evasion_config, basic_exfil_method):
        """Test that env vars without NTLM is valid"""
        config = PayloadConfig(
            target_command=["whoami"],
            exfil_methods=[basic_exfil_method],
            evasion=basic_evasion_config,
            additional_vars=["USERNAME"],
            ntlm_capture=False
        )
        assert len(config.additional_vars) > 0


class TestEvasionConfig:
    """Test evasion configuration"""

    def test_default_evasion_config(self):
        """Test default evasion configuration"""
        config = EvasionConfig()

        assert config.anti_amsi is True
        assert config.anti_etw is True
        assert config.legitimate_target is True
        assert config.randomize_size is True

    def test_custom_jitter_config(self):
        """Test custom jitter configuration"""
        config = EvasionConfig(
            jitter_min=1000,
            jitter_max=5000
        )

        assert config.jitter_min == 1000
        assert config.jitter_max == 5000


class TestExfiltrationMethod:
    """Test exfiltration method configuration"""

    def test_unc_exfil_method(self, basic_exfil_method):
        """Test UNC exfiltration method"""
        assert basic_exfil_method.type == "unc"
        assert basic_exfil_method.host == "192.168.1.100"
        assert basic_exfil_method.compress is True

    def test_webdav_exfil_method(self, webdav_exfil_method):
        """Test WebDAV exfiltration method"""
        assert webdav_exfil_method.type == "http"
        assert webdav_exfil_method.ssl is True
        assert webdav_exfil_method.port == 443
        assert webdav_exfil_method.path == "/webdav"

    def test_dns_exfil_method(self):
        """Test DNS exfiltration method"""
        exfil = ExfiltrationMethod(
            type="dns",
            host="attacker.com",
            ssl=False,
            compress=True
        )

        assert exfil.type == "dns"
        assert exfil.host == "attacker.com"
