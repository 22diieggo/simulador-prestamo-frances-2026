# ──────────────────────────────────────────────────────────
#  CUADRO DE AMORTIZACIÓN
# ──────────────────────────────────────────────────────────

def imprimir_cuadro(capital: float, i: float, n: int, cuota: float) -> None:
    """
    Imprime el cuadro de amortización sin comisiones ni gastos.
    Columnas: período | cuota | intereses | amortización | capital pendiente
    """
    ancho = 70
    print(f"\n{'─' * ancho}")
    print(f"{'Per':>5} {'Cuota (€)':>13} {'Intereses (€)':>15} " f"{'Amortiz. (€)':>14} {'Cap. Pendiente (€)':>18}")
    print(f"{'─' * ancho}")
 
    C = capital
    total_cuotas = total_intereses = total_amort = 0.0
 
    for s in range(1, n + 1):
        I_s = C * i
        A_s = cuota - I_s
        C -= A_s
        if s == n:
            C = 0.0         # corrección de redondeo en último período
 
        total_cuotas    += cuota
        total_intereses += I_s
        total_amort     += A_s
 
        print(f"{s:>5} {cuota:>13,.2f} {I_s:>15,.2f} {A_s:>14,.2f} {C:>18,.2f}")
 
    print(f"{'─' * ancho}")
    print(f"{'TOTAL':>5} {total_cuotas:>13,.2f} {total_intereses:>15,.2f} "
          f"{total_amort:>14,.2f}")
    print(f"{'─' * ancho}")
 
 

