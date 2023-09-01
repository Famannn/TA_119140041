import tkinter as tk
from tkinter import ttk
from Page1_V2 import Halaman1
from Page2_V2 import Halaman2

#inisiasi class untuk memulai frame
class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        #membuat container deffault
        self.container = tk.Frame(self) 
        self.container.pack(side = "top", fill = "both", expand = True)
        self.container.grid_rowconfigure(0, weight = 1)
        self.container.grid_columnconfigure(0, weight = 1)
  
        # inisiasi frame sebagai empty array
        self.frames = {} 
        #memulai program, dimulai dari page 1 dengan memanggil class Halaman1
        self.show_frame(Halaman1)
    
    #fungsi untuk menggunakan frame yang di panggil kedalam parameter
    def show_frame(self, cont):
        self.lates_frame = cont(self.container, self)
        self.lates_frame.tkraise()
        self.lates_frame.grid(row = 0, column = 0, sticky ="nsew")

#Driver Code
app = tkinterApp()
app.title("Double Exponential Smoothing")
app.geometry("862x519")
app.configure(bg = "#979797")
app.mainloop()