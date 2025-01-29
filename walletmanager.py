from PyQt5 import QtWidgets, QtGui, QtCore
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from solders.keypair import Keypair
import base64
import os
import json

class WalletManager(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.wallets = []

    def initUI(self):
        self.setWindowTitle("Solana Wallet Manager")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.wallet_table = QtWidgets.QTableWidget()
        self.wallet_table.setColumnCount(4)
        self.wallet_table.setHorizontalHeaderLabels(["Wallet Name", "Public Key", "Private Key", "Actions"])
        self.layout.addWidget(self.wallet_table)

        self.add_wallet_btn = QtWidgets.QPushButton("+ Add Wallet")
        self.add_wallet_btn.clicked.connect(self.add_wallet)
        self.layout.addWidget(self.add_wallet_btn)

        self.generate_wallet_btn = QtWidgets.QPushButton("Generate Wallet")
        self.generate_wallet_btn.clicked.connect(self.generate_wallet)
        self.layout.addWidget(self.generate_wallet_btn)

        self.encrypt_save_btn = QtWidgets.QPushButton("Encrypt and Save")
        self.encrypt_save_btn.clicked.connect(self.encrypt_and_save)
        self.layout.addWidget(self.encrypt_save_btn)

        self.decrypt_load_btn = QtWidgets.QPushButton("Open and Decrypt")
        self.decrypt_load_btn.clicked.connect(self.decrypt_and_load)
        self.layout.addWidget(self.decrypt_load_btn)

    def add_wallet(self):
        row_position = self.wallet_table.rowCount()
        self.wallet_table.insertRow(row_position)

        for col in range(3):
            self.wallet_table.setItem(row_position, col, QtWidgets.QTableWidgetItem(""))

        remove_btn = QtWidgets.QPushButton("Remove")
        remove_btn.clicked.connect(lambda _, r=row_position: self.remove_wallet(r))
        self.wallet_table.setCellWidget(row_position, 3, remove_btn)

    def generate_wallet(self):
        keypair = Keypair()
        public_key = str(keypair.pubkey())  # Updated to use pubkey()
        private_key = base64.b64encode(bytes(keypair)).decode()  # Updated to use bytes(keypair)

        row_position = self.wallet_table.rowCount()
        self.wallet_table.insertRow(row_position)
        self.wallet_table.setItem(row_position, 0, QtWidgets.QTableWidgetItem("Generated Wallet"))
        self.wallet_table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(public_key))
        self.wallet_table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(private_key))

        remove_btn = QtWidgets.QPushButton("Remove")
        remove_btn.clicked.connect(lambda _, r=row_position: self.remove_wallet(r))
        self.wallet_table.setCellWidget(row_position, 3, remove_btn)

    def remove_wallet(self, row):
        self.wallet_table.removeRow(row)

    def encrypt_and_save(self):
        password, ok = QtWidgets.QInputDialog.getText(self, "Password", "Enter encryption password:", QtWidgets.QLineEdit.Password)
        if not ok or not password:
            return

        wallets = []
        for row in range(self.wallet_table.rowCount()):
            name_item = self.wallet_table.item(row, 0)
            public_key_item = self.wallet_table.item(row, 1)
            private_key_item = self.wallet_table.item(row, 2)
            if name_item and public_key_item and private_key_item:
                wallets.append({
                    "name": name_item.text(),
                    "public_key": public_key_item.text(),
                    "private_key": private_key_item.text()
                })

        encrypted_data = self.encrypt_data(json.dumps(wallets), password)
        options = QtWidgets.QFileDialog.Options()
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Encrypted Wallets", "", "Wallet Files (*.solwallet);;All Files (*)", options=options)
        if file_path:
            with open(file_path, 'wb') as f:
                f.write(encrypted_data)

    def decrypt_and_load(self):
        options = QtWidgets.QFileDialog.Options()
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Encrypted Wallets", "", "Wallet Files (*.solwallet);;All Files (*)", options=options)
        if not file_path:
            return

        password, ok = QtWidgets.QInputDialog.getText(self, "Password", "Enter decryption password:", QtWidgets.QLineEdit.Password)
        if not ok or not password:
            return

        with open(file_path, 'rb') as f:
            encrypted_data = f.read()

        try:
            decrypted_data = json.loads(self.decrypt_data(encrypted_data, password))
            self.wallet_table.setRowCount(0)
            for wallet in decrypted_data:
                row_position = self.wallet_table.rowCount()
                self.wallet_table.insertRow(row_position)
                self.wallet_table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(wallet["name"]))
                self.wallet_table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(wallet["public_key"]))
                self.wallet_table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(wallet["private_key"]))

                remove_btn = QtWidgets.QPushButton("Remove")
                remove_btn.clicked.connect(lambda _, r=row_position: self.remove_wallet(r))
                self.wallet_table.setCellWidget(row_position, 3, remove_btn)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"Decryption failed. Incorrect password or corrupted file.\nError: {str(e)}")

    def encrypt_data(self, data, password):
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = kdf.derive(password.encode())
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        padded_data = data + ' ' * (16 - len(data) % 16)
        ciphertext = encryptor.update(padded_data.encode()) + encryptor.finalize()
        return salt + iv + ciphertext

    def decrypt_data(self, encrypted_data, password):
        salt = encrypted_data[:16]
        iv = encrypted_data[16:32]
        ciphertext = encrypted_data[32:]

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = kdf.derive(password.encode())

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        return padded_data.rstrip().decode()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = WalletManager()
    window.show()
    app.exec_()