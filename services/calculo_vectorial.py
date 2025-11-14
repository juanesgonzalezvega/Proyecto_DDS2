from typing import Tuple, Dict


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