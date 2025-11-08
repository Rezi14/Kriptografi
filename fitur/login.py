# login.py
from data.data_handler import baca_data
import getpass
from clear_screen.clear_screen import clear_screen

def login_user():
    JUMLAH_PERCOBAAN = 3

    for i in range(JUMLAH_PERCOBAAN):
        clear_screen()
        print(f"=== LOGIN BANK ===")

        email_input = input("Masukkan Email Anda: ").strip()
        pin = getpass.getpass("Masukkan PIN: ").strip()

        nasabah_list = baca_data()

        for user in nasabah_list:
            email_dari_file = user['email'].strip()
            pin_dari_file = user['pin'].strip()

            if email_dari_file.lower() == email_input.lower() and pin_dari_file == pin:
                clear_screen()
                print(f"Login berhasil! Selamat datang, {user['nama']}.")
                return user

        # Jika sampai sini berarti gagal
        sisa = JUMLAH_PERCOBAAN - (i + 1)
        if sisa > 0:
            print(f"\nLogin gagal. Anda punya {sisa} percobaan lagi.")
            input("Tekan Enter untuk mencoba lagi...")
        else:
            clear_screen()
            print("Anda telah gagal login 3 kali. Program diblokir demi keamanan.")

    return None
