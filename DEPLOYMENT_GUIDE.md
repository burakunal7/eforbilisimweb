# 🚀 Efor Bilişim - VPS Deployment Rehberi

## 📋 Ön Gereksinimler

### VPS Özellikleri
- **İşletim Sistemi**: Ubuntu 20.04 LTS veya üzeri
- **RAM**: Minimum 1GB (2GB önerilen)
- **CPU**: 1 vCPU (2 vCPU önerilen)
- **Disk**: Minimum 20GB
- **Bant Genişliği**: Sınırsız veya yeterli

### Domain Gereksinimleri
- Alan adı (örn: eforbilisim.com)
- DNS yönetim paneli erişimi

---

## 🔧 Adım 1: VPS'e İlk Bağlantı

### SSH ile Bağlan
```bash
# Windows için (PowerShell veya Git Bash)
ssh root@VPS_IP_ADRESI

# Mac/Linux için
ssh root@VPS_IP_ADRESI
```

### Güvenlik Ayarları
```bash
# Root şifresini değiştir
passwd

# Yeni kullanıcı oluştur
adduser efor
usermod -aG sudo efor

# SSH anahtarı ile giriş (önerilen)
# Bilgisayarından SSH anahtarı oluştur ve VPS'e yükle
```

---

## 🛠️ Adım 2: Sistem Hazırlığı

### Sistem Güncellemeleri
```bash
# Sistem güncellemeleri
sudo apt update && sudo apt upgrade -y

# Gerekli paketleri kur
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    nginx \
    certbot \
    python3-certbot-nginx \
    git \
    curl \
    wget \
    unzip \
    htop \
    ufw \
    fail2ban
```

### Firewall Ayarları
```bash
# Firewall'u etkinleştir
sudo ufw enable

# SSH erişimini aç
sudo ufw allow ssh

# HTTP ve HTTPS erişimini aç
sudo ufw allow 'Nginx Full'

# Firewall durumunu kontrol et
sudo ufw status
```

### Fail2ban Kurulumu (Güvenlik)
```bash
# Fail2ban'ı yapılandır
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local

# SSH koruması için
sudo nano /etc/fail2ban/jail.local
# [sshd] bölümünde:
# enabled = true
# maxretry = 3
# bantime = 3600

# Fail2ban'ı yeniden başlat
sudo systemctl restart fail2ban
sudo systemctl enable fail2ban
```

---

## 📁 Adım 3: Proje Kurulumu

### Proje Klasörünü Oluştur
```bash
# Ana kullanıcıya geç
sudo su - efor

# Proje klasörünü oluştur
mkdir ~/efor-bilisim
cd ~/efor-bilisim
```

### Dosyaları Yükle
**Seçenek 1: WinSCP/FileZilla ile**
- WinSCP veya FileZilla kullanarak tüm proje dosyalarını yükle
- `.env` dosyasını güvenli şekilde transfer et

**Seçenek 2: Git ile (önerilen)**
```bash
# Git repository'den çek
git clone https://github.com/kullanici/efor-bilisim.git .
# veya
# Dosyaları manuel olarak yükle
```

### Dosya İzinlerini Ayarla
```bash
# Dosya sahipliğini ayarla
sudo chown -R efor:efor ~/efor-bilisim

# .env dosyasını güvenli yap
chmod 600 .env

# Diğer dosyalar için izinler
chmod 755 static/
chmod 755 templates/
chmod 644 *.py
chmod 644 *.txt
chmod 644 *.md

# Gerekli klasörleri oluştur
mkdir -p logs uploads backup
chmod 755 logs uploads backup
```

---

## 🐍 Adım 4: Python Ortamı

### Sanal Ortam Oluştur
```bash
# Sanal ortam oluştur
python3 -m venv venv

# Sanal ortamı aktifleştir
source venv/bin/activate

# pip'i güncelle
pip install --upgrade pip
```

### Bağımlılıkları Yükle
```bash
# requirements.txt'den yükle
pip install -r requirements.txt

# Eksik paketler varsa manuel ekle
pip install gunicorn
pip install python-dotenv
```

### Test Et
```bash
# Flask uygulamasını test et
python app.py

# Ctrl+C ile durdur
# Gunicorn ile test et
gunicorn -w 4 -b 127.0.0.1:8000 app:app
```

---

## ⚙️ Adım 5: .env Dosyası Konfigürasyonu

### .env Dosyasını Düzenle
```bash
nano .env
```

### Zorunlu Ayarlar
```env
# Flask Uygulama Ayarları
SECRET_KEY=efor_bilisim_super_gizli_anahtar_2024_xyz123_!@#$%^&*()
FLASK_ENV=production
FLASK_DEBUG=False

# E-posta Ayarları (Gmail için)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=senin-email@gmail.com
SMTP_PASSWORD=senin-16-haneli-app-password
RECIPIENT_EMAIL=info@eforbilisim.com

# Admin Panel Ayarları
ADMIN_USERNAME=admin
ADMIN_PASSWORD=Efor2024!@#$SecurePassword

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

### Gmail App Password Alma
1. [myaccount.google.com](https://myaccount.google.com) adresine git
2. **Güvenlik** → **2 Adımlı Doğrulama** → **AÇ**
3. **Uygulama Şifreleri** → **Uygulama seç** → **Diğer**
4. İsim: "Efor Bilişim Web Sitesi"
5. 16 haneli şifreyi kopyala ve `SMTP_PASSWORD` alanına yapıştır

---

## 🌐 Adım 6: Nginx Konfigürasyonu

### Nginx Site Dosyası Oluştur
```bash
sudo nano /etc/nginx/sites-available/efor-bilisim
```

### Nginx Konfigürasyonu
```nginx
server {
    listen 80;
    server_name eforbilisim.com www.eforbilisim.com;

    # Güvenlik başlıkları
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

    # Gzip sıkıştırma
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied expired no-cache no-store private must-revalidate auth;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss;

    # Ana uygulama
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Statik dosyalar
    location /static {
        alias /home/efor/efor-bilisim/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # Favicon
    location = /favicon.ico {
        alias /home/efor/efor-bilisim/static/images/efor-logo.png;
        access_log off;
        log_not_found off;
    }

    # Robots.txt
    location = /robots.txt {
        alias /home/efor/efor-bilisim/static/robots.txt;
        access_log off;
        log_not_found off;
    }

    # Güvenlik - gizli dosyaları engelle
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }

    # Güvenlik - .env dosyasını engelle
    location ~ \.env {
        deny all;
        access_log off;
        log_not_found off;
    }
}
```

### Nginx'i Etkinleştir
```bash
# Site'ı etkinleştir
sudo ln -s /etc/nginx/sites-available/efor-bilisim /etc/nginx/sites-enabled/

# Varsayılan site'ı devre dışı bırak
sudo rm /etc/nginx/sites-enabled/default

# Nginx konfigürasyonunu test et
sudo nginx -t

# Nginx'i yeniden başlat
sudo systemctl restart nginx
sudo systemctl enable nginx
```

---

## 🔒 Adım 7: SSL Sertifikası (HTTPS)

### Let's Encrypt SSL Sertifikası
```bash
# Certbot kurulumu (zaten kurulu olmalı)
sudo apt install certbot python3-certbot-nginx -y

# SSL sertifikası al
sudo certbot --nginx -d eforbilisim.com -d www.eforbilisim.com

# Otomatik yenileme için cron job ekle
sudo crontab -e
# Aşağıdaki satırı ekle:
# 0 12 * * * /usr/bin/certbot renew --quiet
```

### SSL Test Et
```bash
# SSL sertifikasını test et
sudo certbot certificates

# SSL Labs testi için
# https://www.ssllabs.com/ssltest/analyze.html?d=eforbilisim.com
```

---

## ⚡ Adım 8: Systemd Servisi

### Servis Dosyası Oluştur
```bash
sudo nano /etc/systemd/system/efor-bilisim.service
```

### Servis Konfigürasyonu
```ini
[Unit]
Description=Efor Bilişim Flask Web Application
After=network.target
Wants=network.target

[Service]
Type=exec
User=efor
Group=efor
WorkingDirectory=/home/efor/efor-bilisim
Environment="PATH=/home/efor/efor-bilisim/venv/bin"
Environment="FLASK_ENV=production"
ExecStart=/home/efor/efor-bilisim/venv/bin/gunicorn \
    --workers 4 \
    --bind 127.0.0.1:8000 \
    --access-logfile /home/efor/efor-bilisim/logs/gunicorn-access.log \
    --error-logfile /home/efor/efor-bilisim/logs/gunicorn-error.log \
    --log-level info \
    --timeout 120 \
    --keep-alive 2 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    app:app
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=5
StartLimitInterval=0

[Install]
WantedBy=multi-user.target
```

### Servisi Başlat
```bash
# Systemd'yi yenile
sudo systemctl daemon-reload

# Servisi etkinleştir
sudo systemctl enable efor-bilisim

# Servisi başlat
sudo systemctl start efor-bilisim

# Durumu kontrol et
sudo systemctl status efor-bilisim
```

---

## 🔍 Adım 9: Test ve Doğrulama

### Servis Testleri
```bash
# Servis durumu
sudo systemctl status efor-bilisim

# Nginx durumu
sudo systemctl status nginx

# Port dinleme durumu
sudo netstat -tlnp | grep :80
sudo netstat -tlnp | grep :443
sudo netstat -tlnp | grep :8000

# Log dosyalarını kontrol et
tail -f /home/efor/efor-bilisim/logs/gunicorn-error.log
tail -f /var/log/nginx/error.log
```

### Web Sitesi Testleri
1. **HTTP Test**: `http://eforbilisim.com`
2. **HTTPS Test**: `https://eforbilisim.com`
3. **Admin Panel**: `https://eforbilisim.com/admin/login`
4. **İletişim Formu**: Form gönder ve e-posta kontrol et
5. **Statik Dosyalar**: CSS, JS, resimler yükleniyor mu?

### Performans Testleri
```bash
# Yük testi (opsiyonel)
sudo apt install apache2-utils -y
ab -n 1000 -c 10 https://eforbilisim.com/

# Disk kullanımı
df -h

# RAM kullanımı
free -h

# CPU kullanımı
htop
```

---

## 📊 Adım 10: Monitoring ve Logging

### Log Dosyaları
```bash
# Uygulama logları
tail -f /home/efor/efor-bilisim/logs/gunicorn-access.log
tail -f /home/efor/efor-bilisim/logs/gunicorn-error.log

# Nginx logları
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# System logları
sudo journalctl -u efor-bilisim -f
```

### Monitoring Script'i
```bash
# Monitoring script oluştur
nano ~/monitor.sh
```

```bash
#!/bin/bash
# Efor Bilişim Monitoring Script

echo "=== Efor Bilişim Sistem Durumu ==="
echo "Tarih: $(date)"
echo ""

# Servis durumları
echo "=== Servis Durumları ==="
sudo systemctl is-active efor-bilisim
sudo systemctl is-active nginx

# Disk kullanımı
echo ""
echo "=== Disk Kullanımı ==="
df -h /home/efor/efor-bilisim

# RAM kullanımı
echo ""
echo "=== RAM Kullanımı ==="
free -h

# Son log kayıtları
echo ""
echo "=== Son Hata Logları ==="
tail -5 /home/efor/efor-bilisim/logs/gunicorn-error.log
```

```bash
# Script'i çalıştırılabilir yap
chmod +x ~/monitor.sh

# Test et
./monitor.sh
```

---

## 🔄 Adım 11: Yedekleme Sistemi

### Yedekleme Script'i
```bash
nano ~/backup.sh
```

```bash
#!/bin/bash
# Efor Bilişim Yedekleme Script

BACKUP_DIR="/home/efor/backup"
DATE=$(date +%Y%m%d_%H%M%S)
PROJECT_DIR="/home/efor/efor-bilisim"

# Yedekleme klasörü oluştur
mkdir -p $BACKUP_DIR

# Proje dosyalarını yedekle
tar -czf $BACKUP_DIR/efor-bilisim_$DATE.tar.gz \
    --exclude='venv' \
    --exclude='__pycache__' \
    --exclude='*.log' \
    --exclude='uploads/*' \
    $PROJECT_DIR

# Veritabanı yedekleme (quotes.json)
cp $PROJECT_DIR/quotes.json $BACKUP_DIR/quotes_$DATE.json

# Eski yedekleri temizle (30 günden eski)
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
find $BACKUP_DIR -name "quotes_*.json" -mtime +30 -delete

echo "Yedekleme tamamlandı: $BACKUP_DIR/efor-bilisim_$DATE.tar.gz"
```

```bash
# Script'i çalıştırılabilir yap
chmod +x ~/backup.sh

# Manuel yedekleme
./backup.sh

# Otomatik yedekleme için cron job
crontab -e
# Her gün saat 02:00'de yedekleme
# 0 2 * * * /home/efor/backup.sh
```

---

## 🛠️ Adım 12: Bakım ve Güncelleme

### Güncelleme Script'i
```bash
nano ~/update.sh
```

```bash
#!/bin/bash
# Efor Bilişim Güncelleme Script

PROJECT_DIR="/home/efor/efor-bilisim"

echo "Güncelleme başlıyor..."

# Yedekleme yap
./backup.sh

# Servisi durdur
sudo systemctl stop efor-bilisim

# Sanal ortamı aktifleştir
cd $PROJECT_DIR
source venv/bin/activate

# Bağımlılıkları güncelle
pip install --upgrade pip
pip install -r requirements.txt

# Servisi başlat
sudo systemctl start efor-bilisim

# Durumu kontrol et
sudo systemctl status efor-bilisim

echo "Güncelleme tamamlandı!"
```

### Düzenli Bakım
```bash
# Haftalık bakım için cron job
crontab -e

# Her Pazar saat 03:00'de bakım
# 0 3 * * 0 /home/efor/update.sh

# Her gün saat 04:00'de log temizleme
# 0 4 * * * find /home/efor/efor-bilisim/logs -name "*.log" -mtime +7 -delete
```

---

## 🚨 Adım 13: Sorun Giderme

### Yaygın Sorunlar ve Çözümleri

#### 1. Servis Başlamıyor
```bash
# Log'ları kontrol et
sudo journalctl -u efor-bilisim -n 50

# Manuel test
cd /home/efor/efor-bilisim
source venv/bin/activate
python app.py
```

#### 2. Nginx Hatası
```bash
# Nginx konfigürasyonunu test et
sudo nginx -t

# Nginx log'larını kontrol et
sudo tail -f /var/log/nginx/error.log
```

#### 3. SSL Sertifikası Sorunu
```bash
# Sertifikayı yenile
sudo certbot renew --dry-run

# Manuel yenileme
sudo certbot renew
sudo systemctl reload nginx
```

#### 4. E-posta Gönderilmiyor
```bash
# .env dosyasını kontrol et
cat .env | grep SMTP

# Manuel test
python3 -c "
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
load_dotenv()

try:
    server = smtplib.SMTP(os.getenv('SMTP_SERVER'), int(os.getenv('SMTP_PORT')))
    server.starttls()
    server.login(os.getenv('SMTP_USERNAME'), os.getenv('SMTP_PASSWORD'))
    print('SMTP bağlantısı başarılı!')
    server.quit()
except Exception as e:
    print(f'Hata: {e}')
"
```

#### 5. Disk Alanı Doldu
```bash
# Disk kullanımını kontrol et
df -h

# Büyük dosyaları bul
sudo find /home/efor -type f -size +100M

# Log dosyalarını temizle
sudo find /home/efor/efor-bilisim/logs -name "*.log" -mtime +7 -delete
```

---

## 📞 Adım 14: Destek ve İletişim

### Acil Durum Komutları
```bash
# Servisi yeniden başlat
sudo systemctl restart efor-bilisim

# Nginx'i yeniden başlat
sudo systemctl restart nginx

# Tüm servisleri yeniden başlat
sudo systemctl restart efor-bilisim nginx

# Sistem durumunu kontrol et
./monitor.sh
```

### İletişim Bilgileri
- **E-posta**: info@eforbilisim.com
- **Telefon**: +90 537 958 20 51
- **Adres**: Söğütlü Çeşme Mahallesi, 2.Barbaros Sk. No:2, 34579 Küçükçekmece/İstanbul

### Faydalı Linkler
- [Flask Dokümantasyonu](https://flask.palletsprojects.com/)
- [Gunicorn Dokümantasyonu](https://docs.gunicorn.org/)
- [Nginx Dokümantasyonu](https://nginx.org/en/docs/)
- [Let's Encrypt Dokümantasyonu](https://letsencrypt.org/docs/)

---

## ✅ Deployment Kontrol Listesi

### Kurulum Öncesi
- [ ] VPS paketi alındı
- [ ] Domain alındı ve DNS ayarları yapıldı
- [ ] Gmail App Password alındı
- [ ] Tüm proje dosyaları hazır

### Kurulum Sonrası
- [ ] SSH bağlantısı test edildi
- [ ] Sistem güncellemeleri yapıldı
- [ ] Firewall ayarları yapıldı
- [ ] Python ortamı kuruldu
- [ ] .env dosyası konfigüre edildi
- [ ] Nginx kuruldu ve konfigüre edildi
- [ ] SSL sertifikası alındı
- [ ] Systemd servisi kuruldu
- [ ] Web sitesi test edildi
- [ ] Admin paneli test edildi
- [ ] E-posta sistemi test edildi
- [ ] Yedekleme sistemi kuruldu
- [ ] Monitoring sistemi kuruldu

### Güvenlik Kontrolleri
- [ ] .env dosyası güvenli
- [ ] Admin şifresi güçlü
- [ ] SSL sertifikası aktif
- [ ] Firewall aktif
- [ ] Fail2ban aktif
- [ ] Düzenli yedekleme çalışıyor

---

**🎉 Tebrikler! Efor Bilişim web sitesi başarıyla canlıya alındı!**

**Son Güncelleme**: 2024
**Versiyon**: 1.0.0
**Geliştirici**: Efor Bilişim Teknoloji Ekibi 

# PythonAnywhere Deployment Rehberi

Bu rehber, Efor Bilişim web sitesini PythonAnywhere'e Git kullanarak nasıl kuracağınızı adım adım açıklar.

## 1. Git Repository Hazırlığı

### Yerel Bilgisayarınızda:

1. **Git repository oluşturun:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **GitHub/GitLab'da yeni repository oluşturun:**
   - GitHub.com veya GitLab.com'a gidin
   - "New repository" butonuna tıklayın
   - Repository adını girin (örn: `efor-bilisim-website`)
   - Public veya Private seçin
   - "Create repository" butonuna tıklayın

3. **Yerel repository'yi remote'a bağlayın:**
   ```bash
   git remote add origin https://github.com/KULLANICI_ADINIZ/efor-bilisim-website.git
   git branch -M main
   git push -u origin main
   ```

## 2. PythonAnywhere Hesabı Oluşturma

1. **PythonAnywhere'e kayıt olun:**
   - https://www.pythonanywhere.com adresine gidin
   - "Create a Beginner account" butonuna tıklayın
   - E-posta ve şifre ile kayıt olun

2. **Hesabınızı doğrulayın:**
   - E-posta adresinize gelen doğrulama linkine tıklayın

## 3. PythonAnywhere'de Proje Kurulumu

### Bash Console'da:

1. **Projeyi klonlayın:**
   ```bash
   cd ~
   git clone https://github.com/KULLANICI_ADINIZ/efor-bilisim-website.git
   cd efor-bilisim-website
   ```

2. **Virtual environment oluşturun:**
   ```bash
   python3.9 -m venv venv
   source venv/bin/activate
   ```

3. **Bağımlılıkları yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment variables dosyası oluşturun:**
   ```bash
   nano .env
   ```
   
   Aşağıdaki içeriği ekleyin:
   ```
   SECRET_KEY=efor_bilisim_secret_key_2024
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   RECIPIENT_EMAIL=info@eforbilisim.com
   ```

## 4. Web App Yapılandırması

### Web sekmesinde:

1. **"Add a new web app" butonuna tıklayın**

2. **Domain seçin:**
   - `yourusername.pythonanywhere.com` (ücretsiz hesap)
   - Veya kendi domain'inizi kullanın (ücretli hesap)

3. **Framework seçin:**
   - "Flask" seçin
   - Python 3.9 seçin

4. **Source code path:**
   - `/home/yourusername/efor-bilisim-website`

5. **Working directory:**
   - `/home/yourusername/efor-bilisim-website`

## 5. WSGI Dosyası Düzenleme

### Files sekmesinde:

1. **`/var/www/yourusername_pythonanywhere_com_wsgi.py` dosyasını açın**

2. **İçeriği şu şekilde değiştirin:**
   ```python
   import sys
   import os
   
   # Add the project directory to the Python path
   path = '/home/yourusername/efor-bilisim-website'
   if path not in sys.path:
       sys.path.append(path)
   
   # Activate virtual environment
   activate_this = '/home/yourusername/efor-bilisim-website/venv/bin/activate_this.py'
   with open(activate_this) as file_:
       exec(file_.read(), dict(__file__=activate_this))
   
   # Import the Flask app
   from app import app as application
   
   # For debugging
   if __name__ == '__main__':
       application.run()
   ```

## 6. Static Files Yapılandırması

### Web sekmesinde "Static files" bölümünde:

1. **URL:** `/static/`
2. **Directory:** `/home/yourusername/efor-bilisim-website/static`

## 7. Uygulamayı Başlatma

1. **Web sekmesinde "Reload" butonuna tıklayın**

2. **Sitenizi test edin:**
   - `https://yourusername.pythonanywhere.com` adresine gidin

## 8. Güncellemeler İçin

### Yerel bilgisayarınızda değişiklik yaptıktan sonra:

1. **Değişiklikleri commit edin:**
   ```bash
   git add .
   git commit -m "Update description"
   git push
   ```

2. **PythonAnywhere'de güncelleyin:**
   ```bash
   cd ~/efor-bilisim-website
   git pull
   ```

3. **Web app'i yeniden başlatın:**
   - Web sekmesinde "Reload" butonuna tıklayın

## 9. Hata Ayıklama

### Log dosyalarını kontrol edin:

1. **Error log:**
   - Web sekmesinde "Log files" bölümünde "Error log" linkine tıklayın

2. **Server log:**
   - Web sekmesinde "Log files" bölümünde "Server log" linkine tıklayın

## 10. Güvenlik Notları

1. **Admin şifresini değiştirin:**
   - `app.py` dosyasında `ADMIN_PASSWORD` değişkenini güncelleyin

2. **Secret key'i değiştirin:**
   - `.env` dosyasında güçlü bir `SECRET_KEY` kullanın

3. **E-posta ayarlarını yapın:**
   - Gmail için App Password kullanın
   - SMTP ayarlarını doğru yapılandırın

## 11. SSL Sertifikası (Ücretli Hesap)

Ücretli hesap kullanıyorsanız:

1. **Web sekmesinde "Security" bölümünde**
2. **"Enable HTTPS" butonuna tıklayın**
3. **SSL sertifikası otomatik olarak yapılandırılacak**

## Sorun Giderme

### Yaygın Hatalar:

1. **Import Error:**
   - Virtual environment'ın aktif olduğundan emin olun
   - WSGI dosyasında path'lerin doğru olduğunu kontrol edin

2. **Static files yüklenmiyor:**
   - Static files yapılandırmasını kontrol edin
   - Dosya izinlerini kontrol edin

3. **E-posta gönderilmiyor:**
   - SMTP ayarlarını kontrol edin
   - Gmail App Password kullandığınızdan emin olun

### Destek:

Sorun yaşarsanız PythonAnywhere support forumlarını kullanabilirsiniz. 