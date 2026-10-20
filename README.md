# 📚 MEB Ders Kitabı Otomatik Hata Tespit Sistemi

Yapay zeka (LLM) destekli, PDF formatındaki MEB ders kitaplarında içerik, pedagojik uygunluk ve tutarlılık hatalarını otomatik olarak tespit eden, sayfa ve koordinat bazlı raporlama yapan yazılım projesi.

## 🚀 Projenin Amacı
Bu proje, Milli Eğitim Bakanlığı (MEB) standartlarına uygun olarak ders kitaplarındaki olası hataları insan gözünden kaçmadan önce tespit etmeyi amaçlar. Sistem, PDF belgelerini yapılandırılmış verilere dönüştürür ve belirlenen 3 ana kritere göre analiz eder.

## ✨ Temel Özellikler

### 1. Akıllı PDF İşleme (Parser) Modülü [Tamamlandı]
- **Koordinat Bazlı (Bounding Box) Okuma:** `PyMuPDF` kullanılarak metinlerin sayfadaki tam koordinatları `(x0, y0, x1, y1)` ile birlikte çekilmesi.
- **Gürültü Filtreleme:** Sayfa üstü ünite adları (header) ve sayfa altı numaralarının (footer) Y-ekseni sınırlarıyla filtrelenmesi.
- **Dijital Bağlantı Yakalama:** Etkileşimli etkinlikler için sayfa içine gömülü linklerin ve URL'lerin otomatik tespiti.

### 2. Yapay Zeka Analiz Kriterleri [Geliştirme Aşamasında]
- **Kriter 1: Dil ve İmla Kuralları:** TDK ve MEB yazım kurallarına aykırı hataların tespiti.
- **Kriter 2: Pedagojik Uygunluk:** İçeriğin hedef yaş grubuna, müfredat yapısına ve bilgi tutarlılığına uygunluğunun Gemini API ile analizi.
- **Kriter 3: Bilişsel Yük ve Etkileşim:** Öğrenciyi yoracak aşırı uzun/monoton paragrafların tespiti ve QR/Link doğrulama mekanizması.

## 🛠️ Kullanılan Teknolojiler
- **Dil:** Python 3.x
- **Belge İşleme:** PyMuPDF (`fitz`)
- **Veri Yapılandırma:** JSON
- **Yapay Zeka:** Gemini API (Planlanan)
- **Versiyon Kontrolü:** Git & GitHub

## ⚙️ Kurulum ve Çalıştırma

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyebilirsiniz:

1. Repoyu klonlayın:
   ```bash
   git clone [https://github.com/sdamlaarici/ders-kitabi-hata-tespit.git](https://github.com/sdamlaarici/ders-kitabi-hata-tespit.git)