from fastapi import APIRouter, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from typing import Dict, Any, List, Tuple
import os
import csv


# Tu código integrado
def clasificar_superficie_conica(ecuacion: Dict[str, float]) -> str:
    A = ecuacion.get('A', 0)
    B = ecuacion.get('B', 0)
    C = ecuacion.get('C', 0)
    D = ecuacion.get('D', 0)
    E = ecuacion.get('E', 0)
    F = ecuacion.get('F', 0)

    coeficientes_cuadrados = [A, B, C]
    ceros = coeficientes_cuadrados.count(0)

    if D != 0 or E != 0 or F != 0:
        return "Clasificación compleja (con términos mixtos)"

    if ceros == 0:
        if (A > 0 and B > 0 and C > 0) or (A < 0 and B < 0 and C < 0):
            return "Elipsoide"
        if A * B * C < 0 and ceros == 0:
            return "Hiperboloide de una o dos hojas"

    if ceros == 1:
        return "Paraboloide (Elíptico o Hiperbólico)"

    if ceros == 2:
        return "Cilindro o Par de planos"

    return "No clasificable o Plano"


def calcular_valor_ecuacion(ecuacion: Dict[str, float], x: float, y: float, z: float) -> float:
    A, B, C, D, E, F, G, H, I, J = (
        ecuacion.get(c, 0) for c in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    )

    valor = (
            A * x ** 2 + B * y ** 2 + C * z ** 2 +
            D * x * y + E * x * z + F * y * z +
            G * x + H * y + I * z + J
    )
    return valor


# Función para guardar en CSV
def guardar_registro_calculo(ecuacion: Dict[str, float], tipo: str, punto: str, valor: float, en_superficie: bool):
    archivo = 'calculo_registros.csv'
    existe = os.path.exists(archivo)
    with open(archivo, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not existe:
            writer.writerow(['Ecuacion', 'Tipo_Superficie', 'Punto', 'Valor', 'En_Superficie'])
        writer.writerow([str(ecuacion), tipo, punto, valor, en_superficie])


# Función para leer registros del CSV
def leer_registros_calculo():
    archivo = 'calculo_registros.csv'
    if not os.path.exists(archivo):
        return []
    with open(archivo, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)


# Función para editar registro (por índice)
def editar_registro_calculo(indice: int, nuevos_datos: Dict[str, Any]):
    archivo = 'calculo_registros.csv'
    if not os.path.exists(archivo):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    registros = leer_registros_calculo()
    if indice < 0 or indice >= len(registros):
        raise HTTPException(status_code=400, detail="Índice inválido")

    # Recalcular con nuevos datos
    ecuacion = nuevos_datos['ecuacion']
    punto = nuevos_datos['punto']
    tipo = clasificar_superficie_conica(ecuacion)
    valor = calcular_valor_ecuacion(ecuacion, punto['x'], punto['y'], punto['z'])
    en_superficie = abs(valor) < 1e-6

    registros[indice] = {
        'Ecuacion': str(ecuacion),
        'Tipo_Superficie': tipo,
        'Punto': f"({punto['x']}, {punto['y']}, {punto['z']})",
        'Valor': valor,
        'En_Superficie': en_superficie
    }

    # Reescribir CSV
    with open(archivo, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Ecuacion', 'Tipo_Superficie', 'Punto', 'Valor', 'En_Superficie'])
        writer.writeheader()
        writer.writerows(registros)


# Función para eliminar registro (por índice)
def eliminar_registro_calculo(indice: int):
    archivo = 'calculo_registros.csv'
    if not os.path.exists(archivo):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    registros = leer_registros_calculo()
    if indice < 0 or indice >= len(registros):
        raise HTTPException(status_code=400, detail="Índice inválido")

    del registros[indice]

    # Reescribir CSV
    with open(archivo, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Ecuacion', 'Tipo_Superficie', 'Punto', 'Valor', 'En_Superficie'])
        writer.writeheader()
        writer.writerows(registros)


# Código de tu amigo integrado
router = APIRouter()

templates_engine = Jinja2Templates(directory=os.path.join("templates"))


@router.post("/clasificar_evaluar", response_model=Dict[str, Any], tags=["Calculo Vectorial"])
def clasificar_y_evaluar_superficie(
        ecuacion_data: Dict[str, float],
        puntos_evaluacion: List[Dict[str, float]]
):
    ecuacion_dict = ecuacion_data

    tipo_superficie = clasificar_superficie_conica(ecuacion_dict)

    resultados_evaluacion = []
    for punto in puntos_evaluacion:
        valor = calcular_valor_ecuacion(ecuacion_dict, punto['x'], punto['y'], punto['z'])
        resultados_evaluacion.append({
            "punto": f"({punto['x']}, {punto['y']}, {punto['z']})",
            "valor_en_ecuacion": valor,
            "esta_en_superficie": abs(valor) < 1e-6
        })

    return {
        "ecuacion_recibida": ecuacion_dict,
        "tipo_superficie": tipo_superficie,
        "evaluacion_puntos": resultados_evaluacion
    }


# Nuevo endpoint para resultado emergente (JSON)
@router.post("/clasificar_evaluar_json", response_class=JSONResponse, tags=["Calculo Vectorial"])
async def clasificar_y_evaluar_json(
        A: float = Form(0.0), B: float = Form(0.0), C: float = Form(0.0),
        D: float = Form(0.0), E: float = Form(0.0), F: float = Form(0.0),
        G: float = Form(0.0), H: float = Form(0.0), I: float = Form(0.0),
        J: float = Form(0.0),
        punto_x: float = Form(0.0), punto_y: float = Form(0.0), punto_z: float = Form(0.0)
):
    ecuacion_data = {
        "A": A, "B": B, "C": C, "D": D, "E": E, "F": F,
        "G": G, "H": H, "I": I, "J": J
    }

    puntos_evaluacion = [{"x": punto_x, "y": punto_y, "z": punto_z}]

    try:
        resultados = clasificar_y_evaluar_superficie(ecuacion_data, puntos_evaluacion)
        # Guardar registro
        evaluacion = resultados['evaluacion_puntos'][0]
        guardar_registro_calculo(
            resultados['ecuacion_recibida'],
            resultados['tipo_superficie'],
            evaluacion['punto'],
            evaluacion['valor_en_ecuacion'],
            evaluacion['esta_en_superficie']
        )
        return resultados
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Nuevo endpoint para editar registro
@router.post("/editar_registro", response_class=JSONResponse, tags=["Calculo Vectorial"])
async def editar_registro(
        indice: int = Form(...),
        A: float = Form(0.0), B: float = Form(0.0), C: float = Form(0.0),
        D: float = Form(0.0), E: float = Form(0.0), F: float = Form(0.0),
        G: float = Form(0.0), H: float = Form(0.0), I: float = Form(0.0),
        J: float = Form(0.0),
        punto_x: float = Form(0.0), punto_y: float = Form(0.0), punto_z: float = Form(0.0)
):
    nuevos_datos = {
        'ecuacion': {
            "A": A, "B": B, "C": C, "D": D, "E": E, "F": F,
            "G": G, "H": H, "I": I, "J": J
        },
        'punto': {"x": punto_x, "y": punto_y, "z": punto_z}
    }
    try:
        editar_registro_calculo(indice, nuevos_datos)
        return {"message": "Registro editado y recalculado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Nuevo endpoint para eliminar registro
@router.post("/eliminar_registro", response_class=JSONResponse, tags=["Calculo Vectorial"])
async def eliminar_registro(indice: int = Form(...)):
    try:
        eliminar_registro_calculo(indice)
        return {"message": "Registro eliminado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/leer_registros_calculo", response_class=JSONResponse, tags=["Calculo Vectorial"])
async def leer_registros_calculo_endpoint():
        """Endpoint para leer registros del CSV y devolverlos como JSON"""
        registros = leer_registros_calculo()
        return registros


@router.get("/calculo_vectorial", response_class=HTMLResponse, tags=["Vistas"])
async def get_calculo_vectorial_form(request: Request):
    registros = leer_registros_calculo()
    return templates_engine.TemplateResponse("calculo.html", {"request": request, "registros": registros})


@router.post("/resultado_calculo", response_class=HTMLResponse, tags=["Vistas"])
async def post_calculo_vectorial(
        request: Request,
        A: float = Form(0.0), B: float = Form(0.0), C: float = Form(0.0),
        D: float = Form(0.0), E: float = Form(0.0), F: float = Form(0.0),
        G: float = Form(0.0), H: float = Form(0.0), I: float = Form(0.0),
        J: float = Form(0.0),
        punto_x: float = Form(0.0), punto_y: float = Form(0.0), punto_z: float = Form(0.0)
):
    ecuacion_data = {
        "A": A, "B": B, "C": C, "D": D, "E": E, "F": F,
        "G": G, "H": H, "I": I, "J": J
    }

    punto_data = {"x": punto_x, "y": punto_y, "z": punto_z}
    puntos_evaluacion = [punto_data]

    try:
        resultados = clasificar_y_evaluar_superficie(ecuacion_data, puntos_evaluacion)
        return templates_engine.TemplateResponse("resultado.html", {"request": request, "resultados": resultados})
    except Exception as e:
        return templates_engine.TemplateResponse("error.html", {"request": request, "error_message": str(e)},
                                                 status_code=500)