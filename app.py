from flask import Flask, render_template, request, flash, redirect, url_for, session
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import json
from dotenv import load_dotenv
import secrets

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'efor_bilisim_secret_key_2024')

# Session ayarları
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)  # 24 saat oturum

# E-posta ayarları (environment variables kullanın)
SMTP_SERVER = os.environ.get('SMTP_SERVER', "smtp.gmail.com")
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
SMTP_USERNAME = os.environ.get('SMTP_USERNAME', "your-email@gmail.com")
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', "your-app-password")
RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL', "info@eforbilisim.com")

# Teklifler dosyası
QUOTES_FILE = "quotes.json"

# Sample services data
services = [
    {
        'id': 1,
        'title': 'Bilgisayar Tamiri',
        'description': 'Tüm marka ve modeller için profesyonel bilgisayar tamir hizmetleri. Donanım yükseltmeleri, yazılım sorunları ve performans optimizasyonu.',
        'icon': 'bi-laptop',
        'features': ['Donanım Teşhisi', 'Yazılım Sorun Giderme', 'Performans Optimizasyonu', 'Veri Kurtarma']
    },
    {
        'id': 2,
        'title': 'Kamera Kurulumu',
        'description': 'Ev ve işyerleri için eksiksiz güvenlik kamerası kurulum hizmetleri. IP kameralar, DVR sistemleri ve uzaktan izleme.',
        'icon': 'bi-camera-video',
        'features': ['IP Kamera Kurulumu', 'DVR Kurulumu', 'Uzaktan İzleme', 'Gece Görüş Sistemleri']
    },
    {
        'id': 3,
        'title': 'Ağ Kurulumu',
        'description': 'Profesyonel ağ altyapısı kurulumu ve yapılandırması. WiFi optimizasyonu, router yapılandırması ve ağ güvenliği.',
        'icon': 'bi-wifi',
        'features': ['WiFi Ağ Kurulumu', 'Router Yapılandırması', 'Ağ Güvenliği', 'Sinyal Optimizasyonu']
    },
    {
        'id': 4,
        'title': 'Teknik Danışmanlık',
        'description': 'IT altyapısı, donanım seçimi ve işletmenizin ihtiyaçları için teknoloji planlaması konusunda uzman tavsiyeler.',
        'icon': 'bi-gear',
        'features': ['IT Altyapı Planlaması', 'Donanım Önerileri', 'Teknoloji Yol Haritası', 'Maliyet Optimizasyonu']
    },
    {
        'id': 5,
        'title': 'Donanım Satışı',
        'description': 'Kaliteli bilgisayar donanımı ve aksesuarları. Özel yapım, yükseltmeler ve profesyonel öneriler.',
        'icon': 'bi-cpu',
        'features': ['Özel PC Yapımı', 'Donanım Yükseltmeleri', 'Aksesuarlar', 'Garanti Desteği']
    },
    {
        'id': 6,
        'title': 'Veri Kurtarma',
        'description': 'Sabit diskler, SSD\'ler ve diğer depolama cihazları için profesyonel veri kurtarma hizmetleri.',
        'icon': 'bi-hdd',
        'features': ['Sabit Disk Kurtarma', 'SSD Veri Kurtarma', 'RAID Kurtarma', 'Acil Durum Hizmetleri']
    }
]

# Admin kullanıcı bilgileri (gerçek kullanımda veritabanından gelir)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "efor2024"  # Güçlü bir şifre kullanın!

def is_admin_logged_in():
    """Admin giriş yapmış mı kontrol et"""
    return session.get('admin_logged_in', False)

def require_admin_login(f):
    """Admin giriş gerektiren sayfalar için decorator"""
    def decorated_function(*args, **kwargs):
        if not is_admin_logged_in():
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def save_quote_to_file(quote_data):
    """Teklifi JSON dosyasına kaydet"""
    try:
        # Mevcut teklifleri oku
        quotes = []
        if os.path.exists(QUOTES_FILE):
            with open(QUOTES_FILE, 'r', encoding='utf-8') as f:
                quotes = json.load(f)
        
        # Yeni teklifi ekle
        quotes.append(quote_data)
        
        # Dosyaya kaydet
        with open(QUOTES_FILE, 'w', encoding='utf-8') as f:
            json.dump(quotes, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"Dosya kaydetme hatası: {e}")
        return False

def send_email(name, email, phone, company, service, urgency, message):
    """Teklif e-postası gönder (ek dosya olmadan)"""
    try:
        subject = f"Yeni Teklif Talebi - {name}"
        html_content = f"""
        <html>
        <body style=\"font-family: Arial, sans-serif; line-height: 1.6; color: #333;\">
            <h2 style=\"color: #00d4aa;\">Yeni Teklif Talebi</h2>
            <p><strong>Tarih:</strong> {datetime.now().strftime('%d.%m.%Y %H:%M')}</p>
            <h3 style=\"color: #00d4aa;\">Müşteri Bilgileri:</h3>
            <ul>
                <li><strong>Ad Soyad:</strong> {name}</li>
                <li><strong>E-posta:</strong> {email}</li>
                <li><strong>Telefon:</strong> {phone or 'Belirtilmemiş'}</li>
                <li><strong>Şirket:</strong> {company or 'Belirtilmemiş'}</li>
            </ul>
            <h3 style=\"color: #00d4aa;\">Hizmet Bilgileri:</h3>
            <p><strong>Hizmet Türü:</strong> {service or 'Belirtilmemiş'}</p>
            <p><strong>Öncelik:</strong> {urgency or 'Normal'}</p>
            <h3 style=\"color: #00d4aa;\">Mesaj:</h3>
            <div style=\"background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 10px 0;\">
                {message.replace(chr(10), '<br>')}
            </div>
            <hr style=\"border: 1px solid #ddd; margin: 20px 0;\">
            <p style=\"font-size: 12px; color: #666;\">
                Bu e-posta Efor Bilişim web sitesinden otomatik olarak gönderilmiştir.
            </p>
        </body>
        </html>
        """
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = SMTP_USERNAME
        msg['To'] = RECIPIENT_EMAIL
        html_part = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(html_part)
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"E-posta gönderme hatası: {e}")
        return False

@app.route('/')
def home():
    return render_template('home.html', services=services[:3])

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services_page():
    return render_template('services.html', services=services)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        company = request.form.get('company')
        service = request.form.get('service')
        urgency = request.form.get('urgency')
        message = request.form.get('message')
        privacy = request.form.get('privacy')
        
        # Form validation
        if not all([name, email, phone, service, message, privacy]):
            flash('Lütfen tüm gerekli alanları doldurun.', 'error')
            return redirect(url_for('contact'))
        
        # Email validation
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            flash('Lütfen geçerli bir e-posta adresi girin.', 'error')
            return redirect(url_for('contact'))
        
        # Phone validation
        phone_pattern = r'^\+?[0-9\s\-\(\)]+$'
        if not re.match(phone_pattern, phone):
            flash('Lütfen geçerli bir telefon numarası girin.', 'error')
            return redirect(url_for('contact'))
        
        # Hizmet adını bul
        service_name = "Belirtilmemiş"
        if service:
            service_map = {
                'computer_repair': 'Bilgisayar Tamiri',
                'camera_installation': 'Kamera Kurulumu',
                'network_setup': 'Ağ Kurulumu',
                'consultancy': 'Teknik Danışmanlık',
                'hardware_sales': 'Donanım Satışı',
                'data_recovery': 'Veri Kurtarma',
                'other': 'Diğer'
            }
            service_name = service_map.get(service, service)
        
        # Öncelik durumu
        urgency_map = {
            'normal': 'Normal',
            'urgent': 'Acil',
            'very_urgent': 'Çok Acil'
        }
        urgency_name = urgency_map.get(urgency, 'Normal')
        
        # Teklif verilerini hazırla
        quote_data = {
            'id': datetime.now().strftime('%Y%m%d%H%M%S'),
            'date': datetime.now().strftime('%d.%m.%Y %H:%M'),
            'name': name,
            'email': email,
            'phone': phone,
            'company': company or 'Belirtilmemiş',
            'service': service_name,
            'urgency': urgency_name,
            'message': message,
            'status': 'Yeni'
        }
        
        # Dosyaya kaydet
        file_saved = save_quote_to_file(quote_data)
        
        # E-posta göndermeyi dene
        email_sent = False
        if SMTP_USERNAME != "your-email@gmail.com":
            email_sent = send_email(name, email, phone, company, service_name, urgency_name, message)
        
        if file_saved:
            if email_sent:
                flash('Mesajınız başarıyla gönderildi! En kısa sürede size dönüş yapacağız.', 'success')
            else:
                flash('Mesajınız kaydedildi. E-posta ayarları yapılandırılmadığı için e-posta gönderilemedi.', 'warning')
        else:
            flash('Teknik bir sorun oluştu. Lütfen telefon ile iletişime geçin.', 'error')
        
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin giriş sayfası"""
    # Zaten giriş yapmışsa admin paneline yönlendir
    if is_admin_logged_in():
        return redirect(url_for('view_quotes'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember_me = request.form.get('remember_me') == 'on'
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            # Giriş başarılı
            session['admin_logged_in'] = True
            session['admin_username'] = username
            session['login_time'] = datetime.now().isoformat()
            
            if remember_me:
                session.permanent = True
            
            flash('Başarıyla giriş yaptınız!', 'success')
            return redirect(url_for('view_quotes'))
        else:
            flash('Kullanıcı adı veya şifre hatalı!', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    """Admin çıkış"""
    session.clear()
    flash('Başarıyla çıkış yaptınız!', 'success')
    return redirect(url_for('admin_login'))

@app.route('/admin/quotes')
@require_admin_login
def view_quotes():
    """Teklifleri görüntüle (session tabanlı admin paneli)"""
    try:
        if os.path.exists(QUOTES_FILE):
            with open(QUOTES_FILE, 'r', encoding='utf-8') as f:
                quotes = json.load(f)
            return render_template('admin/quotes.html', quotes=quotes)
        else:
            return render_template('admin/quotes.html', quotes=[])
    except Exception as e:
        return f"Teklifler yüklenirken hata oluştu: {e}"

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=80, debug=False)