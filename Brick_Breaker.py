import pygame
import random

# Initialize the game
pygame.init()

# Set the dimensions of the game window
window_width = 800
window_height = 600

# Set the colors
black = (0, 0, 0)
white = (255, 255, 255)
brick_colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 128, 0), (0, 0, 255), (75, 0, 130)]

# Set the brick dimensions
brick_width = 70
brick_height = 20

# Set the paddle dimensions
paddle_width = 100
paddle_height = 10

# Set the ball dimensions
ball_radius = 10

# Set the paddle speed
paddle_speed = 7

# Set the ball speed
ball_speed = 5

# Set the number of rows and columns of bricks
num_rows = 6
num_cols = 10

# Initialize the score
score = 0

# Create the game window
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Brick Breaker")

clock = pygame.time.Clock()


# Function to draw the paddle
def draw_paddle(paddle_x, paddle_y):
    pygame.draw.rect(window, white, (paddle_x, paddle_y, paddle_width, paddle_height))


# Function to draw the ball
def draw_ball(ball_x, ball_y):
    pygame.draw.circle(window, white, (ball_x, ball_y), ball_radius)


# Function to draw the bricks
def draw_bricks(bricks):
    for row in range(num_rows):
        for col in range(num_cols):
            if bricks[row][col] == 1:
                brick_x = col * (brick_width + 5) + 30
                brick_y = row * (brick_height + 5) + 50
                pygame.draw.rect(window, brick_colors[row], (brick_x, brick_y, brick_width, brick_height))


# Function to handle collisions between the ball and bricks
def handle_collisions(bricks, ball_rect, ball_speed_y):
    collided = False
    for row in range(num_rows):
        for col in range(num_cols):
            if bricks[row][col] == 1:
                brick_x = col * (brick_width + 5) + 30
                brick_y = row * (brick_height + 5) + 50
                brick_rect = pygame.Rect(brick_x, brick_y, brick_width, brick_height)
                if brick_rect.colliderect(ball_rect):
                    bricks[row][col] = 0
                    collided = True
                    ball_speed_y *= -1
    return ball_speed_y, collided


# Function to update the score
def update_score(collided):
    global score
    if collided:
        score += 10





# Function to display the score
def display_score():
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, white)
    window.blit(score_text, (10, 10))


# Main game loop
def game_loop():
    # Initialize the paddle position
    paddle_x = (window_width - paddle_width) // 2
    paddle_y = window_height - 50

    # Initialize the ball position and speed
    ball_x = window_width // 2
    ball_y = window_height // 2
    ball_speed_x = random.choice([-ball_speed, ball_speed])
    ball_speed_y = -ball_speed

    # Create the bricks
    bricks = []
    for _ in range(num_rows):
        bricks.append([1] * num_cols)

    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < window_width - paddle_width:
            paddle_x += paddle_speed

        # Update the ball position
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Check for collisions with the window edges
        if ball_x <= 0 or ball_x >= window_width - ball_radius:
            ball_speed_x *= -1
        if ball_y <= 0:
            ball_speed_y *= -1
        if ball_y >= window_height:
            game_over = True

        # Check for collisions with the paddle
        if ball_y + ball_radius >= paddle_y and paddle_x - ball_radius <= ball_x <= paddle_x + paddle_width + ball_radius:
            ball_speed_y *= -1

        # Check for collisions with the bricks
        ball_rect = pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)
        ball_speed_y, collided = handle_collisions(bricks, ball_rect, ball_speed_y)

        # Update the score
        update_score(collided)

        # Clear the window
        window.fill(black)

        # Draw game objects
        draw_paddle(paddle_x, paddle_y)
        draw_ball(ball_x, ball_y)
        draw_bricks(bricks)

        # Display the score
        display_score()

        # Update the display
        pygame.display.update()

        # Set the frames per second
        clock.tick(30)


# Start the game
game_loop()
