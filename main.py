from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from rutas import simulation, team, project

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
plantillas = Jinja2Templates(directory="templates")

app.include_router(simulation.router, prefix="/simulation", tags=["Simulation", "Fuerzas"])
app.include_router(team.router, prefix="/team", tags=["Team"])
app.include_router(project.router, prefix="/project", tags=["Project"])

@app.get("/", response_class=HTMLResponse)
async def condatta(request: Request):
    return plantillas.TemplateResponse("condatta.html", {"request": request, "page": "condatta"})

@app.get("/calculo", response_class=HTMLResponse)
async def calculo(request: Request):
    return plantillas.TemplateResponse("calculo.html", {"request": request, "page": "calculo"})

@app.get("/fisica", response_class=HTMLResponse)
async def fisica(request: Request):
    return plantillas.TemplateResponse("fisica.html", {"request": request, "page": "fisica"})

@app.get("/readme", response_class=HTMLResponse)
async def readme(request: Request):
    return plantillas.TemplateResponse("readme.html", {"request": request, "page": "readme"})

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return plantillas.TemplateResponse("about.html", {"request": request, "page": "about"})

@app.post("/resultado", response_class=HTMLResponse)
async def resultado(request: Request, valor1: float = Form(...), valor2: float = Form(...)):
    try:
        resultado = valor1 + valor2
        datos = {"request": request, "valor1": valor1, "valor2": valor2, "resultado": resultado, "page": "calculo"}
        return plantillas.TemplateResponse("resultado.html", datos)
    except Exception as e:
        return plantillas.TemplateResponse("error.html", {"request": request, "mensaje": str(e), "page": "calculo"})