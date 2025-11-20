from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import schemas
from services.calculo_vectorial import clasificar_superficie_conica, calcular_valor_ecuacion

router = APIRouter()

# Variable local para almacenar fuerzas simuladamente
fuerzas_registradas: List[schemas.Fuerza] = []

@router.post("/fuerzas/agregar", response_model=Dict[str, Any], tags=["Fuerzas"])
def agregar_fuerza(fuerza: schemas.Fuerza):
    fuerzas_registradas.append(fuerza)
    return {"mensaje": "Fuerza agregada correctamente", "fuerza": fuerza}

@router.get("/fuerzas", response_model=List[schemas.Fuerza], tags=["Fuerzas"])
def listar_fuerzas():
    return fuerzas_registradas

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