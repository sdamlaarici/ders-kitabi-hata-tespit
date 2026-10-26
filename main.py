import os
import fitz
import json
from moduller.pdf_okuyucu import pdf_metin_ve_koordinat_cikar, json_olarak_kaydet
from moduller.analiz_motoru import KitapAnalizMotoru, hata_raporunu_kaydet

def ornek_test_pdf_olustur(dosya_yolu):
    """3 Kriterin tamamını test etmek için kasıtlı hatalar içeren örnek PDF üretir."""
    os.makedirs(os.path.dirname(dosya_yolu), exist_ok=True)
    doc = fitz.open()
    sayfa = doc.new_page()

    # Üst Bilgi (Filtrelenecek Header - y=30)
    sayfa.insert_text((50, 30), "5. Sinif Fen Bilimleri Ders Kitabi - Unite 1", fontsize=9)

    # 1. Paragraf (Kriter 1: Yazım yanlışı 'yanliz', 'herkez' + Kriter 2: Bilimsel hata)
    p1 = (
        "Gunes sistemimizdeki gezegenler belirli yorungelerde hareket eder. "
        "Yanliz bu hareket sirasinda herkez Gunes Dunya'nin etrafinda doner sanabilir."
    )
    sayfa.insert_textbox(fitz.Rect(50, 80, 540, 140), p1, fontsize=11)

    # 2. Paragraf (Kriter 2: Pedagojik uyumsuzluk 'ezberleyiniz' + Kriter 3: Eksik dijital link)
    p2 = (
        "Etkinlik 1: Asagidaki gezegen isimlerini sirasiyla ezberleyiniz ve "
        "konuyla ilgili dijital videoyu izlemek icin karekodu okutunuz."
    )
    sayfa.insert_textbox(fitz.Rect(50, 160, 540, 220), p2, fontsize=11)

    # 3. Paragraf (Kriter 3: Yüksek Bilişsel Yük - Aşırı uzun ve tekdüze paragraf)
    p3 = (
        "Uzay arastirmalari tarihsel surec icerisinde teleskobun icadiyla hiz kazanmis "
        "olup galaksilerin yildizlarin gezegenlerin uydularin kuyruklu yildizlarin "
        "ve asteroit kusaklarinin yapisi hakkinda bircok farkli bilimsel gozlem "
        "verisi elde edilmesini saglamis ve insanligin evreni anlamlandirma cabasina "
        "cok buyuk katkilar sunarak modern astrofizik biliminin temellerini olusturmustur"
    )
    sayfa.insert_textbox(fitz.Rect(50, 240, 540, 340), p3, fontsize=11)

    # Alt Bilgi (Filtrelenecek Footer - y=810)
    sayfa.insert_text((280, 810), "Sayfa 1", fontsize=9)

    doc.save(dosya_yolu)
    doc.close()
    print(f"[BILGI] 3 kriterli test PDF dosyasi olusturuldu: '{dosya_yolu}'")

if __name__ == "__main__":
    test_pdf = "veriler/ornek_kitap.pdf"

    # Her çalıştırmada güncel test PDF'ini oluştur
    ornek_test_pdf_olustur(test_pdf)

    print("\n1. ADIM: PDF Ayristirma (Parsing) baslatiliyor...")
    bloklar = pdf_metin_ve_koordinat_cikar(test_pdf)
    ham_json_yolu = json_olarak_kaydet(bloklar)
    print(f"-> Toplam {len(bloklar)} anlamli paragraf yakalandi ve '{ham_json_yolu}' dosyasina kaydedildi.")

    print("\n2. ADIM: 3 Kriterli Hata Analiz Motoru calistiriliyor...")
    motor = KitapAnalizMotoru(sinif_seviyesi=5)
    hata_raporu = motor.tum_kitabi_analiz_et(bloklar)
    rapor_yolu = hata_raporunu_kaydet(hata_raporu)

    toplam_hata = sum(item["hata_sayisi"] for item in hata_raporu)
    print(f"-> Analiz tamamlandi! {len(hata_raporu)} paragrafta toplam {toplam_hata} hata tespit edildi.")
    print(f"-> Detayli koordinatli rapor kaydedildi: '{rapor_yolu}'\n")

    print("--- TESPIT EDILEN HATALAR (HATA_RAPORU.JSON) ---")
    print(json.dumps(hata_raporu, ensure_ascii=False, indent=4))