"""Tkinter user interface. Only handles presentation and user input."""

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk

import employee_service as service
from excel_reader import read_employees
from excel_validator import ExcelValidationError


def format_money(value):
    return f"${value:,.0f}"


class EmployeeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Empleados")
        self.geometry("720x460")
        self.minsize(600, 380)
        self.employees = []
        self.data_buttons = []
        self._build_layout()

    # ---------- layout ----------

    def _build_layout(self):
        menu = ttk.Frame(self, padding=10)
        menu.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(menu, text="SISTEMA DE EMPLEADOS", font=("Segoe UI", 11, "bold")).pack(
            pady=(0, 10)
        )

        ttk.Button(menu, text="Leer archivo Excel", command=self.on_load_file).pack(
            fill=tk.X, pady=2
        )

        options = [
            ("Mostrar empleados", self.on_show_employees),
            ("Buscar empleado", self.on_search_employee),
            ("Total de sueldos", self.on_total_salaries),
            ("Sueldo promedio", self.on_average_salary),
            ("Empleado con mayor sueldo", self.on_highest_salary),
            ("Empleados por sueldo", self.on_employees_by_salary),
        ]
        for text, command in options:
            button = ttk.Button(menu, text=text, command=command, state=tk.DISABLED)
            button.pack(fill=tk.X, pady=2)
            self.data_buttons.append(button)

        ttk.Button(menu, text="Salir", command=self.destroy).pack(fill=tk.X, pady=(12, 2))

        content = ttk.Frame(self, padding=10)
        content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.status = ttk.Label(content, text="Cargue un archivo Excel para comenzar.")
        self.status.pack(anchor=tk.W, pady=(0, 6))

        columns = ("doc_type", "doc_number", "salary")
        self.table = ttk.Treeview(content, columns=columns, show="headings")
        for column, title, anchor in (
            ("doc_type", "Tipo doc", tk.W),
            ("doc_number", "Nro documento", tk.W),
            ("salary", "Sueldo", tk.E),
        ):
            self.table.heading(column, text=title)
            self.table.column(column, anchor=anchor)
        self.table.pack(fill=tk.BOTH, expand=True)

    # ---------- helpers ----------

    def show_table(self, employees, message):
        self.table.delete(*self.table.get_children())
        for e in employees:
            self.table.insert("", tk.END, values=(e.doc_type, e.doc_number, format_money(e.salary)))
        self.status.config(text=message)

    def ask_salary(self, prompt):
        value = simpledialog.askstring("Empleados por sueldo", prompt, parent=self)
        if value is None or value.strip() == "":
            return None
        try:
            return float(value.replace(",", "").replace("$", ""))
        except ValueError:
            messagebox.showerror("Valor inválido", f"'{value}' no es un número.")
            raise

    # ---------- menu actions ----------

    def on_load_file(self):
        path = filedialog.askopenfilename(
            title="Seleccione el archivo de empleados",
            filetypes=[("Excel", "*.xlsx *.xlsm")],
        )
        if not path:
            return
        try:
            self.employees = read_employees(path)
        except ExcelValidationError as exc:
            messagebox.showerror("Archivo inválido", "\n".join(exc.errors[:15]))
            return

        for button in self.data_buttons:
            button.config(state=tk.NORMAL)
        self.show_table(self.employees, f"{len(self.employees)} empleados cargados.")

    def on_show_employees(self):
        employees = service.list_employees(self.employees)
        self.show_table(employees, f"Total: {len(employees)} empleados.")

    def on_search_employee(self):
        doc_number = simpledialog.askstring("Buscar empleado", "Número de documento:", parent=self)
        if not doc_number:
            return
        found = service.search_employee(self.employees, doc_number)
        if not found:
            messagebox.showinfo("Buscar empleado", f"No existe el documento {doc_number}.")
            return
        self.show_table(found, f"{len(found)} resultado(s) para {doc_number}.")

    def on_total_salaries(self):
        total = service.total_salaries(self.employees)
        messagebox.showinfo("Total de sueldos", f"Total de sueldos: {format_money(total)}")

    def on_average_salary(self):
        average = service.average_salary(self.employees)
        messagebox.showinfo("Sueldo promedio", f"Sueldo promedio: {format_money(average)}")

    def on_highest_salary(self):
        top = service.highest_paid_employees(self.employees)
        self.show_table(top, f"Mayor sueldo: {format_money(top[0].salary)}")

    def on_employees_by_salary(self):
        try:
            min_salary = self.ask_salary("Sueldo mínimo (vacío = sin límite):")
            max_salary = self.ask_salary("Sueldo máximo (vacío = sin límite):")
        except ValueError:
            return
        if min_salary is not None and max_salary is not None and min_salary > max_salary:
            messagebox.showerror("Rango inválido", "El mínimo no puede ser mayor al máximo.")
            return
        result = service.employees_by_salary(self.employees, min_salary, max_salary)
        self.show_table(result, f"{len(result)} empleados en el rango (mayor a menor).")
