# Proyecto-Final-Progra-3
Proyecto final de programacion 3 que tiene como objetivo el realizar un juego de tik tak toe, el cual incorporará un componente de aprendizaje supervisado para mejorar la estrategia del juego a medida que se juegan más partidas.

## Integrantes

-  Angela Paola García Azañón      Carnet 9490-24-11686  100%
-  Robinson Daniel Dávila Alba     Carnet 9490-24-3939   100%
-  Ingrid Elena Damián Chial       Carnet 9490-24-4375   100%
-  José Daniel Pineda Vicente      Carnet 9490-24-4996   100%

## Requisitos

- **Python 3.8 o superior**
- **Tkinter**
- **Graphviz**

### Instalar Graphviz

**Binario del sistema** (para renderizar los .png):

## Ejecucion

Desde la carpeta raiz del proyecto:

```
python3 main.py
```

Al iniciar, el programa construye el arbol de estados del juego 
y muestra el menu principal. Esta operacion toma unos  pocos segundos 
la primera vez.

## Estructura del proyecto

```
totito/
├── main.py                       # Punto de entrada
├── estructuras/                  # Estructuras de datos propias
│   ├── lista_enlazada.py         # Lista doblemente enlazada
│   ├── cola.py                   # Cola FIFO
│   ├── mapa_hash.py              # Mapa hash con encadenamiento
│   ├── tablero.py                # Tablero 3x3
│   ├── arbol_estados.py          # Arbol/DAG de estados del juego
│   └── arbol_b.py                # Arbol B 
├── juego/
│   ├── logica.py                 # Logica de partida
│   └── aprendizaje.py            # Algoritmo de aprendizaje supervisado
├── interfaz/
│   ├── menu.py                   # Menu principal 
│   ├── ventana_juego.py          # Ventana de juego manual
│   └── ventana_historial.py      # Visor del historial
├── visualizacion/
│   └── grafico.py                # Generador de visualizaciones Graphviz
└── visualizaciones/              # PNGs y archivos .dot generados
```

## Opciones del menu

1. **Entrenamiento manual**: el usuario juega como `X` contra el sistema
   (`O`). Al finalizar, los pesos se ajustan y se genera la visualizacion
   Graphviz de la partida.
2. **Entrenamiento automatico**: simula N partidas contra
   oponente aleatorio. Cada partida genera su visualizacion individual y
   se reporta el aprendizaje.
3. **Ver historial**: muestra todas las partidas almacenadas en el arbol
   B, con su identificador, resumen y tablero representativo.
4. **Iteraciones para victoria**: indica en que partida el sistema logro
   su primera victoria.
5. **Visualizar arbol B**: genera un PNG con la estructura completa del
   arbol B del historial.
6. **Limpiar estructura**: reinicia el aprendizaje y permite reconfigurar
   el grado del arbol B.

## Visualizaciones

Cada partida genera dos archivos en `visualizaciones/`:

- `partida_XXXX.dot` (fuente Graphviz)
- `partida_XXXX.png` (imagen renderizada)

La visualizacion muestra la secuencia de tableros de la partida, las
posiciones jugadas, y los pesos **antes y despues** del ajuste para cada
movimiento del sistema, evidenciando el aprendizaje.

## Notas sobre la implementacion

- No se utilizan listas, diccionarios, tuplas ni conjuntos nativos de
  Python para almacenar la informacion del juego; toda la informacion se
  guarda en estructuras de datos propias.
- El arbol de estados se construye una sola vez al inicio mediante BFS,
  produciendo un DAG con 5478 estados unicos (resultado matematicamente
  correcto para Tic-Tac-Toe).
- El aprendizaje usa explotacion (mejor peso) en el entrenamiento manual
  y exploracion (ruleta ponderada) en el automatico, para evitar que el
  sistema se estanque en una sola estrategia durante el entrenamiento.
