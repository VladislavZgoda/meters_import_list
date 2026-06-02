import tkinter as tk
from tkinter import filedialog

from process_files import process_files


def main():
    window = tk.Tk()
    App(window)
    window.mainloop()


class App:
    def __init__(self, window: tk.Tk):
        self.window = window
        self.window.title("Создать ОП")
        self.window.geometry("800x400")

        self.sims_file_path = ""
        self.meters_file_path = ""

        tk.Label(
            window,
            text="Экспорт из Sims:",
            font=("Arial", 18),
            fg="blue",
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="e",
        )

        self.sims_label = tk.Label(
            window,
            text="Файл не выбран",
            font=("Arial", 12),
            fg="red",
            width=40,
            anchor="w",
            relief="sunken",
        )

        self.sims_label.grid(row=0, column=1, padx=5)

        tk.Button(
            window,
            text="Просмотреть...",
            font=("Arial", 12),
            border=1.5,
            command=self.select_sims_file,
        ).grid(row=0, column=2, padx=5)

        tk.Label(
            window,
            text="Список ПУ:",
            font=("Arial", 18),
            fg="blue",
        ).grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.meters_label = tk.Label(
            window,
            text="Файл не выбран",
            font=("Arial", 12),
            fg="red",
            width=40,
            anchor="w",
            relief="sunken",
        )

        self.meters_label.grid(row=1, column=1, padx=5)

        tk.Button(
            window,
            text="Просмотреть...",
            font=("Arial", 12),
            border=1.5,
            command=self.select_meters_file,
        ).grid(row=1, column=2, padx=5)

        self.error_label = tk.Label(window, text="")
        self.error_label.grid(row=3, column=0, columnspan=3, pady=10)

        tk.Button(
            window,
            text="Сформировать ОП",
            font=("Arial", 14),
            border=3,
            command=self.create_import_list,
        ).grid(row=2, column=1, pady=10)

    def select_sims_file(self):
        path = filedialog.askopenfilename(title="Выбрать экспорт из Sims")

        if path:
            self.sims_file_path = path
            self.sims_label.config(text=path, fg="green")

    def select_meters_file(self):
        path = filedialog.askopenfilename(title="Выбрать список ПУ")

        if path:
            self.meters_file_path = path
            self.meters_label.config(text=path, fg="green")

    def create_import_list(self):
        self.error_label.config(text="")

        if self.sims_file_path and self.meters_file_path:
            import_data = process_files(self.sims_file_path, self.meters_file_path)
            print(import_data)
        else:
            self.error_label.config(
                text="Выберите оба файла!", font=("Arial", 18), fg="red"
            )


if __name__ == "__main__":
    main()
