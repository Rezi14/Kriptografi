# tarik_tunai.py
from data.data_handler import baca_data, simpan_data
from decimal import Decimal, InvalidOperation
from clear_screen.clear_screen import clear_screen

def tarik_tunai(user):
    # idn = input("Masukkan ID Nasabah: ") <-- HAPUS
    nasabah = baca_data()

    try:
        jumlah = Decimal(input("Masukkan jumlah tarik: "))
    except InvalidOperation:
        clear_screen()
        print("Error: Jumlah harus berupa angka.")
        return

    if jumlah <= 0:
        clear_screen()
        print("Error: Jumlah tarik harus lebih dari nol.")
        return

    for n in nasabah:
        if n['nomor_rekening'] == user['nomor_rekening']: # <-- DIUBAH
            if n['saldo'] >= jumlah:
                n['saldo'] -= jumlah
                
                # PENTING: Update juga saldo di objek 'user'
                user['saldo'] = n['saldo']
                
                clear_screen()
                print(f"Tarik berhasil! Saldo baru: Rp{n['saldo']:,}")
                simpan_data(nasabah)
            else:
                clear_screen()
                print("Saldo tidak cukup!")
            return
    clear_screen()
    print("Error: Terjadi kesalahan, data user tidak ditemukan.")