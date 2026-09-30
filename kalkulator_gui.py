import tkinter as tk
from tkinter import ttk, messagebox
import math

class KalkulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Kalkulator")
        self.root.geometry("450x680")
        self.root.resizable(False, False)
        
        # Mengatur background utama jendela menjadi putih bersih
        self.root.configure(bg="#ffffff")

        # Styling
        style = ttk.Style()
        style.theme_use('clam')

        # Notebook (Tab Navigation)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Inisialisasi Tab
        self.tab_kalkulator = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_kalkulator, text="Kalkulator")
        
        # Membangun Tampilan Tab Kalkulator
        self.buat_tab_kalkulator()

    # ==========================================
    # TAB 1: KALKULATOR SAINTIFIK & GUI
    # ==========================================
    def buat_tab_kalkulator(self):
        self.ekspresi = ""
        self.string_var = tk.StringVar(value="0")

        # Layar Tampilan Angka (Entry dengan gaya bersih putih-hitam)
        frame_screen = tk.Frame(self.tab_kalkulator, bg="#ffffff", bd=1, relief="solid")
        frame_screen.pack(fill="x", padx=15, pady=15)

        entry_screen = tk.Entry(
            frame_screen, 
            textvariable=self.string_var, 
            font=("Consolas", 20, "bold"), 
            bg="#f8f9fa", 
            fg="#212529", 
            justify="right", 
            bd=0,
            highlightthickness=0
        )
        entry_screen.pack(fill="x", ipady=14, padx=8, pady=8)

        # Grid Tombol
        frame_buttons = tk.Frame(self.tab_kalkulator, bg="#ffffff")
        frame_buttons.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Layout tombol dengan tambahan Backspace, %, log, dan konstanta (π, e)
        tombol_layout = [
            ('sin', 0, 0, '#f1f3f5', '#212529'), ('cos', 0, 1, '#f1f3f5', '#212529'), ('tan', 0, 2, '#f1f3f5', '#212529'), ('log', 0, 3, '#f1f3f5', '#212529'),
            ('π', 1, 0, '#f1f3f5', '#212529'),   ('e', 1, 1, '#f1f3f5', '#212529'),   ('%', 1, 2, '#f1f3f5', '#212529'),   ('/', 1, 3, '#e9ecef', '#212529'),
            ('C', 2, 0, '#ffe3e3', '#c92a2a'),   ('⌫', 2, 1, '#fff3bf', '#f08c00'),   ('(', 2, 2, '#f1f3f5', '#212529'),   (')', 2, 3, '#f1f3f5', '#212529'),
            ('7', 3, 0, '#ffffff', '#212529'),   ('8', 3, 1, '#ffffff', '#212529'),   ('9', 3, 2, '#ffffff', '#212529'),   ('*', 3, 3, '#e9ecef', '#212529'),
            ('4', 4, 0, '#ffffff', '#212529'),   ('5', 4, 1, '#ffffff', '#212529'),   ('6', 4, 2, '#ffffff', '#212529'),   ('-', 4, 3, '#e9ecef', '#212529'),
            ('1', 5, 0, '#ffffff', '#212529'),   ('2', 5, 1, '#ffffff', '#212529'),   ('3', 5, 2, '#ffffff', '#212529'),   ('+', 5, 3, '#e9ecef', '#212529'),
            ('0', 6, 0, '#ffffff', '#212529'),   ('.', 6, 1, '#ffffff', '#212529'),   ('^', 6, 2, '#f1f3f5', '#212529'),   ('=', 6, 3, '#212529', '#ffffff')
        ]

        for i in range(7):
            frame_buttons.grid_rowconfigure(i, weight=1)
        for j in range(4):
            frame_buttons.grid_columnconfigure(j, weight=1)

        for (teks, baris, kolom, warna_bg, warna_fg) in tombol_layout:
            btn = tk.Button(
                frame_buttons, 
                text=teks, 
                font=("Arial", 12, "bold"), 
                bg=warna_bg, 
                fg=warna_fg, 
                bd=1,
                relief="groove",
                activebackground="#ced4da",
                activeforeground="#212529",
                command=lambda t=teks: self.tekan_tombol(t)
            )
            btn.grid(row=baris, column=kolom, sticky="nsew", padx=2, pady=2)

    def tekan_tombol(self, karakter):
        if karakter == 'C':
            self.ekspresi = ""
            self.string_var.set("0")
        elif karakter == '⌫':
            # Tombol Backspace untuk menghapus 1 karakter terakhir
            if len(self.ekspresi) > 0:
                self.ekspresi = self.ekspresi[:-1]
            if not self.ekspresi:
                self.string_var.set("0")
            else:
                self.string_var.set(self.ekspresi)
        elif karakter == '=':
            try:
                # Konversi operator matematika untuk modul Python
                expr_eval = self.ekspresi.replace('^', '**')
                expr_eval = expr_eval.replace('log', 'math.log10')
                expr_eval = expr_eval.replace('sin', 'math.sin')
                expr_eval = expr_eval.replace('cos', 'math.cos')
                expr_eval = expr_eval.replace('tan', 'math.tan')
                expr_eval = expr_eval.replace('π', 'math.pi')
                expr_eval = expr_eval.replace('e', 'math.e')
                expr_eval = expr_eval.replace('%', '/100')

                # Mengevaluasi ekspresi secara aman
                hasil = eval(expr_eval, {"__builtins__": None}, {"math": math})
                
                if isinstance(hasil, float) and hasil.is_integer():
                    hasil = int(hasil)
                
                self.string_var.set(str(hasil))
                self.ekspresi = str(hasil)
            except Exception:
                messagebox.showerror("Haha", "ekpresi salah, coba Lagi!")
                # PERUBAHAN DI SINI:
                # Kita HAPUS self.ekspresi = "" dan set("0") 
                # Biarkan self.ekspresi tetap berisi teks yang salah tadi 
                # agar user bisa langsung edit atau hapus pakai Backspace (⌫).
                pass
        else:
            # Jika tombol fungsi saintifik ditekan, tambahkan kurung buka otomatis
            if karakter in ('sin', 'cos', 'tan', 'log'):
                tambah = karakter + "("
            else:
                tambah = str(karakter)

            if self.string_var.get() == "0" and tambah not in ('.', '+', '-', '*', '/', '^', '%'):
                self.ekspresi = tambah
            else:
                self.ekspresi += tambah
            self.string_var.set(self.ekspresi)

if __name__ == "__main__":
    root = tk.Tk()
    app = KalkulatorGUI(root)
    root.mainloop()