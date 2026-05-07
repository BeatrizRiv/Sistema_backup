from cryptography.fernet import Fernet

clave = Fernet.generate_key()

fernet = Fernet(clave)