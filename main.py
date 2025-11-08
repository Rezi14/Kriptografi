# main.py
from fitur.menu import menu
from fitur.login import login_user
from clear_screen.clear_screen import clear_screen

if __name__ == '__main__':
    clear_screen()
    print("=== Selamat Datang di Bank ===")

    user_terlogin = login_user()

    if user_terlogin:
        menu(user_terlogin)
    else:
        print("\nSilakan hubungi admin untuk membuka blokir akun Anda.")
