# ==========================================
# Proje: MarketPulse - Fiyat Takip Motoru
# Geliştirici: Yunus
# ==========================================

urun_adi = input("Takip etmek istediğiniz ürünün adını girin: ")
anlik_fiyat = float(input(f"'{urun_adi}' için güncel fiyatı girin (TL): "))
hedef_fiyat = float(input("Hedeflediğiniz (alarm kurmak istediğiniz) maksimum fiyatı girin (TL): "))

print("\n--- MARKETPULSE FİYAT ANALİZ RAPORU ---")
if anlik_fiyat <= hedef_fiyat:
    print(f"Harika haber! {urun_adi} şu an {anlik_fiyat} TL. Hedef fiyatın altında, hemen alınabilir!")
else:
    fark = anlik_fiyat - hedef_fiyat
    print(f"Uyarı: {urun_adi} şu an {anlik_fiyat} TL. Hedef fiyattan {fark:.2f} TL daha pahalı, takipte kal.")