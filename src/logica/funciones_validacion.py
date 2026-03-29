# ──────────────────────────────────────────────────────────
#  FUNCIONES DE ENTRADA CON VALIDACIÓN
# ──────────────────────────────────────────────────────────

def pedir_float(mensaje: str, minimo: float = None, maximo: float = None) -> float:
    """Solicita un número real con rango opcional."""
    while True:
        try:
            valor = float(input(mensaje))
            if minimo is not None and valor < minimo:
                print(f" El valor mínimo es {minimo}.")
                continue
            if maximo is not None and valor > maximo:
                print(f" El valor máximo es {maximo}.")
                continue
            return valor
        except ValueError:
            print(" Introduce un número válido.")


def pedir_int(mensaje: str, minimo: int = None, maximo: int = None) -> int:
    """Solicita un número entero con rango opcional."""
    while True:
        try:
            valor = int(input(mensaje))
            if minimo is not None and valor < minimo:
                print(f"  El valor mínimo es {minimo}.")
                continue
            if maximo is not None and valor > maximo:
                print(f"  El valor máximo es {maximo}.")
                continue
            return valor
        except ValueError:
            print(" Introduce un número entero válido.")


def pedir_periodicidad() -> tuple[int, str]:
    """Devuelve (pagos_por_año, nombre_periodicidad)."""
    opciones = {
        "1": (12, "mensual"),
        "2": (4,  "trimestral"),
        "3": (2,  "semestral"),
        "4": (1,  "anual"),
    }
    print("\n  Periodicidad de los términos amortizativos:")
    for k, (_, nombre) in opciones.items():
        print(f"    {k}. {nombre.capitalize()}")
    while True:
        op = input("  Elige una opción (1-4): ")
        if op in opciones:
            return opciones[op]
        print(" Opción no válida, elige entre 1 y 4.")


def pedir_tipo_interes() -> str:
    """Devuelve 'fijo' o 'variable'."""
    print("\n  Tipo de interés:")
    print("    1. Fijo    → Euribor + 1,00 %")
    print("    2. Variable → Euribor + 0,50 %")
    while True:
        op = input("  Elige una opción (1-2): ")
        if op == "1":
            return "fijo"
        elif op == "2":
            return "variable"
        print(" Opción no válida.")

