import os
import fitz
import json
from moduller.pdf_okuyucu import pdf_metin_ve_koordinat_cikar, json_olarak_kaydet

def ornek_test_pdf_olustur(dosya_yolu):
    """Test için kasıtlı hatalar ve alt/üst bilgi barındıran örnek bir PDF üretir."""
    os.makedirs(os.path.dirname(dosya_yolu), exist_ok=True)
    doc = fitz.open()
    sayfa = doc.new_page()

    # Filtrelenmesi gereken üst bilgi (y=30)
    sayfa.insert_text((50, 30), "5. Sinif Fen Bilimleri - Unite 1", fontsize=9)

    # 1. Paragraf (Kasıtlı imla hataları)
    sayfa.insert_text((50, 100), "Gunes sistemimizdeki gezegenler belirli yorungelerde hareket eder. Yanliz bu hareket sirasinda herkez dunya'nin dondugunu gorebilir.", fontsize=11)

    # 2. Paragraf (Etkinlik metni)
    sayfa.insert_text((50, 180), "Etkinlik 1: Asagidaki sorulari dikkatlice okuyarak defterinize cevaplayiniz.", fontsize=11)

    # Filtrelenmesi gereken alt bilgi (y=810)
    sayfa.insert_text((280, 810), "Sayfa 1", fontsize=9)

    doc.save(dosya_yolu)
    doc.close()
    print(f"[BILGI] Test icin '{dosya_yolu}' olusturuldu.")

if __name__ == "__main__":
    test_pdf = "veriler/ornek_kitap.pdf"

    if not os.path.exists(test_pdf):
        ornek_test_pdf_olustur(test_pdf)

    print("PDF Ayristirma (Parsing) islemi baslatiliyor...\n")
    sonuclar = pdf_metin_ve_koordinat_cikar(test_pdf)
    kayit_yolu = json_olarak_kaydet(sonuclar)

    print(f"Toplam {len(sonuclar)} adet anlamli paragraf blogu yakalandi (Ust/alt bilgiler temizlendi).")
    print(f"Cikti dosyasi kaydedildi: {kayit_yolu}\n")
    print("--- CIKARILAN JSON VERISI ---")
    print(json.dumps(sonuclar, ensure_ascii=False, indent=4))