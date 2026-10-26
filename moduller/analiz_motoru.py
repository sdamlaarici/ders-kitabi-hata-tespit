import json
import re
import os

# KRİTER 1: TDK Yaygın Yazım Yanlışları Sözlüğü
YAZIM_YANLISLARI = {
    "yanlız": "yalnız",
    "yanliz": "yalnız",
    "herkez": "herkes",
    "birşey": "bir şey",
    "birsey": "bir şey",
    "birçokları": "birçoğu",
    "şarz": "şarj",
    "orjinal": "orijinal",
    "farketmek": "fark etmek",
    "kareografi": "koreografi",
    "insiyatif": "inisiyatif",
    "klavuz": "kılavuz",
    "stajyer": "stajyer"
}

# KRİTER 2: Pedagojik Açıdan Sakıncalı / Yapılandırmacı Eğitime Aykırı İfadeler
PEDAGOJIK_UYARI_IFADELERI = {
    "ezberleyiniz": "Yapılandırmacı eğitim modelinde ezber yerine 'kavrayınız, kendi cümlelerinizle açıklayınız' ifadeleri tercih edilmelidir.",
    "ezberleyin": "Öğrenciyi ezbere yönlendirmek yerine keşfedici ve sorgulayıcı yönergeler kullanılmalıdır.",
    "kesinlikle yasaktır": "Buyurgan ve olumsuz ifadeler yerine olumlu davranış kazandıran pedagojik dil kullanılmalıdır.",
    "mecbursunuz": "Zorlayıcı dil yerine öğrenci motivasyonunu artırıcı yönlendirme yapılmalıdır."
}


class KitapAnalizMotoru:
    """
    2. haftada PDF'ten koordinatlarıyla çıkarılan paragrafları
    3 ana MEB kriterine göre analiz eder ve koordinatlı hata raporu üretir.
    """

    def __init__(self, sinif_seviyesi=5):
        self.sinif_seviyesi = sinif_seviyesi
        # Sınıf seviyesine göre maksimum paragraf kelime eşiği (Bilişsel Yük)
        self.max_kelime_esigi = 35 + (sinif_seviyesi * 3)
        self.api_key = os.environ.get("GEMINI_API_KEY", None)

    def _kriter1_dil_ve_imla_kontrolu(self, metin):
        hatalar = []
        kelimeler = re.findall(r'\w+', metin.lower())

        for kelime in kelimeler:
            if kelime in YAZIM_YANLISLARI:
                hatalar.append({
                    "kriter_no": 1,
                    "kriter_adi": "Dil ve Anlatım Doğruluğu",
                    "hata_tipi": "TDK Yazım Yanlışı",
                    "onem_derecesi": "Yüksek",
                    "hatali_ifade": kelime,
                    "aciklama": f"Metinde '{kelime}' kelimesi TDK yazım kurallarına aykırı yazılmıştır.",
                    "duzeltme_onerisi": f"'{kelime}' yerine '{YAZIM_YANLISLARI[kelime]}' kullanılmalıdır."
                })

        # Noktalama kontrolü: Cümle sonu noktalama işareti eksikliği
        temiz = metin.strip()
        if len(temiz) > 20 and temiz[-1] not in [".", "!", "?", ":", "…"]:
            hatalar.append({
                "kriter_no": 1,
                "kriter_adi": "Dil ve Anlatım Doğruluğu",
                "hata_tipi": "Noktalama Eksikliği",
                "onem_derecesi": "Düşük",
                "hatali_ifade": temiz[-15:],
                "aciklama": "Paragraf sonunda uygun bitiş noktalama işareti bulunmamaktadır.",
                "duzeltme_onerisi": "Cümle sonuna anlamına göre nokta (.) veya uygun noktalama işareti eklenmelidir."
            })

        return hatalar

    def _kriter2_pedagojik_uygunluk_kontrolu(self, metin):
        hatalar = []
        kucuk_metin = metin.lower()

        # 1. Kural Tabanlı Pedagojik Denetim
        for ifade, oneri in PEDAGOJIK_UYARI_IFADELERI.items():
            if ifade in kucuk_metin:
                hatalar.append({
                    "kriter_no": 2,
                    "kriter_adi": "Pedagojik Uygunluk ve Tutarlılık",
                    "hata_tipi": "Pedagojik Dil Uyumsuzluğu",
                    "onem_derecesi": "Orta",
                    "hatali_ifade": ifade,
                    "aciklama": f"'{ifade}' ifadesi {self.sinif_seviyesi}. sınıf düzeyinde yapılandırmacı yaklaşıma uygun değildir.",
                    "duzeltme_onerisi": oneri
                })

        # 2. Kavramsal / Bilimsel Tutarlılık Denetimi
        if "güneş dünya'nın etrafında döner" in kucuk_metin or "gunes dunya'nin etrafinda doner" in kucuk_metin:
            hatalar.append({
                "kriter_no": 2,
                "kriter_adi": "Pedagojik Uygunluk ve Tutarlılık",
                "hata_tipi": "Bilimsel / Kavramsal Yanılgı",
                "onem_derecesi": "Yüksek",
                "hatali_ifade": "Güneş Dünya'nın etrafında döner",
                "aciklama": "Metinde astronomik ve bilimsel gerçekliğe aykırı kavramsal hata bulunmaktadır.",
                "duzeltme_onerisi": "'Dünya, Güneş'in etrafında belirli bir yörüngede dolanır' şeklinde düzeltilmelidir."
            })

        return hatalar

    def _kriter3_bilissel_yuk_ve_etkilesim_kontrolu(self, metin, kelime_sayisi, linkler):
        hatalar = []
        kucuk_metin = metin.lower()

        # 1. Bilişsel Yük (Uzun Paragraf / Karmaşık Cümle) Analizi
        if kelime_sayisi > self.max_kelime_esigi:
            hatalar.append({
                "kriter_no": 3,
                "kriter_adi": "Bilişsel Yük ve Dijital Etkileşim",
                "hata_tipi": "Yüksek Bilişsel Yük (Uzun Paragraf)",
                "onem_derecesi": "Orta",
                "hatali_ifade": f"{kelime_sayisi} kelimelik blok",
                "aciklama": f"Paragraf {kelime_sayisi} kelimeden oluşmaktadır. {self.sinif_seviyesi}. sınıf için önerilen üst sınır {self.max_kelime_esigi} kelimedir.",
                "duzeltme_onerisi": "Öğrencinin çalışma belleğini yormamak için paragraf ikiye bölünmeli veya maddeler halinde sunulmalıdır."
            })

        # 2. Dijital Bağlantı / Karekod (URI) Kontrolü
        dijital_anahtarlar = ["karekod", "videoyu", "dijital", "eba", "bağlantı", "baglanti", "tıklayınız", "tiklayiniz"]
        if any(anahtar in kucuk_metin for anahtar in dijital_anahtarlar) and not linkler:
            hatalar.append({
                "kriter_no": 3,
                "kriter_adi": "Bilişsel Yük ve Dijital Etkileşim",
                "hata_tipi": "Eksik Dijital Bağlantı / URI",
                "onem_derecesi": "Yüksek",
                "hatali_ifade": "Dijital etkinlik yönlendirmesi",
                "aciklama": "Metinde dijital bir içeriğe/karekoda atıf yapılmış ancak sayfada gömülü aktif bağlantı (URI) bulunamamıştır.",
                "duzeltme_onerisi": "Sayfaya ilgili EBA/MEB dijital içerik bağlantısı veya karekod linki eklenmelidir."
            })

        return hatalar

    def tum_kitabi_analiz_et(self, cikarilan_bloklar):
        toplam_rapor = []

        for blok in cikarilan_bloklar:
            metin = blok.get("metin", "")
            kelime_sayisi = blok.get("kelime_sayisi", 0)
            linkler = blok.get("sayfadaki_linkler", [])

            blok_hatalari = []
            blok_hatalari.extend(self._kriter1_dil_ve_imla_kontrolu(metin))
            blok_hatalari.extend(self._kriter2_pedagojik_uygunluk_kontrolu(metin))
            blok_hatalari.extend(self._kriter3_bilissel_yuk_ve_etkilesim_kontrolu(metin, kelime_sayisi, linkler))

            if blok_hatalari:
                toplam_rapor.append({
                    "sayfa_no": blok["sayfa_no"],
                    "paragraf_no": blok["paragraf_no"],
                    "koordinatlar": blok["koordinatlar"],
                    "orijinal_metin": metin,
                    "kelime_sayisi": kelime_sayisi,
                    "hata_sayisi": len(blok_hatalari),
                    "bulunan_hatalar": blok_hatalari
                })

        return toplam_rapor


def hata_raporunu_kaydet(rapor_verisi, dosya_yolu="hata_raporu.json"):
    with open(dosya_yolu, "w", encoding="utf-8") as f:
        json.dump(rapor_verisi, f, ensure_ascii=False, indent=4)
    return dosya_yolu