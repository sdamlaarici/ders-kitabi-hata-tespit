import fitz  # PyMuPDF
import json

def pdf_metin_ve_koordinat_cikar(pdf_yolu, ust_sinir=50, alt_sinir_farki=50):
    """PDF dosyasından metinleri, koordinatları ve linkleri filtreleyerek çıkarır."""
    doc = fitz.open(pdf_yolu)
    cikarilan_veri = []

    for sayfa_index in range(len(doc)):
        sayfa = doc.load_page(sayfa_index)
        sayfa_yuksekligi = sayfa.rect.height
        bloklar = sayfa.get_text("blocks")
        
        # Sayfadaki tıklanabilir dijital bağlantıları (linkleri) yakala
        linkler = [link.get("uri", "") for link in sayfa.get_links() if "uri" in link]
        paragraf_sayaci = 0

        for b in bloklar:
            x0, y0, x1, y1, metin, blok_no, blok_tipi = b
            
            # Sadece metin bloklarını al (resimleri atla)
            if blok_tipi != 0:
                continue

            temiz_metin = metin.strip().replace("\n", " ")

            # Header ve Footer filtreleme
            if y0 < ust_sinir or y1 > (sayfa_yuksekligi - alt_sinir_farki):
                continue

            if len(temiz_metin) > 5:
                paragraf_sayaci += 1
                cikarilan_veri.append({
                    "sayfa_no": sayfa_index + 1,
                    "paragraf_no": paragraf_sayaci,
                    "koordinatlar": {
                        "x0": round(x0, 2), "y0": round(y0, 2), 
                        "x1": round(x1, 2), "y1": round(y1, 2)
                    },
                    "kelime_sayisi": len(temiz_metin.split()),
                    "metin": temiz_metin,
                    "sayfadaki_linkler": linkler
                })

    doc.close()
    return cikarilan_veri

def json_olarak_kaydet(veri, cikti_yolu="cikti_verisi.json"):
    with open(cikti_yolu, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=4)
    return cikti_yolu