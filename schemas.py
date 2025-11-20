from pydantic import BaseModel, Field
from typing import List, Optional

class Fuerza(BaseModel):
    tipo: str
    magnitud: float
    direccion: str

class TanqueConFuerzas(BaseModel):
    masa: float
    radio_rueda: float
    fuerza_motriz: float
    coeficiente_rozamiento: float
    fuerzas: Optional[List[Fuerza]] = []

class EcuacionConica(BaseModel):
    A: float = Field(0.0, description="Coeficiente de x^2")
    B: float = Field(0.0, description="Coeficiente de y^2")
    C: float = Field(0.0, description="Coeficiente de z^2")
    D: float = Field(0.0, description="Coeficiente de x*y")
    E: float = Field(0.0, description="Coeficiente de x*z")
    F: float = Field(0.0, description="Coeficiente de y*z")
    G: float = Field(0.0, description="Coeficiente de x")
    H: float = Field(0.0, description="Coeficiente de y")
    I: float = Field(0.0, description="Coeficiente de z")
    J: float = Field(0.0, description="Término constante")

class PuntoEvaluacion(BaseModel):
    x: float
    y: float
    z: float