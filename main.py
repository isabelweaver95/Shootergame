import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 600
screen_height = 400

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Game variables
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Shooter Game")

# Shooter variables
shooter_width = 50
shooter_height = 10
shooter_color = white
shooter_speed = 5
shooter_x = screen_width // 2 - shooter_width // 2
shooter_y = screen_height - shooter_height - 10

# Projectile variables
projectile_width = 5
projectile_height = 10
projectile_color = red
projectile_speed = 7
projectiles = []

# Falling object variables
falling_width = 20
falling_height = 20
falling_color = white
falling_speed = 3
falling_objects = []

class Shooter:
    def __init__(self, x, y, width, height, color, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed

    def move(self, direction):
        if direction == 'left':
            self.x -= self.speed
        elif direction == 'right':
            self.x += self.speed

        # Boundary check for shooter
        if self.x < 0:
            self.x = 0
        elif self.x > screen_width - self.width:
            self.x = screen_width - self.width

    def shoot(self):
        projectiles.append(Projectile(self.x + self.width // 2 - projectile_width // 2, self.y, projectile_width, projectile_height, projectile_color, projectile_speed))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.width, self.height))


class Projectile:
    def __init__(self, x, y, width, height, color, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed

    def move(self):
        self.y -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.width, self.height))


class FallingObject:
    def __init__(self, x, y, width, height, color, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed

    def move(self):
        self.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

# Create objects
# Main game loop
def spawn_falling_object():
    x = random.randint(0, screen_width - falling_width)
    y = -falling_height
    falling_objects.append(FallingObject(x, y, falling_width, falling_height, falling_color, falling_speed))

# Create shooter object
shooter = Shooter(shooter_x, shooter_y, shooter_width, shooter_height, shooter_color, shooter_speed)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                shooter.move('left')
            elif event.key == pygame.K_RIGHT:
                shooter.move('right')
            elif event.key == pygame.K_SPACE:
                shooter.shoot()

    # Continuous movement with held down keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        shooter.move('left')
    if keys[pygame.K_RIGHT]:
        shooter.move('right')

    # Clear screen
    screen.fill(black)

    # Spawn new falling objects at a certain interval
    if random.randint(1, 100) == 1:
        spawn_falling_object()

    # Update and draw falling objects
    for falling_object in falling_objects[:]:
        falling_object.move()
        falling_object.draw(screen)
        # Remove falling objects that go off screen
        if falling_object.y > screen_height:
            falling_objects.remove(falling_object)

    # Update and draw projectiles
    for projectile in projectiles[:]:
        projectile.move()
        projectile.draw(screen)
        # Remove projectiles that go off screen
        if projectile.y < 0:
            projectiles.remove(projectile)

    # Draw shooter
    shooter.draw(screen)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()
