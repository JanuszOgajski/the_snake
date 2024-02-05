from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
SCREEN_CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (255, 255, 255)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (200, 30, 30)

# Цвет змейки
SNAKE_COLOR = (30, 200, 30)

# Скорость движения змейки:
SPEED = 3

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """
    Это базовый класс, от которого наследуются другие игровые объекты.
    Он содержит общие атрибуты игровых объектов — например,
    эти атрибуты описывают позицию и цвет объекта.
    """

    def __init__(self, body_color=(0, 0, 0), position=SCREEN_CENTER):
        self.position = [position]
        self.body_color = body_color

    def draw_cell(self, surface, position):
        """Заготовка метода для отрисовки объекта на игровом поле"""
        rect = pygame.Rect(
            position,
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

    def draw(self, surface):
        """Заглушка для автотестов"""
        pass

    def free_cell(self, surface, target_cell):
        """Затирание последнего сегмента"""
        last_rect = pygame.Rect(
            target_cell,
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)


class Apple(GameObject):
    """Класс, описывающий яблоко"""

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color)
        self.randomize_position()

    def randomize_position(self):
        """Яблоко должно отображаться в случайных клетках игрового поля"""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, surface):
        """Отрисовывает яблоко"""
        self.draw_cell(surface, self.position)


class Snake(GameObject):
    """
    Программно змейка — это список координат,
    Каждый элемент списка соответствует отдельному сегменту тела змейки
    """

    def __init__(self, body_color=SNAKE_COLOR, position=SCREEN_CENTER):
        super().__init__(body_color)
        self.reset()
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки (координаты каждой секции)"""
        head_position = self.get_head_position()
        new_position = (
            (head_position[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head_position[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )
        if new_position in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_position)
        if len(self.positions) > self.length:
            self.last = self.positions[-1]
            self.positions.pop()

    def draw(self, surface):
        """отрисовывает змейку на экране, затирая след"""
        # Отрисовка головы змейки
        self.draw_cell(surface, self.positions[0])
        # Затирание последнего сегмента
        if self.last:
            self.free_cell(surface, self.last)

    def get_head_position(self):
        """Возвращает позицию головы змейки"""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние"""
        self.length = 1
        self.positions = [SCREEN_CENTER]
        self.direction = choice((RIGHT, LEFT, UP, DOWN))
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """
    Обрабатывает нажатия клавиш,
    Чтобы изменить направление движения змейки
    """
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
    """Основной игровой цикл"""
    # Тут нужно создать экземпляры классов.
    playable_snake = Snake(SNAKE_COLOR)
    game_apple = Apple(APPLE_COLOR)

    while True:
        clock.tick(SPEED)
    # Тут опишите основную логику игры.
        handle_keys(playable_snake)
        playable_snake.update_direction()
        playable_snake.move()
        if playable_snake.get_head_position() == game_apple.position:
            playable_snake.length += 1
            game_apple.randomize_position()
        playable_snake.draw(screen)
        game_apple.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
