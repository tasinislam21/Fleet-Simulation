import pygame

# Initialize Pygame
pygame.init()

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Define maze walls (list of rectangles)
walls = [
    pygame.Rect(100, 100, 400, 20),  # Top wall
    pygame.Rect(100, 300, 400, 20),  # Bottom wall
    pygame.Rect(100, 100, 20, 220),  # Left wall
    pygame.Rect(480, 100, 20, 220),  # Right wall
    pygame.Rect(200, 150, 100, 20),  # Extra wall
]

# Define player box
player = pygame.Rect(120, 120, 30, 30)
speed = 3

# Clock for FPS control
clock = pygame.time.Clock()

running = True
while running:
    screen.fill((0, 0, 0))  # Clear screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move player with arrow keys
    keys = pygame.key.get_pressed()
    new_x, new_y = player.x, player.y  # Store new position before updating

    if keys[pygame.K_LEFT]:
        new_x -= speed
    if keys[pygame.K_RIGHT]:
        new_x += speed
    if keys[pygame.K_UP]:
        new_y -= speed
    if keys[pygame.K_DOWN]:
        new_y += speed

    # Create a temporary rect for collision checking
    new_rect = pygame.Rect(new_x, new_y, player.width, player.height)

    # Check collision with maze walls
    if not any(new_rect.colliderect(wall) for wall in walls):
        player.x, player.y = new_x, new_y  # Update position if no collision

    # Draw walls
    for wall in walls:
        pygame.draw.rect(screen, (255, 255, 255), wall)

    # Draw player
    pygame.draw.rect(screen, (0, 255, 0), player)

    pygame.display.flip()
    clock.tick(30)  # Limit FPS

pygame.quit()