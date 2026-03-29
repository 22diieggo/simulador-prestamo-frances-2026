"""
╔══════════════════════════════════════════════════════════╗
║  SIMULADOR DE PRÉSTAMO — SISTEMA FRANCÉS (TÉRMINOS CTES) ║
║  Trabajo 1 — Análisis y Valoración de Proyectos          ║
║  Curso 2025-26                                           ║
╚══════════════════════════════════════════════════════════╝
"""

import calculos_financieros
import funciones_validacion
import calculo_amortizacion
import obtener_Euribor

# ──────────────────────────────────────────────────────────
#  PROGRAMA PRINCIPAL
# ──────────────────────────────────────────────────────────
# Gastos fijos según enunciado
GASTOS_ESTUDIO   = 150.0    # €  (pago único al inicio)
GASTOS_ADMIN     = 0.001    # 1 ‰ sobre cada término amortizativo
 

def main() -> None:
    sep = "=" * 60
    print(f"\n{sep}")
    print("   SIMULADOR DE PRÉSTAMO — SISTEMA FRANCÉS")
    print("   Análisis y Valoración de Proyectos de Inversión 2025-26")
    print(f"{sep}\n")
 
    # ── 1. Datos de entrada ───────────────────────────────────
    capital = funciones_validacion.pedir_float(
        "Capital solicitado (entre 100.000 y 200.000 €): ",
        minimo=100_000, maximo=200_000
    )
    anios = funciones_validacion.pedir_int(
        "Duración del préstamo en años (máximo 30): ",
        minimo=1, maximo=30
    )
    pagos_anio, periodicidad = funciones_validacion.pedir_periodicidad()
    tipo_interes = funciones_validacion.pedir_tipo_interes()
    bonificacion = funciones_validacion.pedir_float(
        "\nBonificación por contratación de otros productos\n"
        "(entre 0,10 % y 0,25 %): ",
        minimo=0.10, maximo=0.25
    )
 
    # ── 2. Euribor ────────────────────────────────────────────
    print("\nConsultando Euribor 12m al BCE...")
    euribor = obtener_Euribor.obtener_euribor()
 
    # ── 3. Tipo nominal ───────────────────────────────────────
    spread = 1.0 if tipo_interes == "fijo" else 0.5
    tipo_nominal_anual = euribor + spread - bonificacion   # %
 
    n = anios * pagos_anio                      # número total de períodos
    i = (tipo_nominal_anual / 100) / pagos_anio # tipo periódico (tanto por uno)
 
    # ── 4. Cuotas ─────────────────────────────────────────────
    cuota_pura    = calculos_financieros.calcular_cuota(capital, i, n)
    gastos_admin_periodo = cuota_pura * GASTOS_ADMIN
    cuota_con_gastos     = cuota_pura + gastos_admin_periodo
 
    # ── 5. Resumen de parámetros ──────────────────────────────
    print(f"\n{sep}")
    print("   PARÁMETROS DE LA OPERACIÓN")
    print(f"{sep}")
    print(f"  Capital solicitado        : {capital:>14,.2f} €")
    print(f"  Duración                  : {anios:>10} años  ({n} períodos {periodicidad}s)")
    print(f"  Tipo de interés           : {tipo_interes.upper()}")
    print(f"  Euribor 12m               : {euribor:>13.3f} %")
    print(f"  Spread                    : {spread:>13.2f} %")
    print(f"  Bonificación              : {bonificacion:>13.2f} %")
    print(f"  ─────────────────────────────────────────────────")
    print(f"  ► Tipo nominal anual (TIN): {tipo_nominal_anual:>13.4f} %")
    print(f"    Tipo periódico           : {i * 100:>12.6f} %")
    print(f"  ─────────────────────────────────────────────────")
    print(f"  Cuota pura (sin gastos)   : {cuota_pura:>14,.2f} €")
    print(f"  Gastos estudio (únicos)   : {GASTOS_ESTUDIO:>14,.2f} €")
    print(f"  Gastos administración/per : {gastos_admin_periodo:>14,.4f} € (1‰ s/cuota)")
    print(f"  Cuota total (con gastos)  : {cuota_con_gastos:>14,.4f} €")
    print(f"  ─────────────────────────────────────────────────")
    print(f"{sep}")
 
    # ── 6. Cuadro de amortización (sin comisiones ni gastos) ─
    print(f"\n{sep}")
    print("   CUADRO DE AMORTIZACIÓN  (sin comisiones ni gastos)")
    print(f"{sep}")
    calculo_amortizacion.imprimir_cuadro(capital, i, n, cuota_pura)
 
 
if __name__ == "__main__":
    main()