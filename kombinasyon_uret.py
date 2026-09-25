#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tohum listesinden 1'li, 2'li ve 3'lü sıralı kombinasyonlar üretir.
Varsayılan: stdout'a akıtır (hashcat'e pipe için). Diske yazmaz.

Kullanım:
  # Doğrudan hashcat'e pipe (ÖNERİLEN, diske dev dosya yazmaz):
  python3 kombinasyon_uret.py turkce_tohum.txt | hashcat -m 22000 hash.hc22000

  # Sadece 2'li kombinasyonlar:
  python3 kombinasyon_uret.py turkce_tohum.txt --min 2 --max 2 | hashcat ...

  # Dosyaya yaz (DİKKAT: 3'lü çok büyük olabilir!):
  python3 kombinasyon_uret.py turkce_tohum.txt -o wordlist.txt

  # Aynı kelimenin tekrarına izin ver (askask gibi), sayı patlar:
  python3 kombinasyon_uret.py turkce_tohum.txt --tekrar
"""
import sys
import argparse
from itertools import permutations, product


def kelimeleri_oku(yol):
    with open(yol, encoding="utf-8") as f:
        return [s.strip() for s in f if s.strip()]


def uret(kelimeler, mn, mx, tekrar):
    kaynak = product if tekrar else permutations
    for n in range(mn, mx + 1):
        if n == 1:
            for k in kelimeler:
                yield k
        else:
            for combo in kaynak(kelimeler, n):
                yield "".join(combo)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("tohum", help="Tohum listesi dosyası")
    p.add_argument("--min", type=int, default=1, dest="mn")
    p.add_argument("--max", type=int, default=3, dest="mx")
    p.add_argument("-o", "--cikti", default=None,
                   help="Dosyaya yaz (yoksa stdout'a akıtır)")
    p.add_argument("--tekrar", action="store_true",
                   help="Aynı kelime bir kombinasyonda tekrar edebilir")
    p.add_argument("--tahmin", action="store_true",
                   help="Sadece toplam aday sayısını tahmin et, üretme")
    args = p.parse_args()

    kelimeler = kelimeleri_oku(args.tohum)
    N = len(kelimeler)

    if args.tahmin:
        toplam = 0
        for n in range(args.mn, args.mx + 1):
            if args.tekrar:
                adet = N ** n
            else:
                adet = 1
                for i in range(n):
                    adet *= (N - i)
            print(f"{n}'li: {adet:,}", file=sys.stderr)
            toplam += adet
        print(f"TOPLAM: {toplam:,} aday", file=sys.stderr)
        print(f"(~{toplam * 15 / 1e9:.1f} GB tahmini dosya boyutu)", file=sys.stderr)
        return

    gen = uret(kelimeler, args.mn, args.mx, args.tekrar)

    if args.cikti:
        with open(args.cikti, "w", encoding="utf-8") as f:
            for aday in gen:
                f.write(aday + "\n")
    else:
        out = sys.stdout
        try:
            for aday in gen:
                out.write(aday + "\n")
        except BrokenPipeError:
            # hashcat şifreyi bulup pipe'ı kapattığında sessizce çık
            try:
                out.close()
            except Exception:
                pass


if __name__ == "__main__":
    main()
