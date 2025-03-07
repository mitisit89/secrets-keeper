from cryptography.fernet import Fernet

secret_key = Fernet.generate_key()

with open("secret.key", "wb") as key_file:
    key_file.write(secret_key)
