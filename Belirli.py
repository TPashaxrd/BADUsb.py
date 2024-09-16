import os
import shutil
import time

# Hangi Klasör Kopyalansın?

source_folder = "C:\\Users\\B\\Desktop"

# USB'nin sürücüsü (kopyalama işlemi USB'ye yapılacak)
usb_drive_letter = "C:\\Users\\B\\Desktop"

def usb_watch():
    while True:
        # Sürücü Kontrol
        if os.path.exists(usb_drive_letter):
            print(f"{usb_drive_letter} bulundu!")
            
            # USB'deki hedef klasör
            target_folder = os.path.join(usb_drive_letter, "Yedek")
            
            # Eğer hedef klasör yoksa oluştur
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)
                print(f"Hedef klasör oluşturuldu: {target_folder}")

            # Kaynak klasördeki dosyaları hedef klasöre kopyala
            for root, dirs, files in os.walk(source_folder):
                for file in files:
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
            
            print("Dosyalar kopyalandı.")
            break  # Kopyalama tamamlandığında döngüyü durdur

        time.sleep(5)  # USB her 5 saniyede bir kontrol ediliyor

# USB izleme başlasın
usb_watch()




# Created by TPàshà
# DC: tpasha_ 
# https://github.com/TPashaxrd