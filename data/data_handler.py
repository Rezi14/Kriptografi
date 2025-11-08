# data_handler.py
import csv
import io
import os
from decimal import Decimal
from kriptografi.crypto_utils import load_aes_key, encrypt_data, decrypt_data

# Ganti nama file database ke file terenkripsi
FILE_NASABAH = 'enc/nasabah.enc'
AES_KEY = load_aes_key() # Load kunci saat modul di-import

def baca_data():
    nasabah = []
    
    if not os.path.exists(FILE_NASABAH):
        # Jika file belum ada (misal, program jalan pertama kali), 
        # kembalikan list kosong agar bisa dibuat baru oleh simpan_data.
        return []
    
    try:
        # 1. Baca data terenkripsi (nonce, tag, ciphertext)
        with open(FILE_NASABAH, mode='rb') as file:
            nonce = file.read(16)
            tag = file.read(16)
            ciphertext = file.read()
            
            if not ciphertext: # File ada tapi kosong
                return []

        # 2. Dekripsi data
        decrypted_csv_bytes = decrypt_data(ciphertext, tag, nonce, AES_KEY)
        if decrypted_csv_bytes is None:
            print("Gagal memuat data. File mungkin korup.")
            return []
            
        decrypted_csv_string = decrypted_csv_bytes.decode('utf-8')

        # 3. Parsing CSV dari string yang sudah didekripsi
        # Gunakan io.StringIO untuk membaca string seolah-olah file
        file_buffer = io.StringIO(decrypted_csv_string)
        reader = csv.DictReader(file_buffer)
        for row in reader:
            # Ubah saldo menjadi integer, pin tetap string
            row['saldo'] = Decimal(row['saldo'])
            nasabah.append(row)
            
    except FileNotFoundError:
        # Ini seharusnya sudah ditangani di atas, tapi sebagai pengaman
        print(f"File {FILE_NASABAH} tidak ditemukan.")
        return []
    except Exception as e:
        print(f"Terjadi error saat membaca data terenkripsi: {e}")
        return []
    
    return nasabah

def simpan_data(nasabah):
    try:
        # 1. Ubah data dictionary kembali ke format string CSV
        # Gunakan io.StringIO sebagai 'file' di memori
        file_buffer = io.StringIO()
        fieldnames = ['nomor_rekening', 'nama', 'saldo', 'pin', 'email']
        writer = csv.DictWriter(file_buffer, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(nasabah)
        
        csv_string = file_buffer.getvalue()
        csv_bytes = csv_string.encode('utf-8')

        # 2. Enkripsi string CSV
        ciphertext, tag, nonce = encrypt_data(csv_bytes, AES_KEY)

        # 3. Simpan data terenkripsi (nonce + tag + ciphertext)
        with open(FILE_NASABAH, mode='wb') as file:
            file.write(nonce)
            file.write(tag)
            file.write(ciphertext)
            
    except Exception as e:
        print(f"Terjadi error saat menyimpan data terenkripsi: {e}")