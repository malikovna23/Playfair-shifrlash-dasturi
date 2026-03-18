import tkinter as tk
from tkinter import messagebox

class PlayfairCipherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Playfair Cipher - I/J Integratsiyasi")
        self.root.geometry("500x700")
        self.root.configure(bg="#f4f7f6")

        # --- Interfeys Dizayni ---
        tk.Label(root, text="Playfair Shifrlash Tizimi", font=("Helvetica", 16, "bold"), bg="#f4f7f6", fg="#2c3e50").pack(pady=15)

        # Kalit kiritish
        tk.Label(root, text="Kalit so'zni kiriting:", bg="#f4f7f6", font=("Arial", 10)).pack()
        self.key_entry = tk.Entry(root, font=("Arial", 12), width=30, justify='center', bd=2)
        self.key_entry.pack(pady=5)
        self.key_entry.insert(0, "TATU")

        # Matn kiritish
        tk.Label(root, text="Matnni kiriting:", bg="#f4f7f6", font=("Arial", 10)).pack(pady=(10, 0))
        self.text_entry = tk.Entry(root, font=("Arial", 12), width=30, justify='center', bd=2)
        self.text_entry.pack(pady=5)

        # Tugmalar
        btn_frame = tk.Frame(root, bg="#f4f7f6")
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Shifrlash", command=lambda: self.process('e'), bg="#27ae60", fg="white", font=("Arial", 10, "bold"), width=12, relief="flat").pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Deshifrlash", command=lambda: self.process('d'), bg="#2980b9", fg="white", font=("Arial", 10, "bold"), width=12, relief="flat").pack(side=tk.LEFT, padx=10)

        # Natija ko'rsatish
        tk.Label(root, text="NATIJA:", bg="#f4f7f6", font=("Arial", 10, "bold")).pack()
        self.result_var = tk.StringVar()
        self.result_display = tk.Entry(root, textvariable=self.result_var, font=("Arial", 13, "bold"), width=35, justify='center', fg="#c0392b", state='readonly', relief="flat")
        self.result_display.pack(pady=10)

        # 5x5 Jadval vizual qismi
        tk.Label(root, text="5x5 Playfair Jadvali (I/J)", font=("Arial", 11, "bold"), bg="#f4f7f6").pack(pady=(20, 5))
        self.table_frame = tk.Frame(root, bg="#bdc3c7", padx=2, pady=2)
        self.table_frame.pack()
        
        self.cells = []
        self._init_grid()

    def _init_grid(self):
        for r in range(5):
            row = []
            for c in range(5):
                lbl = tk.Label(self.table_frame, text="", width=6, height=2, font=("Courier", 12, "bold"), relief="solid", bg="white", bd=1)
                lbl.grid(row=r, column=c, padx=1, pady=1)
                row.append(lbl)
            self.cells.append(row)

    # --- Algoritm qismi ---
    def generate_matrix(self, key):
        key = key.upper().replace('J', 'I')
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ" # J yo'q
        
        matrix_list = []
        for char in key:
            if char.isalpha() and char not in matrix_list:
                matrix_list.append(char)
        
        for char in alphabet:
            if char not in matrix_list:
                matrix_list.append(char)
        
        matrix = [matrix_list[i:i+5] for i in range(0, 25, 5)]
        
        # Jadvalni interfeysda yangilash
        for r in range(5):
            for c in range(5):
                char = matrix[r][c]
                self.cells[r][c].config(text="I/J" if char == "I" else char)
        
        return matrix

    def prepare_text(self, text, mode):
        text = "".join(filter(str.isalpha, text.upper())).replace('J', 'I')
        if mode == 'd': return text # Deshifrlashda tekst o'zgartirilmaydi
        
        prepared = ""
        i = 0
        while i < len(text):
            a = text[i]
            if i + 1 < len(text):
                b = text[i+1]
                if a == b:
                    prepared += a + 'X'
                    i += 1
                else:
                    prepared += a + b
                    i += 2
            else:
                prepared += a + 'X'
                i += 1
        return prepared

    def find_pos(self, matrix, char):
        for r in range(5):
            for c in range(5):
                if matrix[r][c] == char:
                    return r, c
        return None

    def process(self, mode):
        key = self.key_entry.get()
        raw_text = self.text_entry.get()
        
        if not key or not raw_text:
            messagebox.showwarning("Xato", "Kalit va matnni to'liq kiriting!")
            return

        matrix = self.generate_matrix(key)
        text = self.prepare_text(raw_text, mode)
        
        if len(text) % 2 != 0: text += 'X'
        
        result = ""
        step = 1 if mode == 'e' else -1

        for i in range(0, len(text), 2):
            r1, c1 = self.find_pos(matrix, text[i])
            r2, c2 = self.find_pos(matrix, text[i+1])

            if r1 == r2: # Bir xil qator
                result += matrix[r1][(c1 + step) % 5]
                result += matrix[r2][(c2 + step) % 5]
            elif c1 == c2: # Bir xil ustun
                result += matrix[(r1 + step) % 5][c1]
                result += matrix[(r2 + step) % 5][c2]
            else: # To'rtburchak qoidasi
                result += matrix[r1][c2]
                result += matrix[r2][c1]
        
        self.result_var.set(result)

if __name__ == "__main__":
    root = tk.Tk()
    app = PlayfairCipherGUI(root)
    root.mainloop()
