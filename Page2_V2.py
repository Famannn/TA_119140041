from pathlib import Path
import sys
import os
import pandas as pd
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog, font, Toplevel, Label
import  tkinter as tk
from Logic import proses_data, Unduh_data, Grafik 

#inisiasi class untuk Frame Page 2
class Halaman2(tk.Frame):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\USER\OneDrive\Documents\Tugas-Akhir-main\Penelitian\Page_2\build\assets\frame0")
    output_path = ""
    pilihan_parameter = 0
    list_data_forecast = []
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #fungsi button menentukan rentang parameter
        def EventButton(param, btn, buttonNumber):
            self.pilihan_parameter = param
            GantiWarnaButtonParameter(buttonNumber)
            print("Pilihan parameter : "+str(self.pilihan_parameter))

        #fungsi utama button untuk mengirim data dan parameter ke proses peramalan pada file logic
        def input_data() : 
            if canvas_id :
                canvas.delete(canvas_id[0])
                canvas_id.pop()
                self.list_data_forecast.pop()
            #mengirim parameter ke fungsi proses_data pada file logic
            listdata, canvas_delete_id, brown, holt, data = proses_data(entry_1.get(), self.pilihan_parameter, canvas)
            #mengirim parameter ke fungsi Grafik pada file logic
            Grafik(brown, holt, data)
            canvas_id.append(canvas_delete_id)

            if isinstance(listdata, pd.DataFrame) == False :
                print("proses data gagal")
                return 0
            self.list_data_forecast.append(listdata)

        # fungsi untuk membaca file csv
        def select_path():
            self.output_path = filedialog.askopenfilename()
            entry_1.delete(0, tk.END)
            entry_1.insert(0, self.output_path)

        #fungsi untuk membaca file aset GUI
        def relative_to_assets(path: str) -> Path:
            return self.ASSETS_PATH / Path(path)

        #fungsi untuk merubah warna button parameter yang dipilih
        def GantiWarnaButtonParameter(buttonNumber):
            match buttonNumber:
                case 1:
                    # Untuk ubah wanra buttonyang dipencet
                    button_1.configure(bg="#5B5B5B", fg="white")
    
                    # Untuk reset warna button yang tidak dipencet menjadi setelan awal
                    button_3.configure(bg="#F1F5FF", fg="black")
                    button_4.configure(bg="#F1F5FF", fg="black")
                case 3:
                    # Untuk ubah wanra buttonyang dipencet
                    button_3.configure(bg="#5B5B5B", fg="white")
                    
                    # Untuk reset warna button yang tidak dipencet menjadi setelan awal
                    button_1.configure(bg="#F1F5FF", fg="black")
                    button_4.configure(bg="#F1F5FF", fg="black")
                case 4:
                    # Untuk ubah wanra buttonyang dipencet
                    button_4.configure(bg="#5B5B5B", fg="white")
    
                    # Untuk reset warna button yang tidak dipencet menjadi setelan awal
                    button_3.configure(bg="#F1F5FF", fg="black")
                    button_1.configure(bg="#F1F5FF", fg="black")
                case 6:
                    # Untuk reset warna button yang tidak dipencet menjadi setelan awal
                    button_1.configure(bg="#F1F5FF", fg="black")
                    button_3.configure(bg="#F1F5FF", fg="black")
                    button_4.configure(bg="#F1F5FF", fg="black")
                case _:
                    print("button not recognized")

        #fungsi untuk Menampilkan pop up untuk Download dan menentukan nama file data hasil forecast
        def open_popup(win):
            top= Toplevel(win)
            top.geometry("431x272")
            top.geometry("+400+200") 
            # Set the position of the pop-up window
            top.configure( bg = "#979797")
            top.title("Input Nama")

            entry = tk.Entry(
                top,
                bd=0,
                bg="#F1F5FF",
                fg="#000716",
                highlightthickness=0
            )
            entry.place(
                x=43.0,
                y=107.0,
                width=345.0,
                height=59.0
            )

            canvas = Canvas(top, width=100, height=50)
            canvas.create_text(
                0, 10,  
                anchor="nw",
                text="Nama file",
                fill="#000000",
                font=("Roboto Bold", 24 * -1)
            )
            canvas.pack()

            #fungsi untuk mengambil nama file yang diinputkan
            def get_name():
                name = entry.get()
                entered_filename = name
                #mengirim parameter ke fungsi Unduh_data pada file logic
                Unduh_data(self.list_data_forecast[0], entered_filename)
                top.destroy()
            
            button = Button(top, text="Submit", command=get_name)
            button.pack()
            button.place(
                x=190.0,
                y=177.0
            )

        #fungsi untuk mengembalikan semua nilai variabel, input dan output menjadi seperti semula
        def ResetData():
            entry_1.delete(0, tk.END)
            EventButton(0, button_6, 6)
            self.output_path = ""
            canvas.delete(canvas_id[0])
            canvas_id.pop()
            self.list_data_forecast.pop()

        #Tampilan GUI
        bold_font = font.Font(weight="bold")
        entered_filename = str("")
        canvas_id = []

        entry_file_name = Entry()
        canvas = Canvas(
            self,
            bg = "#979797",
            height = 519,
            width = 862,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        canvas.place(x = 0, y = 0)
        canvas.create_rectangle(
            431.0,
            0.0,
            862.0,
            519.0,
            fill="#F1F5FF",
            outline=""
        )

        canvas.create_rectangle(
            113.0,
            31.0,
            318.0,
            84.0,
            fill="#F1F5FF",
            outline="#000000"
        )

        canvas.create_rectangle(
            91.0,
            205.0,
            339.0,
            243.0,
            fill="#F1F5FF",
            outline="#000000"
        )

        #button 0.1
        button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        button_1 = Button()
        button_1.configure(
            text="0.1",
            bg="#F1F5FF",
            font=bold_font,
            borderwidth=0,
            highlightthickness=0,
            command= lambda btn=button_1:EventButton(0.1, btn, 1),
            relief="flat"
        )
        button_1.place(
            x=163.0,
            y=260.0,
            width=103.0,
            height=43.0
        )

        self.entry_image_1 = PhotoImage(
            file=relative_to_assets("entry_1.png")
        )

        entry_bg_1 = canvas.create_image(
            215.0,
            137.0,
            image=self.entry_image_1
        )
        entry_1 = tk.Entry(
            bd=0,
            bg="#F1F5FF",
            fg="#000716",
            highlightthickness=0
        )
        entry_1.place(
            x=55.0,
            y=107.0,
            width=280.0,
            height=59.0
        )

        #button untuk pilih file
        self.button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png")
        )
        button_2 = Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=select_path,
            relief="flat"
        )
        button_2.place(
            x=348.0,
            y=127.0,
            width=24.0,
            height=22.0
        )

        #button 0.01
        button_image_3 = PhotoImage(
            file=relative_to_assets("button_3.png"))
        button_3 = Button()
        button_3.configure(
            text="0.01",
            bg="#F1F5FF",
            font=bold_font,
            borderwidth=0,
            highlightthickness=0,
            command= lambda btn=button_3:EventButton(0.01, btn, 3),
            relief="flat"
        )
        button_3.place(
            x=163.0,
            y=323.0,
            width=103.0,
            height=43.0
        )

        #button 0.001
        button_image_4 = PhotoImage(
            file=relative_to_assets("button_4.png"))
        button_4 = Button()
        button_4.configure(
            text="0.001",
            bg="#F1F5FF",
            font=bold_font,
            borderwidth=0,
            highlightthickness=0,
            command= lambda btn=button_4:EventButton(0.001, btn, 4),
            relief="flat"
        )
        button_4.place(
            x=163.0,
            y=384.0,
            width=103.0,
            height=43.0
        )

        #button untuk reset data
        self.button_image_6 = PhotoImage(
            file=relative_to_assets("button_6.png"))
        button_6 = Button(
            self,
            image=self.button_image_6,
            borderwidth=0,
            highlightthickness=0,
            command =  lambda:ResetData(),
            relief="flat" 
        ) 
        button_6.place( 
            x=575.0, 
            y=425.0, 
            width=143.0, 
            height=53.0 
        )

        #button untuk unduh file hasil forecast
        self.button_image_7 = PhotoImage(
            file=relative_to_assets("button_7.png"))
        button_7 = Button(
            self,
            image=self.button_image_7,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: open_popup(parent),
            relief="flat"
        )
        button_7.place(
            x=575.0,
            y=364.0,
            width=143.0,
            height=38.0
        )

        canvas.create_text(
            135.0,
            44.0,
            anchor="nw",
            text="Masukan Data!",
            fill="#000000",
            font=("Roboto Bold", 24 * -1)
        )

        canvas.create_rectangle(
            544.0,
            31.0,
            749.0,
            84.0,
            fill="#979797",
            outline="#000000"
        )

        canvas.create_text(
            619.0,
            44.0,
            anchor="nw",
            text="Hasil",
            fill="#FFFFFF",
            font=("Roboto Bold", 24 * -1)
        )

        canvas.create_text(
            117.0,
            213.0,
            anchor="nw",
            text="Pilih Rentang Parameter",
            fill="#000000",
            # bd=1,
            font=("Roboto Bold", 18 * -1)
        )

        canvas.create_rectangle(
            538.0,
            130.0,
            756.0,
            325.0,
            fill="#979797",
            outline="#000000"
        )

        #button untuk mulai proses forecast
        self.button_image_8 = PhotoImage(
            file=relative_to_assets("button_8.png"))
        button_8 = Button(
            self,
            image=self.button_image_8,
            borderwidth=0,
            highlightthickness=0,
            command=input_data,
            relief="flat"
        )
        button_8.place(
            x=125.0,
            y=445.0,
            width=180.0,
            height=55.0
        )