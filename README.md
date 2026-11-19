# kumbara-web

Kumbara uygulamasının internetten okuduğu dosyalar:

- `rent-index.json`: kira artış oranı tablosu (elle güncellenir, aşağıya bak).
- `legal.json`: mevduat stopaj oranları ve Ramazan/Kurban Bayramı günleri (elle güncellenir, aşağıya bak).
- `gizlilik.html`: gizlilik politikası; App Store / Play Console'a ve uygulamaya bu adres verilir:
  https://caganerdal.github.io/kumbara-web/gizlilik.html.

Uygulama dosyaları açılışta indirir; değişiklik için uygulama güncellemesi gerekmez.

## rent-index.json (elle)

TÜİK her ayın 3'ünde enflasyonu açıklar; açıklamada "TÜFE 12 aylık ortalamalara göre değişim" oranı yasal azami kira
artışıdır. Bu oranı GitHub web sitesinde (telefondan da olur) dosyanın sonuna ekle. `month` alanı **kira yenileme ayıdır**:
Ekim enflasyonuyla açıklanan oran `"2026-11"` satırına yazılır, `rate` ondalık olarak (%31,49 → `0.3149`).
Eklemezsen uygulama son bilinen oranı "tahmini" diye gösterir. Sonra `updatedAt` tarihini de güncelle.

## legal.json (elle)

Uygulama bu dosyayı günde en fazla iki kez indirir; bozuk ya da mantıksız bir dosya gelirse (oran %0–50 dışında,
gün sınırları sıralı değil) eskisini kullanmaya devam eder.

- **Stopaj değişince** (Cumhurbaşkanı Kararı): `depositWithholding` satırlarını güncelle. `upToDays` vadenin üst sınırı
  (gün), son satırda `null`. Örnek: 6 aya kadar `184`, 1 yıla kadar `366`.
- **Her yıl Diyanet takvimi açıklanınca**: `religiousHolidays` altına yeni yılı `"AA-GG"` biçiminde ekle
  (arife yarım gün olduğu için yazılmaz). Vergi son günü bu günlere denk gelirse ertesi iş gününe kayar.
- Değişiklikten sonra `updatedAt` tarihini de güncelle.
