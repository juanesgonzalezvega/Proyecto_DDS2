from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List

import schemas
from services.calculo_vectorial import clasificar_superficie_conica, calcular_valor_ecuacion
from services.calculations import simular_movimiento  # Nueva importación
from models import Tanque  # Para validar o usar si es necesario

router = APIRouter()

fuerzas_registradas: List[schemas.Fuerza] = []


@router.post("/fuerzas/agregar", response_model=Dict[str, Any], tags=["Fuerzas"])
def agregar_fuerza(fuerza: schemas.Fuerza):
    fuerzas_registradas.append(fuerza)
    return {"mensaje": "Fuerza agregada correctamente", "fuerza": fuerza}


@router.get("/fuerzas", response_model=List[schemas.Fuerza], tags=["Fuerzas"])
def listar_fuerzas():
    return fuerzas_registradas


@router.post("/calcular_parametros", response_model=schemas.SimulationOutput, tags=["Simulacion Fisica"])
def calcular_parametros_fisicos(simulation_input: schemas.SimulationInput):
    # Extrae el tanque y tiempo del input
    tanque_data = simulation_input.tanque
    tiempo = simulation_input.tiempo

    # Crea una instancia de Tanque desde los datos
    tanque = Tanque(
        nombre=tanque_data.nombre if hasattr(tanque_data, 'nombre') else "Tanque de Leonardo da Vinci",
        masa=tanque_data.masa,
        radio_rueda=tanque_data.radio_rueda,
        fuerza_motriz=tanque_data.fuerza_motriz,
        coeficiente_rozamiento=tanque_data.coeficiente_rozamiento,
        fuerzas=tanque_data.fuerzas
    )

    # Calcula los parámetros usando la función ajustada
    resultado = simular_movimiento(tanque, tiempo)

    # Retorna en formato SimulationOutput
    return schemas.SimulationOutput(**resultado)


@router.post("/clasificar_evaluar", response_model=Dict[str, Any], tags=["Calculo Vectorial"])
def clasificar_y_evaluar_superficie(
        ecuacion_data: schemas.EcuacionConica,
        puntos_evaluacion: List[schemas.PuntoEvaluacion]
):
    ecuacion_dict = ecuacion_data.model_dump()
    tipo_superficie = clasificar_superficie_conica(ecuacion_dict)

    resultados_evaluacion = []
    for punto in puntos_evaluacion:
        valor = calcular_valor_ecuacion(ecuacion_dict, punto.x, punto.y, punto.z)
        resultados_evaluacion.append({
            "punto": f"({punto.x}, {punto.y}, {punto.z})",
            "valor_en_ecuacion": valor,
            "esta_en_superficie": abs(valor) < 1e-6
        })

    return {
        "ecuacion_recibida": ecuacion_dict,
        "tipo_superficie": tipo_superficie,
        "evaluacion_puntos": resultados_evaluacion
    }