import pygame
import random
import json
import os
import math
from configuraciones import *

# Inicializamos Pygame
pygame.init()

# Creamos una ventana de 600x600 pixels
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Establecemos el título de la ventana
pygame.display.set_caption("Carita Sonriente Rompecabezas")

# Cargamos la fuente estilo videojuego pixeleado
font = pygame.font.Font(FONT_PATH, FONT_SIZE)

# Creamos un objeto Surface para dibujar la carita
face_surface = pygame.Surface((FACE_SIZE, FACE_SIZE))
face_surface.fill(YELLOW)  # Rellenamos la carita con el color amarillo

# Dibujamos los ojos centrados en la cara
pygame.draw.circle(face_surface, BLACK, (FACE_CENTER_X - EYE_OFFSET_X, EYE_Y), EYE_RADIUS)  # Ojo izquierdo
pygame.draw.circle(face_surface, BLACK, (FACE_CENTER_X + EYE_OFFSET_X, EYE_Y), EYE_RADIUS)  # Ojo derecho

# Función para dibujar la boca
def draw_mouth(surface, pixel_positions):
    for pos in pixel_positions:
        pygame.draw.rect(surface, BLACK, pygame.Rect(pos[0], pos[1], MOUTH_PIXEL_SIZE, MOUTH_PIXEL_SIZE))

# Dibujamos la boca inicial
draw_mouth(face_surface, MOUTH_PIXELS)

# Función para dibujar un borde ondulado para una pieza del rompecabezas
def draw_wavy_line(surface, start_pos, end_pos, amplitude, frequency, is_vertical):
    if is_vertical:
        for y in range(start_pos[1], end_pos[1]):
            x = start_pos[0] + amplitude * math.sin(2 * math.pi * frequency * (y - start_pos[1]) / (end_pos[1] - start_pos[1]))
            surface.set_at((int(x), y), BLACK)
    else:
        for x in range(start_pos[0], end_pos[0]):
            y = start_pos[1] + amplitude * math.sin(2 * math.pi * frequency * (x - start_pos[0]) / (end_pos[0] - start_pos[0]))
            surface.set_at((x, int(y)), BLACK)

# Función para crear piezas del rompecabezas
def create_pieces():
    pieces = []
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            piece_surface = pygame.Surface((PIECE_SIZE, PIECE_SIZE), pygame.SRCALPHA)
            face_part = face_surface.subsurface((j * PIECE_SIZE, i * PIECE_SIZE, PIECE_SIZE, PIECE_SIZE))
            piece_surface.blit(face_part, (0, 0))
            
            # Dibujar los bordes como en la imagen
            if i == 0:
                # Borde superior
                draw_wavy_line(piece_surface, (0, 0), (PIECE_SIZE, 0), AMPLITUDE, FREQUENCY, is_vertical=False)
            if i == GRID_SIZE - 1:
                # Borde inferior
                draw_wavy_line(piece_surface, (0, PIECE_SIZE - 1), (PIECE_SIZE, PIECE_SIZE - 1), AMPLITUDE, FREQUENCY, is_vertical=False)
            if j == 0:
                # Borde izquierdo
                draw_wavy_line(piece_surface, (0, 0), (0, PIECE_SIZE), AMPLITUDE, FREQUENCY, is_vertical=True)
            if j == GRID_SIZE - 1:
                # Borde derecho
                draw_wavy_line(piece_surface, (PIECE_SIZE - 1, 0), (PIECE_SIZE - 1, PIECE_SIZE), AMPLITUDE, FREQUENCY, is_vertical=True)
            
            # Agregar bordes externos a las piezas
            pygame.draw.rect(piece_surface, BLACK, (0, 0, PIECE_SIZE, PIECE_SIZE), 2)
            
            # Asignar posiciones aleatorias a las piezas
            piece_rect = piece_surface.get_rect()
            piece_rect.x = random.randint(0, SCREEN_WIDTH - PIECE_SIZE)
            piece_rect.y = random.randint(0, SCREEN_HEIGHT - PIECE_SIZE)
            pieces.append((piece_surface, piece_rect, (j * PIECE_SIZE, i * PIECE_SIZE)))  # Agregamos la posición correcta para cada pieza

    return pieces

# Función para guardar el estado del juego
def save_game_state(pieces):
    game_state = [{'x': piece[1].x, 'y': piece[1].y, 'correct_pos': piece[2]} for piece in pieces]
    with open('game_state.json', 'w') as f:
        json.dump(game_state, f)

# Función para cargar el estado del juego
def load_game_state():
    if os.path.exists('game_state.json'):
        with open('game_state.json', 'r') as f:
            game_state = json.load(f)
        pieces = []
        for piece_info in game_state:
            piece_surface = pygame.Surface((PIECE_SIZE, PIECE_SIZE), pygame.SRCALPHA)
            face_part = face_surface.subsurface((piece_info['correct_pos'][0], piece_info['correct_pos'][1], PIECE_SIZE, PIECE_SIZE))
            piece_surface.blit(face_part, (0, 0))
            pygame.draw.rect(piece_surface, BLACK, (0, 0, PIECE_SIZE, PIECE_SIZE), 2)
            piece_rect = piece_surface.get_rect()
            piece_rect.x = piece_info['x']
            piece_rect.y = piece_info['y']
            pieces.append((piece_surface, piece_rect, piece_info['correct_pos']))
        return pieces
    else:
        return None

# Creamos un fondo negro para indicar dónde colocar las piezas
background_surface = pygame.Surface((FACE_SIZE, FACE_SIZE))
background_surface.fill(BLACK)
background_rect = background_surface.get_rect()
background_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Variables para el arrastre de piezas
dragging = False
dragged_piece = None
offset_x = 0
offset_y = 0

# Estado inicial
in_menu = True
pieces = []

# Bucle principal del juego
running = True
while running:
    if in_menu:
        # Dibujamos el menú principal
        screen.fill(BACKGROUND_COLOR)
        font = pygame.font.Font(FONT_PATH, FONT_SIZE)
        new_game_text = font.render(MENU_NEW_GAME_TEXT, True, BLACK)
        continue_text = font.render(MENU_CONTINUE_TEXT, True, BLACK)
        new_game_rect = new_game_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(new_game_text, new_game_rect)
        screen.blit(continue_text, continue_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if new_game_rect.collidepoint(event.pos):
                    pieces = create_pieces()
                    in_menu = False
                elif continue_rect.collidepoint(event.pos):
                    loaded_pieces = load_game_state()
                    if loaded_pieces is not None:
                        pieces = loaded_pieces
                        in_menu = False
                    else:
                        font = pygame.font.Font(FONT_PATH, FONT_SIZE)
                        no_save_text = font.render("No se guardó nada", True, BLACK)
                        no_save_rect = no_save_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
                        screen.blit(no_save_text, no_save_rect)
                        pygame.display.flip()
                        pygame.time.wait(2000)
    else:
        # Procesamos los eventos de Pygame (como el cierre de la ventana)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game_state(pieces)
                os.remove('game_state.json')  # Eliminamos el estado guardado si se cierra el juego completamente
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for piece in pieces:
                    if piece[1].collidepoint(event.pos):
                        dragging = True
                        dragged_piece = piece
                        offset_x = piece[1].x - event.pos[0]
                        offset_y = piece[1].y - event.pos[1]
                        break
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
                if dragged_piece:
                    if background_rect.collidepoint(dragged_piece[1].center):
                        # Verifica si la pieza está cerca de su posición correcta
                        correct_x = background_rect.x + dragged_piece[2][0]
                        correct_y = background_rect.y + dragged_piece[2][1]
                        if abs(dragged_piece[1].x - correct_x) < 10 and abs(dragged_piece[1].y - correct_y) < 10:
                            dragged_piece[1].x = correct_x
                            dragged_piece[1].y = correct_y
                        else:
                            dragged_piece[1].x = random.randint(0, SCREEN_WIDTH - PIECE_SIZE)
                            dragged_piece[1].y = random.randint(0, SCREEN_HEIGHT - PIECE_SIZE)
                    else:
                        dragged_piece[1].x = random.randint(0, SCREEN_WIDTH - PIECE_SIZE)
                        dragged_piece[1].y = random.randint(0, SCREEN_HEIGHT - PIECE_SIZE)
                    dragged_piece = None
            elif event.type == pygame.MOUSEMOTION:
                if dragging and dragged_piece:
                    dragged_piece[1].x = event.pos[0] + offset_x
                    dragged_piece[1].y = event.pos[1] + offset_y
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    save_game_state(pieces)
                    in_menu = True

        # Dibujamos el fondo de la pantalla en celeste claro
        screen.fill(BACKGROUND_COLOR)

        # Dibujamos el fondo negro que indica dónde colocar las piezas
        screen.blit(background_surface, background_rect)

        # Dibujamos las piezas del rompecabezas
        for piece in pieces:
            screen.blit(piece[0], piece[1].topleft)

        # Verificamos si se ha completado el rompecabezas
        if all(background_rect.collidepoint(piece[1].center) and piece[1].x == background_rect.x + piece[2][0] and piece[1].y == background_rect.y + piece[2][1] for piece in pieces):
            font = pygame.font.Font(FONT_PATH, WIN_TEXT_SIZE)
            text = font.render(WIN_TEXT, True, BLACK)
            text_rect = text.get_rect()
            text_rect.center = WIN_TEXT_POSITION
            screen.blit(text, text_rect)

        # Añadimos la opción de regresar
        font = pygame.font.Font(FONT_PATH, FONT_SIZE)
        back_text = font.render(BACK_TEXT, True, BLACK)
        back_rect = back_text.get_rect(center=BACK_TEXT_POSITION)
        screen.blit(back_text, back_rect)

        # Verificamos si se ha hecho clic en la opción de regresar
        if event.type == pygame.MOUSEBUTTONDOWN and back_rect.collidepoint(event.pos):
            save_game_state(pieces)
            in_menu = True

        # Actualizamos la pantalla
        pygame.display.flip()

# Cerramos Pygame
pygame.quit()