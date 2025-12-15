# LNKUp Test Suite

Comprehensive test suite for LNKUp payload generator using pytest.

## 📋 Test Structure

```
tests/
├── conftest.py              # Pytest fixtures and configuration
├── test_evasion.py          # Evasion engine tests
├── test_payload_config.py   # Configuration validation tests
├── test_exfiltration.py     # Exfiltration method tests
├── test_lnk_generator.py    # LNK generation tests
└── README.md                # This file
```

## 🚀 Running Tests

### Run All Tests

```bash
# Activate virtual environment
source .venv/bin/activate

# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=. --cov-report=html
```

### Run Specific Test Files

```bash
# Test evasion engine only
pytest tests/test_evasion.py -v

# Test configuration validation only
pytest tests/test_payload_config.py -v

# Test exfiltration methods only
pytest tests/test_exfiltration.py -v

# Test LNK generation only
pytest tests/test_lnk_generator.py -v
```

### Run Specific Test Classes or Functions

```bash
# Run specific test class
pytest tests/test_evasion.py::TestEvasionEngine -v

# Run specific test function
pytest tests/test_evasion.py::TestEvasionEngine::test_amsi_bypass_generation -v
```

## 📊 Test Coverage

### Current Coverage Areas

1. **Evasion Engine** (`test_evasion.py`)
   - AMSI bypass generation
   - Jitter command generation
   - PowerShell obfuscation
   - LNK metadata generation
   - LOLBAS target definitions

2. **Configuration Validation** (`test_payload_config.py`)
   - Pydantic model validation
   - Required field checks
   - NTLM configuration
   - Environment variable configuration
   - Hybrid configuration

3. **Exfiltration Methods** (`test_exfiltration.py`)
   - UNC path generation
   - HTTP/HTTPS URL generation
   - WebDAV path generation
   - DNS exfiltration encoding
   - Path compression
   - Special character handling

4. **LNK Generation** (`test_lnk_generator.py`)
   - Payload building
   - Target generation
   - LOLBAS proxy execution
   - Icon path generation
   - Cross-platform compatibility

### Generate Coverage Report

```bash
# HTML coverage report
pytest tests/ --cov=. --cov-report=html

# Open report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

## 🎯 Test Examples

### Example 1: Testing AMSI Bypass

```python
def test_amsi_bypass_generation(evasion_engine):
    """Test AMSI bypass code generation"""
    bypass = evasion_engine.generate_amsi_bypass()

    assert isinstance(bypass, str)
    assert len(bypass) > 0
    assert "try{" in bypass
```

### Example 2: Testing Payload Configuration

```python
def test_valid_ntlm_config(ntlm_payload_config):
    """Test valid NTLM payload configuration"""
    assert ntlm_payload_config.ntlm_capture is True
    assert len(ntlm_payload_config.exfil_methods) > 0
```

### Example 3: Testing Exfiltration

```python
def test_unc_path_generation(basic_exfil_method):
    """Test UNC path generation"""
    exfil = Exfiltrator(basic_exfil_method)
    path = exfil.generate_unc_path("test_data")

    assert path.startswith("\\\\")
    assert path.endswith(".ico")
```

## 🔧 Fixtures Available

Common fixtures defined in `conftest.py`:

- `test_output_dir` - Temporary output directory
- `basic_evasion_config` - Basic evasion configuration
- `basic_exfil_method` - UNC exfiltration method
- `ntlm_payload_config` - NTLM capture configuration
- `env_exfil_payload_config` - Environment exfil configuration
- `hybrid_payload_config` - Hybrid payload configuration
- `webdav_exfil_method` - WebDAV exfiltration method
- `evasion_engine` - EvasionEngine instance

## 🐛 Debugging Tests

### Run Tests with Print Output

```bash
pytest tests/ -v -s
```

### Run Tests with Debugger

```bash
pytest tests/ --pdb
```

### Run Failed Tests Only

```bash
# Run only tests that failed in last run
pytest tests/ --lf

# Run failed tests first, then others
pytest tests/ --ff
```

## ✅ Test Checklist

Before committing code, ensure:

- [ ] All tests pass: `pytest tests/`
- [ ] No warnings: `pytest tests/ -v`
- [ ] Coverage is adequate: `pytest tests/ --cov=.`
- [ ] New features have tests
- [ ] Edge cases are covered
- [ ] Error handling is tested

## 📝 Writing New Tests

### Test Naming Convention

- Test files: `test_<module>.py`
- Test classes: `Test<ClassName>`
- Test functions: `test_<description>`

### Example Template

```python
"""
Tests for new feature
"""

import pytest
from generate_new import NewFeature


class TestNewFeature:
    """Test new feature functionality"""

    def test_basic_functionality(self):
        """Test basic usage"""
        feature = NewFeature()
        result = feature.do_something()

        assert result is not None
        assert isinstance(result, str)

    def test_edge_case(self):
        """Test edge case handling"""
        feature = NewFeature()

        with pytest.raises(ValueError):
            feature.do_something_invalid()
```

## 🚨 Known Limitations

1. **Platform-Specific Tests**
   - Some LNK generation tests require specific platform features
   - Tests use `pytest.skipif` for platform compatibility

2. **External Dependencies**
   - Tests for actual LNK file creation require `pylnk3` or `pywin32`
   - Some tests may be skipped if dependencies are unavailable

3. **Mock Data**
   - Tests use mock configurations and don't perform actual network operations
   - Real payload testing should be done in isolated environment

## 🔗 Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      - name: Run tests
        run: pytest tests/ --cov=. --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

## 📚 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest Fixtures](https://docs.pytest.org/en/stable/fixture.html)
- [Coverage.py](https://coverage.readthedocs.io/)
- [Pydantic Testing](https://pydantic-docs.helpmanual.io/usage/models/#testing)

---

**For questions or issues with tests, consult the main documentation or open an issue.**
