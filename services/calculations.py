import math
from models import Tanque  # Importa el modelo Tanque desde models.py

def simular_movimiento(tanque: Tanque, tiempo: float) -> dict:
    # Fuerza neta: fuerza motriz menos la fuerza de rozamiento (coeficiente * masa * g)
    fuerza_neta = tanque.fuerza_motriz - (tanque.coeficiente_rozamiento * tanque.masa * 9.81)
    aceleracion = fuerza_neta / tanque.masa
    velocidad_final = aceleracion * tiempo
    distancia = 0.5 * aceleracion * tiempo ** 2

    return {
        "aceleracion": aceleracion,
        "velocidad_final": velocidad_final,
        "distancia_recorrida": distancia
    }