import sys
import random
import math
import pygame

pygame.init()
pygame.font.init()

# --- DIMENZIJE I PROZOR ---
WIDTH, HEIGHT = 1080, 850
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Skočko - RTS Slagalica")

# --- BOJE ---
BG_DARK = (10, 65, 22)
BG_MID = (25, 120, 40)
BG_LIGHT = (45, 160, 58)
GRID_BG = (28, 108, 40)
GRID_BORDER = (110, 225, 120)
SYMBOL_BG = (50, 150, 65)
BLACK = (12, 12, 12)
RED = (235, 20, 20)
YELLOW = (255, 220, 10)
WHITE = (245, 245, 245)
SKOCKO_FACE = (250, 215, 50)

# Boje za štraftu tajmera (zelena kontura)
TIMER_BORDER_OUTER = (15, 75, 30)
TIMER_BORDER_INNER = (110, 225, 120)
TIMER_BG_BLACK = (12, 12, 12)
TIMER_FILL_WHITE = (245, 245, 245)

# --- SIMBOLI ---
SYMBOLS = ["SKOCKO", "TREF", "PIK", "HERC", "KARO", "ZVEZDA"]

secret_code = [random.choice(SYMBOLS) for _ in range(4)]
attempts = [[] for _ in range(6)]
feedbacks = [[] for _ in range(6)]
current_attempt = 0
game_started = False  # Čeka pritisak na R za početak
game_over = False
won = False

# Tajmer (90 sekundi)
TOTAL_TIME = 90
start_ticks = 0

# --- FUNKCIJA ZA CRTANJE SIMBOLA ---
def draw_symbol(surface, name, center, size, head_only=True):
    x, y = center
    r = size // 2

    if name == "SKOCKO":
        if head_only:
            head_y = y
            head_r = int(r * 0.72)
            
            # Antene
            pygame.draw.line(surface, BLACK, (x - int(r*0.12), head_y - int(head_r*0.75)), (x - int(r*0.42), head_y - int(head_r*1.40)), 3)
            pygame.draw.line(surface, BLACK, (x + int(r*0.12), head_y - int(head_r*0.75)), (x + int(r*0.42), head_y - int(head_r*1.40)), 3)
            
            # Glava
            pygame.draw.circle(surface, SKOCKO_FACE, (x, head_y), head_r)
            pygame.draw.circle(surface, BLACK, (x, head_y), head_r, 2)
            
            # Naočari
            pygame.draw.ellipse(surface, BLACK, (x - int(r*0.62), head_y - int(r*0.48), int(r*0.60), int(r*0.58)), 2)
            pygame.draw.ellipse(surface, BLACK, (x + int(r*0.02), head_y - int(r*0.48), int(r*0.60), int(r*0.58)), 2)
            
            # Zenice
            pygame.draw.ellipse(surface, WHITE, (x - int(r*0.38), head_y - int(r*0.38), int(r*0.26), int(r*0.36)))
            pygame.draw.ellipse(surface, BLACK, (x - int(r*0.38), head_y - int(r*0.38), int(r*0.26), int(r*0.36)), 1)
            pygame.draw.ellipse(surface, BLACK, (x - int(r*0.28), head_y - int(r*0.30), int(r*0.14), int(r*0.22)))
            
            pygame.draw.ellipse(surface, WHITE, (x + int(r*0.12), head_y - int(r*0.38), int(r*0.26), int(r*0.36)))
            pygame.draw.ellipse(surface, BLACK, (x + int(r*0.12), head_y - int(r*0.38), int(r*0.26), int(r*0.36)), 1)
            pygame.draw.ellipse(surface, BLACK, (x + int(r*0.16), head_y - int(r*0.30), int(r*0.14), int(r*0.22)))
            
            # Nos i osmeh
            pygame.draw.circle(surface, RED, (x, head_y + int(r*0.04)), int(r*0.13))
            pygame.draw.arc(surface, BLACK, (x - int(r*0.22), head_y + int(r*0.10), int(r*0.44), int(r*0.26)), 3.14, 6.28, 2)
        else:
            # Maskota desno
            head_y = y - int(r * 0.35)
            head_r = int(r * 0.55)
            
            pygame.draw.line(surface, BLACK, (x - int(r*0.12), head_y - int(head_r*0.75)), (x - int(r*0.45), head_y - int(head_r*1.60)), 4)
            pygame.draw.line(surface, BLACK, (x + int(r*0.12), head_y - int(head_r*0.75)), (x + int(r*0.45), head_y - int(head_r*1.60)), 4)
            
            pygame.draw.circle(surface, SKOCKO_FACE, (x, head_y), head_r)
            pygame.draw.circle(surface, BLACK, (x, head_y), head_r, 3)
            
            pygame.draw.ellipse(surface, BLACK, (x - int(r*0.52), head_y - int(r*0.42), int(r*0.50), int(r*0.50)), 3)
            pygame.draw.ellipse(surface, BLACK, (x + int(r*0.02), head_y - int(r*0.42), int(r*0.50), int(r*0.50)), 3)
            
            pygame.draw.ellipse(surface, WHITE, (x - int(r*0.32), head_y - int(r*0.32), int(r*0.22), int(r*0.30)))
            pygame.draw.ellipse(surface, BLACK, (x - int(r*0.26), head_y - int(r*0.26), int(r*0.12), int(r*0.18)))
            
            pygame.draw.ellipse(surface, WHITE, (x + int(r*0.10), head_y - int(r*0.32), int(r*0.22), int(r*0.30)))
            pygame.draw.ellipse(surface, BLACK, (x + int(r*0.14), head_y - int(r*0.26), int(r*0.12), int(r*0.18)))
            
            pygame.draw.circle(surface, RED, (x, head_y + int(r*0.02)), int(r*0.12))
            pygame.draw.arc(surface, BLACK, (x - int(r*0.20), head_y + int(r*0.08), int(r*0.40), int(r*0.25)), 3.14, 6.28, 3)

            sp_top = head_y + head_r - int(r*0.02)
            spirals = 6
            for i in range(spirals):
                factor = (spirals - i) / spirals
                w = int(r * 0.70 * factor)
                h = int(r * 0.14 * factor) + 3
                sy = sp_top + i * int(r * 0.12)
                pygame.draw.ellipse(surface, BLACK, (x - w//2, sy, w, h), 3)

    elif name == "TREF":
        tr = int(r * 0.42)
        pygame.draw.circle(surface, BLACK, (x - int(r*0.32), y + int(r*0.05)), tr)
        pygame.draw.circle(surface, BLACK, (x + int(r*0.32), y + int(r*0.05)), tr)
        pygame.draw.circle(surface, BLACK, (x, y - int(r*0.32)), tr)
        pygame.draw.circle(surface, BLACK, (x, y), int(r*0.25))
        
        pts = [(x, y - int(r*0.1)), (x - int(r*0.25), y + int(r*0.82)), (x + int(r*0.25), y + int(r*0.82))]
        pygame.draw.polygon(surface, BLACK, pts)

    elif name == "PIK":
        top_y = y - int(r * 0.85)
        base_y = y + int(r * 0.28)
        
        pts = [(x, top_y)]
        steps = 15
        for i in range(1, steps + 1):
            t = i / steps
            px = x - (r * 0.88) * (math.sin(t * math.pi / 2) ** 1.4)
            py = top_y + (base_y - top_y) * (t ** 2.0)
            pts.append((px, py))
            
        pts.append((x - int(r * 0.35), base_y - int(r * 0.15)))
        pts.append((x, base_y - int(r * 0.05)))
        pts.append((x + int(r * 0.35), base_y - int(r * 0.15)))
        
        for i in range(steps, 0, -1):
            t = i / steps
            px = x + (r * 0.88) * (math.sin(t * math.pi / 2) ** 1.4)
            py = top_y + (base_y - top_y) * (t ** 2.0)
            pts.append((px, py))
            
        pygame.draw.polygon(surface, BLACK, pts)
        
        stem_pts = [(x, y), (x - int(r * 0.22), y + int(r * 0.82)), (x + int(r * 0.22), y + int(r * 0.82))]
        pygame.draw.polygon(surface, BLACK, stem_pts)

    elif name == "HERC":
        top_y = y - int(r * 0.28)
        tr = int(r * 0.46)
        pygame.draw.circle(surface, RED, (x - tr, top_y), tr)
        pygame.draw.circle(surface, RED, (x + tr, top_y), tr)
        
        pts = [
            (x - int(r * 0.90), top_y + int(r * 0.12)),
            (x + int(r * 0.90), top_y + int(r * 0.12)),
            (x, y + int(r * 0.88))
        ]
        pygame.draw.polygon(surface, RED, pts)

    elif name == "KARO":
        pts = [
            (x, y - int(r * 0.88)),
            (x + int(r * 0.78), y),
            (x, y + int(r * 0.88)),
            (x - int(r * 0.78), y)
        ]
        pygame.draw.polygon(surface, RED, pts)

    elif name == "ZVEZDA":
        pts = []
        for i in range(10):
            angle = i * math.pi / 5 - math.pi / 2
            radius = int(r * 0.90) if i % 2 == 0 else int(r * 0.42)
            pts.append((x + radius * math.cos(angle), y + radius * math.sin(angle)))
        pygame.draw.polygon(surface, YELLOW, pts)

def evaluate_guess(guess, target):
    crvene = 0
    zute = 0
    t_m = target.copy()
    g_m = guess.copy()
    
    for i in range(4):
        if g_m[i] == t_m[i]:
            crvene += 1
            t_m[i] = None
            g_m[i] = None

    for i in range(4):
        if g_m[i] is not None and g_m[i] in t_m:
            zute += 1
            t_m[t_m.index(g_m[i])] = None

    fb = ["RED"] * crvene + ["YELLOW"] * zute
    while len(fb) < 4:
        fb.append("BLACK")
    return fb

def reset_game():
    global secret_code, attempts, feedbacks, current_attempt, game_started, game_over, won, start_ticks
    secret_code = [random.choice(SYMBOLS) for _ in range(4)]
    attempts = [[] for _ in range(6)]
    feedbacks = [[] for _ in range(6)]
    current_attempt = 0
    game_started = True
    game_over = False
    won = False
    start_ticks = pygame.time.get_ticks()

# --- GLAVNA PETLJA ---
clock = pygame.time.Clock()
palette_rects = []

running = True
while running:
    clock.tick(30)
    screen.fill(BG_MID)
    
    # Proračun vremena u celim sekundama (isprekidano spuštanje na svaki sekund)
    elapsed_seconds_int = 0
    if game_started and not game_over:
        elapsed_ms = pygame.time.get_ticks() - start_ticks
        elapsed_seconds_int = int(elapsed_ms // 1000)
        
        if elapsed_seconds_int >= TOTAL_TIME:
            elapsed_seconds_int = TOTAL_TIME
            game_over = True
            won = False

    # Pozadina
    pygame.draw.polygon(screen, BG_DARK, [(0, 0), (540, 0), (320, 850), (0, 850)])
    pygame.draw.polygon(screen, BG_LIGHT, [(540, 0), (1080, 0), (1080, 850), (760, 850)])

    cell_size = 78
    start_x, start_y = 60, 35

    # --- TABELA POKUŠAJA ---
    for row in range(6):
        for col in range(4):
            x = start_x + col * (cell_size + 14)
            y = start_y + row * (cell_size + 10)
            rect = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(screen, GRID_BG, rect)
            pygame.draw.rect(screen, GRID_BORDER, rect, 2)
            
            if col < len(attempts[row]):
                draw_symbol(screen, attempts[row][col], rect.center, cell_size - 8, head_only=True)

    # --- ŠTRAFTA ZA OGRANIČENJE VREMENA (TAJMER) ---
    timer_x = 442
    timer_y = start_y + 4
    timer_w = 20
    timer_h = 6 * (cell_size + 10) - 18
    
    # Zeleni okviri
    outer_timer_rect = pygame.Rect(timer_x, timer_y, timer_w, timer_h)
    pygame.draw.rect(screen, TIMER_BORDER_OUTER, outer_timer_rect, border_radius=6)
    inner_timer_rect = pygame.Rect(timer_x + 2, timer_y + 2, timer_w - 4, timer_h - 4)
    pygame.draw.rect(screen, TIMER_BORDER_INNER, inner_timer_rect, border_radius=4)
    
    # Unutrašnja podloga je crna
    content_rect = pygame.Rect(timer_x + 4, timer_y + 4, timer_w - 8, timer_h - 8)
    pygame.draw.rect(screen, TIMER_BG_BLACK, content_rect)
    
    # Bela traka kreće sa vrha i spušta se na svaki puni sekund
    fill_h = int(content_rect.height * (elapsed_seconds_int / TOTAL_TIME))
    if fill_h > 0:
        fill_rect = pygame.Rect(content_rect.x, content_rect.y, content_rect.width, fill_h)
        pygame.draw.rect(screen, TIMER_FILL_WHITE, fill_rect)

    # --- INDIKATORI (POGOCI) ---
    fb_start_x = 490
    for row in range(6):
        for col in range(4):
            cx = fb_start_x + col * 54
            cy = start_y + row * (cell_size + 10) + cell_size // 2
            
            color = BLACK
            if col < len(feedbacks[row]):
                if feedbacks[row][col] == "RED":
                    color = RED
                elif feedbacks[row][col] == "YELLOW":
                    color = YELLOW
            
            pygame.draw.circle(screen, color, (cx, cy), 22)
            pygame.draw.circle(screen, BLACK, (cx, cy), 22, 2)

    # Maskota
    draw_symbol(screen, "SKOCKO", (880, 260), 230, head_only=False)

    # --- ZAJEDNIČKI NIVO NA DNU: REŠENJE I PALETA ---
    bottom_y = 670

    # 1. REŠENJE (TAČNA KOMBINACIJA)
    for col in range(4):
        x = start_x + col * (cell_size + 14)
        rect = pygame.Rect(x, bottom_y, cell_size, cell_size)
        pygame.draw.rect(screen, GRID_BG, rect)
        pygame.draw.rect(screen, GRID_BORDER, rect, 2)
        if game_over:
            draw_symbol(screen, secret_code[col], rect.center, cell_size - 8, head_only=True)

    # 2. PALETA ZA IZBOR SIMBOLA
    pal_x = 480
    pal_w = 520
    pal_h = cell_size + 24
    pygame.draw.rect(screen, SYMBOL_BG, (pal_x, bottom_y - 12, pal_w, pal_h), border_radius=18)
    pygame.draw.rect(screen, GRID_BORDER, (pal_x, bottom_y - 12, pal_w, pal_h), 3, border_radius=18)

    palette_rects = []
    symbol_spacing = 82
    for i, sym in enumerate(SYMBOLS):
        cx = pal_x + 55 + i * symbol_spacing
        cy = bottom_y + cell_size // 2
        r = pygame.Rect(cx - cell_size//2, cy - cell_size//2, cell_size, cell_size)
        palette_rects.append((r, sym))
        draw_symbol(screen, sym, (cx, cy), cell_size - 8, head_only=True)

    # Statusne poruke
    font = pygame.font.SysFont("Arial", 30, bold=True)
    if not game_started:
        txt = "PRITISNITE R ZA START"
        txt_surf = font.render(txt, True, WHITE)
        screen.blit(txt_surf, (WIDTH // 2 - txt_surf.get_width() // 2, HEIGHT - 45))
    elif game_over:
        txt = "POGODAK! Pritisnite R za novu igru." if won else "KRAJ IGRE! Pritisnite R za novu igru."
        txt_surf = font.render(txt, True, WHITE)
        screen.blit(txt_surf, (WIDTH // 2 - txt_surf.get_width() // 2, HEIGHT - 45))

    # --- EVENT LOGIKA ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN and game_started and not game_over:
            if event.button == 1:
                for rect, sym in palette_rects:
                    if rect.collidepoint(event.pos):
                        if len(attempts[current_attempt]) < 4:
                            attempts[current_attempt].append(sym)
                            
                            if len(attempts[current_attempt]) == 4:
                                fb = evaluate_guess(attempts[current_attempt], secret_code)
                                feedbacks[current_attempt] = fb
                                if fb.count("RED") == 4:
                                    game_over = True
                                    won = True
                                else:
                                    current_attempt += 1
                                    if current_attempt == 6:
                                        game_over = True
            
            elif event.button == 3:
                if len(attempts[current_attempt]) > 0:
                    attempts[current_attempt].pop()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and game_started and not game_over:
                if len(attempts[current_attempt]) > 0:
                    attempts[current_attempt].pop()
            elif event.key == pygame.K_r:
                reset_game()

    pygame.display.flip()

pygame.quit()
sys.exit()