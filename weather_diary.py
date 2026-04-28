import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class WeatherDiary(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weather Diary (Дневник погоды)")
        self.geometry("700x550")
        self.db_file = "weather_data.json"
        self.data = self.load_data()

        # --- Интерфейс ввода ---
        input_frame = ttk.LabelFrame(self, text="Новая запись")
        input_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(input_frame, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(input_frame)
        self.date_entry.insert(0, datetime.now().strftime("%d.%m.%Y"))
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Температура (°C):").grid(row=0, column=2, padx=5, pady=5)
        self.temp_entry = ttk.Entry(input_frame)
        self.temp_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(input_frame, text="Описание:").grid(row=1, column=0, padx=5, pady=5)
        self.desc_entry = ttk.Entry(input_frame)
        self.desc_entry.grid(row=1, column=1, columnspan=3, sticky="we", padx=5, pady=5)

        self.rain_var = tk.BooleanVar()
        self.rain_check = ttk.Checkbutton(input_frame, text="Осадки", variable=self.rain_var)
        self.rain_check.grid(row=2, column=0, padx=5, pady=5)

        self.add_btn = ttk.Button(input_frame, text="Добавить запись", command=self.add_entry)
        self.add_btn.grid(row=2, column=3, padx=5, pady=5)

        # --- Интерфейс фильтрации ---
        filter_frame = ttk.LabelFrame(self, text="Фильтрация")
        filter_frame.pack(padx=10, pady=5, fill="x")

        ttk.Label(filter_frame, text="Мин. темп:").grid(row=0, column=0, padx=5, pady=5)
        self.filter_temp = ttk.Entry(filter_frame, width=10)
        self.filter_temp.grid(row=0, column=1, padx=5, pady=5)

        self.filter_btn = ttk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
        self.filter_btn.grid(row=0, column=2, padx=5, pady=5)

        self.reset_btn = ttk.Button(filter_frame, text="Сбросить", command=self.refresh_table)
        self.reset_btn.grid(row=0, column=3, padx=5, pady=5)

        # --- Таблица ---
        self.tree = ttk.Treeview(self, columns=("date", "temp", "desc", "rain"), show="headings")
        self.tree.heading("date", text="Дата")
        self.tree.heading("temp", text="Темп. (°C)")
        self.tree.heading("desc", text="Описание")
        self.tree.heading("rain", text="Осадки")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        self.refresh_table()

    def add_entry(self):
        date_str = self.date_entry.get()
        temp_str = self.temp_entry.get()
        desc_str = self.desc_entry.get()

        # Валидация
        try:
            datetime.strptime(date_str, "%d.%m.%Y")
            temp = float(temp_str)
            if not desc_str.strip(): raise ValueError("Описание пустое")
        except ValueError as e:
            messagebox.showerror("Ошибка ввода", f"Проверьте данные: {e}")
            return

        new_record = {
            "date": date_str,
            "temp": temp,
            "desc": desc_str,
            "rain": "Да" if self.rain_var.get() else "Нет"
        }
        
        self.data.append(new_record)
        self.save_data()
        self.refresh_table()
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)

    def apply_filter(self):
        try:
            min_t = float(self.filter_temp.get())
            filtered = [r for r in self.data if r['temp'] >= min_t]
            self.refresh_table(filtered)
        except ValueError:
            messagebox.showwarning("Фильтр", "Введите число для фильтрации по температуре")

    def refresh_table(self, display_data=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        target = display_data if display_data is not None else self.data
        for row in target:
            self.tree.insert("", tk.END, values=(row['date'], row['temp'], row['desc'], row['rain']))

    def save_data(self):
        with open(self.db_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

if __name__ == "__main__":
    app = WeatherDiary()
    app.mainloop()
