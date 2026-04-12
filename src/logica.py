from __future__ import annotations
from math import isclose
import requests
from modelo import FilaAmortizacion, Prestamo, ResultadoSimulacion

PERIODOS_POR_ANIO = {
    "mensual": 12,
    "trimestral": 4,
    "semestral": 2,
    "anual": 1,
}

SPREAD_POR_TIPO = {
    "fijo": 1.0,
    "variable": 0.5,
}

EURIBOR_FALLBACK = 2.407
EURIBOR_URL = (
    "https://data-api.ecb.europa.eu/service/data/"
    "FM/M.U2.EUR.RT.MM.EURIBOR1YD_.HSTA"
    "?lastNObservations=24&detail=dataonly&format=jsondata"
)


def validar_prestamo(prestamo: Prestamo) -> None:
    if prestamo.capital <= 0:
        raise ValueError("El nominal debe ser mayor que 0.")
    if prestamo.duracion_anios <= 0:
        raise ValueError("La duracion debe ser mayor que 0.")
    if prestamo.periodicidad not in PERIODOS_POR_ANIO:
        raise ValueError("La periodicidad indicada no es valida.")
    if prestamo.tipo_interes not in SPREAD_POR_TIPO:
        raise ValueError("El tipo de interes indicado no es valido.")
    if prestamo.gasto_estudio < 0:
        raise ValueError("El gasto de estudio no puede ser negativo.")
    if prestamo.gasto_administracion_por_cuota < 0:
        raise ValueError("El gasto de administracion no puede ser negativo.")


def obtener_periodos_por_anio(periodicidad: str) -> int:
    try:
        return PERIODOS_POR_ANIO[periodicidad]
    except KeyError as error:
        raise ValueError("La periodicidad indicada no es valida.") from error


def calcular_tipo_nominal_inicial(prestamo: Prestamo) -> float:
    spread = SPREAD_POR_TIPO[prestamo.tipo_interes]
    return prestamo.euribor + spread - prestamo.bonificacion


def calcular_interes_periodico(prestamo: Prestamo) -> float:
    periodos_por_anio = obtener_periodos_por_anio(prestamo.periodicidad)
    return (calcular_tipo_nominal_inicial(prestamo) / 100) / periodos_por_anio


def calcular_numero_periodos(prestamo: Prestamo) -> int:
    return prestamo.duracion_anios * obtener_periodos_por_anio(prestamo.periodicidad)


def calcular_cuota_sistema_frances(
    capital: float,
    interes_periodico: float,
    numero_periodos: int,
) -> float:
    if numero_periodos <= 0:
        raise ValueError("El numero de periodos debe ser mayor que 0.")
    if interes_periodico == 0:
        return capital / numero_periodos
    return capital * (
        interes_periodico / (1 - (1 + interes_periodico) ** (-numero_periodos))
    )


def generar_cuadro_amortizacion(
    prestamo: Prestamo,
    cuota: float | None = None,
) -> list[FilaAmortizacion]:
    interes_periodico = calcular_interes_periodico(prestamo)
    numero_periodos = calcular_numero_periodos(prestamo)
    cuota = cuota or calcular_cuota_sistema_frances(
        prestamo.capital,
        interes_periodico,
        numero_periodos,
    )

    saldo = prestamo.capital
    cuadro: list[FilaAmortizacion] = []

    for periodo in range(1, numero_periodos + 1):
        interes = saldo * interes_periodico
        amortizacion = cuota - interes
        saldo -= amortizacion

        if periodo == numero_periodos or isclose(saldo, 0.0, abs_tol=1e-8):
            saldo = 0.0

        cuadro.append(
            FilaAmortizacion(
                periodo=periodo,
                cuota=cuota,
                interes=interes,
                amortizacion=amortizacion,
                saldo_pendiente=saldo,
            )
        )

    return cuadro


def calcular_coste_efectivo_operacion(
    prestamo: Prestamo,
    cuota: float | None = None,
    numero_periodos: int | None = None,
) -> float:
    interes_periodico = calcular_interes_periodico(prestamo)
    numero_periodos = numero_periodos or calcular_numero_periodos(prestamo)
    cuota = cuota or calcular_cuota_sistema_frances(
        prestamo.capital,
        interes_periodico,
        numero_periodos,
    )
    gasto_administracion = cuota * prestamo.gasto_administracion_por_cuota
    total_pagado = (
        (cuota + gasto_administracion) * numero_periodos + prestamo.gasto_estudio
    )
    return ((total_pagado - prestamo.capital) / prestamo.capital) * 100


def simular_prestamo(prestamo: Prestamo) -> ResultadoSimulacion:
    validar_prestamo(prestamo)

    periodos_por_anio = obtener_periodos_por_anio(prestamo.periodicidad)
    numero_periodos = calcular_numero_periodos(prestamo)
    tipo_nominal_inicial = calcular_tipo_nominal_inicial(prestamo)
    interes_periodico = calcular_interes_periodico(prestamo)
    cuota = calcular_cuota_sistema_frances(
        prestamo.capital,
        interes_periodico,
        numero_periodos,
    )
    cuadro_amortizacion = generar_cuadro_amortizacion(prestamo, cuota=cuota)
    total_intereses = sum(fila.interes for fila in cuadro_amortizacion)
    gasto_administracion = cuota * prestamo.gasto_administracion_por_cuota
    cuota_total = cuota + gasto_administracion
    total_pagado = prestamo.gasto_estudio + cuota_total * numero_periodos
    coste_efectivo = calcular_coste_efectivo_operacion(
        prestamo,
        cuota=cuota,
        numero_periodos=numero_periodos,
    )

    return ResultadoSimulacion(
        tipo_nominal_inicial=tipo_nominal_inicial,
        interes_periodico=interes_periodico,
        periodos_por_anio=periodos_por_anio,
        numero_periodos=numero_periodos,
        cuota=cuota,
        gasto_estudio=prestamo.gasto_estudio,
        gasto_administracion_por_cuota=gasto_administracion,
        cuota_total=cuota_total,
        coste_efectivo_operacion=coste_efectivo,
        total_intereses=total_intereses,
        total_pagado=total_pagado,
        cuadro_amortizacion=cuadro_amortizacion,
    )


def obtener_euribor() -> float:
    try:
        respuesta = requests.get(EURIBOR_URL, timeout=5)
        respuesta.raise_for_status()
        datos = respuesta.json()
        observaciones = datos["dataSets"][0]["series"]["0:0:0:0:0:0:0"]["observations"]
        ultimo_indice = str(max(int(clave) for clave in observaciones))
        valor = observaciones[ultimo_indice][0]
        return round(valor, 3)
    except Exception:
        return EURIBOR_FALLBACK
