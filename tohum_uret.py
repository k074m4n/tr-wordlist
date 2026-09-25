#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Türkçe ŞİFRE TABANLI çekirdek tohum üreteci (~1000+ kelime, ASCII).
Ölçüt: her kelime ya şifrelerde sık geçen bir kalıp, ya yaygın bir
kavram/nesne, ya da sık İngilizce şifre kelimesi. Rastgele nadir kelime yok.
İsim/şehir/takım bloğu modest tutulur (kişisel spesifik kelimeleri sen eklersin).
"""

TR = str.maketrans({"ç":"c","ğ":"g","ı":"i","ö":"o","ş":"s","ü":"u","â":"a",
                    "î":"i","û":"u","Ç":"c","Ğ":"g","İ":"i","I":"i","Ö":"o",
                    "Ş":"s","Ü":"u"})
import unicodedata
def ascii_kucuk(k):
    k = k.strip().translate(TR).lower()
    k = unicodedata.normalize("NFKD", k)
    return "".join(c for c in k if not unicodedata.combining(c))

kategoriler = {}

# --- Selamlaşma / gündelik / ünlemler ---
kategoriler["gunluk"] = """
selam naber merhaba slm mrb nbr naberr selamlar merhabalar gunaydin
iyigunler iyiaksamlar iyigeceler hosgeldin hoscakal gorusuruz bay baybay
tamam tamamdir olur peki hadi haydi yaa yav ya be lan kanka moruk kardes
abi abla birader dostum kanki reis usta hocam patron evet hayir belki
bilmem valla vallahi yani iste sey hah oha vay eyvah aferin bravo yasa
cok az hep hic simdi sonra once bugun yarin dun helal maalesef inanmam
""".split()

# --- Sevgi / ilişki (şifrede en sık) ---
kategoriler["sevgi"] = """
ask askim seni seviyorum canim hayatim bebegim balim guzelim tatlim
melegim bebek prenses prensim askimsin sevgi sevgilim yarim kalbim kalp
sevda hasret ozlem mutluluk huzur umut hayal sevdim seviyorum1
seniseviyorum canimsin askim1 birtanem gozum gozbebegim cicegim gulum
kalbimsin nefesim sevgim gonlum gonul asik sevgili flort iliski beraber
birlikte sonsuzask opuyorum ozluyorum kucak sarilmak askolsun sevgiyle
sevgilim1 askmm bitanem hayatimsin canimmm mutluyum ozledim
""".split()

# --- Kalıp / argo / karakter ---
kategoriler["kalip"] = """
kral efsane bomba harika muhtesem delikanli centilmen beyefendi ozgur
bagimsiz cesur korkusuz yenilmez guclu tek bir yalniz sonsuz ebedi
olumsuz efsanevi reis patron boss kanka kral1 efsane1 gercek gururlu
onurlu serefli namuslu babayigit babacan kabadayi racon adam adamlik mert
mertlik sozum soz yemin kahraman yigit alperen bozkurt kartal sahin efe
delikanlilik dava fedai koruma bela belali sert haşin celik demir
""".split()

# --- Milli / kültürel (Türk şifrelerinde sık) ---
kategoriler["milli"] = """
turk turkiye turkoglu vatan millet bayrak sancak ordu asker mehmetcik
sehit gazi ataturk cumhuriyet istiklal ay yildiz hilal anadolu bozkurt
turan ergenekon oguz kayi altay tanri gokturk selcuklu osmanli fatih
""".split()

# --- İngilizce şifre klasikleri (geniş) ---
kategoriler["ingilizce"] = """
love baby angel forever heart password welcome hello world admin summer
winter money power super mega king queen boss master dragon phoenix ninja
gamer player online star sky moon fire ice happy lucky crazy dark light
shadow black white gold silver football music dream life soul cool best
good pro vip letmein monkey secret hunter warrior legend hero champion
victory freedom trust brave strong wild free magic sunshine rainbow
butterfly diamond crystal thunder storm ocean river mountain forest garden
flower rose lily tiger lion eagle falcon wolf knight castle sword shield
crown throne empire kingdom galaxy cosmos planet comet meteor midnight
sunrise sunset twilight dawn dusk eclipse aurora horizon smile beautiful
princess prince iloveyou babygirl babyboy sweetheart darling honey kiss
mylove truelove soulmate heaven paradise destiny blessed faith hope grace
peace joy spirit energy vibe cute pretty boss1 champ winner rockstar
superstar killer savage beast alpha elite royal noble sunny lovely
""".split()

# --- Klavye desenleri / leet / sık diziler ---
kategoriler["klavye"] = """
qwe qwerty asdf asdasd zxc asd123 qwe123 sifre parola admin test deneme
demo giris kullanici user root pass abc abcabc asdfg qazwsx zxcvbn
password1 admin1 q1w2e3 a1b2c3 aaa zzz asdf1234 qwerty123 iloveyou1
sifre123 parola123 123abc abc123 qweasd zxcasd 1q2w3e trustno1
""".split()

# --- Zaman: ay / gün / mevsim ---
kategoriler["zaman"] = """
ocak subat mart nisan mayis haziran temmuz agustos eylul ekim kasim
aralik pazartesi sali carsamba persembe cuma cumartesi pazar ilkbahar yaz
sonbahar kis bahar sabah oglen aksam gece gunduz gunes yildiz ay hafta
yil saat dakika mevsim tatil dogumgunu yilbasi
""".split()

# --- Gündelik nesne / yer ---
kategoriler["genel"] = """
para ev araba is yol kapi anahtar kitap kalem defter telefon bilgisayar
internet sifre gizli aile okul universite ogretmen ogrenci doktor asker
polis muhendis avukat isci mudur patron sirket ofis market magaza dukkan
cafe restoran hastane eczane banka fabrika koy sehir kasaba mahalle sokak
cadde meydan liman istasyon otobus tren vapur ucak bisiklet motor bahce
balkon pencere masa sandalye yatak koltuk ayna saat cuzdan canta
""".split()

# --- Duygu / sıfat ---
kategoriler["duygu"] = """
mutlu uzgun kizgin sakin deli akilli tatli aci sicak soguk buyuk kucuk
uzun kisa genis dar yeni eski taze dolu bos acik kapali guzel cirkin
zengin fakir hizli yavas sabir cesaret gurur onur seref namus vicdan
merhamet sadakat guven inanc korku nese keder ofke sevinc heyecan merak
tembel caliskan durust iyi kotu dogru yanlis hakli haksiz cesur utangac
neseli huzursuz rahat yorgun dinc genc gencelik
""".split()

# --- Soyut / kavram ---
kategoriler["kavram"] = """
hayat yasam dunya evren zaman mekan gecmis gelecek an sonsuzluk baslangic
son hakikat gercek yalan sir gizem bilgi akil zeka hafiza ruya kabus
dusunce fikir hayal umut ilham yetenek basari zafer kayip hata sans firsat
secim karar amac hedef ozgurluk adalet esitlik kardeslik baris savas
devrim isyan direnis mucadele umutsuzluk pismanlik ozgur
""".split()

# --- Eylem / fiil (emir kipi, kalıplarda geçer) ---
kategoriler["eylem"] = """
gel git bak dur otur kalk gul agla uyu uyan kos yuru atla bekle inan sev
sar op tut ver al koru sakla ac kapa bul kazan yen konus sus dinle duy gor
izle oku yaz ciz cal soyle anlat gulumse dur kacma unut hatirla ozle bekle
sevme birak don gitme kalma saril opucuk
""".split()

# --- Doğa / hayvan / bitki ---
kategoriler["doga"] = """
deniz dag orman gol nehir irmak cicek gul lale papatya menekse orkide
agac yaprak toprak tas kaya magara vadi tepe zirve doruk kumsal sahil ada
cam mese kavak sogut zeytin nar incir dut ceviz findik kedi kopek kus
kartal aslan kaplan ayi kurt tilki at tavsan kelebek balik yilan panter
leopar zebra fil kobra kaplumbaga guvercin marti bulbul serce bulut ruzgar
yagmur kar dolu sis firtina simsek gokkusagi safak dalga gunes yildiz
""".split()

# --- Renk ---
kategoriler["renk"] = """
kirmizi mavi yesil sari siyah beyaz mor pembe turuncu gri kahverengi
lacivert bordo altin gumus turkuaz eflatun krem bej visne
""".split()

# --- Sayı kelimeleri ---
kategoriler["sayi"] = """
bir iki uc dort bes alti yedi sekiz dokuz on yirmi otuz kirk elli yuz bin
milyon milyar sifir ilk son tek cift yarim birinci ikinci ucuncu dorduncu
besinci
""".split()

# --- Dini / kültürel ---
kategoriler["kultur"] = """
bayram ramazan seker kurban cami ezan namaz oruc dua amin insallah
masallah bereket rizik nasip kader kismet sabir sukur mevlana yunus allah
hak nur iman rahman rahim melek cennet gunah sevap helal haram ecel ruh
sadaka zekat hac umre kabe medine
""".split()

# --- Yiyecek / içecek ---
kategoriler["yemek"] = """
cay kahve su ekmek peynir zeytin bal recel domates biber patates pilav
makarna corba kofte kebap doner lahmacun pide borek baklava kunefe
cikolata dondurma elma armut muz portakal karpuz kiraz uzum cilek limon
nane kekik tarcin ayran kola gazoz meyve sebze et tavuk yumurta sut
yogurt tereyagi simit poğaca menemen kahvalti
""".split()

# --- Vücut / aile ---
kategoriler["vucut_aile"] = """
goz kulak burun agiz dis dil el ayak parmak sac kalp beyin kan ten yuz
alin anne baba kardes dede nine torun yegen amca dayi hala teyze enise
gelin damat es koca kari oglan kiz bebek cocuk genc yasli anneanne
babaanne kuzen bacanak nine dede
""".split()

# --- Marka / pop-kültür (leak listelerinde çok sık) ---
kategoriler["marka_pop"] = """
superman batman spiderman ironman goku naruto pokemon mario sonic zelda
minecraft fortnite gaming xbox playstation nintendo steam discord youtube
instagram google android iphone samsung apple nike adidas puma ferrari bmw
audi mercedes toyota honda harley joker gucci prada rolex chanel netflix
whatsapp telegram twitter spotify snapchat tiktok
""".split()

# --- Hobi / spor ---
kategoriler["hobi_spor"] = """
futbol basketbol voleybol tenis yuzme kosu kamp yoga fitness spor antrenman
halisaha mac gol pas sut kale forma formula ralli drift kayak snowboard
dalis surat vites gaz fren direksiyon
""".split()

# --- Halk ağzı / fonetik / kısaltma yazımlar (şifrede ÇOK sık) ---
# İnsanlar doğru yazımı değil, konuştukları gibi yazar: bitanem, meraba...
kategoriler["halk_agzi"] = """
bitanem bitanam birtanam askm askimm askitem askimsss canm canimm canismm
canimmm hayatm hayatimm hayatimsin bebis bebisim bebism bebegm meleyim
guzelm guzelimm tatlimm seviyom sevyorum seviyorm seviom seniseviyom
seniseviyom1 napiyon napion naptin noluyo nolur nasilsn naslsin nabıyon
meraba merabaa merhabaa selamm slm1 mrb1 knk kanks mrk tmm tamamm tamamdr
eyw eyvallah eyvallah1 saol sagol saolun tsk vallaa vallahi insalah insh
masallah maasallah helal hellal hoscakal gorusruz oki okey pekii yaaa yaw
lann aynen aynnen harbi harbiden cidden hadee prensesim kalbimm gozumsun
askimsin1 canimsin1 kimsin nabersin iyiyim iyidir idare
""".split()

# --- Argo / küfür (parola dökümlerinde çok sık; test gerçekçiliği için) ---
kategoriler["argo"] = """
anan ananin baban amk aq mk amına amina koyim koyayim orospu oc pic
gavat pezevenk siktir sikerim sikeyim got gotveren yarrak yarak tasak
ibne ipne pust kahpe kaltak surtuk dol amcik sikik hassiktir hasiktir
serefsiz namussuz salak aptal gerizekali mal dangalak okuz esek hayvan
hiyar keko ezik dallama hoduk angut avanak embesil gerzek ahmak budala
sersem beyinsiz kafasiz manyak deli capsal zibidi zirto ucuz kaltak1
pislik rezil kepaze aptalsin salaksin gerizekalisin oespu amcigi
""".split()

# İSTEĞE BAĞLI popüler isim/takım/şehir (modest). Kapatmak icin False yap.
POPULER_EKSTRA = True
if POPULER_EKSTRA:
    kategoriler["populer_isim"] = """
    mehmet ahmet mustafa ali huseyin hasan ibrahim yusuf murat emre burak
    fatih can cem deniz kaan kerem eren berk arda ayse fatma zeynep elif
    merve busra irem esra sultan zehra pinar gamze derya nur melek yasemin
    """.split()
    kategoriler["populer_takim"] = """
    fenerbahce galatasaray besiktas trabzonspor cimbom aslan kartal kanarya
    fener gala bjk gs fb ts sampiyon forma taraftar carsi
    """.split()
    kategoriler["populer_sehir"] = """
    istanbul ankara izmir bursa antalya adana konya turkiye anadolu
    karadeniz akdeniz ege marmara kadikoy taksim
    """.split()

gorulen, sonuc = set(), []
for grup in kategoriler.values():
    for k in grup:
        k = ascii_kucuk(k)
        if k and k not in gorulen:
            gorulen.add(k); sonuc.append(k)

with open("turkce_tohum.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(sonuc) + "\n")

print(f"Toplam benzersiz (ASCII) kelime: {len(sonuc)}")
