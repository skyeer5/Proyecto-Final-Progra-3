"""
Punto de entrada del proyecto Totito con aprendizaje supervisado.

Universidad Mariano Galvez - Programacion III

"""

import os
import sys

_DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
if _DIRECTORIO_ACTUAL not in sys.path:
    sys.path.insert(0, _DIRECTORIO_ACTUAL)


def main():
    """Inicializa y arranca la aplicacion grafica del Totito."""
    try:
        from interfaz.menu import AplicacionTotito
    except ImportError as error:
        print("ERROR: No se pudieron importar los modulos del proyecto.")
        print(f"Detalle: {error}")
        print("\nAsegurese de ejecutar el programa desde el directorio raiz")
        print("del proyecto y de tener Python 3.8 o superior instalado.")
        sys.exit(1)

    try:
        aplicacion = AplicacionTotito()
        aplicacion.iniciar()
    except Exception as error:
        print(f"ERROR al iniciar la aplicacion: {error}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
