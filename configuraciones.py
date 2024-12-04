# configuraciones.py

import math

# Dimensiones de la pantalla
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Colores
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
BACKGROUND_COLOR = (135, 206, 250)  # Celeste claro

# Fuente
FONT_PATH = "PressStart2P.ttf"  # Asegúrate de que la fuente esté en el mismo directorio que el script
FONT_SIZE = 24

# Dimensiones de la cara
FACE_SIZE = 300  # Tamaño de la carita: 300x300 pixels
FACE_CENTER_X = FACE_SIZE // 2
FACE_CENTER_Y = FACE_SIZE // 2

# Ojos
EYE_RADIUS = 20
EYE_OFFSET_X = 60
EYE_Y = FACE_CENTER_Y - 50  # Posición vertical de los ojos

# Boca
MOUTH_Y = FACE_CENTER_Y + 50  # Posición vertical de la boca
MOUTH_PIXEL_SIZE = 10
MOUTH_PIXELS = [
    (FACE_CENTER_X - 60, MOUTH_Y),
    (FACE_CENTER_X - 50, MOUTH_Y + 10),
    (FACE_CENTER_X - 40, MOUTH_Y + 20),
    (FACE_CENTER_X - 30, MOUTH_Y + 20),
    (FACE_CENTER_X - 20, MOUTH_Y + 20),
    (FACE_CENTER_X - 10, MOUTH_Y + 20),
    (FACE_CENTER_X, MOUTH_Y + 20),
    (FACE_CENTER_X + 10, MOUTH_Y + 20),
    (FACE_CENTER_X + 20, MOUTH_Y + 20),
    (FACE_CENTER_X + 30, MOUTH_Y + 20),
    (FACE_CENTER_X + 40, MOUTH_Y + 10),
    (FACE_CENTER_X + 50, MOUTH_Y)
]

# Rompecabezas
GRID_SIZE = 3
PIECE_SIZE = FACE_SIZE // GRID_SIZE

# Borde ondulado
AMPLITUDE = 10
FREQUENCY = 5

# Textos del menú
MENU_NEW_GAME_TEXT = "Juego Nuevo"
MENU_CONTINUE_TEXT = "Seguir en tu proceso"

# Texto de victoria
WIN_TEXT = "!win!"
WIN_TEXT_SIZE = 72
WIN_TEXT_POSITION = (SCREEN_WIDTH // 2, 50)

# Texto de regresar
BACK_TEXT = "Atras"
BACK_TEXT_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)