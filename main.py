import sys
import pygame
from constants import *
from player import *
from asteroid import Asteroid
from asteroidfield import AsteroidField

def main():
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0

    score = 0

    font = pygame.font.Font(None, 50)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    shop_button_rect = pygame.Rect(SCREEN_WIDTH - SHOP_BUTTON_WIDTH - 20, 20, SHOP_BUTTON_WIDTH, SHOP_BUTTON_HEIGHT)

    shop_open = False

    upgrade_rects = [
        pygame.Rect(350, 220, 600, 80),
        pygame.Rect(350, 320, 600, 80),
        pygame.Rect(350, 420, 600, 80)
        ]
    upgrade_labels = ["Increase Bullet Size", "Increase Fire Rate", "Increase Asteroid Spawns"]

    print("Starting Asteroids! \nScreen width: 1280 \nScreen height: 720")

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if shop_button_rect.collidepoint(event.pos):
                    shop_open = not shop_open
                if shop_open:
                    for i, rect in enumerate(upgrade_rects):
                        if rect.collidepoint(event.pos):
                            match i:
                                case 0:
                                    if score >= 50:
                                        score -= 50
                                        player.bullet_size += 1
                                case 1:
                                    if score >= 50:
                                        score -= 50
                                        player.cooldown -= 0.01
                                case 2:
                                    if score >= 50:
                                        score -= 50
                                        asteroid_field.spawn_rate -= 0.1
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)
        for asteroid in asteroids:
            if asteroid.collision(player):
                print("Game over!")
                sys.exit()
            for shot in shots:
                if shot.collision(asteroid):
                    if asteroid.radius <= ASTEROID_MIN_RADIUS:
                        score += 3
                    else:
                        score += 1
                    asteroid.split()
                    shot.kill()

        screen.fill("black")

        pygame.draw.rect(screen, "White", shop_button_rect)
        shop_text = font.render("SHOP", True, "Black")
        shop_text_rect = shop_text.get_rect(center=shop_button_rect.center)
        screen.blit(shop_text, shop_text_rect)

        score_text = font.render("Score: " + str(score), True, "White")
        screen.blit(score_text, (580, 20))

        if shop_open:
            pygame.draw.rect(screen, "gray", (250, 100, 780, 520)) 
            shop_title = font.render("SHOP", True, "white")
            shop_title_rect = shop_title.get_rect(center=(640, 150))
            screen.blit(shop_title, shop_title_rect)

            for i, upgrade_rect in enumerate(upgrade_rects):
                pygame.draw.rect(screen, "white", upgrade_rect)
                text = f"{upgrade_labels[i]} (Cost: 50)"
                upgrade_text = font.render(text, True, "black")
                upgrade_text_rect = upgrade_text.get_rect(center=upgrade_rect.center)
                screen.blit(upgrade_text, upgrade_text_rect)
            

        for obj in drawable:
            obj.draw(screen)

        # refresh the screen
        pygame.display.flip()

        # limit the framerate to 60 FPS 
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()