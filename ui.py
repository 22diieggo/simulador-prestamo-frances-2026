from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from logica import obtener_euribor, simular_prestamo
from modelo import Prestamo, ResultadoSimulacion

PERIODICIDAD_UI = {
    "Mensual": "mensual",
    "Trimestral": "trimestral",
    "Semestral": "semestral",
    "Anual": "anual",
}

TIPO_INTERES_UI = {
    "Fijo": "fijo",
    "Variable": "variable",
}


class SimuladorPrestamoUI:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Simulador de prestamo frances")
        self.root.geometry("980x720")

        self.entry_nominal: tk.Entry
        self.entry_duracion: tk.Entry
        self.entry_euribor: tk.Entry
        self.entry_bonificacion: tk.Entry
        self.combo_periodo: ttk.Combobox
        self.combo_tipo: ttk.Combobox
        self.label_resumen: tk.Label
        self.tabla: ttk.Treeview

        self._crear_widgets()
        self._establecer_valores_iniciales()

    def _crear_widgets(self) -> None:
        frame_inputs = tk.LabelFrame(self.root, text="Datos", padx=10, pady=10)
        frame_inputs.pack(fill="x", padx=10, pady=10)

        tk.Label(frame_inputs, text="Nominal en EUR:").grid(row=0, column=0, sticky="w")
        self.entry_nominal = tk.Entry(frame_inputs)
        self.entry_nominal.grid(row=0, column=1, sticky="ew", padx=(0, 10))

        tk.Label(frame_inputs, text="Duracion en anios:").grid(
            row=1,
            column=0,
            sticky="w",
        )
        self.entry_duracion = tk.Entry(frame_inputs)
        self.entry_duracion.grid(row=1, column=1, sticky="ew", padx=(0, 10))

        tk.Label(frame_inputs, text="Periodo:").grid(row=2, column=0, sticky="w")
        self.combo_periodo = ttk.Combobox(
            frame_inputs,
            values=list(PERIODICIDAD_UI),
            state="readonly",
        )
        self.combo_periodo.grid(row=2, column=1, sticky="ew", padx=(0, 10))

        tk.Label(frame_inputs, text="Tipo de interes:").grid(row=3, column=0, sticky="w")
        self.combo_tipo = ttk.Combobox(
            frame_inputs,
            values=list(TIPO_INTERES_UI),
            state="readonly",
        )
        self.combo_tipo.grid(row=3, column=1, sticky="ew", padx=(0, 10))

        tk.Label(frame_inputs, text="Euribor en %:").grid(row=4, column=0, sticky="w")
        self.entry_euribor = tk.Entry(frame_inputs)
        self.entry_euribor.grid(row=4, column=1, sticky="ew", padx=(0, 10))
        tk.Button(
            frame_inputs,
            text="Cargar Euribor",
            command=self.cargar_euribor,
        ).grid(row=4, column=2, sticky="w")

        tk.Label(frame_inputs, text="Bonificacion en %:").grid(
            row=5,
            column=0,
            sticky="w",
        )
        self.entry_bonificacion = tk.Entry(frame_inputs)
        self.entry_bonificacion.grid(row=5, column=1, sticky="ew", padx=(0, 10))

        frame_inputs.columnconfigure(1, weight=1)

        frame_botones = tk.Frame(self.root)
        frame_botones.pack(fill="x", padx=10)

        tk.Button(frame_botones, text="Calcular", command=self.calcular).pack(
            side="left",
            padx=(0, 10),
            pady=10,
        )
        tk.Button(frame_botones, text="Limpiar", command=self.limpiar).pack(
            side="left",
            pady=10,
        )

        frame_resumen = tk.LabelFrame(self.root, text="Resumen", padx=10, pady=10)
        frame_resumen.pack(fill="x", padx=10, pady=10)

        self.label_resumen = tk.Label(frame_resumen, text="", justify="left", anchor="w")
        self.label_resumen.pack(fill="x")

        frame_tabla = tk.LabelFrame(self.root, text="Cuadro de amortizacion")
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

        columnas = ("periodo", "cuota", "interes", "amortizacion", "saldo")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

        self.tabla.heading("periodo", text="Periodo")
        self.tabla.heading("cuota", text="Cuota")
        self.tabla.heading("interes", text="Interes")
        self.tabla.heading("amortizacion", text="Amortizacion")
        self.tabla.heading("saldo", text="Capital pendiente")

        self.tabla.column("periodo", width=90, anchor="center")
        self.tabla.column("cuota", width=140, anchor="e")
        self.tabla.column("interes", width=140, anchor="e")
        self.tabla.column("amortizacion", width=140, anchor="e")
        self.tabla.column("saldo", width=180, anchor="e")

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _establecer_valores_iniciales(self) -> None:
        self.combo_periodo.current(0)
        self.combo_tipo.current(0)
        self.entry_bonificacion.insert(0, "0.15")

    def _leer_float(self, valor: str, nombre_campo: str) -> float:
        texto = valor.strip().replace(",", ".")
        if not texto:
            raise ValueError(f"Debes indicar {nombre_campo}.")
        return float(texto)

    def _leer_int(self, valor: str, nombre_campo: str) -> int:
        texto = valor.strip()
        if not texto:
            raise ValueError(f"Debes indicar {nombre_campo}.")
        return int(texto)

    def _crear_prestamo_desde_formulario(self) -> Prestamo:
        euribor_texto = self.entry_euribor.get().strip()
        euribor = (
            obtener_euribor()
            if not euribor_texto
            else self._leer_float(euribor_texto, "el Euribor")
        )

        if not euribor_texto:
            self.entry_euribor.delete(0, tk.END)
            self.entry_euribor.insert(0, f"{euribor:.3f}")

        return Prestamo(
            capital=self._leer_float(self.entry_nominal.get(), "el nominal"),
            duracion_anios=self._leer_int(self.entry_duracion.get(), "la duracion"),
            periodicidad=PERIODICIDAD_UI[self.combo_periodo.get()],
            tipo_interes=TIPO_INTERES_UI[self.combo_tipo.get()],
            euribor=euribor,
            bonificacion=self._leer_float(
                self.entry_bonificacion.get(),
                "la bonificacion",
            ),
        )

    def _formatear_moneda(self, valor: float) -> str:
        return f"{valor:,.2f} EUR"

    def _mostrar_resumen(self, resultado: ResultadoSimulacion) -> None:
        resumen = "\n".join(
            [
                f"Tipo nominal inicial (TNA): {resultado.tipo_nominal_inicial:.2f}%",
                f"Interes periodico: {resultado.interes_periodico * 100:.4f}%",
                f"Cuota sistema frances: {self._formatear_moneda(resultado.cuota)}",
                (
                    "Gasto de administracion por cuota: "
                    f"{self._formatear_moneda(resultado.gasto_administracion_por_cuota)}"
                ),
                f"Gasto de estudio: {self._formatear_moneda(resultado.gasto_estudio)}",
                f"Cuota total con gastos: {self._formatear_moneda(resultado.cuota_total)}",
                (
                    "Coste efectivo aproximado: "
                    f"{resultado.coste_efectivo_operacion:.2f}%"
                ),
                f"Total intereses pagados: {self._formatear_moneda(resultado.total_intereses)}",
                f"Total pagado: {self._formatear_moneda(resultado.total_pagado)}",
            ]
        )
        self.label_resumen.config(text=resumen)

    def _mostrar_tabla(self, resultado: ResultadoSimulacion) -> None:
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for fila in resultado.cuadro_amortizacion:
            self.tabla.insert(
                "",
                "end",
                values=(
                    fila.periodo,
                    self._formatear_moneda(fila.cuota),
                    self._formatear_moneda(fila.interes),
                    self._formatear_moneda(fila.amortizacion),
                    self._formatear_moneda(fila.saldo_pendiente),
                ),
            )

    def cargar_euribor(self) -> None:
        euribor = obtener_euribor()
        self.entry_euribor.delete(0, tk.END)
        self.entry_euribor.insert(0, f"{euribor:.3f}")

    def calcular(self) -> None:
        try:
            prestamo = self._crear_prestamo_desde_formulario()
            resultado = simular_prestamo(prestamo)
        except ValueError as error:
            messagebox.showerror("Error", str(error))
            return
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo calcular el prestamo: {error}")
            return

        self._mostrar_resumen(resultado)
        self._mostrar_tabla(resultado)

    def limpiar(self) -> None:
        for entry in (
            self.entry_nominal,
            self.entry_duracion,
            self.entry_euribor,
            self.entry_bonificacion,
        ):
            entry.delete(0, tk.END)

        self.combo_periodo.current(0)
        self.combo_tipo.current(0)
        self.entry_bonificacion.insert(0, "0.15")
        self.label_resumen.config(text="")

        for item in self.tabla.get_children():
            self.tabla.delete(item)

    def ejecutar(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    SimuladorPrestamoUI().ejecutar()
