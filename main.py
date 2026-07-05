import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 640))
clock = pygame.time.Clock()
running = True
dt = 0


# essential entities of the game
# Player
class Player:
    def __init__(self):
        self.position = pygame.Vector2(
            screen.get_width() / 2, screen.get_height() - 200
        )
        self.width = 40
        self.height = 30
        self.health = 1

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            (120, 220, 0),
            (self.position.x, self.position.y, self.width, self.height),
        )


# Enemy
class Enemy:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.width = 40
        self.height = 40
        self.health = 1

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            "orange",
            (self.position.x, self.position.y, self.width, self.height),
        )


enemies = []
enemies_died = [0] * (3 * 17)
rows_destroyed = [0] * 17
# print(screen.get_width() // (65))
for row in range(3):
    for col in range(17):
        x = 50 + (col + 1) * (60)
        y = 80 + row * 60
        enemies.append(Enemy(x, y))


# print(enemies)
player_obj = Player()

# for enemy in enemies:
# print(enemy.width)
frame_count = 0

has_reached_right = False
last_moved_time = pygame.time.get_ticks()
game_over = False
while running:
    # poll for events
    # dt = clock.tick(60) / 1000
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    player_obj.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        # print("True")
        player_obj.position.x = max(0, player_obj.position.x - (500 * dt))
    if keys[pygame.K_d]:
        # print(screen.get_width() - player_obj.width, player_obj.position.x + (500 * dt))
        player_obj.position.x = min(
            screen.get_width() - player_obj.width, (player_obj.position.x + (500 * dt))
        )
    if pygame.time.get_ticks() - last_moved_time > 1000:
        #     # these hardcoded index values to check right most enenmy later we can fix that
        right_most = max(
            enemies[16].position.x, enemies[32].position.x, enemies[50].position.x
        )
        right_most = float("-inf")
        left_most = float("inf")
        if len(enemies) > 0:
            for enemy in enemies:
                right_most = max(
                    right_most, enemy.position.x
                )  # assign the maximum value for right most end

            for enemy in enemies:
                left_most = min(
                    left_most, enemy.position.x
                )  # assign the minimum value for left most end

            if not has_reached_right:
                # print()
                if right_most + 20 <= screen.get_width() - 40:
                    for enemy in enemies:
                        enemy.position.x += 30
                else:
                    for enemy in enemies:
                        enemy.position.y += (
                            50  # after reaching the extreme, go down some position
                        )
                    has_reached_right = True
            elif has_reached_right:
                if left_most - 20 >= 0:
                    for enemy in enemies:
                        enemy.position.x -= 30
                else:
                    for enemy in enemies:
                        enemy.position.y += (
                            50  # after reaching the extreme, go down some position
                        )
                    has_reached_right = False

        last_moved_time = pygame.time.get_ticks()

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    dt = clock.tick(60) / 1000
    # independent physics.

pygame.quit()
