from fitur.setor_tunai import setor_tunai
from fitur.tarik_tunai import tarik_tunai
from fitur.transfer import transfer
from fitur.tampilkan_nasabah import tampilkan_info_saldo 
from clear_screen.clear_screen import clear_screen

# Menu sekarang menerima argumen 'user'
def menu(user_yang_login):
    while True:
        print("╔════════════════════════════════════╗")
        print("║             Menu Bank              ║")
        print("╠════════════════════════════════════╣")
        print("║ ╔════════════════════════════════╗ ║")
        print("║ ║ 1. Tampilkan Info Saldo        ║ ║")
        print("║ ║ 2. Setor Tunai                 ║ ║")
        print("║ ║ 3. Tarik Tunai                 ║ ║")
        print("║ ║ 4. Transfer                    ║ ║")
        print("║ ║ 5. Keluar                      ║ ║")
        print("║ ╚════════════════════════════════╝ ║")
        print("╚════════════════════════════════════╝")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            # Kirim data user ke fungsi, jadi tidak perlu baca file lagi
            clear_screen()
            tampilkan_info_saldo(user_yang_login)
        elif pilihan == '2':
            clear_screen()
            # Kirim data user agar fungsinya tahu siapa yang setor
            setor_tunai(user_yang_login)
        elif pilihan == '3':
            clear_screen()
            tarik_tunai(user_yang_login)
        elif pilihan == '4':
            clear_screen()
            transfer(user_yang_login)
        elif pilihan == '5':
            clear_screen()
            print("Terima kasih telah menggunakan layanan kami.")
            break
        else:
            clear_screen()
            print("Pilihan tidak valid!")