import pygame
import random

# Pygame'i başlat
pygame.init()

# Ekran boyutları
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Görselleri yükle
player_img = pygame.image.load("pspace.png")
enemy_img = pygame.image.load("enemy_spaceship.png")
bullet_img = pygame.image.load("bullet.png")

# Oyuncu sınıfı
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.speed = 5
        self.lives = 3

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Düşman sınıfı
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemy_img
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedy = 2  # Sabit hız
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 2000  # 2 saniye arası ateş etme süresi

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.shoot()
            self.last_shot = now

    def shoot(self):
        enemy_bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
        all_sprites.add(enemy_bullet)
        enemy_bullets.add(enemy_bullet)

# Mermi sınıfı
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.image = pygame.transform.scale(self.image, (10, 20))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.image = pygame.transform.scale(self.image, (10, 20))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

# Tüm sprite'ları gruplar
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

def create_enemy():
    enemy_spacing = WIDTH // 2  # Ekranı 2 eşit parçaya bölecek şekilde aralık belirle
    for i in range(1, 3):  # Düşman sayısını daha da azalttık
        x = i * enemy_spacing - enemy_spacing // 2
        y = random.randint(-100, -40)
        enemy = Enemy(x, y)
        all_sprites.add(enemy)
        enemies.add(enemy)

create_enemy()

# Sayaç
timer = 120
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)  # Büyük font

# Oyun durumu
game_over = False
win = False

# Oyun döngüsü
running = True
clock = pygame.time.Clock()
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
        elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
            mouse_pos = event.pos
            if restart_button.collidepoint(mouse_pos):
                # Oyunu yeniden başlat
                game_over = False
                win = False
                timer = 120
                player.lives = 3
                for enemy in enemies:
                    enemy.kill()
                for bullet in bullets:
                    bullet.kill()
                for enemy_bullet in enemy_bullets:
                    enemy_bullet.kill()
                create_enemy()

    if not game_over and not win:
        # Güncelleme
        all_sprites.update()

        # Çarpışma kontrolü
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            create_enemy()

        if pygame.sprite.spritecollideany(player, enemies):
            player.lives -= 1
            if player.lives <= 0:
                game_over = True

        enemy_hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
        for hit in enemy_hits:
            player.lives -= 1
            if player.lives <= 0:
                game_over = True

        # Sayaç
        timer -= 1 / 60
        if timer <= 0:
            win = True

    # Ekranı çiz
    screen.fill(BLACK)
    all_sprites.draw(screen)
    timer_text = font.render(f"Time: {int(timer)}", True, WHITE)
    screen.blit(timer_text, (10, 10))
    lives_text = font.render(f"Lives: {player.lives}", True, WHITE)
    screen.blit(lives_text, (WIDTH - 100, 10))

    if game_over:
        game_over_text = large_font.render("Game Over", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(game_over_text, game_over_rect)
        restart_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 10, 100, 50)
        pygame.draw.rect(screen, WHITE, restart_button)
        restart_text = font.render("Restart", True, BLACK)
        screen.blit(restart_text, (restart_button.x + 10, restart_button.y + 10))
    elif win:
        win_text = large_font.render("You Win!", True, WHITE)
        win_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(win_text, win_rect)
        restart_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 10, 100, 50)
        pygame.draw.rect(screen, WHITE, restart_button)
        restart_text = font.render("Restart", True, BLACK)
        screen.blit(restart_text, (restart_button.x + 10, restart_button.y + 10))

    pygame.display.flip()

pygame.quit()
