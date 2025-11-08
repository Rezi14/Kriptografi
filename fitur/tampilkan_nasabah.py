# tampilkan_nasabah.py
from clear_screen.clear_screen import clear_screen
# Kita ubah fungsinya untuk hanya menampilkan info user yang login
def tampilkan_info_saldo(user):
    print("=== Info Akun Anda ===")
    print(f"No. Rek : {user['nomor_rekening']}") # <-- DIUBAH
    print(f"Nama    : {user['nama']}")
    print(f"Saldo   : Rp{user['saldo']:,}")
    
    input("\nKlik Enter Untuk Kembali ")
    clear_screen()
    # Kita tidak menampilkan PIN demi keamanan