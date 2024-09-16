from PIL import ImageGrab
import time

def take_screenshot(file_path):
    try:
        # Ekran görüntüsünden önce kısa bir süre bekle
        time.sleep(2)  # 2 saniye bekle

        # Ekran görüntüsü al
        screenshot = ImageGrab.grab()

        # Ekran görüntüsünü dosyaya kaydet
        screenshot.save(file_path)
        print(f"Ekran görüntüsü '{file_path}' dosyasına kaydedildi.")
    except Exception as e:
        print(f"Ekran görüntüsü alınırken hata oluştu: {e}")

# Ekran görüntüsü almak için dosya yolu
screenshot_path = "screenshot.png"

# Ekran görüntüsü al
take_screenshot(screenshot_path)


# Created by TPàshà
# https://github.com/TPashaxrd