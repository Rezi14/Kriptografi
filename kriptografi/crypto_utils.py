# crypto_utils.py
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP

# Cache kunci AES di memori agar tidak perlu dekripsi RSA berulang kali
_AES_KEY_CACHE = None

def load_aes_key():
    """
    Mendekripsi dan me-load kunci AES ke memori.
    Menggunakan RSA private key untuk mendekripsi 'aes_key.enc'.
    """
    global _AES_KEY_CACHE
    if _AES_KEY_CACHE:
        return _AES_KEY_CACHE

    try:
        # 1. Load RSA Private Key (untuk dekripsi)
        with open('keys/private.pem', 'rb') as f:
            private_key_data = f.read()
            private_key = RSA.import_key(private_key_data)

        # 2. Load Kunci AES yang Terenkripsi
        with open('enc/aes_key.enc', 'rb') as f:
            encrypted_aes_key = f.read()

        # 3. Dekripsi Kunci AES menggunakan RSA
        cipher_rsa = PKCS1_OAEP.new(private_key)
        aes_key = cipher_rsa.decrypt(encrypted_aes_key)

        _AES_KEY_CACHE = aes_key
        return aes_key

    except FileNotFoundError:
        print("Error: File kunci ('private.pem' atau 'aes_key.enc') tidak ditemukan.")
        exit(1)
    except Exception as e:
        print(f"Error saat me-load kunci: {e}")
        exit(1)

def encrypt_data(data_bytes, key):
    """
    Mengenkripsi data (bytes) menggunakan AES-GCM.
    Mengembalikan tuple: (ciphertext, tag, nonce)
    """
    cipher_aes_gcm = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher_aes_gcm.encrypt_and_digest(data_bytes)
    return ciphertext, tag, cipher_aes_gcm.nonce

def decrypt_data(ciphertext, tag, nonce, key):
    """
    Mendekripsi data (bytes) menggunakan AES-GCM.
    Akan memverifikasi tag (integritas data).
    Mengembalikan data bytes asli (plaintext).
    """
    try:
        cipher_aes_gcm = AES.new(key, AES.MODE_GCM, nonce=nonce)
        decrypted_bytes = cipher_aes_gcm.decrypt_and_verify(ciphertext, tag)
        return decrypted_bytes
    except ValueError:
        print("Error: Gagal mendekripsi data! Kunci salah atau data korup.")
        return None
    except Exception as e:
        print(f"Error saat dekripsi: {e}")
        return None