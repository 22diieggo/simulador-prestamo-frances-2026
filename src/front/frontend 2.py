import tkinter as tk
from tkinter import ttk, messagebox

# Cabecera de la ventana principal
root = tk.Tk()
root.title("Simulador de préstamo frances: Practica 1")
root.geometry("900x700")

#Datos a pedir
frame_inputs = tk.LabelFrame(root, text=" Datos", padx=10, pady=10)
frame_inputs.pack(fill="x", padx=10, pady=10)

tk.Label(frame_inputs, text="Nominal en €:").grid(row=0, column=0, sticky="w")
entry_nominal = tk.Entry(frame_inputs)
entry_nominal.grid(row=0, column=1)

tk.Label(frame_inputs, text="Duración en años):").grid(row=1, column=0, sticky="w")
entry_duracion = tk.Entry(frame_inputs)
entry_duracion.grid(row=1, column=1)

tk.Label(frame_inputs, text="Periodo:").grid(row=2, column=0, sticky="w")
combo_periodo = ttk.Combobox(frame_inputs, values=["Mensual", "Trimestral", "Semestral", "Anual"], state="readonly")
combo_periodo.grid(row=2, column=1)
combo_periodo.current(0)

tk.Label(frame_inputs, text="Tipo de interés:").grid(row=3, column=0, sticky="w")
combo_tipo = ttk.Combobox(frame_inputs, values=["Fijo", "Variable"], state="readonly")
combo_tipo.grid(row=3, column=1)
combo_tipo.current(0)

tk.Label(frame_inputs, text="Euribor en %:").grid(row=4, column=0, sticky="w")
entry_euribor = tk.Entry(frame_inputs)
entry_euribor.grid(row=4, column=1)

tk.Label(frame_inputs, text="Bonificación en %:").grid(row=5, column=0, sticky="w")
entry_bonificacion = tk.Entry(frame_inputs)
entry_bonificacion.grid(row=5, column=1)

#Calculo de los datos necesarios para la practica
def calcular():
    try:
        # Leer los datos
        nominal = float(entry_nominal.get())
        duracion = int(entry_duracion.get())
        euribor = float(entry_euribor.get()) / 100
        bonificacion = float(entry_bonificacion.get()) / 100
        tipo = combo_tipo.get()
        periodo = combo_periodo.get()

        # La validación básica
        if nominal <= 0 or duracion <= 0:
            raise ValueError

        # Periodos por año
        periodos = {"Mensual": 12, "Trimestral": 4, "Semestral": 2, "Anual": 1}
        p = periodos[periodo]

        # Tipo de interés si es fijo o variable
        if tipo == "Fijo":
            tna = euribor + 0.01 - bonificacion
        else:
            tna = euribor + 0.005 - bonificacion

        # Cálculos
        i = tna / p
        n = duracion * p

        # Cuota
        if i == 0:
            cuota = nominal / n
        else:
            cuota = nominal * (i / (1 - (1 + i) ** (-n)))

        # Gastos
        gasto_estudio = 150
        gasto_admin = cuota * 0.001
        cuota_total = cuota + gasto_admin

        # Coste total simple
        coste_total = ((cuota_total * n) - nominal) / nominal * 100

        # Limpiar la tabla
        for item in tabla.get_children():
            tabla.delete(item)

        saldo = nominal

        # Rellenar tabla
        for k in range(1, n + 1):
            interes = saldo * i
            amortizacion = cuota - interes
            saldo = saldo - amortizacion


            tabla.insert("", "end", values=(
                k,
                f"{saldo:,.2f}",
                f"{interes:,.2f}",
                f"{amortizacion:,.2f}",
                f"{cuota:,.2f}"
            ))

        # Mostrar el resumen de los valores
        resumen = (
            f"Tipo de interés (TNA): {tna*100:.2f}%\n"
            f"Cuota: {cuota:.2f} €\n"
            f"Gastos por cuota: {gasto_admin:.2f} €\n"
            f"Coste total aproximado: {coste_total:.2f}%"
        )

        label_resumen.config(text=resumen)

    except:
        messagebox.showerror("Error", "Introduce datos correctos")

#Los botones de la interfaz
frame_botones = tk.Frame(root)
frame_botones.pack(pady=10)

tk.Button(frame_botones, text="Calcular", command=calcular).grid(row=0, column=0, padx=10)

def limpiar():
    entry_nominal.delete(0, tk.END)
    entry_duracion.delete(0, tk.END)
    entry_euribor.delete(0, tk.END)
    entry_bonificacion.delete(0, tk.END)
    label_resumen.config(text="")
    for item in tabla.get_children():
        tabla.delete(item)

tk.Button(frame_botones, text="Limpiar", command=limpiar).grid(row=0, column=1, padx=10)

#Resumen de los calculos
frame_resumen = tk.LabelFrame(root, text="Resumen", padx=10, pady=10)
frame_resumen.pack(fill="x", padx=10, pady=10)

label_resumen = tk.Label(frame_resumen, text="", justify="left")
label_resumen.pack()

#Interfaz de la tabla
frame_tabla = tk.LabelFrame(root, text="Amortización")
frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

columnas = ("cuota", "saldo", "interes", "amort", "pago")
tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

tabla.heading("cuota", text="Cuota")
tabla.heading("saldo", text="Saldo")
tabla.heading("interes", text="Interés")
tabla.heading("amort", text="Amortización")
tabla.heading("pago", text="Pago")

tabla.pack(fill="both", expand=True)

# Se ejecuta
root.mainloop()