import os
import shutil
import time

# Kaynak klasörler
source_folders = [
    "C:\\Users\\B\\Desktop",
    "C:\\Users\\B\\Downloads",
    "C:\\Users\\B\\Documents"  # Üçüncü kaynak klasörü | İsterseniz daha fazla açabilirsiniz.
]

# USB'nin sürücüsü (kopyalama işlemi USB'ye yapılacak)
usb_drive_letter = "G:\\"

def usb_watch():
    # USB Döngüsü
    while True:
        # USB sürücüsü mevcut mu diye kontrol et
        if os.path.exists(usb_drive_letter):
            print(f"{usb_drive_letter} bulundu!")

            target_folder = os.path.join(usb_drive_letter, "Yedek")

            # Eğer hedef klasör yoksa oluştur
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)
                print(f"Hedef klasör oluşturuldu: {target_folder}")

            # Her kaynak klasör için dosyaları kopyala
            for source_folder in source_folders:
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

                        # Dosyayı kopyaladığı yer
                        shutil.copy(file_path, dest_path)
                        print(f"Kopyalanan dosya: {file_path} -> {dest_path}")

            print("Dosyalar kopyalandı.")
            break  # Kopyalama tamamlandığında döngüyü durdur

        time.sleep(5)  # USB her 5 saniyede bir kontrol ediliyor

# USB izleme
usb_watch()
