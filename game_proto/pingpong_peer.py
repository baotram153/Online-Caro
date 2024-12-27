import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class GameEngine:
    def __init__(self, share_queue):
        pygame.init()
        
        self.share_queue = share_queue
        self.player = "unknow"

        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Ping Pong Game")

        # frame per second
        self.clock = pygame.time.Clock()

        self.PADDLE_WIDTH, self.PADDLE_HEIGHT = 15, 100
        self.BALL_SIZE = 20

        # initial paddle position (topleft corner + size)
        self.paddle_left = pygame.Rect(30, self.HEIGHT // 2 - self.PADDLE_HEIGHT // 2, self.PADDLE_WIDTH, self.PADDLE_HEIGHT)
        self.paddle_right = pygame.Rect(self.WIDTH - 30 - self.PADDLE_WIDTH, self.HEIGHT // 2 - self.PADDLE_HEIGHT // 2, self.PADDLE_WIDTH, self.PADDLE_HEIGHT)
        
        # ball at the middle of the screen
        self.ball = pygame.Rect(self.WIDTH // 2 - self.BALL_SIZE // 2, self.HEIGHT // 2 - self.BALL_SIZE // 2, self.BALL_SIZE, self.BALL_SIZE)

        # speed
        self.ball_speed_x = 7 * random.choice((1, -1))
        self.ball_speed_y = 7 * random.choice((1, -1))
        self.paddle_speed = 15

        # scores
        self.score_left = 0
        self.score_right = 0
        
        # font
        self.font = pygame.font.Font(None, 36)
        
    def assign_player(self, player):
        # player_1: "w" and "s"
        # player_2: "up" and "down"
        self.player = player
        
    def draw_score(self):
        score_text = self.font.render(f"{self.score_left} - {self.score_right}", True, WHITE)
        self.screen.blit(score_text, (self.WIDTH // 2 - score_text.get_width() // 2, 20))

    def draw_screen(self):
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, WHITE, self.paddle_left)
        pygame.draw.rect(self.screen, WHITE, self.paddle_right)
        pygame.draw.ellipse(self.screen, WHITE, (self.WIDTH // 2 - 5, 0, 10, self.HEIGHT))
        pygame.draw.ellipse(self.screen, WHITE, (self.WIDTH // 2 - 5, self.HEIGHT - 10, 10, 10))
        pygame.draw.rect(self.screen, WHITE, self.ball)
        self.draw_score()
        pygame.display.update()

    # move paddle
    def move_paddle(self):
        keys = pygame.key.get_pressed()
        
        if self.player == "player_1":
            if keys[pygame.K_w] and self.paddle_left.top > 0:
                self.paddle_left.y -= self.paddle_speed
            if keys[pygame.K_s] and self.paddle_left.bottom < self.HEIGHT:
                self.paddle_left.y += self.paddle_speed
            
            while not self.share_queue.empty():
                op_key = self.share_queue.get()
                if op_key=="up" and self.paddle_right.top > 0:
                    self.paddle_right.y -= self.paddle_speed
                if op_key=="down" and self.paddle_right.bottom < self.HEIGHT:
                    self.paddle_right.y += self.paddle_speed  
        elif self.player == "player_2":
            if keys[pygame.K_UP] and self.paddle_right.top > 0:
                self.paddle_right.y -= self.paddle_speed
            if keys[pygame.K_DOWN] and self.paddle_right.bottom < self.HEIGHT:
                self.paddle_right.y += self.paddle_speed
            
            while not self.share_queue.empty():
                op_key = self.share_queue.get()
                if op_key=="w" and self.paddle_left.top > 0:
                    self.paddle_left.y -= self.paddle_speed
                if op_key=="s" and self.paddle_left.bottom < self.HEIGHT:
                    self.paddle_left.y += self.paddle_speed

    # Hàm xử lý bóng va chạm với tường hoặc paddle
    def move_ball(self):

        self.ball.x += self.ball_speed_x
        self.ball.y += self.ball_speed_y

        # collide with top or bottom wall
        if self.ball.top <= 0 or self.ball.bottom >= self.HEIGHT:
            self.ball_speed_y = -self.ball_speed_y

        # collide with left paddle
        if self.ball.colliderect(self.paddle_left) and self.ball_speed_x < 0:
            self.ball_speed_x = -self.ball_speed_x

        # collide with right paddle
        if self.ball.colliderect(self.paddle_right) and self.ball_speed_x > 0:
            self.ball_speed_x = -self.ball_speed_x

        # ball move out of screen
        if self.ball.left <= 0:
            self.score_right += 1
            self.reset_ball()

        if self.ball.right >= self.WIDTH:
            self.score_left += 1
            self.reset_ball()

    # reset ball to center
    def reset_ball(self):
        self.ball.center = (self.WIDTH // 2, self.HEIGHT // 2)
        self.ball_speed_x = 7 * random.choice((1, -1))
        self.ball_speed_y = 7 * random.choice((1, -1))
        
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.move_paddle()
            self.move_ball()
            self.draw_screen()
            self.clock.tick(60)
        pygame.quit()