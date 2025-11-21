##############################################################
###               S P A C E     E S C A P E                ###
##############################################################
###                  versao Alpha 0.3                      ###
##############################################################
### Objetivo: desviar dos meteoros que caem.               ###
### Cada colisão tira uma vida. Sobreviva o máximo que     ###
### conseguir!                                             ###
##############################################################
### Prof. Filipo Novo Mor - github.com/ProfessorFilipo     ###
##############################################################

import ast
from imaplib import Literal

import pygame
import random
import os


# Inicializa o PyGame
pygame.init()

# ----------------------------------------------------------
# 🔧 CONFIGURAÇÕES GERAIS DO JOGO
# ----------------------------------------------------------
WIDTH, HEIGHT = 800, 600
FPS = 60
pygame.display.set_caption("🚀 Space Escape")

# ----------------------------------------------------------
# 🧩 SEÇÃO DE ASSETS (os alunos podem trocar os arquivos aqui)
# ----------------------------------------------------------
# Dica: coloque as imagens e sons na mesma pasta do arquivo .py
# e troque apenas os nomes abaixo.

ASSETS = {
    "background": "background1.jpg",               # imagem de fundo
    "background2": "background2.png",              # imagem de fundo
    "background3": "background3.png",              # imagem de fundo
    "player": "ship1.png",                         # imagem da nave
    "player2": "ship2.png",                        # imagem da nave
    "meteor": "meteoro001.png",                    # imagem do meteoro
    "meteor2": "meteoro002.png",                   # imagem do meteoro especial
    "sound_point": "classic-game-action-positive-9-224399.mp3",         # som ao destruir meteoro. direitos: Music by floraphonic from Pixabay
    "sound_hit": "stab-f-01-brvhrtz-224599.mp3",                        # som de colisão
    "sound_hit_stage2": "large-underwater-explosion-190270.mp3",        # som de colisão
    "sound_hit_meteor2": "energy-2-90733.mp3",                          # som de colisão com meteoro especial. Music by freesound_community from Pixabay
    "music1": "chill-synthwave-211190.mp3",                             # música de fundo. direitos: Music by The_Mountain from Pixabay
    "music2": "moebius-21329.mp3",                                      # música de fundo. direitos: Music by Eidunn from Pixabay
    "music3": "synthwave-80s-retro-background-music-400483.mp3"         # música de fundo. direitos: Music by lNPLUSMUSIC from Pixabay

}

# ----------------------------------------------------------
# 🖼️ CARREGAMENTO DE IMAGENS E SONS
# ----------------------------------------------------------
# Cores para fallback (caso os arquivos não existam)
WHITE = (255, 255, 255)
RED = (255, 60, 60)
BLUE = (60, 100, 255)

# Tela do jogo
screen = pygame.display.set_mode((WIDTH, HEIGHT))


# Função auxiliar para carregar imagens de forma segura
def load_image(filename, fallback_color, size=None):
    if os.path.exists(filename):
        img = pygame.image.load(filename).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    else:
        # Gera uma superfície simples colorida se a imagem não existir
        surf = pygame.Surface(size or (50, 50))
        surf.fill(fallback_color)
        return surf

# Carrega imagens
background = load_image(ASSETS["background"], WHITE, (WIDTH, HEIGHT))
background2 = load_image(ASSETS["background2"], WHITE, (WIDTH, HEIGHT))
background3 = load_image(ASSETS["background3"], WHITE, (WIDTH, HEIGHT))
player_img = load_image(ASSETS["player"], BLUE, (50, 30))
player2_img = load_image(ASSETS["player2"], BLUE, (50, 30))
meteor_img = load_image(ASSETS["meteor"], RED, (30, 30))
meteor2_img = load_image(ASSETS["meteor2"], BLUE, (30, 30))

# Sons
def load_sound(filename):
    if os.path.exists(filename):
        return pygame.mixer.Sound(filename)
    return None

sound_point = load_sound(ASSETS["sound_point"])
sound_point.set_volume(0.3)
sound_hit = load_sound(ASSETS["sound_hit"])
sound_hit.set_volume(0.3)
sound_life = load_sound(ASSETS["sound_hit_meteor2"])
sound_life.set_volume(0.3)

# Música de fundo (opcional)
pygame.mixer.music.load(ASSETS["music1"])
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # loop infinito

# ----------------------------------------------------------
# 🧠 VARIÁVEIS DE JOGO
# ----------------------------------------------------------
player_rect = player_img.get_rect(center=(WIDTH // 2, HEIGHT - 60))
player_rect2 = player2_img.get_rect(center=(WIDTH // 2, HEIGHT - 60))
player_speed = 7

meteor_list = []
meteor2_list = []
meteor_list_speed = []
meteor2_list_speed = []
meteor_list_speed_stage2 = []
meteor_list_speed_stage3 = []

for _ in range(5):
    x = random.randint(0, WIDTH - 40)
    y = random.randint(-500, -40)
    meteor_list.append(pygame.Rect(x, y, 40, 40))
    meteor_list_speed.append(random.randint(1, 5))

for _ in range(5):
    x = random.randint(0, WIDTH - 40)
    y = random.randint(-500, -40)
    meteor_list_speed_stage2.append(random.randint(5, 8))

for _ in range(5):
    x = random.randint(0, WIDTH - 40)
    y = random.randint(-500, -40)
    meteor_list_speed_stage3.append(random.randint(8, 12))

for _ in range(1):
    x = random.randint(0, WIDTH - 40)
    y = random.randint(-500, -40)
    meteor2_list.append(pygame.Rect(x, y, 40, 40))
    meteor2_list_speed.append(random.randint(1, 3))

score = 0
lives = 3
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
running = True

# ----------------------------------------------------------
# LENDO SAVE DO JOGO
# ----------------------------------------------------------
high_scores = []

try:
    with open('main_save.txt', 'r') as arquivo:
        save = arquivo.read()
        high_scores = ast.literal_eval(save.split('=')[1].strip())

except FileNotFoundError:
    print("Não existe nenhum arquivo de save ainda.")

# ----------------------------------------------------------
# 🏁 TELA DE INICIO DE JOGO
# ----------------------------------------------------------
screen.fill((20, 20, 20))
end_text = font.render("Início DE JOGO! Pressione qualquer tecla para começar.", True, BLUE)
high_scores_text = font.render(f"High scores: ", True, WHITE)
high_scores_reversed = sorted(high_scores, reverse=True)

screen.blit(end_text, (70, 260))
screen.blit(high_scores_text, (300, 300))

for indice, item in enumerate(high_scores_reversed):
    high_scores_score_text = font.render(f"{item}", True, WHITE)
    screen.blit(high_scores_score_text, (450, 300 + (indice * 30)))
    if indice >= 4:
        break

pygame.display.flip()

waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            waiting = False
        if event.type == pygame.QUIT:
            pygame.quit()

# ----------------------------------------------------------
# 🕹️ LOOP PRINCIPAL
# ----------------------------------------------------------
stage2 = True
stage3 = True

BULLET_SPEED = 6
BULLET_HEIGHT = 10
BULLET_WIDTH = 4
bullets = []

while running:
    clock.tick(FPS)
    screen.blit(background, (0, 0))

    if 20 < score < 50:
        screen.blit(background2, (0, 0))

        if stage2:
            meteor_list_speed = meteor_list_speed_stage2
            sound_hit = load_sound(ASSETS["sound_hit_stage2"])
            pygame.mixer.music.load(ASSETS["music2"])
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
            stage2 = False

    if score > 50:
        screen.blit(background3, (0, 0))
        if stage3:
            meteor_list_speed = meteor_list_speed_stage3
            pygame.mixer.music.load(ASSETS["music3"])
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
            stage3 = False

    # --- Eventos ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = pygame.Rect(player_rect.x + player_rect.width // 2 - BULLET_WIDTH // 2,
                                     player_rect.y - BULLET_HEIGHT, BULLET_WIDTH, BULLET_HEIGHT)
                bullets.append(bullet)

        if pygame.mouse.get_pressed()[0]:
            bullet = pygame.Rect(player_rect2.x + player_rect2.width // 2 - BULLET_WIDTH // 2,
                                 player_rect2.y - BULLET_HEIGHT, BULLET_WIDTH, BULLET_HEIGHT)
            bullets.append(bullet)


    for bullet in bullets:
        bullet.y -= BULLET_SPEED

    bullets = [bullet for bullet in bullets if bullet.y > 0]

    # --- Movimento do jogador ---
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_rect.left > 0:
        player_rect.x -= player_speed
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_rect.right < WIDTH:
        player_rect.x += player_speed
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player_rect.bottom < HEIGHT:
        player_rect.y += player_speed
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and player_rect.top > 0:
        player_rect.y -= player_speed

    (posX, posY) = pygame.mouse.get_pos()
    if 0 <= posX <= WIDTH - player_rect2.width:
        player_rect2.x = posX

    if 0 <= posY <= HEIGHT - player_rect2.height:
        player_rect2.y = posY

    for index, meteor in enumerate(meteor2_list):
        meteor.y += meteor2_list_speed[index]

        # Saiu da tela → reposiciona e soma pontos
        if meteor.y > HEIGHT:
            meteor.y = random.randint(-100, -40)
            meteor.x = random.randint(0, WIDTH - meteor.width)

        if meteor.colliderect(player_rect):
            lives += 1
            meteor.y = random.randint(-100, -40)
            meteor.x = random.randint(0, WIDTH - meteor.width)
            if sound_life:
                sound_life.play()
            if lives <= 0:
                running = False

        if meteor.colliderect(player_rect2):
            lives += 1
            meteor.y = random.randint(-100, -40)
            meteor.x = random.randint(0, WIDTH - meteor.width)
            if sound_life:
                sound_life.play()
            if lives <= 0:
                running = False


    # --- Movimento dos meteoros ---
    for index, meteor in enumerate(meteor_list):
        meteor.y += meteor_list_speed[index]

        # Saiu da tela → reposiciona e soma pontos
        if meteor.y > HEIGHT:
            meteor.y = random.randint(-100, -40)
            meteor.x = random.randint(0, WIDTH - meteor.width)


        # Colisão
        if meteor.colliderect(player_rect):
            lives -= 1
            meteor.y = random.randint(-100, -40)
            meteor.x = random.randint(0, WIDTH - meteor.width)
            if sound_hit:
                sound_hit.play()
            if lives <= 0:
                running = False

        if meteor.colliderect(player_rect2):
            lives -= 1
            meteor.y = random.randint(-100, -40)
            meteor.x = random.randint(0, WIDTH - meteor.width)
            if sound_hit:
                sound_hit.play()
            if lives <= 0:
                running = False

        for bullet in bullets:
            if bullet.colliderect(meteor):
                bullets.remove(bullet)
                meteor.x = random.randint(0, WIDTH - meteor.width)
                meteor.y = 0
                score += 1
                if sound_point:
                    sound_point.play()


    # --- Desenha tudo ---
    screen.blit(player_img, player_rect)
    screen.blit(player2_img, player_rect2)

    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)

    for meteor in meteor_list:
        screen.blit(meteor_img, meteor)

    for meteor in meteor2_list:
        screen.blit(meteor2_img, meteor)

    # --- Exibe pontuação e vidas ---
    text = font.render(f"Pontos: {score}   Vidas: {lives}", True, WHITE)
    screen.blit(text, (300, 10))

    pygame.display.flip()

# ----------------------------------------------------------
# 🏁 TELA DE FIM DE JOGO
# ----------------------------------------------------------
pygame.mixer.music.stop()
screen.fill((20, 20, 20))
end_text = font.render("Fim de jogo! Pressione qualquer tecla para sair.", True, WHITE)
final_score = font.render(f"Pontuação final: {score}", True, WHITE)
high_scores.append(score)
with open('main_save.txt', 'w', encoding='utf-8') as arquivo:
    arquivo.write(f"high_scores={high_scores}\n")

screen.blit(end_text, (150, 260))
screen.blit(final_score, (300, 300))
pygame.display.flip()

waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            waiting = False

pygame.quit()
