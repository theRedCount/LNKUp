"""
Tests for evasion techniques
"""

import pytest
import base64
from generate_new import EvasionEngine


class TestEvasionEngine:
    """Test evasion engine functionality"""

    def test_amsi_bypass_generation(self, evasion_engine):
        """Test AMSI bypass code generation"""
        bypass = evasion_engine.generate_amsi_bypass()

        assert isinstance(bypass, str)
        assert len(bypass) > 0
        assert "try{" in bypass
        assert "}catch{}" in bypass
        # Check it contains some form of AMSI reference (obfuscated)
        assert any(x in bypass.lower() for x in ["amsi", "assembly", "reflection"])

    def test_jitter_generation(self, evasion_engine):
        """Test jitter command generation"""
        min_ms = 500
        max_ms = 3000

        jitter_cmd = evasion_engine.add_jitter(min_ms, max_ms)

        assert isinstance(jitter_cmd, str)
        assert "Start-Sle" in jitter_cmd  # Obfuscated sleep
        assert "Milli" in jitter_cmd
        assert "seconds" in jitter_cmd

        # Check jitter value is in range (extract from command)
        import re
        match = re.search(r'(\d+)', jitter_cmd)
        assert match
        jitter_value = int(match.group(1))
        assert min_ms <= jitter_value <= max_ms

    def test_command_obfuscation(self, evasion_engine):
        """Test PowerShell command obfuscation"""
        test_command = "Write-Host 'Hello World'"

        obfuscated = evasion_engine.obfuscate_command(test_command)

        # Should be base64 encoded
        assert isinstance(obfuscated, str)
        assert len(obfuscated) > 0

        # Verify it's valid base64
        try:
            decoded = base64.b64decode(obfuscated)
            # Should be UTF-16LE encoded
            decoded_str = decoded.decode('utf-16le')
            assert test_command in decoded_str
        except Exception:
            pytest.fail("Obfuscated command is not valid base64 UTF-16LE")

    def test_lnk_metadata_generation(self, evasion_engine):
        """Test LNK metadata generation"""
        metadata = evasion_engine.generate_lnk_metadata()

        assert isinstance(metadata, dict)
        assert "created" in metadata
        assert "modified" in metadata
        assert "accessed" in metadata
        assert "size" in metadata

        # Check dates are in the past
        from datetime import datetime
        now = datetime.now()
        assert metadata["created"] < now
        assert metadata["modified"] < now
        assert metadata["accessed"] < now

        # Check size is reasonable
        assert metadata["size"] > 0

    def test_amsi_bypass_uniqueness(self, evasion_engine):
        """Test that AMSI bypass generates different outputs"""
        bypasses = [evasion_engine.generate_amsi_bypass() for _ in range(10)]

        # Should have some variation (random variable names)
        unique_bypasses = set(bypasses)
        assert len(unique_bypasses) > 1, "AMSI bypass should generate unique outputs"

    def test_legitimate_targets_defined(self, evasion_engine):
        """Test that LOLBAS targets are properly defined"""
        assert hasattr(EvasionEngine, 'LEGITIMATE_TARGETS')
        assert isinstance(EvasionEngine.LEGITIMATE_TARGETS, dict)
        assert len(EvasionEngine.LEGITIMATE_TARGETS) > 0

        # Check common LOLBAS binaries
        targets = EvasionEngine.LEGITIMATE_TARGETS
        assert any(x in targets for x in ["explorer.exe", "rundll32.exe", "cmd.exe"])

    def test_amsi_patches_defined(self, evasion_engine):
        """Test that AMSI patches are defined"""
        assert hasattr(EvasionEngine, 'AMSI_PATCHES')
        assert isinstance(EvasionEngine.AMSI_PATCHES, list)
        assert len(EvasionEngine.AMSI_PATCHES) > 0

        # Check patches contain relevant keywords
        for patch in EvasionEngine.AMSI_PATCHES:
            assert isinstance(patch, str)
            assert len(patch) > 10
