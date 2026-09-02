from selenium.webdriver.common.by import By


def fiyat_cek_alternatifli(driver, url):
    driver.get(url)

    # Denenecek olası fiyat seçicileri (Farklı HTML etiketleri / sınıfları)
    aday_seciciler = [
        "span.a-price-whole",  # Amazon genel fiyat sınıfı
        "span#priceblock_ourprice",  # Alternatif Amazon ID
        ".price-val",  # Örnek e-ticaret sınıfı
        "[data-price]"  # Data niteliği taşıyan etiketler
    ]

    bulunan_fiyat = None

    for secici in aday_seciciler:
        try:
            # Alternatifleri sırayla deniyoruz (if-else mantığıyla akıllı arama)
            element = driver.find_element(By.CSS_SELECTOR, secici)
            if element and element.text.strip():
                bulunan_fiyat = element.text.strip()
                break  # Fiyatı bulduysa döngüden çık
        except:
            continue  # Bulamazsa sıradakine geç

    if bulunan_fiyat:
        print(f"Başarılı! Yakalanan Fiyat: {bulunan_fiyat}")
        return bulunan_fiyat
    else:
        print("Bu turda fiyat okunamadı, alternatifler tükendi.")
        return None


