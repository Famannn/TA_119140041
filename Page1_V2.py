from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import  tkinter as tk
from Page2_V2 import Halaman2

#inisiasi class untuk Frame Page 1
class Halaman1(tk.Frame):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\USER\OneDrive\Documents\Tugas-Akhir-main\Penelitian\Page_1\build\assets\frame0")
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #fungsi untuk membaca file aset GUI
        def relative_to_assets(path: str) -> Path:
            return self.ASSETS_PATH / Path(path)
        
        #Tampilan GUI
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
            outline="")

        #button paham, untuk memindahkan frame ke halaman 2
        self.button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda : controller.show_frame(Halaman2),
            relief="flat"
        )
        button_1.place(
            x=557.0,
            y=425.0,
            width=180.0,
            height=55.0
        )
        
        canvas.create_rectangle(
            113.0,
            32.0,
            318.0,
            85.0,
            fill="#F1F5FF",
            outline="")
        
        canvas.create_text(
            129.0,
            44.0,
            anchor="nw",
            text="Peramalan Data",
            fill="#000000",
            font=("Roboto Bold", 24 * -1)
        )
        
        canvas.create_rectangle(
            28.0,
            132.0,
            402.0,
            386.0,
            fill="#F1F5FF",
            outline="")
        
        canvas.create_text(
            49.0,
            154.0,
            anchor="nw",
            text="1. Program akan membuat 2 buah model prediksi dengan menggunakan metode Double Exponential Smoothing dari Brown dan Holt\n2. Program akan mencari yang terbaik di antara keduanya berdasarkan Mean Absolute Percentage Error\n3. Program akan memberikan prediksi 3 periode selanjutnya dengan metode terbaik!",
            fill="#000000",
            font=("Roboto Bold", 18 * -1),
            width=340
        )
        
        canvas.create_rectangle(
            516.0,
            32.0,
            777.0,
            85.0,
            fill="#979797",
            outline="")
        
        canvas.create_text(
            535.0,
            44.0,
            anchor="nw",
            text="Bagaimana caranya?",
            fill="#F1F5FF",
            font=("Roboto Bold", 24 * -1)
        )
        
        canvas.create_rectangle(
            460.0,
            132.0,
            834.0,
            386.0,
            fill="#979797",
            outline="")
        
        canvas.create_text(
            490.0,
            151.0,
            anchor="nw",
            text="1. Masukan file data yang ingin di prediksi.\n2. Pastikan data telah bersih dan file berbentuk csv.\n3. Pilih range desimal parameter.\n4. Jika data telah berhasil di prediksi, terdapat grafik prediksi dan data prediksi siap di unduh.",
            fill="#000000",
            font=("Roboto Bold", 18 * -1),
            width=335
        )