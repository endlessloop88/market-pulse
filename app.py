from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re

# Selenium Kütüphaneleri
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)


# Veritabanını başlatan fonksiyon
def init_db():
    conn = sqlite3.connect('market_pulse.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS urunler
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       url
                       TEXT,
                       hedef_fiyat
                       REAL,
                       tarih
                       TEXT
                   )
                   ''')

    conn.commit()
    conn.close()


init_db()


# --- E-POSTA BİLDİRİM FONKSİYONU ---
def eposta_gonder(urun_url, hedef_fiyat, anlik_fiyat):
    gonderen_email = "ilguny929@gmail.com"
    sifre = "lrsc duoo qugi foca"  # Gmail Uygulama Şifresi
    alici_email = "senin_mailin@gmail.com"

    konu = "MarketPulse - Fiyat Düştü Alarmı! 🚨"
    govde = f"Harika haber!\n\nTakip ettiğin ürünün fiyatı düştü ve hedefinin altına indi:\n\nÜrün Linki: {urun_url}\nHedef Fiyatın: {hedef_fiyat} TL\nGüncel Fiyat: {anlik_fiyat} TL\n\nHemen incele ve kaçırma!"

    msg = MIMEMultipart()
    msg['From'] = gonderen_email
    msg['To'] = alici_email
    msg['Subject'] = konu
    msg.attach(MIMEText(govde, 'plain', 'utf-8'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gonderen_email, sifre)
        server.sendmail(gonderen_email, alici_email, msg.as_string())
        server.quit()
        print("Fiyat alarmı e-postası başarıyla gönderildi!")
    except Exception as e:
        print(f"E-posta gönderilemedi, hata: {e}")


# --- ÇOKLU SEÇİCİ (FALLBACK) İLE AKILLI FİYAT ÇEKME ---
def fiyat_getir_selenium(url):
    options = Options()
    options.add_argument("--headless")  # Arka planda çalıştırır
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)

        # Farklı sitelerin yaygın fiyat etiketleri (Sırayla taranır)
        seciciler = [
            "[data-test-id='price-current-price']",  # Hepsiburada
            ".prc-dsc",  # Trendyol
            ".a-price .a-offscreen",  # Amazon
            ".product-price",  # Genel e-ticaret
            ".price",  # Genel e-ticaret
            "span[class*='price']"  # İçinde 'price' geçen class'lar
        ]

        fiyat_str = None
        for secici in seciciler:
            try:
                element = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, secici))
                )
                if element and element.text.strip():
                    fiyat_str = element.text.strip()
                    break  # Fiyat bulunduysa döngüden çık
            except:
                continue  # Bulamazsa bir sonraki seçiciyi dene

        if fiyat_str:
            # Metin temizliği (Örn: "2.499,99 TL" formatını düzenleme)
            fiyat_temiz = fiyat_str.replace(" TL", "").replace("TL", "").replace(".", "").replace(",", ".").strip()

            # Regex ile güvenli bir şekilde sayısal değeri çekelim
            sayi_eslesmesi = re.findall(r'\d+\.\d+|\d+', fiyat_temiz)
            if sayi_eslesmesi:
                return float("".join(sayi_eslesmesi))

    except Exception as e:
        print(f"Selenium fiyat çekme hatası: {e}")
    finally:
        driver.quit()

    return None


# --- ARKA PLAN KONTROL MEKANİZMASI ---
def arka_plan_fiyat_kontrol():
    print("--- MarketPulse Akıllı Fallback Taraması Başladı ---")
    conn = sqlite3.connect('market_pulse.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, url, hedef_fiyat FROM urunler")
    kayitlar = cursor.fetchall()
    conn.close()

    for kayit in kayitlar:
        urun_id, url, hedef_fiyat = kayit
        print(f"Ürün Kontrol Ediliyor (ID: {urun_id})...")

        anlik_fiyat = fiyat_getir_selenium(url)

        if anlik_fiyat:
            print(f"-> Güncel Fiyat: {anlik_fiyat} TL | Hedef Fiyat: {hedef_fiyat} TL")
            if anlik_fiyat <= hedef_fiyat:
                print("Hedef fiyata ulaşıldı! E-posta tetikleniyor...")
                eposta_gonder(url, hedef_fiyat, anlik_fiyat)
        else:
            print(f"-> Bu turda fiyat okunamadı, sonraki turda tekrar denenecek.")

    print("--- Tarama Tamamlandı ---")


# APScheduler'ı Başlatıyoruz (Her 60 saniyede bir otomatik kontrol)
scheduler = BackgroundScheduler()
scheduler.add_job(func=arka_plan_fiyat_kontrol, trigger="interval", seconds=60)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>MarketPulse - Çoklu Seçici Akıllı Takip</title>
</head>
<body style="font-family: Arial, sans-serif; background-color: #121212; color: #e0e0e0; display: flex; justify-content: center; align-items: center; flex-direction: column; min-height: 100vh; margin: 0;">
    <div style="background: #1e1e1e; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); width: 550px; margin-bottom: 20px;">
        <h2 style="color: #00ffcc; text-align: center;">MarketPulse Akıllı Robot</h2>
        <p style="font-size: 12px; color: #888; text-align: center;">Çoklu seçici (fallback) mekanizması ile fiyatlar taranıyor.</p>

        <form method="POST">
            <label>Ürün Linki (URL):</label><br>
            <input type="text" name="url" required placeholder="https://www.ornek.com/urun" style="width: 100%; padding: 8px; margin: 8px 0 15px 0; background: #2d2d2d; border: 1px solid #444; color: #fff; border-radius: 4px;"><br>

            <label>Hedef Fiyatın (TL):</label><br>
            <input type="number" step="any" name="hedef_fiyat" required placeholder="Örn: 500" style="width: 100%; padding: 8px; margin: 8px 0 20px 0; background: #2d2d2d; border: 1px solid #444; color: #fff; border-radius: 4px;"><br>

            <button type="submit" style="width: 100%; padding: 10px; background: #00ffcc; color: #121212; font-weight: bold; border: none; border-radius: 4px; cursor: pointer;">Ürünü Akıllı Takibe Ekle</button>
        </form>

        {% if mesaj %}
            <div style="margin-top: 20px; padding: 12px; background: #252525; border-left: 4px solid #00ffcc; border-radius: 4px;">
                <p style="margin: 0; font-size: 14px;">{{ mesaj }}</p>
            </div>
        {% endif %}
    </div>

    <!-- Geçmiş Takip Edilen Ürünler Tablosu -->
    <div style="background: #1e1e1e; padding: 20px; border-radius: 10px; width: 720px; box-shadow: 0 4px 15px rgba(0,0,0,0.5);">
        <h3 style="color: #00ffcc; margin-top: 0; text-align: center;">Aktif Akıllı Takipler</h3>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px; table-layout: fixed;">
            <thead>
                <tr style="border-bottom: 1px solid #444; text-align: left; color: #888;">
                    <th style="padding: 8px; width: 8%;">ID</th>
                    <th style="padding: 8px; width: 37%;">Ürün Linki</th>
                    <th style="padding: 8px; width: 18%;">Hedef Fiyat</th>
                    <th style="padding: 8px; width: 25%;">Tarih</th>
                    <th style="padding: 8px; width: 12%; text-align: center;">İşlem</th>
                </tr>
            </thead>
            <tbody>
                {% for urun in kayitlar %}
                <tr style="border-bottom: 1px solid #2d2d2d;">
                    <td style="padding: 8px;">{{ urun[0] }}</td>
                    <td style="padding: 8px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                        <a href="{{ urun[1] }}" target="_blank" style="color: #ff6600; text-decoration: none;" title="{{ urun[1] }}">{{ urun[1] }}</a>
                    </td>
                    <td style="padding: 8px; color: #00ffcc;">{{ urun[2] }} TL</td>
                    <td style="padding: 8px; color: #aaa; font-size: 11px;">{{ urun[3] }}</td>
                    <td style="padding: 8px; text-align: center;">
                        <a href="{{ url_for('sil', id=urun[0]) }}" style="background: #ff4444; color: white; padding: 4px 8px; border-radius: 3px; text-decoration: none; font-size: 11px; font-weight: bold;">Sil</a>
                    </td>
                </tr>
                {% else %}
                <tr>
                    <td colspan="5" style="padding: 10px; text-align: center; color: #666;">Henüz takip edilen ürün yok.</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>
"""


@app.route('/', methods=['GET', 'POST'])
def index():
    mesaj = None
    if request.method == 'POST':
        url = request.form.get('url')
        hedef_fiyat = request.form.get('hedef_fiyat')
        tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = sqlite3.connect('market_pulse.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO urunler (url, hedef_fiyat, tarih) VALUES (?, ?, ?)", (url, hedef_fiyat, tarih))
        conn.commit()
        conn.close()

        mesaj = "Ürün çoklu seçici mekanizmasıyla takibe eklendi!"

    conn = sqlite3.connect('market_pulse.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, url, hedef_fiyat, tarih FROM urunler ORDER BY id DESC")
    kayitlar = cursor.fetchall()
    conn.close()

    return render_template_string(HTML_TEMPLATE, mesaj=mesaj, kayitlar=kayitlar)


@app.route('/sil/<int:id>')
def sil(id):
    conn = sqlite3.connect('market_pulse.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM urunler WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)