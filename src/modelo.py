from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Prestamo:
    capital: float
    duracion_anios: int
    periodicidad: str
    tipo_interes: str
    euribor: float
    bonificacion: float = 0.0
    gasto_estudio: float = 150.0
    gasto_administracion_por_cuota: float = 0.001


@dataclass(slots=True)
class FilaAmortizacion:
    periodo: int
    cuota: float
    interes: float
    amortizacion: float
    saldo_pendiente: float


@dataclass(slots=True)
class ResultadoSimulacion:
    tipo_nominal_inicial: float
    interes_periodico: float
    periodos_por_anio: int
    numero_periodos: int
    cuota: float
    gasto_estudio: float
    gasto_administracion_por_cuota: float
    cuota_total: float
    coste_efectivo_operacion: float
    total_intereses: float
    total_pagado: float
    cuadro_amortizacion: list[FilaAmortizacion] = field(default_factory=list)
