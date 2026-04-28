import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class WeatherDiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary / Дневник погоды")
        self.root.geometry("750x520")
        self.entries = []
        self.json_file = "weather_diary.json"
        self._setup_ui()

    def _setup_ui(self):
        # --- Ввод данных ---
        input_frame = ttk.LabelFrame(self.root, text="📝 Новая запись")
        input_frame.pack(padx=10, pady=5, fill="x")

        ttk.Label(input_frame, text="Дата (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.date_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.date_var, width=20).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(input_frame, text="Температура (°C):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.temp_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.temp_var, width=20).grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(input_frame, text="Описание:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.desc_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.desc_var, width=40).grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(input_frame, text="Осадки:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.precip_var = tk.StringVar(value="Нет")
        ttk.Combobox(input_frame, textvariable=self.precip_var, values=["Да", "Нет"], state="readonly", width=10).grid(row=3, column=1, padx=5, pady=5, sticky="w")

        ttk.Button(input_frame, text="➕ Добавить запись", command=self.add_entry).grid(row=4, column=0, columnspan=2, pady=10)

        # --- Фильтрация ---
        filter_frame = ttk.LabelFrame(self.root, text="🔍 Фильтр")
        filter_frame.pack(padx=10, pady=5, fill="x")

        ttk.Label(filter_frame, text="Дата (опционально):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.filter_date_var = tk.StringVar()
        ttk.Entry(filter_frame, textvariable=self.filter_date_var, width=20).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(filter_frame, text="Температура (напр. >10):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.filter_temp_var = tk.StringVar()
        ttk.Entry(filter_frame, textvariable=self.filter_temp_var, width=20).grid(row=1, column=1, padx=5, pady=5, sticky="w")

        btn_frame = ttk.Frame(filter_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=5)
        ttk.Button(btn_frame, text="Применить", command=self.apply_filter).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Сбросить", command=self.reset_filter).pack(side="left", padx=5)

        # --- Таблица ---
        table_frame = ttk.Frame(self.root)
        table_frame.pack(padx=10, pady=5, fill="both", expand=True)

        columns = ("Дата", "Температура", "Описание", "Осадки")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # --- Работа с файлами ---
        file_frame = ttk.Frame(self.root)
        file_frame.pack(padx=10, pady=5, fill="x")
        ttk.Button(file_frame, text="💾 Сохранить в JSON", command=self.save_json).pack(side="left", padx=5)
        ttk.Button(file_frame, text="📂 Загрузить из JSON", command=lambda: self.load_json(silent=False)).pack(side="left", padx=5)

        # Автозагрузка при старте
        self.load_json(silent=True)

    def _validate_inputs(self):
        date_str = self.date_var.get().strip()
        temp_str = self.temp_var.get().strip()
        desc = self.desc_var.get().strip()
        precip = self.precip_var.get()

        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Неверный формат даты. Используйте YYYY-MM-DD")
            return None

        try:
            temp = float(temp_str)
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Температура должна быть числом")
            return None

        if not desc:
            messagebox.showerror("Ошибка ввода", "Описание не должно быть пустым")
            return None

        return {"date": date_str, "temperature": temp, "description
