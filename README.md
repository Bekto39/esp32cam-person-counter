# ESP32-CAM & YOLOv8 Kişi Sayma ve Doluluk Takip Sistemi

Bu proje, ESP32-CAM modülü ile yakalanan görüntülerin bir Ubuntu sunucusuna aktarılarak YOLOv8 derin öğrenme modeli ile gerçek zamanlı analiz edilmesini sağlar.

## 🚀 Mimari Yapı
1. **Uç Cihaz (ESP32-CAM):** Görüntüyü yakalar ve HTTP POST ile sunucuya iletir.
2. **Sunucu (Ubuntu/Flask):** Görüntüyü alır, YOLOv8 ile "insan" nesnelerini algılar ve sayar.
3. **Web Arayüzü:** Canlı video akışını ve anlık kişi sayısını kullanıcıya gösterir.

## 🛠️ Kurulum

### 1. Sunucu Tarafı (Linux VPS)
Sistemin izole çalışması ve paket çakışmalarını önlemek için **Sanal Ortam (venv)** kullanılmıştır.

```bash
# Bağımlılıkları kurun
sudo apt update && sudo apt install python3-venv libgl1 -y
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Sunucuyu başlatın
python3 index.py