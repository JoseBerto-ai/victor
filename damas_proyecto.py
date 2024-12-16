#Proyecto de Juego de Damas de Inteligencia Artificial sobre agente basado en conocimiento
#Creado por Victor Rojas, V-30.891.822. 
#Ingeniería en Informática en la UNEG 

import pygame 
import sys

# Inicializar pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 4, 4
SQUARE_SIZE = WIDTH // COLS

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Crear ventana
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Damas 4x4")

# Fuente para mostrar texto
FONT = pygame.font.SysFont('arial', 32)
FONT_SMALL = pygame.font.SysFont('arial', 24)

# Tablero inicial
def create_initial_board():
    return [
        ['AI', None, 'AI', None],
        [None, None, None, None],
        [None, None, None, None],
        [None, 'H', None, 'H']
    ]

# Contador de movimientos
move_count = 0

def draw_board(win):

    for row in range(ROWS):
        for col in range(COLS):
            color = BLACK if (row + col) % 2 == 0 else WHITE
            pygame.draw.rect(win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Dibujar fichas
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == 'H':
                pygame.draw.circle(win, RED, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 3)
            elif board[row][col] == 'AI':
                pygame.draw.circle(win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 3)
            elif board[row][col] == 'HR':  # Reina del jugador humano
                pygame.draw.circle(win, RED, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 3)
                pygame.draw.circle(win, WHITE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 6)
            elif board[row][col] == 'AIR':  # Reina de la IA
                pygame.draw.circle(win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 3)
                pygame.draw.circle(win, WHITE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 6)

def get_square_under_mouse():
    # Obtener la celda sobre la que está el mouse
    x, y = pygame.mouse.get_pos()
    row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
    return row, col

def get_possible_moves(player):
    # Obtener movimientos posibles para el jugador
    directions = []
    if player == 'H':
        directions = [(-1, -1), (-1, 1)]
    elif player == 'AI':
        directions = [(1, -1), (1, 1)]
    elif player in ['HR', 'AIR']:  # Reinas pueden moverse en todas las direcciones
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    normal_moves = []
    jump_moves = []

    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == player:
                for dr, dc in directions:
                    new_row, new_col = row + dr, col + dc
                    if 0 <= new_row < ROWS and 0 <= new_col < COLS and board[new_row][new_col] is None:
                        normal_moves.append(((row, col), (new_row, new_col)))

                    # Verificar saltos
                    jump_row, jump_col = new_row + dr, new_col + dc
                    if (
                        0 <= jump_row < ROWS and 0 <= jump_col < COLS
                        and board[new_row][new_col] not in (None, player)
                        and board[jump_row][jump_col] is None
                    ):
                        jump_moves.append(((row, col), (jump_row, jump_col)))

    return jump_moves if jump_moves else normal_moves

def make_move(move, player):
    global move_count
    # Realizar un movimiento
    start, end = move
    start_row, start_col = start
    end_row, end_col = end

    board[start_row][start_col] = None
    board[end_row][end_col] = player

    # Eliminar pieza capturada
    if abs(start_row - end_row) == 2:
        mid_row, mid_col = (start_row + end_row) // 2, (start_col + end_col) // 2
        board[mid_row][mid_col] = None

    # Coronar si alcanza el otro extremo
    if player == 'H' and end_row == 0:
        board[end_row][end_col] = 'HR'
    elif player == 'AI' and end_row == ROWS - 1:
        # Convertir la pieza de IA en reina permanentemente
        if board[end_row][end_col] != 'AIR':
            board[end_row][end_col] = 'AIR'

def ai_move():
    # Movimiento simple de IA: seleccionar el primer movimiento disponible
    moves = get_possible_moves('AIR') if any('AIR' in row for row in board) else get_possible_moves('AI')
    if moves:
        make_move(moves[0], 'AIR' if 'AIR' in moves[0][0] else 'AI')

def check_game_over():
    # Verificar si los jugadores tienen piezas
    human_pieces = sum(row.count('H') + row.count('HR') for row in board)
    ai_pieces = sum(row.count('AI') + row.count('AIR') for row in board)

    # Verificar si algún jugador ha perdido todas sus piezas
    if human_pieces == 0:
        return "IA\n(el humano no tiene piezas)"
    elif ai_pieces == 0:
        return "Humano\n(la IA no tiene piezas)"
    
    # Verificar si hay movimientos posibles para ambos jugadores
    human_moves = get_possible_moves('H') or get_possible_moves('HR')
    ai_moves = get_possible_moves('AI') or get_possible_moves('AIR')
    
    # Si el humano no puede mover sus piezas ni comer, se considera pérdida
    if not human_moves:
        return "IA\n(el humano no puede hacer más movimientos)"
    
    # Si la IA no puede mover sus piezas ni comer, se considera pérdida
    if not ai_moves:
        return "Humano\n(la IA no puede hacer más movimientos)"
    
    # Si hay movimientos disponibles, el juego continúa
    return None

def display_winner(win, winner):
    # Mostrar el ganador en la interfaz con formato adaptado para saltos de línea
    lines = f"Ganador: {winner}".split("\n")
    win.fill(BLACK)

    for i, line in enumerate(lines):
        text = FONT.render(line, True, RED if "Humano" in line else (BLUE if "IA" in line else GREEN))
        win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 + i * 40))
    
    pygame.display.flip()

    # Esperar a que el jugador presione Enter para volver al menú
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting_for_input = False
                    return  # Regresar al menú principal

def draw_move_counter(win, move_count):
    text = FONT_SMALL.render(f"Movimientos: {move_count}", True, (255, 255, 0))  # Amarillo
    win.blit(text, (10, 10))

# Modificar la función main para manejar el límite de movimientos
def main(player_starts):
    global move_count, board
    board = create_initial_board()
    move_count = 0  # Reiniciar el contador de movimientos
    clock = pygame.time.Clock()
    running = True
    selected_piece = None
    player_turn = 'H' if player_starts else 'AI'

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and player_turn == 'H':
                row, col = get_square_under_mouse()
                possible_moves = get_possible_moves('HR') + get_possible_moves('H')

                if selected_piece:
                    move = (selected_piece, (row, col))
                    if move in possible_moves:
                        make_move(move, 'HR' if board[selected_piece[0]][selected_piece[1]] == 'HR' else 'H')
                        selected_piece = None
                        player_turn = 'AI'
                        move_count += 1  # Incrementar el contador de movimientos del jugador
                    else:
                        selected_piece = None
                elif board[row][col] in ['H', 'HR']:
                    selected_piece = (row, col)

        if player_turn == 'AI':
            ai_move()
            player_turn = 'H'
            move_count += 1  # Incrementar el contador de movimientos de la IA

        # Verificar si el juego terminó
        winner = check_game_over()
        if winner:
            display_winner(WIN, winner)
            return  # Regresar al menú principal

        # Verificar si se llegó al límite de movimientos (empate)
        if move_count >= 64:
            display_winner(WIN, "Empate (se alcanzó el límite de movimientos)")
            return  # Regresar al menú principal

        # Dibujar el tablero y el contador de movimientos
        draw_board(WIN)
        draw_move_counter(WIN, move_count)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

def menu():
    while True:
        WIN.fill(BLACK)

        # Títulos y opciones
        title_text = FONT.render("Damas Minimax 4x4", True, WHITE)
        play_text_lines = [
            "'1' Jugar (Humano vs IA)",
            "'2' Salir"
        ]

        WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))
        for i, line in enumerate(play_text_lines):
            rendered_line = FONT.render(line, True, WHITE)
            WIN.blit(rendered_line, (WIDTH // 2 - rendered_line.get_width() // 2, 150 + i * 50))  # Ajuste de espacio entre líneas

        pygame.display.flip()

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    # Elegir si el humano comienza la partida
                    WIN.fill(BLACK)
                    start_text_lines = [
                        "'1' Si el humano comienza",
                        "",
                        "",
                        "'2' Si la IA comienza"
                    ]
                    for i, line in enumerate(start_text_lines):
                        rendered_line = FONT.render(line, True, WHITE)
                        WIN.blit(rendered_line, (WIDTH // 2 - rendered_line.get_width() // 2, HEIGHT // 2 - (len(start_text_lines) // 2 - i) * 30))
                    pygame.display.flip()
                    waiting_for_input = True
                    while waiting_for_input:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_1:
                                    waiting_for_input = False
                                    main(True)
                                elif event.key == pygame.K_2:
                                    waiting_for_input = False
                                    main(False)
                elif event.key == pygame.K_2:
                    pygame.quit()
                    sys.exit()

menu()