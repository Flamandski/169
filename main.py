import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")
        self.entries = []
        self.load_data()

        # Создаём виджеты
        self.create_widgets()

    def create_widgets(self):
        # Поля ввода
        tk.Label(self.root, text="Дата (YYYY-MM-DD):").grid(row=0, column=0, sticky="w")
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Температура (°C):").grid(row=1, column=0, sticky="w")
        self.temp_entry = tk.Entry(self.root)
        self.temp_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Описание погоды:").grid(row=2, column=0, sticky="w")
        self.desc_entry = tk.Entry(self.root)
        self.desc_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Осадки:").grid(row=3, column=0, sticky="w")
        self.precipitation_var = tk.BooleanVar()
        tk.Checkbutton(self.root, variable=self.precipitation_var).grid(row=3, column=1, sticky="w")

        # Кнопка добавления
        tk.Button(self.root, text="Добавить запись", command=self.add_entry).grid(row=4, column=0, columnspan=2)

        # Таблица для отображения записей
        self.tree = ttk.Treeview(self.root, columns=("Date", "Temp", "Desc", "Precip"), show="headings")
        self.tree.heading("Date", text="Дата")
        self.tree.heading("Temp", text="Температура")
        self.tree.heading("Desc", text="Описание")
        self.tree.heading("Precip", text="Осадки")
        self.tree.grid(row=5, column=0, columnspan=2, sticky="nsew")

        # Фильтры
        tk.Label(self.root, text="Фильтр по дате:").grid(row=6, column=0, sticky="w")
        self.filter_date_entry = tk.Entry(self.root)
        self.filter_date_entry.grid(row=6, column=1)
        tk.Button(self.root, text="Применить фильтр", command=self.apply_filter).grid(row=7, column=0, columnspan=2)

        # Кнопки сохранения/загрузки
        tk.Button(self.root, text="Сохранить в JSON", command=self.save_data).grid(row=8, column=0)
        tk.Button(self.root, text="Загрузить из JSON", command=self.load_data).grid(row=8, column=1)

    def validate_input(self):
        try:
            date = datetime.strptime(self.date_entry.get(), "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте YYYY-MM-DD.")
            return False

        try:
            temp = float(self.temp_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом.")
            return False

        if not self.desc_entry.get():
            messagebox.showerror("Ошибка", "Описание не может быть пустым.")
            return False

        return True

    def add_entry(self):
        if not self.validate_input():
            return

        entry = {
            "date": self.date_entry.get(),
            "temperature": float(self.temp_entry.get()),
            "description": self.desc_entry.get(),
            "precipitation": self.precipitation_var.get()
        }
        self.entries.append(entry)
        self.update_table()

        # Очищаем поля ввода
        self.date_entry.delete(0, tk.END)
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.precipitation_var.set(False)

    def update_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for entry in self.entries:
            self.tree.insert("", "end", values=(
                entry["date"],
                f"{entry['temperature']}°C",
                entry["description"],
                "Да" if entry["precipitation"] else "Нет"
            ))

    def save_data(self):
        with open("weather_data.json", "w", encoding="utf-8") as f:
            json.dump(self.entries, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Успех", "Данные сохранены в weather_data.json")

    def load_data(self):
        if os.path.exists("weather_data.json"):
            with open("weather_data.json", "r", encoding="utf-8") as f:
                self.entries = json.load(f)
            self.update_table()
        else:
            messagebox.showwarning("Предупреждение", "Файл weather_data.json не найден.")

    def apply_filter(self):
        filter_date = self.filter_date_entry.get()
        filtered_entries = [e for e in self.entries if e["date"] == filter_date]
        for item in self.tree.get_children():
            self.tree.delete(item)
        for entry in filtered_entries:
            self.tree.insert("", "end", values=(
                entry["date"],
                f"{entry['temperature']}°C",
                entry["description"],
                "Да" if entry["precipitation"] else "Нет"
            ))

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()
