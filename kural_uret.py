#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Üç kademeli hashcat kural seti üretir: hafif.rule, orta.rule, sert.rule.
Kural sözdizimi (hashcat):
  :      hiçbir şey yapma (kelimeyi olduğu gibi dene)
  c      ilk harf büyük        u  tümü büyük     t  büyük/küçük ters çevir
  r      tersten yaz           d  kelimeyi ikile
  $X     sona X ekle           ^X  başa X ekle    sXY  X harfini Y yap
"""

def yaz(dosya, kurallar):
    # tekilleştir, sırayı koru
    seen, out = set(), []
    for k in kurallar:
        if k not in seen:
            seen.add(k); out.append(k)
    with open(dosya, "w") as f:
        f.write("\n".join(out) + "\n")
    return len(out)

son_yillar = ["2020","2021","2022","2023","2024","2025","2026"]

def yil_kurali(y):  # "2024" -> "$2$0$2$4"
    return "".join("$" + d for d in y)

def sayi_ekle(n_basamak, ust):  # 0..ust arası, sabit basamak
    for i in range(ust):
        s = str(i).zfill(n_basamak)
        yield "".join("$" + d for d in s)

# ---------- HAFİF ----------
hafif = [":", "c", "u"]
hafif += ["$" + d for d in "0123456789"]          # sona tek rakam
hafif += ["$1$2$3", "$1$2$3$4"]                    # 123, 1234
hafif += [yil_kurali(y) for y in son_yillar]       # 2020..2026
hafif += ["$!", "$.", "$_"]                         # sık semboller
hafif += ["c$1", "c$1$2$3", "c$2$0$2$4", "c$2$0$2$5"]
hafif += ["so0", "se3", "si1"]                      # temel leet
n_hafif = yaz("hafif.rule", hafif)

# ---------- ORTA ----------
orta = [":", "c", "u", "l", "t", "r"]
orta += list(sayi_ekle(2, 100))                    # 00..99
orta += [yil_kurali(str(y)) for y in range(1980, 2031)]  # 1980..2030
orta += ["c$" + d for d in "0123456789"]           # cX
orta += ["c" + yil_kurali(y) for y in son_yillar]  # c + yil
orta += ["so0", "se3", "si1", "sa@", "ss$", "sg9", "sb8", "st7"]  # leet
orta += ["$!", "$.", "$_", "$*", "$?", "$1$!", "$!$1"]
n_orta = yaz("orta.rule", orta)

# ---------- SERT ----------
sert = list(orta)                                  # orta her şeyi içerir
sert += ["^" + d for d in "0123456789"]            # başa tek rakam
sert += list(sayi_ekle(3, 500))                    # 000..499
# çoklu leet kombinasyonları
leet = ["so0se3", "so0sa@", "se3sa@", "so0si1", "si1se3",
        "so0se3sa@", "so0se3si1", "sa@se3so0", "si1so0se3",
        "cso0", "cse3", "csa@", "cso0se3", "uso0", "use3"]
sert += leet
sert += ["d", "d$1", "f", "{", "}", "$0$0", "$1$1$1", "$6$9",
         "$1$2$3$!", "c$1$2$3$4", "$q", "$w", "c$0$0"]
sert += ["$" + a + "$" + b for a in "!@#" for b in "123"]  # sembol+rakam
n_sert = yaz("sert.rule", sert)

print(f"hafif.rule : {n_hafif} kural")
print(f"orta.rule  : {n_orta} kural")
print(f"sert.rule  : {n_sert} kural")
