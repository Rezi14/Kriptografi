# transfer.py
from data.data_handler import baca_data, simpan_data
from decimal import Decimal, InvalidOperation
from clear_screen.clear_screen import clear_screen

def transfer(user_pengirim): # User yang login adalah pengirim
    nasabah = baca_data()
    
    # dari = input("Masukkan ID Pengirim: ") <-- HAPUS
    try:
        ke = input("Masukkan Nomor Rekening Penerima: ")
    except ValueError:
        clear_screen()
        print("Error: Jumlah harus berupa angka.")
        return
    
    if ke == user_pengirim['nomor_rekening']: # <-- DIUBAH
        clear_screen()
        print("Error: Anda tidak bisa transfer ke diri sendiri.")
        return

    try:
        jumlah = Decimal(input("Masukkan jumlah transfer: "))
    except InvalidOperation:
        clear_screen()
        print("Error: Jumlah harus berupa angka.")
        return

    if jumlah <= 0:
        clear_screen()
        print("Error: Jumlah transfer harus lebih dari nol.")
        return

    # Cari pengirim dan penerima di database
    pengirim_db = None
    penerima_db = None
    
    for n in nasabah:
        # 3. Ubah logika pencarian
        if n['nomor_rekening'] == user_pengirim['nomor_rekening']: # <-- DIUBAH
            pengirim_db = n
        if n['nomor_rekening'] == ke: # <-- DIUBAH
            penerima_db = n

    if not pengirim_db or not penerima_db:
        # 4. Ubah pesan error
        clear_screen()
        print("Nomor rekening pengirim atau penerima tidak ditemukan.") # <-- DIUBAH
        return

    if pengirim_db['saldo'] < jumlah:
        clear_screen()
        print("Saldo pengirim tidak cukup.")
        return

    pengirim_db['saldo'] -= jumlah
    penerima_db['saldo'] += jumlah
    
    user_pengirim['saldo'] = pengirim_db['saldo']

    simpan_data(nasabah)
    clear_screen()
    print(f"Transfer ke {penerima_db['nama']} berhasil!")
    print(f"Saldo baru Anda: Rp{user_pengirim['saldo']:,}")