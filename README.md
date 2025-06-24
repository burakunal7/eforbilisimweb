# Efor Bilişim - IT Destek ve Donanım Hizmetleri

## 📋 Proje Hakkında

Efor Bilişim, profesyonel IT destek ve donanım hizmetleri sunan bir şirketin web sitesidir. Flask framework kullanılarak geliştirilmiş modern, responsive ve kullanıcı dostu bir web uygulamasıdır.

### 🎯 Özellikler

- **Responsive Tasarım**: Tüm cihazlarda mükemmel görünüm
- **Modern UI/UX**: Neon renk teması ve animasyonlar
- **İletişim Formu**: Müşteri talepleri için gelişmiş form sistemi
- **Admin Paneli**: Teklif yönetimi için yönetici paneli
- **E-posta Bildirimleri**: Otomatik e-posta gönderimi
- **SEO Optimizasyonu**: Arama motorları için optimize edilmiş
- **Güvenlik**: CSRF koruması ve güvenli form işleme

## 🚀 Kurulum

### Gereksinimler

- Python 3.8+
- pip
- virtualenv (önerilen)

### Adım Adım Kurulum

1. **Projeyi klonlayın**
```bash
git clone <repository-url>
cd efor-bilisim
```

2. **Sanal ortam oluşturun**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate     # Windows
```

3. **Bağımlılıkları yükleyin**
```bash
pip install -r requirements.txt
```

4. **Çevre değişkenlerini ayarlayın**
```bash
cp .env.example .env
# .env dosyasını düzenleyin
```

5. **Uygulamayı çalıştırın**
```bash
python app.py
```

## 📁 Proje Yapısı

```
efor-bilisim/
├── app.py                 # Ana Flask uygulaması
├── requirements.txt       # Python bağımlılıkları
├── .env                  # Çevre değişkenleri (gizli)
├── .gitignore           # Git ignore dosyası
├── README.md            # Bu dosya
├── static/              # Statik dosyalar
│   ├── css/
│   │   └── style.css    # Ana CSS dosyası
│   ├── js/
│   │   └── script.js    # JavaScript dosyası
│   └── images/          # Resim dosyaları
│       ├── efor-logo.png
│       ├── 1.jpg
│       ├── 2.jpg
│       └── ...
├── templates/           # HTML şablonları
│   ├── base.html       # Ana şablon
│   ├── home.html       # Ana sayfa
│   ├── about.html      # Hakkımızda
│   ├── services.html   # Hizmetler
│   ├── contact.html    # İletişim
│   └── admin/          # Admin paneli şablonları
│       ├── login.html
│       └── quotes.html
├── logs/               # Log dosyaları (otomatik oluşturulur)
├── uploads/            # Yüklenen dosyalar (otomatik oluşturulur)
└── quotes.json         # Teklif verileri (otomatik oluşturulur)
```

## ⚙️ Konfigürasyon

### .env Dosyası Ayarları

#### Zorunlu Ayarlar
```env
# Flask Uygulama Ayarları
SECRET_KEY=your-super-secret-key-here
FLASK_ENV=production
FLASK_DEBUG=False

# E-posta Ayarları
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
RECIPIENT_EMAIL=info@eforbilisim.com

# Admin Panel Ayarları
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-secure-password
```

#### Opsiyonel Ayarlar
```env
# Şirket Bilgileri
COMPANY_NAME=Efor Bilişim
COMPANY_PHONE=+90 537 958 20 51
COMPANY_EMAIL=info@eforbilisim.com
COMPANY_ADDRESS=Söğütlü Çeşme Mahallesi, 2.Barbaros Sk. No:2, 34579 Küçükçekmece/İstanbul

# Sosyal Medya
INSTAGRAM_URL=https://instagram.com/
FACEBOOK_URL=https://www.facebook.com/eforbilisimweb/
LINKEDIN_URL=https://linkedin.com/
WHATSAPP_NUMBER=+905379582051
```

## 🌐 Canlıya Alma (Deployment)

### VPS Üzerinde Deployment

#### 1. VPS'e Bağlanın
```bash
ssh kullanici@vps-ip-adresi
```

#### 2. Sistem Güncellemeleri
```bash
sudo apt update && sudo apt upgrade -y
```

#### 3. Python ve Gerekli Paketleri Kurun
```bash
sudo apt install python3 python3-pip python3-venv nginx -y
```

#### 4. Proje Klasörünü Oluşturun
```bash
mkdir ~/efor-bilisim
cd ~/efor-bilisim
```

#### 5. Proje Dosyalarını Yükleyin
- WinSCP, FileZilla veya `scp` kullanarak dosyaları yükleyin
- `.env` dosyasını güvenli şekilde transfer edin

#### 6. Sanal Ortam Oluşturun
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 7. Gerekli Klasörleri Oluşturun
```bash
mkdir logs uploads
chmod 755 logs uploads
```

#### 8. Gunicorn ile Test Edin
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

#### 9. Nginx Konfigürasyonu
```bash
sudo nano /etc/nginx/sites-available/efor-bilisim
```

Nginx konfigürasyonu:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /home/kullanici/efor-bilisim/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

#### 10. Nginx'i Etkinleştirin
```bash
sudo ln -s /etc/nginx/sites-available/efor-bilisim /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 11. SSL Sertifikası (HTTPS)
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

#### 12. Systemd Servisi Oluşturun
```bash
sudo nano /etc/systemd/system/efor-bilisim.service
```

Servis dosyası:
```ini
[Unit]
Description=Efor Bilişim Flask App
After=network.target

[Service]
User=kullanici
WorkingDirectory=/home/kullanici/efor-bilisim
Environment="PATH=/home/kullanici/efor-bilisim/venv/bin"
ExecStart=/home/kullanici/efor-bilisim/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

#### 13. Servisi Başlatın
```bash
sudo systemctl daemon-reload
sudo systemctl enable efor-bilisim
sudo systemctl start efor-bilisim
```

## 🔧 Bakım ve Yönetim

### Log Dosyalarını Kontrol Etme
```bash
# Uygulama logları
tail -f logs/efor_bilisim.log

# Systemd servis logları
sudo journalctl -u efor-bilisim -f

# Nginx logları
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Servis Yönetimi
```bash
# Servisi yeniden başlat
sudo systemctl restart efor-bilisim

# Servis durumunu kontrol et
sudo systemctl status efor-bilisim

# Servisi durdur
sudo systemctl stop efor-bilisim
```

### Yedekleme
```bash
# Veritabanı yedekleme (quotes.json)
cp quotes.json backup/quotes_$(date +%Y%m%d_%H%M%S).json

# Tüm proje yedekleme
tar -czf backup/efor-bilisim_$(date +%Y%m%d_%H%M%S).tar.gz .
```

## 🛠️ Geliştirme

### Yeni Özellik Ekleme

1. **Yeni sayfa eklemek için:**
   - `templates/` klasörüne HTML dosyası ekle
   - `app.py`'ye route ekle
   - `base.html`'e menü linki ekle

2. **Yeni CSS eklemek için:**
   - `static/css/style.css` dosyasını düzenle
   - Responsive tasarım için medya sorguları ekle

3. **Yeni JavaScript eklemek için:**
   - `static/js/script.js` dosyasını düzenle
   - DOMContentLoaded event listener kullan

### Kod Standartları

- **Python**: PEP 8 standartlarına uygun
- **HTML**: Semantic HTML5 kullan
- **CSS**: BEM metodolojisi takip et
- **JavaScript**: ES6+ özellikleri kullan

## 🔒 Güvenlik

### Güvenlik Önlemleri

1. **Dosya İzinleri**
```bash
chmod 600 .env
chmod 755 static/
chmod 755 templates/
```

2. **Firewall Ayarları**
```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow ssh
sudo ufw enable
```

3. **Düzenli Güncellemeler**
```bash
sudo apt update && sudo apt upgrade -y
```

### Güvenlik Kontrol Listesi

- [ ] `.env` dosyası git'e commit edilmedi
- [ ] Admin şifresi güçlü
- [ ] SSL sertifikası aktif
- [ ] Firewall aktif
- [ ] Düzenli yedekleme yapılıyor
- [ ] Log dosyaları kontrol ediliyor

## 📊 Performans

### Optimizasyon Önerileri

1. **Resim Optimizasyonu**
   - WebP formatı kullan
   - Lazy loading ekle
   - Responsive images kullan

2. **CSS/JS Optimizasyonu**
   - Minify CSS/JS dosyaları
   - Gzip sıkıştırma aktif
   - Browser caching kullan

3. **Database Optimizasyonu**
   - JSON dosyası yerine SQLite/PostgreSQL kullan
   - Index'ler ekle
   - Query optimizasyonu yap

## 🐛 Sorun Giderme

### Yaygın Sorunlar

#### 1. E-posta Gönderilmiyor
- SMTP ayarlarını kontrol et
- Gmail App Password doğru mu?
- Firewall SMTP portunu engelliyor mu?

#### 2. Admin Paneli Açılmıyor
- Session ayarlarını kontrol et
- Admin kullanıcı adı/şifre doğru mu?
- .env dosyası yüklenmiş mi?

#### 3. Statik Dosyalar Yüklenmiyor
- Nginx konfigürasyonunu kontrol et
- Dosya izinlerini kontrol et
- Path doğru mu?

#### 4. SSL Sertifikası Sorunu
```bash
sudo certbot renew --dry-run
sudo systemctl reload nginx
```

## 📞 Destek

### İletişim
- **E-posta**: info@eforbilisim.com
- **Telefon**: +90 537 958 20 51
- **Adres**: Söğütlü Çeşme Mahallesi, 2.Barbaros Sk. No:2, 34579 Küçükçekmece/İstanbul

### Faydalı Linkler
- [Flask Dokümantasyonu](https://flask.palletsprojects.com/)
- [Bootstrap Dokümantasyonu](https://getbootstrap.com/docs/)
- [Gunicorn Dokümantasyonu](https://docs.gunicorn.org/)
- [Nginx Dokümantasyonu](https://nginx.org/en/docs/)

## 📄 Lisans

Bu proje Efor Bilişim için özel olarak geliştirilmiştir. Tüm hakları saklıdır.

---

**Son Güncelleme**: 2024
**Versiyon**: 1.0.0
**Geliştirici**: Efor Bilişim Teknoloji Ekibi 