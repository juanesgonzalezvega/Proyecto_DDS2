from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

try:
    from rutas import simulation, team, project
except ImportError:
    raise

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
plantillas = Jinja2Templates(directory="templates")

app.include_router(simulation.router, prefix="/simulation", tags=["Simulation"])
app.include_router(team.router, prefix="/team", tags=["Team"])
app.include_router(project.router, prefix="/project", tags=["Project"])

@app.get("/", response_class=HTMLResponse)
async def inicio(request: Request):
    return plantillas.TemplateResponse("index.html", {"request": request})

@app.get("/calculo", response_class=HTMLResponse)
async def calculo(request: Request):
    return plantillas.TemplateResponse("calculo.html", {"request": request})

@app.post("/resultado", response_class=HTMLResponse)
async def resultado(request: Request, valor1: float = Form(...), valor2: float = Form(...)):
    try:
        resultado = valor1 + valor2
        datos = {"request": request, "valor1": valor1, "valor2": valor2, "resultado": resultado}
        return plantillas.TemplateResponse("resultado.html", datos)
    except Exception as e:
        return plantillas.TemplateResponse("error.html", {"request": request, "mensaje": str(e)})