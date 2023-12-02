import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import hashlib

# Huffman Ağacı ile Şifreleme ve Deşifreleme
frekans = []

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

def desifrele(huffmanKodu, sifrelenmis_veri):
    ters_huffmanKodu = {v: k for k, v in huffmanKodu.items()}
    karakter = ""
    desifrelenmis_veri = ""
    for bit in sifrelenmis_veri:
        karakter += bit
        if karakter in ters_huffmanKodu:
            desifrelenmis_veri += ters_huffmanKodu[karakter]
            karakter = ""
    return desifrelenmis_veri
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
    return sifrelenmis_veri
def desifrele_veri():
    sifrelenmis_veri = desifre_metin_giris.get("1.0", 'end-1c')
    sonuc = desifrele(huffmanKodu, sifrelenmis_veri)
    sonuc_text = ' Karakter | Frekans \n'
    sonuc_text += '---------------------\n'
    for (karakter, frekan) in frekans:
        sonuc_text += ' %-4r | %-9d \n' % (karakter, frekan)
    sonuc_text += '---------------------\n'
    sonuc_text += 'Deşifrelenmiş Veri: ' + sonuc
    desifre_metin_giris.delete(1.0, tk.END)
    desifre_metin_giris.insert(tk.END, sonuc_text)


def md5_sifrele(veri):
    md5_obj = hashlib.md5()
    md5_obj.update(veri.encode('utf-8'))
    return md5_obj.hexdigest()


def veri_gonder():
    veri = metin_giris.get("1.0", 'end-1c')
    giris_cerceve.pack_forget()
    cikti_cerceve.pack(padx=20, pady=20)

    sifrelenmis_veri = huffman_hesapla(veri)
    md5_sonuc = md5_sifrele(sifrelenmis_veri)

    sonuc = "Huffman ile Şifrelenmiş Veri:\n" + sifrelenmis_veri + "\n\nHuffman ve MD5 ile Şifrelenmiş Veri:\n" + md5_sonuc

    metin_cikti.delete(1.0, tk.END)
    metin_cikti.insert(tk.END, sonuc)

def geri_dön():
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
    menu_cerceve.pack(padx=20, pady=20)


def sifreleme_ekrani():
    menu_cerceve.pack_forget()
    giris_cerceve.pack(padx=20, pady=20)

pencere = tk.Tk()
pencere.title("Huffman Şifreleme")
def karakter_frekans_ekrani():
    cikti_cerceve.pack_forget()
    frekans_cerceve.pack(padx=20, pady=20)

    frekans_text = ' Karakter | Frekans \n'
    frekans_text += '---------------------\n'
    for (karakter, frekan) in frekans:
        frekans_text += ' %-4r | %-9d \n' % (karakter, frekan)

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

#Huffman ağacı resmi ekledik resmi Yapay Zeka ile oluşturduk.
resim_yolu = "OIG.jfif"
resim = Image.open(resim_yolu)
resim = resim.resize((150, 150))
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

geri_buton = tk.Button(giris_cerceve, text="Geri", command=geri_dön)
geri_buton.pack(side=tk.LEFT, padx=10)

cikis_buton = tk.Button(giris_cerceve, text="Çıkış", command=cikis_yap)
cikis_buton.pack(side=tk.RIGHT, padx=10)

cikti_cerceve = tk.Frame(pencere, padx=10, pady=10)

metin_cikti = scrolledtext.ScrolledText(cikti_cerceve, wrap=tk.WORD, width=40, height=10)
metin_cikti.pack()
devam_buton_cikti = tk.Button(cikti_cerceve, text="Karakter ve Frekans", command=karakter_frekans_ekrani)
devam_buton_cikti.pack(pady=10)

geri_buton_cikti = tk.Button(cikti_cerceve, text="Geri", command=geri_dön)
geri_buton_cikti.pack(side=tk.LEFT, padx=10)

cikis_buton_cikti = tk.Button(cikti_cerceve, text="Çıkış", command=cikis_yap)
cikis_buton_cikti.pack(side=tk.RIGHT, padx=10)

desifre_cerceve = tk.Frame(pencere, padx=10, pady=10)
desifre_metin_giris = scrolledtext.ScrolledText(desifre_cerceve, wrap=tk.WORD, width=40, height=10)
desifre_metin_giris.pack()

desifrele_buton = tk.Button(desifre_cerceve, text="Metni Deşifrele", command=desifrele_veri)

desifrele_buton.pack(pady=10)

geri_buton_desifre = tk.Button(desifre_cerceve, text="Geri", command=ana_menu)
geri_buton_desifre.pack(side=tk.LEFT, padx=10)

cikis_buton_desifre = tk.Button(desifre_cerceve, text="Çıkış", command=cikis_yap)
cikis_buton_desifre.pack(side=tk.RIGHT, padx=10)

pencere.mainloop()
