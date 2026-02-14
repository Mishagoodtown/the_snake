from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Константы позиции для удобства:
DEFAULT_POSITIONS = (0, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 15

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.

class GameObject:
    """Базовый класс игрового объекта"""

    def __init__(self,
                 position=DEFAULT_POSITIONS,
                 body_color=BOARD_BACKGROUND_COLOR
                 ):
        self.body_color = body_color
        self.position = position

    def draw(self):
        """Метод отрисовки объекта"""
        raise NotImplementedError(
            'Метод draw() должен быть реализован в дочернем классе'
        )


class Apple(GameObject):
    """Класс яблока"""

    def __init__(self, occupied_positions=None):
        super().__init__(position=DEFAULT_POSITIONS, body_color=APPLE_COLOR)
        if occupied_positions is None:
            occupied_positions = []
        self.randomize_position(occupied_positions)

    def randomize_position(self, snake_positions):
        """Метод случайного размещения яблока на поле"""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if self.position not in snake_positions:
                break

    def draw(self):
        """Метод отрисовки яблока"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки"""

    def __init__(self):
        super().__init__((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), SNAKE_COLOR)
        self.reset()

    def get_head_position(self):
        """Метод получения позиции головы змейки"""
        return self.positions[0]

    def turn(self, direction):
        """Метод изменения направления движения змейки"""
        direction_vector_x, direction_vector_y = direction
        if (-direction_vector_x, -direction_vector_y) == self.direction:
            return
        self.next_direction = direction

    def move(self):
        """Метод движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        current_x, current_y = self.get_head_position()
        x, y = self.direction

        # Вычисление новой позиции головы змейки
        #  с учетом выхода за границы экрана
        new = (
            (current_x + (x * GRID_SIZE)) % SCREEN_WIDTH,
            (current_y + (y * GRID_SIZE)) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, new)
        if self.grow > 0:
            self.grow -= 1
        else:
            self.last = self.positions.pop()

    def reset(self):
        """Метод сброса змейки в начальное положение и состояние"""
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None
        self.grow = 0

    def draw(self):
        """Метод отрисовки змейки"""
        # Отрисовка тела змейки
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 10)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция игры"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    screen.fill(BOARD_BACKGROUND_COLOR)

    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Тут опишите основную логику игры.
        if snake.get_head_position() == apple.position:
            snake.grow += 1
            apple.randomize_position(snake.positions)
        # Проверка столкновения с самим собой
        elif snake.get_head_position() in snake.positions[4:]:
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
