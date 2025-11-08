# setup_keys.py
import os
import csv
import io
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

# --- Bagian 1: Pembuatan Kunci ---

print("Membuat RSA key pair (2048 bit)...")
# 1. Buat RSA Key Pair (Private & Public)
key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()

# 2. Simpan RSA keys ke file
with open('keys/private.pem', 'wb') as f:
    f.write(private_key)
print("  -> private.pem")

with open('keys/public.pem', 'wb') as f:
    f.write(public_key)
print("  -> public.pem")

# 3. Buat Kunci AES (Symmetric Key)
print("Membuat AES key (256 bit)...")
aes_key = get_random_bytes(32) # 256-bit = 32 bytes

# 4. Enkripsi Kunci AES menggunakan RSA Public Key
print("Mengenkripsi AES key dengan RSA public key...")
rsa_public_key_obj = RSA.import_key(public_key)
cipher_rsa = PKCS1_OAEP.new(rsa_public_key_obj)
encrypted_aes_key = cipher_rsa.encrypt(aes_key)

# 5. Simpan Kunci AES yang sudah terenkripsi
with open('enc/aes_key.enc', 'wb') as f:
    f.write(encrypted_aes_key)
print("  -> aes_key.enc (Kunci AES terenkripsi)")

# --- Bagian 2: Migrasi Data CSV ---

FILE_CSV_LAMA = 'data/nasabah.csv'
FILE_ENKRIPSI_BARU = 'enc/nasabah.enc'

print(f"\nMemigrasi data dari {FILE_CSV_LAMA} ke {FILE_ENKRIPSI_BARU}...")

if not os.path.exists(FILE_CSV_LAMA):
    print(f"Error: File {FILE_CSV_LAMA} tidak ditemukan. Lewati migrasi.")
    print("Setup Kunci Selesai.")
    exit()

try:
    # 1. Baca data plain text dari CSV
    with open(FILE_CSV_LAMA, mode='r', encoding='utf-8') as file:
        csv_content = file.read()
    
    csv_bytes = csv_content.encode('utf-8')

    # 2. Enkripsi data CSV menggunakan Kunci AES (GCM Mode)
    cipher_aes_gcm = AES.new(aes_key, AES.MODE_GCM)
    ciphertext, tag = cipher_aes_gcm.encrypt_and_digest(csv_bytes)
    
    # 3. Simpan data terenkripsi (nonce + tag + ciphertext)
    with open(FILE_ENKRIPSI_BARU, 'wb') as f:
        f.write(cipher_aes_gcm.nonce) # 16 bytes
        f.write(tag)                 # 16 bytes
        f.write(ciphertext)

    print(f"Migrasi sukses! Data telah dienkripsi ke {FILE_ENKRIPSI_BARU}.")

except Exception as e:
    print(f"Terjadi error saat migrasi data: {e}")

print("\nSetup Selesai.")

