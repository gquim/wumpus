import pygame
import random
from board import Board
from player import Player
from timer import Timer
from scores import save_score


pygame.init()
screen = pygame.display.set_mode((950, 650))  
pygame.display.set_caption("Mundo de Wumpus")
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

# imagenes
player_img = pygame.image.load("player.png")
wumpus_img = pygame.image.load("wumpus.png")
pit_img = pygame.image.load("pit.png")
gold_img = pygame.image.load("gold.png")
hedor_img = pygame.image.load("hedor.png")
brisa_img = pygame.image.load("brisa.png")
discovered_img = pygame.image.load("discovered.png")

board = Board(12, 16)
player = Player()
timer = Timer()

vidas = 2
oro_total = random.randint(3, 5)  
oro_recogido = 0
timer.start()
discovered_cells = set()
visible_gold = set()
wumpus_alive = True
wumpus_position = None

for _ in range(oro_total):
    while True:
        x, y = random.randint(0, 15), random.randint(0, 11)
        if board.grid[y][x] == " ":  
            board.grid[y][x] = "O"
            break
#wumpus
for y in range(board.rows):
    for x in range(board.cols):
        if board.is_wumpus((x, y)):
            wumpus_position = (x, y)


def get_adjacent_cells(x, y):
    adjacent = []
    if x > 0:
        adjacent.append((x-1, y))
    if x < board.cols - 1:
        adjacent.append((x+1, y))
    if y > 0:
        adjacent.append((x, y-1))
    if y < board.rows - 1:
        adjacent.append((x, y+1))
    return adjacent

for y in range(board.rows):
    for x in range(board.cols):
        if board.is_wumpus((x, y)):
            for adj in get_adjacent_cells(x, y):
                board.grid[adj[1]][adj[0]] += "H"
        if board.is_pit((x, y)):
            for adj in get_adjacent_cells(x, y):
                board.grid[adj[1]][adj[0]] += "B"

def draw_board():
    screen.fill((0, 0, 0))
    cell_width = 800 // board.cols
    cell_height = 600 // board.rows
    
    for y in range(board.rows):
        for x in range(board.cols):
            rect = pygame.Rect(x * cell_width, y * cell_height, cell_width, cell_height)
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)
            if (x, y) in discovered_cells or (x, y) == player.position:
                screen.blit(discovered_img, rect.topleft)
                percepts = board.get_percepts((x, y))
                if "H" in board.grid[y][x] and wumpus_alive:
                    screen.blit(hedor_img, rect.topleft)
                if "B" in board.grid[y][x]:
                    screen.blit(brisa_img, rect.topleft)
                if (x, y) == player.position:
                    screen.blit(player_img, rect.topleft)
                if (x, y) in visible_gold or board.has_gold((x, y)):
                    screen.blit(gold_img, rect.topleft)
                elif board.is_wumpus((x, y)) and wumpus_alive:
                    screen.blit(wumpus_img, rect.topleft)
                elif board.is_pit((x, y)):
                    screen.blit(pit_img, rect.topleft)
    
    # informacion del juego
    info_x = 820
    vidas_text = font.render(f"vidas: {vidas}", True, (255, 255, 255))
    screen.blit(vidas_text, (info_x, 50))
    tiempo_text = font.render(f"tiempo: {timer.elapsed():.2f} s", True, (255, 255, 255))
    screen.blit(tiempo_text, (info_x, 100))
    oro_text = font.render(f"oro: {oro_recogido}/{oro_total}", True, (255, 255, 255))
    screen.blit(oro_text, (info_x, 150))
    
    pygame.display.flip()

running = True
while running and oro_recogido < oro_total and vidas > 0:
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
            elif event.key == pygame.K_RETURN and board.has_gold(player.position):
                player.collect_gold()
                visible_gold.discard(player.position)
                oro_recogido += 1  # Actualizar contador de oro
                print("encontraste oro")
            elif event.key == pygame.K_SPACE and wumpus_alive:
                print("disparo")
                if "H" in board.grid[player.position[1]][player.position[0]]:
                    wumpus_alive = False
                    print("Wumpus muerto")
                    if wumpus_position:
                        board.grid[wumpus_position[1]][wumpus_position[0]] = " "

    percepts = board.get_percepts(player.position)
    player.update(percepts)
    discovered_cells.add(player.position)
    if board.has_gold(player.position):
        visible_gold.add(player.position)
    
    if board.is_wumpus(player.position) and wumpus_alive or board.is_pit(player.position):
        if vidas > 1:
            vidas -= 1
            player.reset()
            discovered_cells.add(player.position)
        else:
            running = False

    draw_board()
    clock.tick(30)


timer.stop()
if oro_recogido == oro_total:
    tiempo_total = timer.elapsed()
    print(f"Tiempo: {tiempo_total}")
    nombre = input("Ingresa tu nombre: ")
    save_score(nombre, tiempo_total)
else:
    print("Perdiste")

pygame.quit()
