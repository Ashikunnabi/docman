from cryptography.fernet import Fernet
from django.conf import settings


class Encryption:
    def __init__(self) -> None:
        self.key = settings.ENCRYPTION_KEY

    def key_create(self):
        key = Fernet.generate_key()
        return key

    def key_write(self, key, key_name):
        with open(key_name, "wb") as mykey:
            mykey.write(key)

    def file_encrypt(self, original_file, encrypted_file):
        fernet = Fernet(self.key)

        with open(original_file, "rb") as file:
            original = file.read()

        encrypted = fernet.encrypt(original)

        with open(encrypted_file, "wb") as file:
            file.write(encrypted)

    def file_decrypt(self, encrypted_file, decrypted_file):
        fernet = Fernet(self.key)

        with open(encrypted_file, "rb") as file:
            encrypted = file.read()

        decrypted = fernet.decrypt(encrypted)

        with open(decrypted_file, "wb") as file:
            file.write(decrypted)
