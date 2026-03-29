# ──────────────────────────────────────────────────────────
#  CÁLCULOS FINANCIEROS
# ──────────────────────────────────────────────────────────

def calcular_cuota(capital: float, i: float, n: int) -> float:
    """
    Cuota constante — Sistema francés.
        a = C · i / [1 − (1+i)^(−n)]
    """
    if i == 0:
        return capital / n
    return capital * i / (1 - (1 + i) ** (-n))

