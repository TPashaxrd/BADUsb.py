import os
import shutil
import time

# Dokunma. Tüm C Kopyalanıyor. 
source_folder = "C:\\"

# Senin USB Sürücün. Kendi USB'nin Yolunu Gir
usb_drive_letter = "B:\\"

def usb_watch():
    # Sürekli USB izleme döngüsü
    while True:
        # USB sürücüsü (G:) mevcut mu diye kontrol et
        if os.path.exists(usb_drive_letter):
            print(f"{usb_drive_letter} bulundu!")
            
            # USB'deki hedef klasör
            target_folder = os.path.join(usb_drive_letter, "Yedek_Dosya")
            
            # Eğer hedef klasör yoksa oluştur
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)
                print(f"Hedef klasör oluşturuldu: {target_folder}")

            # Kaynak klasördeki tüm dosyaları ve klasörleri hedefe kopyala
            for root, dirs, files in os.walk(source_folder):
                for file in files:
                    try:
                        # Kopyalama sırasında klasör yapısını korumak için hedef yolu oluştur
                        relative_path = os.path.relpath(root, source_folder)
                        dest_dir = os.path.join(target_folder, relative_path)
                        
                        if not os.path.exists(dest_dir):
                            os.makedirs(dest_dir)
                        
                        file_path = os.path.join(root, file)
                        dest_path = os.path.join(dest_dir, file)
                        
                        # Dosyayı kopyala
                        shutil.copy(file_path, dest_path)
                        print(f"Kopyalanan dosya: {file_path} -> {dest_path}")
                    except Exception as e:
                        print(f"Dosya kopyalama hatası: {file_path}. Hata: {e}")
            
            print("Dosyalar kopyalandı.")
            break  # Kopyalama tamamlandığında döngüyü durdur

        time.sleep(5)  # USB her 5 saniyede bir kontrol ediliyor

# USB izleme başlasın
usb_watch()


# Created by TPàshà
# DC: tpasha_ 
# https://github.com/TPashaxrd