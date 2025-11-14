from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List

from ..schemas import EcuacionConica, PuntoEvaluacion
from ..services.calculo_vectorial import clasificar_superficie_conica, calcular_valor_ecuacion

router = APIRouter()


@router.post("/clasificar_evaluar", response_model=Dict[str, Any], tags=["Calculo Vectorial"])
def clasificar_y_evaluar_superficie(
        ecuacion_data: EcuacionConica,
        puntos_evaluacion: List[PuntoEvaluacion]
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
