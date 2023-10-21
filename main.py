import tkinter as tk
from tkinter import scrolledtext


# Huffman Kodlama

class DugumAgaci(object):
    def __init__(self, sol=None, sag=None):
        self.sol = sol
        self.sag = sag

    def cocuklar(self):
        return (self.sol, self.sag)

    def __str__(self):
        return '%s_%s' % (self.sol, self.sag)


def huffman_kod_agaci(dugum, sol=True, binString=''):
    if type(dugum) is str:
        return {dugum: binString}
    (l, r) = dugum.cocuklar()
    d = dict()
    d.update(huffman_kod_agaci(l, True, binString + '0'))
    d.update(huffman_kod_agaci(r, False, binString + '1'))
    return d


def huffman_hesapla(veri):
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
    sonuc = ' Karakter | Frekans | Huffman kodu \n'
    sonuc += '-----------------------------------\n'
    for (karakter, frekan) in frekans:
        sonuc += ' %-4r | %-9d | %s\n' % (karakter, frekan, huffmanKodu[karakter])

    sifrelenmis_veri = ''.join([huffmanKodu[karakter] for karakter in veri])
    sonuc += '-----------------------------------\n'
    sonuc += 'Şifrelenmiş Veri: ' + sifrelenmis_veri

    return sonuc


def veri_gonder():
    veri = metin_giris.get("1.0", 'end-1c')
    giris_cerceve.pack_forget()
    cikti_cerceve.pack(padx=20, pady=20)
    sonuc = huffman_hesapla(veri)
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


def desifreleme_ekrani():
    menu_cerceve.pack_forget()
    desifre_cerceve.pack(padx=20, pady=20)


pencere = tk.Tk()
pencere.title("Huffman Şifreleme")

menu_cerceve = tk.Frame(pencere, padx=10, pady=10)
menu_cerceve.pack(padx=20, pady=20)

sifrele_buton = tk.Button(menu_cerceve, text="Şifrele", command=sifreleme_ekrani)
sifrele_buton.grid(row=0, column=0, padx=10)

desifrele_buton = tk.Button(menu_cerceve, text="Deşifre", command=desifreleme_ekrani)
desifrele_buton.grid(row=0, column=1, padx=10)

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

geri_buton_cikti = tk.Button(cikti_cerceve, text="Geri", command=geri_dön)
geri_buton_cikti.pack(side=tk.LEFT, padx=10)

cikis_buton_cikti = tk.Button(cikti_cerceve, text="Çıkış", command=cikis_yap)
cikis_buton_cikti.pack(side=tk.RIGHT, padx=10)

desifre_cerceve = tk.Frame(pencere, padx=10, pady=10)
desifre_metin_giris = scrolledtext.ScrolledText(desifre_cerceve, wrap=tk.WORD, width=40, height=10)
desifre_metin_giris.pack()

desifrele_buton = tk.Button(desifre_cerceve, text="Metni Deşifrele", command=veri_gonder)
desifrele_buton.pack(pady=10)

geri_buton_desifre = tk.Button(desifre_cerceve, text="Geri", command=ana_menu)
geri_buton_desifre.pack(side=tk.LEFT, padx=10)

cikis_buton_desifre = tk.Button(desifre_cerceve, text="Çıkış", command=cikis_yap)
cikis_buton_desifre.pack(side=tk.RIGHT, padx=10)

pencere.mainloop()
