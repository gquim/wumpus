import pygame
from board import Board
from player import Player
from timer import Timer
from scores import save_score

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Mundo de Wumpus")
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

# Inicializar tablero
board = Board(10, 12)
player = Player()
timer = Timer()

vidas = 2
timer.start()

def draw_board():
    screen.fill((0, 0, 0))
    cell_width = 800 // board.cols
    cell_height = 600 // board.rows
    
    for y in range(board.rows):
        for x in range(board.cols):
            rect = pygame.Rect(x * cell_width, y * cell_height, cell_width, cell_height)
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)
            if (x, y) == player.position:
                pygame.draw.circle(screen, (0, 255, 0), rect.center, cell_width // 4)
    
    vidas_text = font.render(f"Vidas: {vidas}", True, (255, 255, 255))
    screen.blit(vidas_text, (10, 10))
    tiempo_text = font.render(f"Tiempo: {timer.elapsed():.2f} s", True, (255, 255, 255))
    screen.blit(tiempo_text, (10, 50))
    pygame.display.flip()

running = True
while running and not player.has_gold and vidas > 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.move("N")
            elif event.key == pygame.K_DOWN:
                player.move("S")
            elif event.key == pygame.K_LEFT:
                player.move("O")
            elif event.key == pygame.K_RIGHT:
                player.move("E")
    
    percepts = board.get_percepts(player.position)
    player.update(percepts)
    
    if board.is_wumpus(player.position) or board.is_pit(player.position):
        if vidas > 1:
            print("¡Perdiste una vida! Regresando a posición segura...")
            vidas -= 1
            player.reset()
        else:
            print("¡Juego terminado!")
            running = False
    
    if board.has_gold(player.position):
        print("¡Has encontrado el oro!")
        player.has_gold = True
        running = False

    draw_board()
    clock.tick(30)

# Finalizar juego
timer.stop()
if player.has_gold:
    tiempo_total = timer.elapsed()
    print(f"Tiempo final: {tiempo_total} segundos")
    nombre = input("Ingresa tu nombre: ")
    save_score(nombre, tiempo_total)
else:
    print("No lograste encontrar el oro.")

pygame.quit()