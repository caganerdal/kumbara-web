# kumbara-web

Kumbara uygulamasının internetten okuduğu kira artış oranı tablosu (`rent-index.json`).

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

## Yerel test

```
python3 scripts/update_rent_index.py --fixture scripts/fixtures/evds_sample.json --dry-run
```
