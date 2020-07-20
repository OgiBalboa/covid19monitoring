import tkinter
from tkinter import ttk
from tkinter import *
import matplotlib.pyplot as plt
import json
import http.client
from datetime import datetime
conn = http.client.HTTPSConnection("api.covid19api.com")

headers = {
    'content-type': "application/json",
    'authorization': "apikey your_token"
    }

ulkeler = ["us"] # Sistemdeki Ülkeleri Listele
conn.request("GET","/countries")
for ulke in json.loads(conn.getresponse().read().decode("utf-8")): # json.loads veriyi json diline çevirir. getresponse() API'den gelen cevabı alır ve read() ile okur
    # Veriyi anlaşılır bir srtinge çevirmek için decode() kullanılır ve utf-8 formatında okunur.
    ulkeler.append(ulke["Country"].lower().replace(" ","-")) # for döngüsü ile tüm ülkeler tek tek diziye eklenir.

vaka_sayilari = [] # Vaka sayıları bu değişkene eklenecektir.

def tarih_ayarla(): #Kullanıcıdan gelen tarih bilgisi güncel tarihe göre ayarlanır.
    global date
    date = [] # istenilen tarih aralığı bu değişkene eklenir.
    anlik_tarih = str(datetime.now())
    ay = int(anlik_tarih[5:7])  # Ay bilgisi çıkarma işlemi yapabilmek için integer'a çevrilir.
    if tarih.get() == "Last Month":
        date.append(anlik_tarih[0:7]) #datetime dan gelen bilgiye göre ilk 7 eleman bu yıl ve bu ay bilgisini içerir. 
    elif tarih.get() == "Last 3 Months":
        date.append(anlik_tarih[0:7])
        if ay > 3 :
            for i in range(2):            
                ay -= 1
                if ay < 10:
                    ay = "0" + str(ay)
                date.append(anlik_tarih[0:5] + str(ay))
                ay = int(ay) # Ay bilgisi çıkarma işlemi yapabilmek için integer'a çevrilir.
def grafik ():
    if len(vaka_sayilari) <1:
        return
    x_ekseni = []
    for i in range(len(vaka_sayilari)): # Vaka sayısı bilgisi kadar gün sayısı x eksenine eklenir.
        x_ekseni.append(i+1)
    plt.plot(x_ekseni,vaka_sayilari)
    plt.xlabel("Day")
    plt.ylabel("Client Number")
    plt.show() # Grafik gösterilir.

def ulkelere_gore_vaka_sayisi():

    global vaka_sayilari
    global date
    tarih_ayarla() # Tarih ayarlanır.
    vaka_sayilari = [] #Değişken sıfırlanır
    ulke = country_entry.get().lower().replace(" ","-") # Girilen ülke bilgisi küçük karakterlere çevrilir.
    try:
        if ulke in ulkeler:
            if ulke == "china":
                sorgu = "/country/china"
            else:
                sorgu = "/total/dayone/country/" +ulke   # ülke bilgisi ile sorgu yapılır.
            conn.request("GET", sorgu, headers=headers)
            cevap = conn.getresponse().read()
            veriler = json.loads(cevap.decode("utf-8")) #alınan veriler değişkene aktarılır.
            
            for i in range (len(veriler)): # tüm veriler tek tek dolaşılır.
                if tarih.get() ==  "Total":  # İstenilen tarihe göre veriler eklenir.
                    vaka_sayilari.append(int(veriler[i][istek.get()]))
                elif veriler[i]["Date"][0:7] in date: #Veriler değişkeninin ilk 7 elemanı tarih bilgisini içerir. 
                    vaka_sayilari.append(int(veriler[i][istek.get()]))
            grafik()
        else:
            tkinter.messagebox.showerror("ERROR","Please be sure that true name of country given!")
            return
    except Exception as e:
        tkinter.messagebox.showerror("ERROR",e)
# ARAYÜZ TASARIMI AŞAĞIDADIR
menu = Tk()
info = StringVar()
info.set('')
tarih = StringVar()
istek = StringVar()
menu.title("Country Based Corona Virus Datas")
menu.geometry("400x400")
Label(text = "Please submit a country name").pack()
country_entry = Entry(menu,width=15)
country_entry.pack()
Label(text = "Please choose time period ?").pack()
tarih_secin = ttk.Combobox(menu, width = 27, textvariable = tarih)
tarih_secin['values'] = ("Total","Last 3 Months","Last Month")
tarih_secin.pack()
Label(text = "Which type of data you want?").pack()
sorgu_secin = ttk.Combobox(menu, width = 27, textvariable = istek)
sorgu_secin['values'] = ("Confirmed","Active","Deaths","Recovered")
sorgu_secin.pack()
Button(text = "Submit",command = ulkelere_gore_vaka_sayisi).pack()
Label(text = "Please use 'us' to search values from United States. Results will show total client quantity.").pack()
menu.mainloop()
