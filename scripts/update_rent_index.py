#!/usr/bin/env python3
"""Updates rent-index.json with the legal maximum rent increase (TBK m.344).

The cap for contracts renewing in month M is the change in the 12-month average of TÜFE,
using the index published for month M-1:

    rate(M) = avg(index[M-12 .. M-1]) / avg(index[M-24 .. M-13]) - 1

Index data comes from TCMB EVDS, series TP.TUKFIY2025.GENEL (TÜFE, 2025=100).
EVDS needs a free API key: https://evds3.tcmb.gov.tr -> Kayıt Ol -> Profilim -> API Key.

Usage:
    EVDS_API_KEY=... python3 scripts/update_rent_index.py
    python3 scripts/update_rent_index.py --fixture scripts/fixtures/evds_sample.json   # offline test
"""

import argparse
import datetime as dt
import json
import os
import pathlib
import sys
import urllib.request

SERIES = "TP.TUKFIY2025.GENEL"
EVDS_URL = "https://evds3.tcmb.gov.tr/igmevdsms-dis/series={series}&startDate={start}&endDate={end}&type=json"
OUTPUT = pathlib.Path(__file__).resolve().parent.parent / "rent-index.json"
KEEP_MONTHS = 24


def fetch_evds(api_key: str) -> dict:
    today = dt.date.today()
    url = EVDS_URL.format(series=SERIES, start=f"01-01-{today.year - 3}", end=today.strftime("%d-%m-%Y"))
    request = urllib.request.Request(url, headers={"key": api_key, "User-Agent": "kumbara-rent-index"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def parse_index(payload: dict) -> dict[tuple[int, int], float]:
    """Returns {(year, month): index}, skipping months without a value yet."""
    index = {}
    for item in payload.get("items", []):
        value_key = next((k for k in item if k.startswith("TP_")), None)
        value = item.get(value_key) if value_key else None
        if value in (None, "", "null"):
            continue
        year, month = (int(part) for part in str(item["Tarih"]).split("-")[:2])
        index[(year, month)] = float(value)
    return index


def shift(year: int, month: int, delta: int) -> tuple[int, int]:
    total = year * 12 + (month - 1) + delta
    return total // 12, total % 12 + 1


def rent_rates(index: dict[tuple[int, int], float]) -> dict[str, float]:
    """Rate for every renewal month that has 24 months of index data behind it."""
    rates = {}
    for (year, month) in sorted(index):
        last12 = [index.get(shift(year, month, -i)) for i in range(12)]
        prev12 = [index.get(shift(year, month, -i)) for i in range(12, 24)]
        if None in last12 or None in prev12:
            continue
        rate = (sum(last12) / 12) / (sum(prev12) / 12) - 1
        renewal_year, renewal_month = shift(year, month, 1)
        rates[f"{renewal_year:04d}-{renewal_month:02d}"] = round(rate, 4)
    return rates


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", help="Read EVDS JSON from a file instead of the API")
    parser.add_argument("--dry-run", action="store_true", help="Print the result without writing")
    args = parser.parse_args()

    if args.fixture:
        payload = json.loads(pathlib.Path(args.fixture).read_text())
    else:
        api_key = os.environ.get("EVDS_API_KEY")
        if not api_key:
            print("EVDS_API_KEY tanımlı değil. GitHub > Settings > Secrets and variables > Actions altına ekle.", file=sys.stderr)
            return 1
        payload = fetch_evds(api_key)

    computed = rent_rates(parse_index(payload))
    if not computed:
        print("EVDS verisinden oran hesaplanamadı (en az 24 aylık endeks gerekir).", file=sys.stderr)
        return 1

    # Sanity check: published caps have stayed between -10% and +200%.
    bad = {month: rate for month, rate in computed.items() if not -0.1 < rate < 2}
    if bad:
        print(f"Beklenmeyen oranlar, dosya güncellenmedi: {bad}", file=sys.stderr)
        return 1

    document = json.loads(OUTPUT.read_text()) if OUTPUT.exists() else {"rates": []}
    merged = {entry["month"]: entry["rate"] for entry in document.get("rates", [])}
    merged.update(computed)
    months = sorted(merged)[-KEEP_MONTHS:]
    new_rates = [{"month": month, "rate": merged[month]} for month in months]

    if new_rates == document.get("rates"):
        print("Değişiklik yok.")
        return 0

    document["rates"] = new_rates
    document["updatedAt"] = dt.date.today().isoformat()
    text = json.dumps(document, ensure_ascii=False, indent=2) + "\n"
    if args.dry_run:
        print(text)
    else:
        OUTPUT.write_text(text)
        print(f"Güncellendi. En son ay: {months[-1]} → %{merged[months[-1]] * 100:.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
