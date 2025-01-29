
# Solana Wallet Manager

A PyQt5-based Solana wallet manager that allows you to generate, encrypt, and manage Solana wallets.

## Features
- Generate Solana wallets (public and private keys).
- Encrypt and save wallet data to a file.
- Decrypt and load wallet data from a file.
- Manage multiple wallets in a user-friendly GUI.

---

## Dependencies
The following dependencies are required to run the script:

- Python 3.9 or higher
- PyQt5
- cryptography
- solana-py (or solders for newer versions)

---

## Installation Instructions

### **Windows**
1. Install Python 3.9 or higher from [python.org](https://www.python.org/).
2. Open Command Prompt and install the required dependencies:
   ```bash
   pip install PyQt5 cryptography solana
   ```
3. Download the `walletmanager.py` script from this repository.
4. Run the script:
   ```bash
   python walletmanager.py
   ```

### **macOS**
1. Install Python 3.9 or higher (you can use [Homebrew](https://brew.sh/)):
   ```bash
   brew install python
   ```
2. Install the required dependencies:
   ```bash
   pip3 install PyQt5 cryptography solana
   ```
3. Download the `walletmanager.py` script from this repository.
4. Run the script:
   ```bash
   python3 walletmanager.py
   ```

---

## Troubleshooting
- If `PyQt5` installation hangs, try:
  ```bash
  pip install --only-binary :all: PyQt5
  ```
- If you're using an M1/M2 Mac, run the installation under Rosetta:
  ```bash
  arch -x86_64 pip install PyQt5
  ```
- If the `Keypair` module is not found, ensure you are using the correct version of the `solana` package:
  ```bash
  pip install solana==0.18.0
  ```

---

## Contributing
Feel free to open issues or submit pull requests to improve the project.

---

## License
This project is licensed under the MIT License.
```
