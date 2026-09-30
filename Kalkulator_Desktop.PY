import tkinter as tk
from tkinter import messagebox
import ast
import operator


class SafeCalculator:
    """
    Mesin kalkulator sederhana yang hanya mengizinkan:
    +, -, *, /, %, tanda kurung, dan angka.
    """

    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    @classmethod
    def evaluate(cls, expression):
        expression = expression.replace("×", "*")
        expression = expression.replace("÷", "/")
        expression = expression.replace(",", ".")

        tree = ast.parse(expression, mode="eval")
        return cls._calculate(tree.body)

    @classmethod
    def _calculate(cls, node):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Nilai tidak valid")

        if isinstance(node, ast.Num):
            return node.n

        if isinstance(node, ast.BinOp):
            operator_function = cls.OPERATORS.get(type(node.op))

            if operator_function is None:
                raise ValueError("Operator tidak didukung")

            angka_kiri = cls._calculate(node.left)
            angka_kanan = cls._calculate(node.right)

            if isinstance(node.op, ast.Div) and angka_kanan == 0:
                raise ZeroDivisionError

            return operator_function(angka_kiri, angka_kanan)

        if isinstance(node, ast.UnaryOp):
            operator_function = cls.OPERATORS.get(type(node.op))

            if operator_function is None:
                raise ValueError("Operator tidak didukung")

            return operator_function(cls._calculate(node.operand))

        raise ValueError("Ekspresi tidak valid")


class KalkulatorDesktop:
    def __init__(self, root):
        self.root = root
        self.root.title("Kalkulator Desktop")
        self.root.geometry("390x570")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2f")

        self.ekspresi = tk.StringVar()
        self.status = tk.StringVar(value="Siap digunakan")

        self.buat_tampilan()

        self.root.bind("<Return>", lambda event: self.hitung())
        self.root.bind("<Escape>", lambda event: self.bersihkan())
        self.root.bind("<BackSpace>", lambda event: self.hapus_satu())

    def buat_tampilan(self):
        judul = tk.Label(
            self.root,
            text="KALKULATOR DESKTOP",
            font=("Segoe UI", 18, "bold"),
            bg="#1e1e2f",
            fg="#ffffff"
        )
        judul.pack(pady=(18, 5))

        subjudul = tk.Label(
            self.root,
            text="Operasi Matematika Dasar",
            font=("Segoe UI", 10),
            bg="#1e1e2f",
            fg="#a9b0c3"
        )
        subjudul.pack(pady=(0, 12))

        frame_tampilan = tk.Frame(
            self.root,
            bg="#292943",
            highlightthickness=1,
            highlightbackground="#454568"
        )
        frame_tampilan.pack(padx=20, fill="x")

        self.display = tk.Entry(
            frame_tampilan,
            textvariable=self.ekspresi,
            font=("Consolas", 25, "bold"),
            justify="right",
            state="readonly",
            readonlybackground="#292943",
            fg="#ffffff",
            bd=0,
            relief="flat"
        )
        self.display.pack(
            padx=15,
            pady=(18, 5),
            ipady=10,
            fill="x"
        )

        label_status = tk.Label(
            frame_tampilan,
            textvariable=self.status,
            font=("Segoe UI", 9),
            bg="#292943",
            fg="#a9b0c3",
            anchor="e"
        )
        label_status.pack(
            padx=15,
            pady=(0, 12),
            fill="x"
        )

        frame_tombol = tk.Frame(self.root, bg="#1e1e2f")
        frame_tombol.pack(padx=20, pady=18, fill="both", expand=True)

        tombol = [
            ("C", 0, 0, "#d9534f"),
            ("⌫", 0, 1, "#6c6c88"),
            ("(", 0, 2, "#6c6c88"),
            (")", 0, 3, "#6c6c88"),

            ("7", 1, 0, "#353552"),
            ("8", 1, 1, "#353552"),
            ("9", 1, 2, "#353552"),
            ("÷", 1, 3, "#ff9f43"),

            ("4", 2, 0, "#353552"),
            ("5", 2, 1, "#353552"),
            ("6", 2, 2, "#353552"),
            ("×", 2, 3, "#ff9f43"),

            ("1", 3, 0, "#353552"),
            ("2", 3, 1, "#353552"),
            ("3", 3, 2, "#353552"),
            ("-", 3, 3, "#ff9f43"),

            ("%", 4, 0, "#353552"),
            ("0", 4, 1, "#353552"),
            (".", 4, 2, "#353552"),
            ("+", 4, 3, "#ff9f43"),

            ("=", 5, 0, "#2ecc71"),
        ]

        for teks, baris, kolom, warna in tombol:
            kolomspan = 4 if teks == "=" else 1

            tombol_gui = tk.Button(
                frame_tombol,
                text=teks,
                font=("Segoe UI", 16, "bold"),
                bg=warna,
                fg="#ffffff",
                activebackground=self.warna_aktif(warna),
                activeforeground="#ffffff",
                bd=0,
                relief="flat",
                cursor="hand2",
                command=lambda nilai=teks: self.proses_tombol(nilai)
            )

            tombol_gui.grid(
                row=baris,
                column=kolom,
                columnspan=kolomspan,
                padx=4,
                pady=4,
                sticky="nsew"
            )

        for baris in range(6):
            frame_tombol.rowconfigure(baris, weight=1)

        for kolom in range(4):
            frame_tombol.columnconfigure(kolom, weight=1)

        footer = tk.Label(
            self.root,
            text="Enter = Hitung   |   Esc = Bersihkan   |   Backspace = Hapus",
            font=("Segoe UI", 8),
            bg="#1e1e2f",
            fg="#777793"
        )
        footer.pack(pady=(0, 12))

    def warna_aktif(self, warna):
        warna_aktif = {
            "#d9534f": "#c9302c",
            "#6c6c88": "#8585a8",
            "#353552": "#4b4b70",
            "#ff9f43": "#f39c12",
            "#2ecc71": "#27ae60",
        }
        return warna_aktif.get(warna, warna)

    def proses_tombol(self, nilai):
        if nilai == "C":
            self.bersihkan()
        elif nilai == "⌫":
            self.hapus_satu()
        elif nilai == "=":
            self.hitung()
        elif nilai == "%":
            self.tambahkan_persen()
        else:
            self.tambahkan(nilai)

    def tambahkan(self, nilai):
        isi_lama = self.ekspresi.get()

        if isi_lama in ("Error", "Tidak valid"):
            isi_lama = ""

        simbol_baru = nilai

        if nilai == "×":
            simbol_baru = "×"
        elif nilai == "÷":
            simbol_baru = "÷"

        self.ekspresi.set(isi_lama + simbol_baru)
        self.status.set("Masukkan angka atau operator")

    def tambahkan_persen(self):
        isi_lama = self.ekspresi.get()

        if not isi_lama:
            return

        self.ekspresi.set(isi_lama + "%")
        self.status.set("Persentase ditambahkan")

    def bersihkan(self):
        self.ekspresi.set("")
        self.status.set("Kalkulator dibersihkan")

    def hapus_satu(self):
        isi_lama = self.ekspresi.get()

        if isi_lama in ("Error", "Tidak valid"):
            self.bersihkan()
            return

        self.ekspresi.set(isi_lama[:-1])
        self.status.set("Karakter terakhir dihapus")

    def hitung(self):
        ekspresi = self.ekspresi.get().strip()

        if not ekspresi:
            self.status.set("Masukkan ekspresi terlebih dahulu")
            return

        try:
            hasil = SafeCalculator.evaluate(ekspresi)

            if isinstance(hasil, float):
                if hasil.is_integer():
                    hasil = int(hasil)
                else:
                    hasil = round(hasil, 10)

            self.ekspresi.set(str(hasil))
            self.status.set("Perhitungan berhasil")

        except ZeroDivisionError:
            self.ekspresi.set("Error")
            self.status.set("Tidak dapat membagi dengan nol")
            messagebox.showerror(
                "Kesalahan Perhitungan",
                "Pembagian dengan angka nol tidak diperbolehkan."
            )

        except (SyntaxError, ValueError, TypeError):
            self.ekspresi.set("Tidak valid")
            self.status.set("Ekspresi tidak valid")
            messagebox.showwarning(
                "Input Tidak Valid",
                "Silakan masukkan ekspresi matematika yang benar."
            )


if __name__ == "__main__":
    root = tk.Tk()
    aplikasi = KalkulatorDesktop(root)
    root.mainloop()