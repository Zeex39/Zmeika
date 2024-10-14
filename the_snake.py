import pygame
import random
import sys

# Константы
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BOARD_BACKGROUND_COLOR = (50, 50, 50)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

ALL_CELLS = set((x * GRID_SIZE, y * GRID_SIZE) for x in range(GRID_WIDTH)
                for y in range(GRID_HEIGHT))

# Глобальные переменные
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=(0, 0)):
        """
        Инициализация объекта.

        :param position: Позиция объекта на экране.
        """
        self.position = position
        self.body_color = None

    def draw(self, screen):
        """Метод для отрисовки объекта."""
        pass


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self, snake_positions=None):
        """
        Инициализация яблока с генерацией случайной позиции.

        :param snake_positions: Позиции змейки, которые нужно исключить.
        """
        if snake_positions is None:
            snake_positions = []
        super().__init__(self.randomize_position(snake_positions))
        self.body_color = RED

    def randomize_position(self, snake_positions):
        """
        Установка случайной позиции яблока, исключая позицию змейки.

        :param snake_positions: Позиции змейки, которые нужно исключить.
        :return: Случайная свободная позиция для яблока.
        """
        free_cells = ALL_CELLS - set(snake_positions)
        return random.choice(list(free_cells))

    def draw(self, screen):
        """Отрисовка яблока."""
        pygame.draw.rect(screen, self.body_color,
                         pygame.Rect(self.position[0], self.position[1],
                                     GRID_SIZE, GRID_SIZE))


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self):
        """Инициализация змейки."""
        super().__init__((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = GREEN
        self.grow_pending = False

    def update_direction(self, new_direction):
        """
        Обновление направления, не допуская обратного хода.

        :param new_direction: Новое направление движения.
        """
        if new_direction:
            x, y = new_direction
            current_x, current_y = self.direction
            if (x, y) != (-current_x, -current_y):
                self.direction = new_direction

    def move(self):
        """Движение змейки и обновление позиции."""
        head_x, head_y = self.positions[0]
        new_head = ((head_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
                    (head_y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT)

        if self.grow_pending:
            self.positions.insert(0, new_head)
            self.grow_pending = False
        else:
            self.positions = [new_head] + self.positions[:-1]

        # Проверка на самоукус
        if len(self.positions) > 1 and new_head in self.positions[1:]:
            self.reset()

    def grow(self):
        """Увеличение длины змейки."""
        self.grow_pending = True

    def reset(self):
        """Сброс змейки до одной головы при самоукусе."""
        self.positions = [self.position]

    def draw(self, screen):
        """Отрисовка змейки."""
        for pos in self.positions:
            pygame.draw.rect(screen, self.body_color,
                             pygame.Rect(pos[0], pos[1], GRID_SIZE, GRID_SIZE))

    def get_head_position(self):
        """Возврат позиции головы змейки."""
        return self.positions[0]


def handle_keys(snake):
    """Обработка событий."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_UP:
                snake.update_direction(UP)
            elif event.key == pygame.K_DOWN:
                snake.update_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.update_direction(RIGHT)


def game_loop():
    """Основной игровой цикл."""
    pygame.display.set_caption('Змейка')

    snake = Snake()
    apple = Apple(snake.positions)
    score = 0
    record = 0

    while True:
        handle_keys(snake)

        # Движение змейки
        snake.move()

        # Проверка столкновения с яблоком
        if snake.get_head_position() == apple.position:
            snake.grow()
            score += 1
            apple = Apple(snake.positions)  # Новое яблоко
            if score > record:
                record = score

        # Обновление экрана
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()

        # Замедление змейки
        clock.tick(10)


def main():
    """Точка входа в игру."""
    pygame.init()
    game_loop()


if __name__ == '__main__':
    main()
