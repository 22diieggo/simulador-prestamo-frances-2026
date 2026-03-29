#Euribor + spread(dato profesor) - bonificación → tipo nominal → i → cuota → cuadro de amortización
import requests # para obtener el valor del Euribor de internet

def pedir_periocidad():
    print("Elije la pericidad de la consulta:")
    print("1. Mensual")
    print("2. Trimestral")
    print("3. Semestral")
    print("4. Anual")

    opcion = input("Ingrese el número correspondiente 1-4: ")
    if opcion == "1":
        return 12, "mensual"
    elif opcion == "2":
        return 4, "trimestral"
    elif opcion == "3":
        return 2, "semestral"
    elif opcion == "4":
        return 1, "anual"
    else:
        print("Opción no válida → mensual por defecto")
        return 12, "mensual"
    
def pedir_tipo_interes():
    print("Elige el tipo de interés:")
    print("1. Fijo (Euribor + 1%)")
    print("2. Variable (Euribor + 0,5%)")
    opcion = input("Ingrese el número correspondiente 1-2: ")
    if opcion == "1":
        return "fijo"
    elif opcion == "2":
        return "variable"
    else:
        print("Opción no válida → fijo por defecto")
        return "fijo"


def calcular_cuota(capital, i, n):
    # C₀ = a · (1 - (1+i)⁻ⁿ) / i     , despejando a:
    if i == 0:
        return capital / n
    return capital * (i / (1 - (1 + i) ** (-n)))

def obtener_euribor():
    url = "https://data-api.ecb.europa.eu/service/data/FM/M.U2.EUR.RT.MM.EURIBOR1YD_.HSTA?lastNObservations=24&detail=dataonly&format=jsondata"
    try:
        respuesta = requests.get(url, timeout=5)
        datos = respuesta.json()
        observaciones = datos["dataSets"][0]["series"]["0:0:0:0:0:0:0"]["observations"]
        ultimo_indice = str(max(int(k) for k in observaciones.keys()))
        valor = observaciones[ultimo_indice][0]
        print(f"Euribor obtenido correctamente: {round(valor, 3)}%") 
        return round(valor, 3)
    except Exception as e:
        print(f"No se pudo obtener el Euribor ({e}). Usando valor por defecto: 2.407%")
        return 2.407

def main():
    print("Bienvenido al programa de cálculo de cuotas.")


    #Datos de entrada
    capital = float(input("Ingrese el capital a financiar (€): "))
    anios = int(input("Ingrese el número de años para el préstamo: "))
    pagos_anio, periodicidad = pedir_periocidad()

    #Valores fijos,                                                                                                     TODO: hacer que el usuario los ingrese
    bonificacion = 0.15
    euribor = obtener_euribor()
    tipo_interes = pedir_tipo_interes()      
    spread = 1.0 if tipo_interes == "fijo" else 0.5
    tipo_nominal = euribor + spread - bonificacion # preguntar al profesor en clase
    n = anios * pagos_anio
    i = (tipo_nominal / 100) / pagos_anio
    
    cuota = calcular_cuota(capital, i, n)



    # Resultados
    print("\n=== RESULTADOS ===")
    print(f"Periocidad: {periodicidad}")
    print(f"Tipo: {tipo_interes} — {tipo_nominal:.2f}%")
    print(f"Cuota: {cuota:.2f} €")



    C = capital  # capital pendiente inicial

    # f-string alineación: {'texto':>ancho} → ancho mínimo en caracteres, > alinea a la derecha
    print(f"\n{'Per':>4} {'Cuota':>10} {'Intereses':>10} {'Amortización':>13} {'Capital pendiente':>18}")
    print("-" * 60)

    for s in range(1, n + 1):
        I = C * i
        A = cuota - I
        C = C - A
        
        if s == n:
            C = 0  # corregir flotante en último período
        
        print(f"{s:>4} {cuota:>10.2f} {I:>10.2f} {A:>13.2f} {C:>18.2f}")


if __name__ == "__main__":
    main()




