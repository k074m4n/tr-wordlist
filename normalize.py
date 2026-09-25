#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Türkçe kelimeleri ASCII + küçük harfe çevirip tekilleştirir.
Kullanım:  python3 normalize.py girdi.txt > cikti.txt
           cat a.txt b.txt | python3 normalize.py > tam_tohum.txt
"""
import sys, unicodedata
TR = str.maketrans({"ç":"c","ğ":"g","ı":"i","ö":"o","ş":"s","ü":"u","â":"a",
                    "î":"i","û":"u","Ç":"c","Ğ":"g","İ":"i","I":"i","Ö":"o",
                    "Ş":"s","Ü":"u"})

def norm(k):
    k = k.strip().translate(TR)          # Türkçe'ye özel önce (İ, I dahil)
    k = k.lower()
    k = unicodedata.normalize("NFKD", k) # kalan birleşik işaretleri ayır
    return "".join(c for c in k if not unicodedata.combining(c))

kaynaklar = [open(a, encoding="utf-8") for a in sys.argv[1:]] or [sys.stdin]
seen, out = set(), []
for src in kaynaklar:
    for satir in src:
        k = norm(satir)
        if k and k not in seen:
            seen.add(k); out.append(k)
sys.stdout.write("\n".join(out) + "\n")
