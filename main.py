import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
from math import ceil
from sympy import symbols, diff
import random

# Global değişkenlerimiz
ozel_alfabe = "abcçdefgğhıijklmnoöpqrsştuüvwxyzABCÇDEFGĞHIİJKLMNOÖQRSŞTUÜWVXYZ.,:;-+!?/*1234567890 "
frekans = []
kaydirma = None

# x sembolünü ve fonksiyonları tanımladık
x = symbols('x')
fonksiyonlar = [4 * x ** 3, 2 * x ** 4 + 3 * x + 5, x ** 4 - 6 * x ** 4 + 8]


def kaydirma_degeri_hesapla():
    rastgele_x_degeri = random.randint(1, 100)
    secilen_fonksiyon = random.choice(fonksiyonlar)
    turev = diff(secilen_fonksiyon, x, 2)
    sonuc = turev.subs(x, rastgele_x_degeri)
    alfabe_uzunlugu = len(ozel_alfabe)
    return int(sonuc % alfabe_uzunlugu)


kaydirma = kaydirma_degeri_hesapla()


class DugumAgaci(object):
    def __init__(self, sol=None, sag=None):
        self.sol = sol
        self.sag = sag

    def cocuklar(self):
        return (self.sol, self.sag)

    def __str__(self):
        return '%s_%s' % (self.sol, self.sag)


huffmanKodu = {}


def huffman_kod_agaci(dugum, sol=True, binString=''):
    if type(dugum) is str:
        return {dugum: binString}
    (l, r) = dugum.cocuklar()
    d = dict()
    d.update(huffman_kod_agaci(l, True, binString + '0'))
    d.update(huffman_kod_agaci(r, False, binString + '1'))
    return d


def huffman_hesapla(veri):
    global huffmanKodu, frekans
    frekans = {}
    for c in veri:
        if c in frekans:
            frekans[c] += 1
        else:
            frekans[c] = 1

    frekans = sorted(frekans.items(), key=lambda x: x[1], reverse=True)
    dugumler = frekans

    while len(dugumler) > 1:
        (anahtar1, c1) = dugumler[-1]
        (anahtar2, c2) = dugumler[-2]
        dugumler = dugumler[:-2]
        dugum = DugumAgaci(anahtar1, anahtar2)
        dugumler.append((dugum, c1 + c2))
        dugumler = sorted(dugumler, key=lambda x: x[1], reverse=True)

    huffmanKodu = huffman_kod_agaci(dugumler[0][0])
    sifrelenmis_veri = ''.join([huffmanKodu[karakter] for karakter in veri])

    original_bit_size = len(veri) * 8
    compressed_bit_size = len(sifrelenmis_veri)

    tasarruf_yuzdesi = ((original_bit_size - compressed_bit_size) / original_bit_size) * 100

    return sifrelenmis_veri, original_bit_size, compressed_bit_size, tasarruf_yuzdesi


original_bit_size = None
compressed_bit_size = None
tasarruf_yuzdesi = None

sifrelenmis_metin = ""

def ozel_sifrele(metin):
    global kaydirma, sifrelenmis_metin
    sifrelenmis_metin = ""
    for karakter in metin:
        if karakter in ozel_alfabe:
            yeni_index = (ozel_alfabe.index(karakter) + kaydirma) % len(ozel_alfabe)
            sifrelenmis_metin += ozel_alfabe[yeni_index]
        else:
            sifrelenmis_metin += karakter
            sifrelenmis_metin="burada şifreleme sonucunuz olacak"
    return sifrelenmis_metin


def veri_gonder():
    global original_bit_size, compressed_bit_size, tasarruf_yuzdesi
    veri = metin_giris.get("1.0", 'end-1c')
    veri = veri.replace('\xa0', ' ')  # NBSP'yi kaldırır
    giris_cerceve.pack_forget()
    cikti_cerceve.pack(padx=20, pady=20)

    sifrelenmis_veri = ozel_sifrele(veri)

    sifrelenmis_veri_huffman, original_bit_size, compressed_bit_size, tasarruf_yuzdesi = huffman_hesapla(
        sifrelenmis_veri)
    byte = ceil(original_bit_size / 8)
    compressed_byte = ceil(compressed_bit_size / 8)

    sonuc = f"Huffman ile Şifrelenmiş Veri:\n{sifrelenmis_veri_huffman}\n"
    sonuc += f"Orijinal Veri Boyutu: {original_bit_size} bit ve {byte} byte  \n"
    sonuc += f"Sıkıştırılmış Veri Boyutu: {compressed_bit_size} bit ve {compressed_byte} byte \n"
    sonuc += f"Veri Tasarrufu: %{tasarruf_yuzdesi:.2f}\n"
    metin_cikti.delete(1.0, tk.END)
    metin_cikti.insert(tk.END, sonuc)


def desifrele_veri():
    global huffmanKodu, frekans, original_bit_size, compressed_bit_size, tasarruf_yuzdesi
    desifrele_buton.pack_forget()

    # Kullanıcıdan Huffman kodunu alıyoruz
    huffman_kodu = desifre_metin_giris.get("1.0", 'end-1c')

    # Huffman kodunu kullanarak şifrelenmiş veriyi elde ediyoruz
    ters_huffmanKodu = {v: k for k, v in huffmanKodu.items()}
    karakter = ""
    sifrelenmis_veri = ""
    for bit in huffman_kodu:
        karakter += bit
        if karakter in ters_huffmanKodu:
            sifrelenmis_veri += ters_huffmanKodu[karakter]
            karakter = ""

    # Şifrelenmiş veriyi özel şifreleme algoritması ile deşifre ediyoruz
    desifrelenmis_veri = ""
    for karakter in sifrelenmis_veri:
        if karakter in ozel_alfabe:
            eski_index = (ozel_alfabe.index(karakter) - kaydirma) % len(ozel_alfabe)
            desifrelenmis_veri += ozel_alfabe[eski_index]
        else:
            desifrelenmis_veri += karakter

    sonuc_text = 'Deşifrelenmiş Veri: ' + desifrelenmis_veri + '\n'
    desifre_metin_giris.delete("1.0", tk.END)
    desifre_metin_giris.insert("1.0", sonuc_text)



def geri_don():
    giris_cerceve.pack_forget()
    cikti_cerceve.pack_forget()
    desifre_cerceve.pack_forget()
    menu_cerceve.pack(padx=20, pady=20)


def cikis_yap():
    pencere.destroy()


def ana_menu():
    giris_cerceve.pack_forget()
    cikti_cerceve.pack_forget()
    desifre_cerceve.pack_forget()
    frekans_cerceve.pack_forget()
    menu_cerceve.pack(padx=20, pady=20)


def sifreleme_ekrani():
    menu_cerceve.pack_forget()
    giris_cerceve.pack(padx=20, pady=20)


pencere = tk.Tk()
pencere.title("Huffman Şifreleme")


def alfabeyi_otele(kaydirma, ozel_alfabe):
    return ozel_alfabe[kaydirma:] + ozel_alfabe[:kaydirma]


def karakter_frekans_ekrani():
    cikti_cerceve.pack_forget()
    frekans_cerceve.pack(padx=20, pady=20)

    frekans_text = ' Karakter | Frekans \n'
    frekans_text += '---------------------\n'
    for (karakter, frekan) in frekans:
        frekans_text += ' %-4r | %-9d \n' % (karakter, frekan)

    otelemis_alfabe = alfabeyi_otele(kaydirma, ozel_alfabe)
    frekans_text += '---------------------\n'
    frekans_text+=f'şifrelenmiş veri ={sifrelenmis_metin} \n'
    frekans_text += f"Ötelenmiş Alfabe: {otelemis_alfabe}\n"

    frekans_metin_cikti.delete(1.0, tk.END)
    frekans_metin_cikti.insert(tk.END, frekans_text)


frekans_cerceve = tk.Frame(pencere, padx=10, pady=10)
frekans_metin_cikti = scrolledtext.ScrolledText(frekans_cerceve, wrap=tk.WORD, width=40, height=10)
frekans_metin_cikti.pack()

geri_buton_frekans = tk.Button(frekans_cerceve, text="Geri", command=ana_menu)
geri_buton_frekans.pack(side=tk.LEFT, padx=10)

cikis_buton_frekans = tk.Button(frekans_cerceve, text="Çıkış", command=cikis_yap)
cikis_buton_frekans.pack(side=tk.RIGHT, padx=10)


def desifreleme_ekrani():
    menu_cerceve.pack_forget()
    desifre_cerceve.pack(padx=20, pady=20)


menu_cerceve = tk.Frame(pencere, padx=10, pady=10)
menu_cerceve.pack(padx=20, pady=20)

# Huffman ağacı resmi ekledik resmi Yapay Zeka ile oluşturduk.
resim_yolu = "huffmant_ree.png"
resim = Image.open(resim_yolu)
resim = resim.resize((225, 225))
tk_resim = ImageTk.PhotoImage(resim)
resim_etiketi = tk.Label(menu_cerceve, image=tk_resim)
resim_etiketi.grid(row=0, column=0, columnspan=2, pady=20)

sifrele_buton = tk.Button(menu_cerceve, text="Şifrele", command=sifreleme_ekrani)
sifrele_buton.grid(row=1, column=0, padx=10)

desifrele_buton = tk.Button(menu_cerceve, text="Deşifre", command=desifreleme_ekrani)
desifrele_buton.grid(row=1, column=1, padx=10)

giris_cerceve = tk.Frame(pencere, padx=10, pady=10)
etiket_giris = tk.Label(giris_cerceve, text="Şifrelenecek metni giriniz:")
etiket_giris.pack(padx=10, pady=5)
metin_giris = scrolledtext.ScrolledText(giris_cerceve, wrap=tk.WORD, width=40, height=10)
metin_giris.pack()

sifrele_buton = tk.Button(giris_cerceve, text="Metni Şifrele", command=veri_gonder)
sifrele_buton.pack(pady=10)

geri_buton = tk.Button(giris_cerceve, text="Geri", command=geri_don)
geri_buton.pack(side=tk.LEFT, padx=10)

cikis_buton = tk.Button(giris_cerceve, text="Çıkış", command=cikis_yap)
cikis_buton.pack(side=tk.RIGHT, padx=10)

cikti_cerceve = tk.Frame(pencere, padx=10, pady=10)

metin_cikti = scrolledtext.ScrolledText(cikti_cerceve, wrap=tk.WORD, width=40, height=10)
metin_cikti.pack()
devam_buton_cikti = tk.Button(cikti_cerceve, text="Karakter ve Frekans", command=karakter_frekans_ekrani)
devam_buton_cikti.pack(pady=10)

geri_buton_cikti = tk.Button(cikti_cerceve, text="Geri", command=geri_don)
geri_buton_cikti.pack(side=tk.LEFT, padx=10)

cikis_buton_cikti = tk.Button(cikti_cerceve, text="Çıkış", command=cikis_yap)
cikis_buton_cikti.pack(side=tk.RIGHT, padx=10)

desifre_cerceve = tk.Frame(pencere, padx=10, pady=10)
desifre_metin_giris = scrolledtext.ScrolledText(desifre_cerceve, wrap=tk.WORD, width=40, height=10)
desifre_metin_giris.pack()

desifrele_buton = tk.Button(desifre_cerceve, text="Veriyi Deşifrele", command=desifrele_veri)

desifrele_buton.pack(pady=10)

geri_buton_desifre = tk.Button(desifre_cerceve, text="Geri", command=ana_menu)
geri_buton_desifre.pack(side=tk.LEFT, padx=10)

cikis_buton_desifre = tk.Button(desifre_cerceve, text="Çıkış", command=cikis_yap)
cikis_buton_desifre.pack(side=tk.RIGHT, padx=10)

pencere.mainloop()
