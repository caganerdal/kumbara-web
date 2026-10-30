# kumbara-web

Kumbara uygulamasının internetten okuduğu dosyalar:

- `rent-index.json`: kira artış oranı tablosu (her ay otomatik güncellenir, aşağıya bak).
- `legal.json`: mevduat stopaj oranları ve Ramazan/Kurban Bayramı günleri (elle güncellenir, aşağıya bak).
- `gizlilik.html`: gizlilik politikası; App Store / Play Console'a ve uygulamaya bu adres verilir:
  https://caganerdal.github.io/kumbara-web/gizlilik.html (yayınlamadan önce `ILETISIM_EPOSTASI` yerine iletişim adresini yaz).

Her ay TÜİK enflasyonu açıkladıktan sonra GitHub Actions, TCMB EVDS'den TÜFE endeksini çeker,
yasal azami kira artışını (TÜFE'nin 12 aylık ortalamalara göre değişimi) hesaplar ve dosyayı günceller.
Uygulama dosyayı açılışta indirir; uygulama güncellemesi gerekmez.

## Kurulum (bir kez)

1. Bu klasörü GitHub'da **herkese açık** `kumbara-web` adlı bir depo olarak yayınla:
   ```
   cd kumbara-web
   git init && git add . && git commit -m "Kira artış tablosu"
   gh repo create kumbara-web --public --source . --push
   ```
2. GitHub Pages'i aç: depo → **Settings → Pages → Source: Deploy from a branch → main / (root)**.
   Birkaç dakika sonra dosya şu adreste görünür: https://caganerdal.github.io/kumbara-web/rent-index.json
   (Uygulama bu adresi okuyor: `Shared/Models/RentContract.swift` → `RentIndex.remoteURL`.)
3. TCMB EVDS'den ücretsiz API anahtarı al: https://evds3.tcmb.gov.tr → **Kayıt Ol** → **Profilim → API Key**.
4. Anahtarı depoya gizli değişken olarak ekle: **Settings → Secrets and variables → Actions → New repository secret**,
   adı `EVDS_API_KEY`.
5. **Actions → Kira artış oranını güncelle → Run workflow** ile bir kez elle çalıştırıp yeşil yandığını kontrol et.

Bundan sonra iş akışı her ayın 3–8'i arasında kendiliğinden çalışır.

## Elle güncelleme

İş akışı bir ay çalışmazsa `rent-index.json` dosyasını GitHub web sitesinde (telefondan da olur) düzenleyip
yeni ayı ekleyebilirsin. `month` alanı **kira yenileme ayıdır**: Eylül enflasyonuyla hesaplanan oran `"2026-10"` satırına yazılır.

## legal.json (elle)

Uygulama bu dosyayı günde en fazla iki kez indirir; bozuk ya da mantıksız bir dosya gelirse (oran %0–50 dışında,
gün sınırları sıralı değil) eskisini kullanmaya devam eder.

- **Stopaj değişince** (Cumhurbaşkanı Kararı): `depositWithholding` satırlarını güncelle. `upToDays` vadenin üst sınırı
  (gün), son satırda `null`. Örnek: 6 aya kadar `184`, 1 yıla kadar `366`.
- **Her yıl Diyanet takvimi açıklanınca**: `religiousHolidays` altına yeni yılı `"AA-GG"` biçiminde ekle
  (arife yarım gün olduğu için yazılmaz). Vergi son günü bu günlere denk gelirse ertesi iş gününe kayar.
- Değişiklikten sonra `updatedAt` tarihini de güncelle.

## Yerel test

```
python3 scripts/update_rent_index.py --fixture scripts/fixtures/evds_sample.json --dry-run
```
