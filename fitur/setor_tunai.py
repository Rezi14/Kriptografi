# setor_tunai.py
from data.data_handler import baca_data, simpan_data
from decimal import Decimal, InvalidOperation
from clear_screen.clear_screen import clear_screen

# Fungsi sekarang menerima 'user' yang sedang login
def setor_tunai(user):
    # Tidak perlu tanya ID lagi! Kita sudah punya dari 'user'
    # idn = input("Masukkan ID Nasabah: ") <-- HAPUS

    nasabah = baca_data()
    
    try:
        jumlah = Decimal(input("Masukkan jumlah setor: "))
    except InvalidOperation:
        clear_screen()
        print("Error: Jumlah harus berupa angka.")
        return

    if jumlah <= 0:
        clear_screen()
        print("Error: Jumlah setor harus lebih dari nol.")
        return

    # Cari data user di list lengkap untuk di-update
    for n in nasabah:
        if n['nomor_rekening'] == user['nomor_rekening']: # <-- DIUBAH
            n['saldo'] += jumlah
            
            # Update juga saldo di objek 'user' yang dipegang menu
            user['saldo'] = n['saldo'] 
            
            clear_screen()
            print(f"Setor berhasil! Saldo baru: Rp{n['saldo']:,}")
            simpan_data(nasabah)
            return
    
    # Seharusnya tidak akan pernah sampai sini jika user sudah login
    clear_screen()
    print("Error: Terjadi kesalahan, data user tidak ditemukan.")