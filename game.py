################################################
#                                              #
#   This sample game has been created by       #
#     self created AI Multi-Agents Team        #
#  https://github.com/Borsh8m3/AI_agents_team  #
################################################     

import pygame
import math
import random

# Ustawienia stałe
WIDTH, HEIGHT = 400, 600
BG_COLOR = (26, 26, 36)
BLOCK_COLOR = (150, 50, 200)
BALL_COLOR = (255, 255, 255)
TEXT_COLOR = (255, 255, 255)
AVATAR_COLOR = (255, 204, 0)
COLS = 7
BLOCK_SIZE = WIDTH // COLS
BALL_RADIUS = 6
BALL_SPEED = 12

class Block:
    def __init__(self, col, row, hp):
        self.col = col
        self.row = row
        self.rect = pygame.Rect(col * BLOCK_SIZE + 2, row * BLOCK_SIZE + 50, BLOCK_SIZE - 4, BLOCK_SIZE - 4)
        self.hp = hp

    def draw(self, surface, font):
        pygame.draw.rect(surface, BLOCK_COLOR, self.rect)
        text = font.render(str(self.hp), True, TEXT_COLOR)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

class Ball:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.vx = math.cos(angle) * BALL_SPEED
        self.vy = math.sin(angle) * BALL_SPEED
        self.active = True
        self.rect = pygame.Rect(x - BALL_RADIUS, y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)

    def move(self):
        if not self.active: return
        self.x += self.vx
        self.y += self.vy
        self.rect.center = (int(self.x), int(self.y))

        # Odbicia od ścian
        if self.rect.left <= 0:
            self.rect.left = 0
            self.x = self.rect.centerx
            self.vx *= -1
        elif self.rect.right >= WIDTH:
            self.rect.right = WIDTH
            self.x = self.rect.centerx
            self.vx *= -1
            
        if self.rect.top <= 0:
            self.rect.top = 0
            self.y = self.rect.centery
            self.vy *= -1

    def draw(self, surface):
        if self.active:
            pygame.draw.circle(surface, BALL_COLOR, (int(self.x), int(self.y)), BALL_RADIUS)

class BBTAN:
    def __init__(self, render_mode=False):
        self.render_mode = render_mode
        self.width = WIDTH
        self.height = HEIGHT
        
        if self.render_mode:
            pygame.init()
            self.screen = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption("BBTAN")
            self.clock = pygame.time.Clock()
            self.font = pygame.font.SysFont(None, 24)
        
        self.reset()

    def get_params(self):
        current_level = self.level
        blocks_on_screen = len(self.blocks)
        total_hp_on_screen = sum(b.hp for b in self.blocks)
        
        if blocks_on_screen > 0:
            lowest_block_row = max(b.row for b in self.blocks)
            distance_to_ground = 10 - lowest_block_row
        else:
            distance_to_ground = 10
            
        # ZWRACAMY CZYSTY SŁOWNIK (bez list!)
        return {
            'Level': current_level,
            'Floor': distance_to_ground,
            'Blocks': blocks_on_screen,
            'Blocks_HP': total_hp_on_screen
        }


    def reset(self):
        """Resetuje grę do stanu początkowego i zwraca pierwszą obserwację."""
        self.level = 1
        self.max_balls = 1
        self.blocks = []
        self.start_x = self.width // 2
        self.start_y = self.height - 20
        self.done = False
        self.score = 0
        
        self._spawn_row()
        return self._get_state()

    def _spawn_row(self):
        # Przesuń istniejące klocki w dół
        for b in self.blocks:
            b.rect.y += BLOCK_SIZE
            b.row += 1
            if b.rect.bottom > self.height - 40:
                self.done = True # Klocek dotknął dołu - koniec gry
        
        if not self.done:
            # Generuj nowy rząd
            for c in range(COLS):
                if random.random() > 0.5:
                    self.blocks.append(Block(c, 0, self.level))
            
            self.max_balls += 1
            self.level += 1

    def _get_state(self):
        """
        Zwraca stan gry ('oczy' agenta). 
        Zwracamy prostą macierz (listę list) reprezentującą planszę.
        """
        # Plansza 10 wierszy na 7 kolumn (można dostosować)
        grid = [[0 for _ in range(COLS)] for _ in range(10)]
        
        for b in self.blocks:
            if b.row < 10:
                grid[b.row][b.col] = b.hp
                
        # Agent dostaje planszę, pozycję startową X oraz liczbę kulek
        state = {
            "grid": grid,
            "start_x": self.start_x,
            "balls": self.max_balls
        }
        return state

    def step(self, action_angle):
        """
        Wykonuje pełną turę gry dla zadanego kąta strzału.
        action_angle: Kąt strzału w radianach (np. od -math.pi do 0)
        Zwraca: (stan, nagroda, czy_koniec, info)
        """
        if self.done:
            return self._get_state(), 0, self.done, {}

        balls = []
        balls_to_shoot = self.max_balls - 1
        shoot_timer = 0
        first_return_x = None
        turn_over = False
        reward = 0

        # Wewnętrzna pętla symulująca całą turę fizyki w "jednym kroku" agenta
        while not turn_over:
            shoot_timer += 1
            
            # Wystrzeliwanie nowych kulek
            if shoot_timer % 4 == 0 and balls_to_shoot > 0:
                balls.append(Ball(self.start_x, self.start_y, action_angle))
                balls_to_shoot -= 1

            # Fizyka i kolizje
            all_returned = True
            for ball in balls:
                if not ball.active: continue
                all_returned = False
                ball.move()

                for b in self.blocks[:]:
                    if ball.rect.colliderect(b.rect):
                        b.hp -= 1
                        reward += 0.1  # Mała nagroda za trafienie klocka
                        if b.hp <= 0:
                            self.blocks.remove(b)
                            reward += 1.0  # Duża nagroda za zniszczenie klocka
                        
                        overlap_left = ball.rect.right - b.rect.left
                        overlap_right = b.rect.right - ball.rect.left
                        overlap_top = ball.rect.bottom - b.rect.top
                        overlap_bottom = b.rect.bottom - ball.rect.top
                        
                        min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)
                        if min_overlap in (overlap_left, overlap_right):
                            ball.vx *= -1
                        else:
                            ball.vy *= -1
                        break

                if ball.rect.bottom >= self.height:
                    ball.active = False
                    if first_return_x is None:
                        first_return_x = ball.x

            # Jeśli wymuszono renderowanie podczas symulacji tury
            if self.render_mode:
                self._render_frame(balls)

            # Koniec tury
            if balls_to_shoot == 0 and all_returned:
                turn_over = True

        # Po zakończeniu tury ustaw nową pozycję i wygeneruj nowy rząd
        if first_return_x is not None:
            self.start_x = max(BALL_RADIUS, min(self.width - BALL_RADIUS, first_return_x))
            
        self._spawn_row()

        if self.done:
            reward -= 10.0  # Kara za śmierć
        else:
            reward += 1.0   # Nagroda za przetrwanie tury
            self.score += 1

        return self._get_state(), reward, self.done, {"score": self.score}

    def _render_frame(self, balls):
        """Prywatna metoda rysująca klatkę gry."""
        self.screen.fill(BG_COLOR)
        
        for b in self.blocks:
            b.draw(self.screen, self.font)
            
        for ball in balls:
            ball.draw(self.screen)
            
        pygame.draw.circle(self.screen, AVATAR_COLOR, (int(self.start_x), int(self.start_y)), BALL_RADIUS + 4)
        
        hud_text = self.font.render(f"LINE: {self.level-1}   Kulki: {self.max_balls-1}", True, TEXT_COLOR)
        self.screen.blit(hud_text, (10, 10))
        
        pygame.display.flip()
        self.clock.tick(120)  # Zwiększone FPS dla szybszego podglądu, agent i tak liczy szybciej

    def close(self):
        if self.render_mode:
            pygame.quit()