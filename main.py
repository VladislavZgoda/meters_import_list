import os
import traceback
import tkinter as tk
from tkinter import ttk, filedialog

from process_files import process_files
from write_data import fill_in_import_list


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

        self._setup_styles()

        ttk.Label(
            window,
            text="Экспорт из Sims:",
            style="Title.TLabel",
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="e",
        )

        self.sims_label = ttk.Label(
            window,
            text="Файл не выбран",
            style="NotSelected.TLabel",
            width=40,
            anchor="w",
            relief="sunken",
        )

        self.sims_label.grid(row=0, column=1, padx=5)

        ttk.Button(
            window,
            text="Просмотреть...",
            style="Normal.TButton",
            command=self.select_sims_file,
        ).grid(row=0, column=2, padx=5)

        ttk.Label(
            window,
            text="Список ПУ:",
            font=("Arial", 18),
            style="Title.TLabel",
        ).grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.meters_label = ttk.Label(
            window,
            text="Файл не выбран",
            style="NotSelected.TLabel",
            width=40,
            anchor="w",
            relief="sunken",
        )

        self.meters_label.grid(row=1, column=1, padx=5)

        ttk.Button(
            window,
            text="Просмотреть...",
            style="Normal.TButton",
            command=self.select_meters_file,
        ).grid(row=1, column=2, padx=5)

        self.status_label = ttk.Label(window, text="", style="Status.TLabel")
        self.status_label.grid(row=3, column=0, columnspan=3, pady=10)

        ttk.Button(
            window,
            text="Сформировать ОП",
            style="Submit.TButton",
            command=self.create_import_list,
        ).grid(row=2, column=1, pady=10)

    def select_sims_file(self):
        path = filedialog.askopenfilename(
            title="Выбрать экспорт из Sims",
            filetypes=[("Excel files", "*.xlsx")],
        )

        if path:
            self.sims_file_path = path
            self.sims_label.config(text=os.path.basename(path), foreground="green")

    def select_meters_file(self):
        path = filedialog.askopenfilename(
            title="Выбрать список ПУ",
            filetypes=[("Excel files", "*.xlsx")],
        )

        if path:
            self.meters_file_path = path
            self.meters_label.config(text=os.path.basename(path), foreground="green")

    def create_import_list(self):
        self.status_label.config(text="")

        if not self.sims_file_path or not self.meters_file_path:
            self.status_label.config(text="Выберите оба файла!", foreground="red")
            return

        try:
            import_data = process_files(self.sims_file_path, self.meters_file_path)

            save_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                title="Сохранить файл как",
            )

            if not save_path:
                self.status_label.config(
                    text="Сохранение отменено", foreground="orange"
                )
                return

            wb_import_list = fill_in_import_list(import_data)
            wb_import_list.save(save_path)
            self.status_label.config(text="Файл успешно сохранён!", foreground="green")
        except Exception as e:
            self.status_label.config(
                text=f"Ошибка: {e}", foreground="red", wraplength=500
            )
            traceback.print_exc()

    def _setup_styles(self):
        style = ttk.Style()

        style.configure("Title.TLabel", font=("Arial", 18), foreground="blue")
        style.configure("NotSelected.TLabel", font=("Arial", 12), foreground="red")
        style.configure("Status.TLabel", font=("Arial", 14))

        style.configure("Normal.TButton", font=("Arial", 12))
        style.configure("Submit.TButton", font=("Arial", 14))


if __name__ == "__main__":
    main()
