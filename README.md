# 🔐 CyberSec ToolKit
## 📝Overview

CyberSec Toolkit is a Python-based project that provides a set of tools for cybersecurity learning and concept practice.  
It includes installation scripts, a CLI launcher, and a modular design for extending functionality.

## Project Note
- This project is a **final graduation project** of student **Abdalla Azam**.  
- Developed as part of academic requirements to demonstrate skills in **Programming, Python, cybersecurity concepts, and software engineering practices**.
---

## ✨Features
- 🚀 **Port Scanning** with service/version detection  
- 🌐 **Network Reconnaissance**  
- 🔑 **Password Utilities** (hashing, brute-force testing, etc.)  
- 🔒 **Cryptography Tools** (AES encryption, decryption, hashing)  
- 📊 Beautiful and interactive terminal UI using `rich`  
- 🎨 ASCII Banners with `pyfiglet`  
- ⚡ Multi-threaded execution for fast performance

---
## 📂 Project Structure 
```
CyberSec-ToolKit/
├── CaesarCipher.py # Caesar cipher utility (encrypt / decrypt text)
├── file_Enc_Dec.py # File encryption/decryption (AES, password-derived keys)
├── hashGenerator.py # Generate common hashes (MD5, SHA1, SHA256, ...)
├── passwordGenerator.py # Password generator (custom length / charset)
├── passwordChecker.py # Password strength checker / feedback tool
├── portScanner.py # Multi-threaded port scanner with banner/version detection
├── vt_antivirus.py # VirusTotal API helper / scan-check integration
├── __init__.py # Package entrypoint (runs the toolkit CLI)
├── install.sh # Installer script: installs deps, creates cybersec launcher/alias
├── README.md
└── LICENSE # Project license (MIT)
```
---
  
## 🛠️ Requirements
- Python 3.13.1 or later
- Required libraries:
  - `requests`
  - `rich`
  - `pyfiglet`
  - `cryptography`
Required dependencies will installed after:
```bash
./install.sh
```

---

## 🏗️Installation

1. Clone the Repository:

   Clone the GitHub repository to your local machine:

   ```bash
   git clone https://github.com/Hussein-Ibrahim043/CyberSec.git

2. Run the provided install.sh script to install the tool and set up an alias for easy usage.
   ```bash
   cd CyberSec
   ```
3. Run the following command to make the script executable:
   ```bash
    chmod +x install.sh
    ```
5.  Run install.sh :
    ```bash
    sudo bash install.sh
    ```
   
    ```bash
    sudo bash install.sh
    ```
   
The alias `cybersec` will be created for the tool.

---

## 🚀 How to Use
   - Launch the CyberSec ToolKit from the terminal:
```bash
   cybersec
```
     
        
---

## 🛡️ Troubleshooting

**Error: Command '['python3', '.py']' returned non-zero exit status 2.** : Ensure that you use aliac 'cybersec' under CyberSec/ directory.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

---

## Author
- **Hussein Ibrahim (Instructor)**
  - GitHub (https://github.com/Hussein-Ibrahim043)
  - LinkedIn (https://linkedin.com/in/hussein-ibrahim043)
- **Abdalla Azzam (Student)**
