from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import csv
import os
from typing import Dict, Any

from rutas import simulation, team, project
from rutas.simulation import leer_registros_calculo

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
plantillas = Jinja2Templates(directory="templates")

app.include_router(simulation.router, prefix="/simulation", tags=["Simulation", "Fuerzas"])
app.include_router(team.router, prefix="/team", tags=["Team"])
app.include_router(project.router, prefix="/project", tags=["Project"])

# Función para guardar en CSV física
def guardar_registro_fisica(tipo_calculo: str, valores: str, resultado: str):
    archivo = 'fisica_registros.csv'
    existe = os.path.exists(archivo)
    with open(archivo, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not existe:
            writer.writerow(['Tipo_Calculo', 'Valores_Ingresados', 'Resultado'])
        writer.writerow([tipo_calculo, valores, resultado])

# Función para leer registros del CSV física
def leer_registros_fisica():
    archivo = 'fisica_registros.csv'
    if not os.path.exists(archivo):
        return []
    with open(archivo, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

# Función para editar registro física (por índice)
def editar_registro_fisica(indice: int, nuevos_datos: Dict[str, Any]):
    archivo = 'fisica_registros.csv'
    if not os.path.exists(archivo):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    registros = leer_registros_fisica()
    if indice < 0 or indice >= len(registros):
        raise HTTPException(status_code=400, detail="Índice inválido")

    # Recalcular (simplificado, ajusta según lógica de física)
    registros[indice] = nuevos_datos

    # Reescribir CSV
    with open(archivo, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Tipo_Calculo', 'Valores_Ingresados', 'Resultado'])
        writer.writeheader()
        writer.writerows(registros)

# Función para eliminar registro física (por índice)
def eliminar_registro_fisica(indice: int):
    archivo = 'fisica_registros.csv'
    if not os.path.exists(archivo):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    registros = leer_registros_fisica()
    if indice < 0 or indice >= len(registros):
        raise HTTPException(status_code=400, detail="Índice inválido")

    del registros[indice]

    # Reescribir CSV
    with open(archivo, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Tipo_Calculo', 'Valores_Ingresados', 'Resultado'])
        writer.writeheader()
        writer.writerows(registros)

@app.get("/", response_class=HTMLResponse)
async def condatta(request: Request):
    return plantillas.TemplateResponse("condatta.html", {"request": request, "page": "condatta"})

@app.get("/calculo", response_class=HTMLResponse)
async def calculo(request: Request):
    registros = leer_registros_calculo()
    return plantillas.TemplateResponse("calculo.html", {"request": request, "registros": registros, "page": "calculo"})

@app.get("/fisica", response_class=HTMLResponse)
async def fisica(request: Request):
    registros = leer_registros_fisica()
    return plantillas.TemplateResponse("fisica.html", {"request": request, "registros": registros, "page": "fisica"})

@app.get("/readme", response_class=HTMLResponse)
async def readme(request: Request):
    return plantillas.TemplateResponse("readme.html", {"request": request, "page": "readme"})

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return plantillas.TemplateResponse("about.html", {"request": request, "page": "about"})

# Endpoint para leer registros de física (para AJAX)
@app.get("/leer_registros_fisica", response_class=JSONResponse)
async def leer_registros_fisica_endpoint():
    registros = leer_registros_fisica()
    return registros

# Nuevo endpoint para guardar registros de física
@app.post("/guardar_fisica", response_class=JSONResponse)
async def guardar_fisica(tipo_calculo: str = Form(...), valores: str = Form(...), resultado: str = Form(...)):
    guardar_registro_fisica(tipo_calculo, valores, resultado)
    return {"message": "Registro guardado"}

# Nuevo endpoint para editar registro física
@app.post("/editar_registro_fisica", response_class=JSONResponse)
async def editar_registro_fisica_endpoint(indice: int = Form(...), tipo_calculo: str = Form(...), valores: str = Form(...), resultado: str = Form(...)):
    nuevos_datos = {'Tipo_Calculo': tipo_calculo, 'Valores_Ingresados': valores, 'Resultado': resultado}
    try:
        editar_registro_fisica(indice, nuevos_datos)
        return {"message": "Registro editado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Nuevo endpoint para eliminar registro física
@app.post("/eliminar_registro_fisica", response_class=JSONResponse)
async def eliminar_registro_fisica_endpoint(indice: int = Form(...)):
    try:
        eliminar_registro_fisica(indice)
        return {"message": "Registro eliminado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/resultado", response_class=HTMLResponse)
async def resultado(request: Request, valor1: float = Form(...), valor2: float = Form(...)):
    try:
        resultado = valor1 + valor2
        datos = {"request": request, "valor1": valor1, "valor2": valor2, "resultado": resultado, "page": "calculo"}
        return plantillas.TemplateResponse("resultado.html", datos)
    except Exception as e:
        return plantillas.TemplateResponse("error.html", {"request": request, "mensaje": str(e), "page": "calculo"})