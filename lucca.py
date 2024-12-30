import pygame
import random
import sys
import os

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


pygame.init()

WIDTH, HEIGHT = 650, 600
PLAYER_WIDTH, PLAYER_HEIGHT = 20, 20
GRAVITY = 0.25
JUMP_VELOCITY = -10
MOVEMENT_SPEED = 4
FPS = 60
RAIN_DELAY = 4000
MAX_RAIN_PARTICLES = 10
COUNTDOWN_FONT_SIZE = 120
SCORE_FONT_SIZE = 60

WHITE = (255, 255, 255)
RED = (255, 0, 0)
NAVY_BLUE = (0, 0, 128)

player_image = pygame.image.load(resource_path("assets/IMG_0615-2.jpg"))
background_image = pygame.image.load(resource_path("assets/D85095D8-.jpg"))
raindrop1_image = pygame.image.load(resource_path("assets/90DD7B9E--2.jpg"))
raindrop2_image = pygame.image.load(resource_path("assets/298B6100--2.jpg"))
image_3 = pygame.image.load(resource_path("assets/549A4F07--2.jpg"))
new_player_image = pygame.image.load(resource_path("assets/IMG_0624-2.jpg"))

#setting icon
icon = pygame.image.load(resource_path('assets/IMG_0615.jpg'))
pygame.display.set_icon(icon)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lucca")

pygame.mixer.music.load(resource_path("assets/downRight.mp3"))
pygame.mixer.music.play(-1)
point_sound = pygame.mixer.Sound(resource_path("assets/cute-level-up-3-189853.mp3"))
level_passed_sound = pygame.mixer.Sound(resource_path("assets/level-passed-143039.mp3"))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.velocity = 0
        self.score = 0
        self.moving_left = False
        self.moving_right = False
        self.progress = 0
        self.level_up_sound_played = False

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

        if self.moving_left:
            self.rect.x -= MOVEMENT_SPEED
        if self.moving_right:
            self.rect.x += MOVEMENT_SPEED

        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

        if self.score >= 77:
            self.image = new_player_image

            if not self.level_up_sound_played:
                level_passed_sound.play()
                self.level_up_sound_played = True

    def jump(self):
        self.velocity = JUMP_VELOCITY

    def increase_score(self):
        self.score += 1
        self.progress = self.score / 10

class Raindrop(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice([raindrop1_image, raindrop2_image, image_3])
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-HEIGHT, 0)
        self.speed = random.randint(3, 8)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.y = random.randint(-HEIGHT, 0)
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.image = random.choice([raindrop1_image, raindrop2_image, image_3])

def draw_text(text, font, color, surface, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

def draw_progress_bar(surface, x, y, width, height, percent):
    BAR_COLOR = NAVY_BLUE
    BAR_BG_COLOR = (100, 100, 100)

    progress_width = int(width * percent)
    progress_rect = pygame.Rect(x, y, progress_width/7.7, height)
    pygame.draw.rect(surface, BAR_COLOR, progress_rect)

    bg_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, BAR_BG_COLOR, bg_rect, 2)

def main():
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    raindrops = pygame.sprite.Group()

    start_time = pygame.time.get_ticks()
    countdown_started = True
    countdown_duration = 3000

    clock = pygame.time.Clock()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
                elif event.key == pygame.K_LEFT:
                    player.moving_left = True
                elif event.key == pygame.K_RIGHT:
                    player.moving_right = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.moving_left = False
                elif event.key == pygame.K_RIGHT:
                    player.moving_right = False

        all_sprites.update()

        if pygame.time.get_ticks() - start_time >= RAIN_DELAY:
            if len(raindrops) < MAX_RAIN_PARTICLES:
                raindrop = Raindrop()
                all_sprites.add(raindrop)
                raindrops.add(raindrop)

        collisions = pygame.sprite.spritecollide(player, raindrops, True)
        if collisions:
            player.increase_score()
            point_sound.play()

        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)

        if countdown_started:
            countdown_remaining = max(0, (countdown_duration - (pygame.time.get_ticks() - start_time)) // 1000 + 1)
            if countdown_remaining > 0:
                countdown_font = pygame.font.Font(None, COUNTDOWN_FONT_SIZE)
                draw_text(str(countdown_remaining), countdown_font, RED, screen, WIDTH // 2, HEIGHT // 2)
            else:
                countdown_started = False

        draw_text("POINTS: " + str(player.score), pygame.font.Font(None, SCORE_FONT_SIZE), RED, screen, 20, 20)
        draw_text("POWER", pygame.font.Font(None, SCORE_FONT_SIZE), RED, screen, 20, 100)

        draw_progress_bar(screen, 20, 140, 600, 30, player.progress)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
