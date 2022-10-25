import mysql.connector
import bcrypt
import base64
import binascii
from base64 import b64encode
import os
import secrets
import string
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Encryptor:

    fake_salt = binascii.unhexlify('aaef2d3f4d77ac66e9c5a6c3d8f921d1')

    def __init__(self, key: str):
        self.key = key
        self.fernet_key = self.get_fernet_key()
        self.fernet = Fernet(self.fernet_key)

    
    def get_fernet_key(self):
        hashing = PBKDF2HMAC(hashes.SHA256(), 32, self.fake_salt, 390000)
        fernet_key = base64.urlsafe_b64encode(hashing.derive(self.key.encode('utf-8')))    
        return fernet_key
    

    def encrypt_data(self, data):
        if not data == "":
            # If not empty
            if not isinstance(data, str):
                # If not string
                data = str(data)        

            # encrypt the data
            return self.fernet.encrypt(data.encode("utf-8"))
        return data


    def decrypt_data(self, data):
        if not data == "":
            # If not empty
            if not isinstance(data, str):
                # If not string
                return data

            # decrypt the data
            decrypted = self.fernet.decrypt(data.encode("utf-8"))
            return decrypted.decode("utf-8")
        return data        


    def encrypt_dict(self, dictionary: dict):
        encrypted_dict = {}
        for key in dictionary:
            value = dictionary[key]
            encrypted_dict[key] = self.encrypt_data(value)

        return encrypted_dict

    def decrypt_dict(self, dictionary: dict):
        decrypted = {}
        for key in dictionary:
            value = dictionary[key]
            decrypted[key] = self.decrypt_data(value)

        return decrypted
                



def decrypt_data(key, data):
    cipher = Fernet(get_fernet_key(key))
    decoded_data = cipher.decrypt(data.encode("utf-8")) 
    return decoded_data.decode("utf-8")

def encrypt_data(key, data):
    cipher = Fernet(get_fernet_key(key))
    encoded_data = cipher.encrypt(data.encode("utf-8")) 
    return encoded_data   

def get_fernet_key(key):
    salt = binascii.unhexlify('aaef2d3f4d77ac66e9c5a6c3d8f921d1')
    hashing = PBKDF2HMAC(hashes.SHA256(), 32, salt, 390000)
    fernet_key = base64.urlsafe_b64encode(hashing.derive(key.encode('utf-8')))    
    return fernet_key