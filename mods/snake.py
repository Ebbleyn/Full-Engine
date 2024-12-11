import pygame
import random

class SnakeGameMod:
    def __init__(self, game):
        self.game = game
        self.cell_size = 20
        self.grid_width = self.game.width // self.cell_size
        self.grid_height = self.game.height // self.cell_size
        self.snake = [(self.grid_width // 2, self.grid_height // 2)]
        self.direction = (1, 0)  # начальное направление движения - вправо
        self.food = self.generate_food()
        self.score = 0
        self.speed = 0.1  # устанавливаем медленную скорость
        self.game_over = False

    def generate_food(self):
        while True:
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            if (x, y) not in self.snake:
                return x, y

    def handle_events(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.direction != (0, 1):
            self.direction = (0, -1)
        elif keys[pygame.K_s] and self.direction != (0, -1):
            self.direction = (0, 1)
        elif keys[pygame.K_a] and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif keys[pygame.K_d] and self.direction != (-1, 0):
            self.direction = (1, 0)
        elif keys[pygame.K_r] and self.game_over:
            self.restart_game()

    def update(self):
        if not self.game_over:
            # Двигаем змейку с учетом скорости
            self.speed -= 0.01  # уменьшаем скорость постепенно
            if self.speed <= 0:
                head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])
                # Проверяем, не врезалась ли змейка сама в себя или в стену
                if (head in self.snake or
                        head[0] < 0 or head[0] >= self.grid_width or
                        head[1] < 0 or head[1] >= self.grid_height):
                    self.game_over = True
                    return
                self.snake.insert(0, head)
                # Проверяем, не съела ли змейка еду
                if head == self.food:
                    self.score += 1
                    self.food = self.generate_food()
                else:
                    self.snake.pop()
                self.speed = 0.1  # сбрасываем скорость

    def render(self):
        # Отрисовываем фон
        self.game.screen.fill((100, 100, 100))

        # Отрисовываем клетки сетки
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                pygame.draw.rect(self.game.screen, (50, 50, 50),
                                 (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size), 1)

        # Отрисовываем змейку
        for segment in self.snake:
            pygame.draw.rect(self.game.screen, (0, 255, 0),
                             (segment[0] * self.cell_size, segment[1] * self.cell_size, self.cell_size, self.cell_size))
        # Отрисовываем еду
        pygame.draw.rect(self.game.screen, (255, 0, 0),
                         (self.food[0] * self.cell_size, self.food[1] * self.cell_size, self.cell_size, self.cell_size))
        # Отрисовываем счет
        font = pygame.font.Font(None, 18)
        score_text = font.render("Score: " + str(self.score), True, (255, 255, 255))
        self.game.screen.blit(score_text, (10, 10))

        # Отрисовываем сообщение о конце игры и кнопку рестарта
        if self.game_over:
            game_over_text = font.render("Game Over! Press 'R' to Restart", True, (255, 255, 255))
            self.game.screen.blit(game_over_text, (self.game.width // 2 - 120, self.game.height // 2 - 10))

    def restart_game(self):
        # Сбрасываем параметры игры
        self.snake = [(self.grid_width // 2, self.grid_height // 2)]
        self.direction = (1, 0)
        self.food = self.generate_food()
        self.score = 0
        self.speed = 0.1
        self.game_over = False

def load(game):
    mod = SnakeGameMod(game)
    return mod
