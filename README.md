# 🚀 MarketPulse - Akıllı E-Ticaret Fiyat Takip & Alarm Robotu

**MarketPulse**, e-ticaret sitelerindeki fiyat dalgalanmalarını anlık olarak izlemek, olası anti-bot/DOM değişikliklerine karşı esnek bir şekilde uyum sağlamak ve hedef fiyatlara ulaşıldığında kullanıcıya otomatik e-posta bildirimleri göndermek amacıyla Python ile geliştirilmiş tam kapsamlı bir web otomasyonu ve takip sistemidir.

---

## 🛠️ Kullanılan Teknolojiler ve Kütüphaneler

* **Backend & Web Framework:** Python, Flask
* **Web Scraping & Otomasyon:** Selenium (`--headless`, akıllı çoklu seçici fallback mekanizması)
* **Zamanlanmış Görevler (Background Scheduler):** APScheduler
* **Veritabanı:** SQLite (`guncel_fiyat` ve hedef fiyat entegrasyonu)
* **Bildirim Servisi:** `smtplib` (SMTP e-posta entegrasyonu)
* **Arayüz Tasarımı:** HTML5 / CSS3 (Özel koyu tema tasarımı)

---

## 🧠 Öne Çıkan Mimari Özellikler

1. **Akıllı Fallback (Çoklu Seçici) Mekanizması:** 
   Farklı e-ticaret altyapılarının (Trendyol, Hepsiburada, Amazon vb.) CSS seçicileri dinamik olarak değiştirebilmesine karşı kod, önceden tanımlanmış alternatif seçici havuzunu sırayla dener; fiyatı başarıyla yakaladığı an döngüyü kırarak veri kaybını önler.
2. **Arka Plan Otomasyonu:** 
   APScheduler kullanılarak kullanıcı arayüzünü kilitlemeden, arka planda periyodik aralıklarla (ör. her 60 saniyede bir) tüm aktif ürünleri gezen ve güncel fiyatları kontrol eden akıllı bir döngü barındırır.
3. **Anında Alarm Mekanizması:** 
   Taranan güncel fiyat, kullanıcının belirlediği hedef fiyatın altına düştüğü veya eşitlendiği anda sistem otomatik olarak SMTP protokolü üzerinden e-posta alarmı tetikler.
4. **Dinamik Kontrol Paneli:** 
   Flask tabanlı arayüz sayesinde kullanıcılar yeni ürün linklerini ve hedef fiyatlarını sisteme kolayca ekleyebilir, geçmiş takipleri, anlık güncel fiyatları ve eklenme tarihlerini modern bir tabloda takip edebilir.

---

## ⚙️ Kurulum ve Çalıştırma

Projeyi yerel ortamınızda çalıştırmak için aşağıdaki adımları takip edebilirsiniz:

1. **Depoyu klonlayın:**
   ```bash
   git clone [https://github.com/endlessloop88/market-pulse.git](https://github.com/endlessloop88/market-pulse.git)
   cd market-pulse
Sanal ortam oluşturun ve aktif edin:

Bash
python -m venv .venv
# Windows için:
.venv\Scripts\activate
# Mac/Linux için:
source .venv/bin/activate
Gerekli kütüphaneleri yükleyin:

Bash
pip install -r requirements.txt
Uygulamayı başlatın:

Bash
python app.py
Tarayıcınızda http://127.0.0.1:5000 adresine giderek uygulamayı kullanmaya başlayabilirsiniz.

💡 Proje Görseli / Mimari Akış
Arka planda çalışan Selenium başsız (headless) tarayıcı oturumları, SQLite veritabanı senkronizasyonu ve Flask arayüzüyle uçtan uca çalışan bir otomasyon çözümüdür.


---

### Güncellemeyi GitHub'a Gönderme Adımları:

1. Sol menüden **`README.md`** dosyasına tıkla ve yukarıdaki metni yapıştırıp kaydet (`Ctrl + S`).
2. Terminale gelip şu komutlarla GitHub'a son halini gönder:
   ```bash
   git add README.md
   git commit -m "README.md dokümantasyonu güncellendi"
   git push origin main
