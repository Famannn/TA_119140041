#import library
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import os
from tabulate import tabulate
import time

global canvas_id

#1. fungsi untuk menerima parameter yang dikirimkan oleh file Page2 dan memulai program yang terdapat pada file
def proses_data (path, operDist, canvas) :
    start_time = time.time()
    if os.path.isfile(path) == False :
        print("file tidak ada")
        return False
    data = Data(path)
    parameter = Parameter(operDist)
    AllFtBrown, best_at_brown, best_bt_brown, AllFtHolt, best_St_holt, best_bt_holt = main_program(data, parameter)
    FinalHolt, FinalBrown, BrownCalc, HoltCalc, Brownalpha, holtalpha, holtbeta = move(AllFtBrown, AllFtHolt, data)
    list_data_forecast, brown, holt, canvas_id = Metode_terbaik(AllFtBrown, AllFtHolt, FinalHolt, FinalBrown, best_St_holt, best_bt_holt, best_at_brown, best_bt_brown, BrownCalc, HoltCalc, Brownalpha, holtalpha, holtbeta, canvas)

    end_time = time.time()
    execution_time = end_time - start_time

    # Menampilkan waktu eksekusi
    print(f"Waktu eksekusi: {execution_time} detik\n\n")
    return list_data_forecast, canvas_id, brown, holt, data

#2. fungsi untuk inisiasi data
def Data(path) :
    data = pd.read_csv(path).values

    #list data aktual
    index = []
    for i in range(len(data[0:])):
        index.append(f'X{i+1}')
    list_data = pd.DataFrame(data, index=index, columns = ['data'])
    return data

#3. fungsi untuk inisiasi parameter
def Parameter(operDist) :
    operators=[]
    for i in range(int(1/operDist)):
        if(i!=0):
            operators.append(round((i*operDist),4))
    return operators

#4. fungsi untuk inisiasi rumus brown
def brown(a, data):
    S1=[]
    S2=[]
    Ft=[]
    #perulangan untuk data setiap periode
    for t,X in enumerate(data):
        if t==0:
            S1.append(X)
            S2.append(X)          
        else:
            S1.append(a*X+(1-a)*S1[-1])
            S2.append(a*S1[-1]+(1-a)*S2[-1])
        at=(2*S1[-1])-S2[-1]
        bt=(a/(1-a))*(S1[-1]-S2[-1])
        Ft.append(at+(bt*1))
    #perhitungan mape
    Ft[-1] = mape(data[1:], Ft)
    return Ft, at, bt

#5. fungsi untuk inisiasi rumus holt
def holt(a, b, data):
    St=[]
    Bt=[]
    Ft=[]
    #perulangan untuk data setiap periode
    for t,X in enumerate(data):
        if t==0:
            St.append(X)
            Bt.append(((data[1]-data[0])+(data[3]-data[2]))/2)
        else:
            St.append(a*X+(1-a)*(St[-1]+Bt[-1]))
            Bt.append(b*(St[-1]-St[-2])+(1-b)*Bt[-1])
        Ft.append(St[-1]+(Bt[-1]*1))
    #perhitungan mape
    Ft[-1] = mape(data[1:], Ft)
    return Ft, St[-1], Bt[-1]

#6. fungsi untuk inisiasi rumus prediksi 3 periode brown
def new_brown(atl, btl, m):
    Ft = (atl+(btl*m))
    return Ft

#7. fungsi untuk inisiasi rumus prediksi 3 periode holt
def new_holt(Stl, Btl, m):
    Ft = (Stl+(Btl*m))
    return Ft

#8. fungsi untuk inisiasi rumus mape
def mape(act, fore):
    allAbsolute=[]
    for a,f in zip(act,fore):
        allAbsolute.append((abs(a-f)/a)*100)
    return sum(allAbsolute)/len(allAbsolute)

#9. fungsi utama pada Program
def main_program (data, operators) :
    #main program
    AllFtBrown=[]
    AllFtHolt=[]
    pertama = True
    #perulangan untuk setiap parameter
    for a in operators:
        #Proses perhitungan Brown
        e=[a]
        Ft, at, bt = brown(a,data)
        e.extend(Ft)
        AllFtBrown.append(e)
        if pertama:
            best_at_brown = at
            best_bt_brown = bt
            best_mape_brown = AllFtBrown[-1][-1]
        elif AllFtBrown[-1][-1] < best_mape_brown:
            best_at_brown = at
            best_bt_brown = bt
            best_mape_brown = AllFtBrown[-1][-1]
        for b in operators:
        #Proses perhitungan Brown
            e=[a,b]
            Ft, St, Bt = holt(a,b,data)
            e.extend(Ft)
            AllFtHolt.append(e)
            if pertama:
                best_St_holt = St
                best_bt_holt = Bt
                best_mape_holt = AllFtHolt[-1][-1]
                pertama = False
            elif AllFtHolt[-1][-1] < best_mape_holt:
                best_St_holt = St
                best_bt_holt = Bt
                best_mape_holt = AllFtHolt[-1][-1]
    del e
    del Ft
    del at
    del bt
    del St
    return AllFtBrown, best_at_brown, best_bt_brown, AllFtHolt, best_St_holt, best_bt_holt

#10. fungsi untuk input hasil brown and holt ke dalam dataframe
def move(AllFtBrown, AllFtHolt, data) :
    pd.set_option('display.max_columns', None)
    columns = ['alpha']
    for i in range(len(data[:-1])):
        columns.append(f'F{i+2}')
    columns.append('mape')
    BrownCalc = pd.DataFrame(AllFtBrown, columns=columns)
    columns.insert(1,'beta')
    HoltCalc = pd.DataFrame(AllFtHolt, columns=columns)

    #BROWN
    #list data prediksi brown dengan urutan berdasarkan nilai mape
    BrownCalc = BrownCalc.sort_values(by=['mape'])
    
    #parameter brown terbaik
    Brownalpha = BrownCalc.iloc[0][['alpha']].item()
    FinalBrown = BrownCalc.iloc[0][['mape']].item()
    print(tabulate(BrownCalc.head(10), headers='keys', tablefmt='psql'))
    print('')
    print(tabulate(BrownCalc.tail(10), headers='keys', tablefmt='psql'))

    #HOLT
    #list data prediksi holt dengan urutan berdasarkan nilai mape
    HoltCalc = HoltCalc.sort_values(by=['mape'])

    #parameter holt terbaik
    holtalpha = HoltCalc.iloc[0][['alpha']].item()
    holtbeta = HoltCalc.iloc[0][['beta']].item()
    FinalHolt = HoltCalc.iloc[0][['mape']].item()
    print(tabulate(HoltCalc.head(10), headers='keys', tablefmt='psql'))
    print('')
    print(tabulate(HoltCalc.tail(10), headers='keys', tablefmt='psql'))
    return FinalHolt, FinalBrown, BrownCalc, HoltCalc, Brownalpha, holtalpha, holtbeta

#11. Fungsi untuk menentukan metode terbaik berdasarkan mape
def Metode_terbaik(AllFtBrown, AllFtHolt, FinalHolt, FinalBrown, best_St_holt, best_bt_holt, best_at_brown, best_bt_brown, BrownCalc, HoltCalc, Brownalpha, holtalpha, holtbeta, canvas) :
    
    #input data aktual, hasil prediksi brown dan hasil prediksi holt ke dataframe
    brown = AllFtBrown[BrownCalc.index.values[0]][1:-1]
    holt = AllFtHolt[HoltCalc.index.values[0]][2:-1]
    indexF = []
    Status = ""

    #jika mape terkecil dari holt lebih kecil daripada mape terkecil dari brown
    if FinalHolt < FinalBrown :
        #menambah list dengan hasil perhitungan fungsi new_holt
        for M in range (3):
            holt.append(new_holt(best_St_holt,best_bt_holt,M+1))
        for i in range(len(holt[0:])):
            indexF.append(f'F{i+2}')
        #status kualitas model prediksi
        if FinalHolt <= 10:
            Status = "Tinggi"
        elif FinalHolt <= 20:
            Status = "Baik"
        elif FinalHolt <= 50:
            Status = "Wajar"
        else:
            Status = "Rendah"
        list_data_forecast = pd.DataFrame(holt[-3:], index=indexF[-3:], columns = ['data'])
        #tampilan untuk kesimpulan pada GUI
        canvas_id = canvas.create_text(
            548.0,
            140.0,
            anchor="nw",
            text=f"Metode terbaik : Holt\nParamater Alpha = {holtalpha}\nParamater Beta = {holtbeta}\nNilai MAPE = {round(FinalHolt[0], 2)}%\nKualitas Prediksi : {Status}\n\nPrediksi :\nPeriode 1 (F{len(holt[:-2])+1}) = {math.floor(holt[-3][0])}\nPeriode 2 (F{len(holt[:-1])+1}) = {math.floor(holt[-2][0])}\nPeriode 3 (F{len(holt)+1}) = {math.floor(holt[-1][0])}",
            fill="#FFFFFF",
            font=("Roboto Bold", 16 * -1),
            width=180
        )
        print(f"Metode terbaik : Holt (Paramater Alpha = {holtalpha} & Beta = {holtbeta})")
        print(f"Nilai MAPE : {FinalHolt[0]}%")
    #jika mape terkecil dari holt lebih kecil daripada mape terkecil dari brown
    else :
        #menambah list dengan hasil perhitungan fungsi new_brown
        for M in range (3):
            brown.append(new_brown(best_at_brown,best_bt_brown,M+1))
        for i in range(len(brown[0:])):
            indexF.append(f'F{i+2}')
        #status kualitas model prediksi
        if FinalBrown <= 10:
            Status = "Tinggi"
        elif FinalBrown <= 20:
            Status = "Baik"
        elif FinalBrown <= 50:
            Status = "Wajar"
        else:
            Status = "Rendah"
        list_data_forecast = pd.DataFrame(brown[-3:], index=indexF[-3:], columns = ['data'])
        #tampilan untuk kesimpulan pada GUI
        canvas_id = canvas.create_text(
            548.0,
            140.0,
            anchor="nw",
            text=f"Metode terbaik : Brown\nParamater Alpha = {Brownalpha}\nNilai MAPE = {round(FinalBrown[0], 2)}%\nKualitas Prediksi : {Status}\n\nPrediksi :\nPeriode 1 (F{len(brown[:-2])+1}) = {math.floor(brown[-3][0])}\nPeriode 2 (F{len(brown[:-1])+1}) = {math.floor(brown[-2][0])}\nPeriode 3 (F{len(brown)+1}) = {math.floor(brown[-1][0])}",
            fill="#FFFFFF",
            font=("Roboto Bold", 16 * -1),
            width=180
        )
        print(f"Metode terbaik : Brown (Paramater Alpha = {Brownalpha})")
        print(f"Nilai MAPE : {FinalBrown[0]}%")
    return list_data_forecast, brown, holt, canvas_id

#12. Fungsi untuk menampilkan grafik hasil prediksi
def Grafik(brown, holt, data):
    bulat_brown = np.floor(brown).astype(int)
    bulat_holt = np.floor(holt).astype(int)
    if len(brown) > len(holt):
        panjang = bulat_brown
        Text_kuat = "DES Brown"
        label_kuat ="Brown Point"
        pendek = bulat_holt
        Text_lemah = "DES Holt"
        label_lemah ="Holt Point"
    else:
        panjang = bulat_holt
        Text_kuat = "DES Holt"
        label_kuat ="Holt Point"
        pendek = bulat_brown
        Text_lemah = "DES Brown"
        label_lemah ="Brown Point"

    axis_data = list(range(1, len(data) + 1, 1))
    axis_other = list(range(2, len(pendek) + 2, 1))
    axis_predic = list(range(2, len(panjang) + 2, 1))

    # Grafik data aktual, prediksi brown & holt ke dataframe
    fig, ax = plt.subplots()
    ax.set_xticks(range(len(data)+4))
    
    # Plot 3 garis grafik
    ax.plot(axis_data, data, color='red', label='Data Aktual')
    ax.plot(axis_other, pendek, color='blue', label=Text_lemah)
    ax.plot(axis_predic, panjang, color='green', label=Text_kuat)
    
    # menambahkan dot dan nilai untuk ketiga garis grafik
    ax.scatter(axis_data, data, color='red', label='Data Point')
    for i, j in zip(axis_data, data):
        ax.annotate(str(j), xy=(i, j), xytext=(i, j + 1), color='red')
    ax.scatter(axis_other, pendek, color='blue', label=label_lemah)
    for i, j in zip(axis_other, pendek):
        ax.annotate(str(j), xy=(i, j), xytext=(i, j + 1), color='blue')
    ax.scatter(axis_predic, panjang, color='green', label=label_kuat)
    for i, j in zip(axis_predic, panjang):
        ax.annotate(str(j), xy=(i, j), xytext=(i, j + 1), color='green')
        
    # Add legend and labels
    ax.legend()
    ax.set_xlabel('Periode')
    ax.set_ylabel('Jumlah Data')
    
    # Show the plot
    plt.show(block=False)

#13. fungsi untuk mengunduh data hasil forecast
def Unduh_data(list_data_forecast, filename) :
    #pembuatan file csv
    print(f"nama file : {filename}\n")
    list_data_forecast.to_csv(f"{filename}.csv")
    insert = pd.read_csv(f"{filename}.csv", index_col=0)
    print(insert)
    return insert



    