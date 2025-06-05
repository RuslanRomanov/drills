import pygame
import random

import pygame.draw

# Инициализация Pygame и шрифтов
pygame.init()
pygame.font.init()


# Константы для размеров поля и карты
FIELD_WIDTH = 51 # Ширина одного поля в пикселях
FIELD_HEIGHT = 51 # Высота одного поля в пикселях
MAP_WIDTH_IN_FIELDS = 14 # Ширина карты в полях
MAP_HEIGHT_IN_FIELDS = 14 # Высота карты в полях
MAP_WIDTH = MAP_WIDTH_IN_FIELDS * FIELD_WIDTH # Ширина карты в пикселях
MAP_HEIGHT = MAP_HEIGHT_IN_FIELDS * FIELD_HEIGHT # Высота карты в пикселях
MAP_X_CENTRAL = MAP_WIDTH // 2 # Центр карты по X
MAP_SQUARE_IN_FIELDS = MAP_WIDTH_IN_FIELDS * MAP_HEIGHT_IN_FIELDS # Общее количество полей

# Параметры игры
WALLS_MAX_NUMBER = MAP_SQUARE_IN_FIELDS * 1 // 5 # Максимальное количество внутренних стен
PLAYER_DRILLS_NUMBER = 5 # Количество буров у каждого игрока
TURN_DELAY = 1000 # Задержка хода в миллисекундах

# Цвета
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (185, 122, 87)
YELLOW = (255, 242, 0)
YELLOW2 = (255, 255, 128)
GREY = (192, 192, 192)
GREY2 = (128, 128, 128)


class Text():
    """Класс для работы с текстовыми элементами"""
    def __init__(self, x_central, y_central, text, text_color, font, font_size, surface_color):
        self.x_central = x_central # Центр текста по X
        self.y_central = y_central # Центр текста по Y
        self.text = text # Текст
        self.text_color = text_color # Цвет текста
        self.font = font # Шрифт
        self.font_size = font_size # Размер шрифта
        self.surface_color = surface_color # Цвет фона
        self.Font_with_size = pygame.font.SysFont(self.font, self.font_size) # Объект шрифта
        self.surface = self.Font_with_size.render(self.text, False, self.text_color) # Поверхность с текстом
        self.width = self.surface.get_width() # Ширина текста
        self.height = self.surface.get_height() # Высота текста
        self.x_left = self.x_central - self.width // 2 # Левая граница
        self.y_up = self.y_central - self.height // 2 # Верхняя граница
        self.x_right = self.x_central + self.width // 2 # Правая граница
        self.y_down = self.y_central + self.height // 2 # Нижняя граница


class Player():
    """Класс игрока для хранения его состояния"""
    def __init__(self, game_points, last_game_result, turn, destroyed_drills):
        self.game_points = game_points # Очки игрока
        self.last_game_result = last_game_result # Результат последней игры
        self.turn = turn # Активность хода (True, False)
        self.destroyed_drills = destroyed_drills # Количество уничтоженных буров


class Game_object():
    """Класс для игровых объектов"""
    def __init__(self, name, drill_position, color, death):
        self.name = name # Тип объекта ("wall", "drill", "empty field")
        self.drill_position = drill_position # Направление бура
        self.color = color # Цвет объекта
        self.death = death # Состояние


def draw_menu(screen, menu_texts):
    """Отрисовка меню игры"""
    screen.fill(YELLOW2) # Заливка фона
    
    # Отрисовка всех текстовых элементов меню
    for i in range(len(menu_texts)):
        pygame.draw.rect(screen, menu_texts[i].surface_color, (menu_texts[i].x_left, menu_texts[i].y_up, menu_texts[i].width, menu_texts[i].height))
        screen.blit(menu_texts[i].surface, (menu_texts[i].x_left, menu_texts[i].y_up))
    
    pygame.display.update() # Обновление экрана


def choose_announcement_of_the_winer_text(players):
    """Выбор текста объявления победителя"""
    if players[0].last_game_result == "the were no matches":
        announcement_of_the_winer_text = "Ещё не было игр!"
    elif players[0].last_game_result == "draw":
        announcement_of_the_winer_text = "Ничья!"
    elif players[0].last_game_result == "won":
        announcement_of_the_winer_text = "Победил синий игрок!"
    else:
        announcement_of_the_winer_text = "Победил красный игрок!"

    return announcement_of_the_winer_text


def react_on_actions_in_menu(screen, menu_texts, players):
    """Обработка действий в меню"""
    was_action = False
    while not was_action:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Выход из игры
                was_action = True
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONUP: # Отпускание кнопки мыши
                if event.button == 1: # Левая кнопка мыши
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # Проверка клика по кнопке "Играть"
                    if mouse_x >= menu_texts[0].x_left and mouse_x <= menu_texts[0].x_right and mouse_y >= menu_texts[0].y_up and mouse_y <= menu_texts[0].y_down:
                        was_action = True
                        game(screen, players) # Запуск игры


def menu(screen, players):
    """Создание меню игры"""
    menu_texts = []
    # Создание элементов меню
    menu_texts.append(Text(MAP_X_CENTRAL, MAP_HEIGHT * 5 // 6, "Играть", BLACK, None, 120, GREEN))
    menu_texts.append(Text(MAP_X_CENTRAL, MAP_HEIGHT * 1 // 6, choose_announcement_of_the_winer_text(players), BLACK, None, 70, GREEN))
    menu_texts.append(Text(MAP_X_CENTRAL, MAP_HEIGHT * 3 // 6, ":", BLACK, None, 120, GREEN))
    score_text_margin = 75
    menu_texts.append(Text(MAP_X_CENTRAL - score_text_margin, MAP_HEIGHT * 3 // 6, str(players[0].game_points), BLUE, None, 120, GREEN))
    menu_texts.append(Text(MAP_X_CENTRAL + score_text_margin, MAP_HEIGHT * 3 // 6, str(players[1].game_points), RED, None, 120, GREEN))
    
    draw_menu(screen, menu_texts) # Отрисовка меню
    react_on_actions_in_menu(screen, menu_texts, players) # Обработка действий


def choose_drill_color(drill):
    """Выбор цвета бура"""
    if drill.color == "blue":
        drill_color = BLUE
    else:
        drill_color = RED

    return drill_color


def choose_tower_color(drill):
    """Выбор цвета башни бура"""
    if drill.death == "dead":
        tower_color = YELLOW
    else:
        tower_color = GREY
    
    return tower_color


def choose_walls_color(players):
    """Выбор цвета стен в зависимости от текущего игрока"""
    if players[0].turn:
        walls_color = BLUE
    else:
        walls_color = RED

    return walls_color


def draw_wall(screen, wall_color, wall_x_left, wall_y_up):
    """Отрисовка стены"""
    pygame.draw.rect(screen, BLACK, (wall_x_left, wall_y_up, FIELD_WIDTH, FIELD_HEIGHT)) # Черный контур

    # Рисуем узор стены (10 сегментов)
    pygame.draw.rect(screen, wall_color, (wall_x_left + 1, wall_y_up + 1, 24, 11))
    pygame.draw.rect(screen, wall_color, (wall_x_left + 27, wall_y_up + 1, 23, 11))
    pygame.draw.rect(screen, wall_color, (wall_x_left, wall_y_up + 14, 12, 10))
    pygame.draw.rect(screen, wall_color, (wall_x_left + 14, wall_y_up + 14, 23, 10))
    pygame.draw.rect(screen, wall_color, (wall_x_left + 39, wall_y_up + 14, 12, 10))
    pygame.draw.rect(screen, wall_color, (wall_x_left + 1, wall_y_up + 26, 24, 11))
    pygame.draw.rect(screen, wall_color, (wall_x_left + 27, wall_y_up + 26, 23, 11))
    pygame.draw.rect(screen, wall_color, (wall_x_left, wall_y_up + 39, 12, 11))
    pygame.draw.rect(screen, wall_color, (wall_x_left + 14, wall_y_up + 39, 23, 11))
    pygame.draw.rect(screen, wall_color, (wall_x_left + 39, wall_y_up + 39, 12, 11))


def draw_drill(screen, drill, drill_x_left, drill_y_up):
    """Отрисовка бура в зависимости от его направления"""
    drill_x_right = drill_x_left + FIELD_WIDTH - 1
    drill_y_down = drill_y_up + FIELD_HEIGHT - 1

    drill_color = choose_drill_color(drill)
    tower_color = choose_tower_color(drill)

    # Отрисовка в зависимости от направления
    if drill.drill_position == "up":
        # Рисуем сверло (направлено вверх)
        pygame.draw.polygon(screen, GREY, [[drill_x_left + 20 + 5, drill_y_up], [drill_x_left + 20, drill_y_up + 15], [drill_x_left + 20 + 10, drill_y_up + 15]])

        # Детали сверла
        pygame.draw.line(screen, GREY2, (drill_x_left + 20 + 4, drill_y_up + 3), (drill_x_left + 20 + 7, drill_y_up + 6))
        pygame.draw.line(screen, GREY2, (drill_x_left + 20 + 3, drill_y_up + 6), (drill_x_left + 20 + 9, drill_y_up + 12))
        pygame.draw.line(screen, GREY2, (drill_x_left + 20 + 2, drill_y_up + 9), (drill_x_left + 20 + 8, drill_y_up + 15))
        pygame.draw.line(screen, GREY2, (drill_x_left + 20 + 1, drill_y_up + 12), (drill_x_left + 20 + 4, drill_y_up + 15))

        # Основной корпус
        pygame.draw.rect(screen, drill_color, (drill_x_left + 15, drill_y_up + 15, 21, 31))

        # Колёса
        pygame.draw.rect(screen, BLACK, (drill_x_left + 10, drill_y_up + 18, 5, 10))
        pygame.draw.rect(screen, BLACK, (drill_x_left + 10, drill_y_up + 33, 5, 10))
        pygame.draw.rect(screen, BLACK, (drill_x_left + 36, drill_y_up + 18, 5, 10))
        pygame.draw.rect(screen, BLACK, (drill_x_left + 36, drill_y_up + 33, 5, 10))

        # Крепежные болты
        pygame.draw.circle(screen, GREY, (drill_x_left + 20, drill_y_up + 20), 2)
        pygame.draw.circle(screen, GREY, (drill_x_left + 20, drill_y_up + 40), 2)
        pygame.draw.circle(screen, GREY, (drill_x_left + 30, drill_y_up + 20), 2)
        pygame.draw.circle(screen, GREY, (drill_x_left + 30, drill_y_up + 40), 2)

        # Башня
        pygame.draw.circle(screen, tower_color, (drill_x_left + 25, drill_y_up + 30), 5)
    elif drill.drill_position == "down":
        # Рисуем сверло (направлено вниз)
        pygame.draw.polygon(screen, GREY, [[drill_x_left + 25, drill_y_down], [drill_x_left + 20, drill_y_down - 15], [drill_x_left + 30, drill_y_down - 15]])
        
        # Детали сверла
        pygame.draw.line(screen, GREY2, (drill_x_left + 26, drill_y_down - 3), (drill_x_left + 23, drill_y_down - 6))
        pygame.draw.line(screen, GREY2, (drill_x_left + 27, drill_y_down - 6), (drill_x_left + 21, drill_y_down - 12))
        pygame.draw.line(screen, GREY2, (drill_x_left + 28, drill_y_down - 9), (drill_x_left + 22, drill_y_down - 15))
        pygame.draw.line(screen, GREY2, (drill_x_left + 29, drill_y_down - 12), (drill_x_left + 26, drill_y_down - 15))

        # Основной корпус
        pygame.draw.rect(screen, drill_color, (drill_x_left + 15, drill_y_down - 46, 21, 31))
        
        # Колёса
        pygame.draw.rect(screen, BLACK, (drill_x_left + 10, drill_y_down - 43, 5, 10))
        pygame.draw.rect(screen, BLACK, (drill_x_left + 10, drill_y_down - 28, 5, 10))
        pygame.draw.rect(screen, BLACK, (drill_x_left + 36, drill_y_down - 43, 5, 10))
        pygame.draw.rect(screen, BLACK, (drill_x_left + 36, drill_y_down - 28, 5, 10))

        # Крепежные болты
        pygame.draw.circle(screen, GREY, (drill_x_left + 20, drill_y_down - 41), 2)
        pygame.draw.circle(screen, GREY, (drill_x_left + 20, drill_y_down - 21), 2)
        pygame.draw.circle(screen, GREY, (drill_x_left + 30, drill_y_down - 41), 2)
        pygame.draw.circle(screen, GREY, (drill_x_left + 30, drill_y_down - 21), 2)

        # Башня
        pygame.draw.circle(screen, tower_color, (drill_x_left + 25, drill_y_down - 31), 5)
    elif drill.drill_position == "left":
        # Рисуем сверло (направлено влево)
        pygame.draw.polygon(screen, GREY, [[drill_x_left, drill_y_up + 25], [drill_x_left + 15, drill_y_up + 20], [drill_x_left + 15, drill_y_up + 30]])
        
        # Детали сверла
        pygame.draw.line(screen, GREY2, (drill_x_left + 3, drill_y_up + 26), (drill_x_left + 6, drill_y_up + 23))
        pygame.draw.line(screen, GREY2, (drill_x_left + 6, drill_y_up + 27), (drill_x_left + 12, drill_y_up + 21))
        pygame.draw.line(screen, GREY2, (drill_x_left + 9, drill_y_up + 28), (drill_x_left + 15, drill_y_up + 22))
        pygame.draw.line(screen, GREY2, (drill_x_left + 12, drill_y_up + 29), (drill_x_left + 15, drill_y_up + 26))

        # Основной корпус
        pygame.draw.rect(screen, drill_color, (drill_x_left + 15, drill_y_up + 15, 31, 21))
        
        # Колёса
        pygame.draw.rect(screen, BLACK, (drill_x_left + 18, drill_y_up + 10, 10, 5))
        pygame.draw.rect(screen, BLACK, (drill_x_left + 33, drill_y_up + 10, 10, 5))
        pygame.draw.rect(screen, BLACK, (drill_x_left + 18, drill_y_up + 36, 10, 5))
        pygame.draw.rect(screen, BLACK, (drill_x_left + 33, drill_y_up + 36, 10, 5))

        # Крепежные болты
        pygame.draw.circle(screen, GREY, (drill_x_left + 20, drill_y_up + 20), 2)
        pygame.draw.circle(screen, GREY, (drill_x_left + 40, drill_y_up + 20), 2)
        pygame.draw.circle(screen, GREY, (drill_x_left + 20, drill_y_up + 30), 2)
        pygame.draw.circle(screen, GREY, (drill_x_left + 40, drill_y_up + 30), 2)

        # Башня
        pygame.draw.circle(screen, tower_color, (drill_x_left + 30, drill_y_up + 25), 5)
    else:
        # Рисуем сверло (направлено вправо)
        pygame.draw.polygon(screen, GREY, [[drill_x_right, drill_y_up + 25], [drill_x_right - 15, drill_y_up + 20], [drill_x_right - 15, drill_y_up + 30]])
        
        # Детали сверла
        pygame.draw.line(screen, GREY2, (drill_x_right - 3, drill_y_up + 24), (drill_x_right - 6, drill_y_up + 27))
        pygame.draw.line(screen, GREY2, (drill_x_right - 6, drill_y_up + 23), (drill_x_right - 12, drill_y_up + 29))
        pygame.draw.line(screen, GREY2, (drill_x_right - 9, drill_y_up + 22), (drill_x_right - 15, drill_y_up + 28))
        pygame.draw.line(screen, GREY2, (drill_x_right - 12, drill_y_up + 21), (drill_x_right - 15, drill_y_up + 24))

        # Основной корпус
        pygame.draw.rect(screen, drill_color, (drill_x_right - 46, drill_y_up + 15, 31, 21))
        
        # Колёса
        pygame.draw.rect(screen, BLACK, (drill_x_right - 28, drill_y_up + 10, 10, 5))
        pygame.draw.rect(screen, BLACK, (drill_x_right - 43, drill_y_up + 10, 10, 5))
        pygame.draw.rect(screen, BLACK, (drill_x_right - 28, drill_y_up + 36, 10, 5))
        pygame.draw.rect(screen, BLACK, (drill_x_right - 43, drill_y_up + 36, 10, 5))

        # Крепежные болты
        pygame.draw.circle(screen, GREY, (drill_x_right - 41, drill_y_up + 20), 2)
        pygame.draw.circle(screen, GREY, (drill_x_right - 21, drill_y_up + 20), 2)
        pygame.draw.circle(screen, GREY, (drill_x_right - 41, drill_y_up + 30), 2)
        pygame.draw.circle(screen, GREY, (drill_x_right - 21, drill_y_up + 30), 2)

        # Башня
        pygame.draw.circle(screen, tower_color, (drill_x_right - 31, drill_y_up + 25), 5)

def draw_game(screen, players, objects, Menu_text):
    """Отрисовка игрового поля"""
    screen.fill(BROWN) # Заливка земли
    
    walls_color = choose_walls_color(players)
    
    # Проход по всем полям карты
    for i in range(MAP_HEIGHT_IN_FIELDS):
        for j in range(MAP_WIDTH_IN_FIELDS):
            object_x_left = j * FIELD_WIDTH
            object_y_up = i * FIELD_HEIGHT
            if objects[i][j].name == "wall": # Если стена
                draw_wall(screen, walls_color, object_x_left, object_y_up)
            elif objects[i][j].name == "drill": # Если бур
                draw_drill(screen, objects[i][j], object_x_left, object_y_up)

    # Если есть разрушенные буры - показываем кнопку меню                
    if players[0].destroyed_drills > 0 or players[1].destroyed_drills > 0:
        pygame.draw.rect(screen, Menu_text.surface_color, (Menu_text.x_left, Menu_text.y_up, Menu_text.width, Menu_text.height))
        screen.blit(Menu_text.surface, (Menu_text.x_left, Menu_text.y_up))

    pygame.display.update() # Обновление экрана


def create_walls(objects):
    """Создание стен на карте"""
    # Граничные стены по периметру
    for j in range(MAP_WIDTH_IN_FIELDS):
        objects[0][j] = Game_object("wall", "no drill", "no color", "inanimate")
        objects[MAP_HEIGHT_IN_FIELDS - 1][j] = Game_object("wall", "no drill", "no color", "inanimate")

    for i in range(1, MAP_HEIGHT_IN_FIELDS - 1):
        objects[i][0] = Game_object("wall", "no drill", "no color", "inanimate")
        objects[i][MAP_WIDTH_IN_FIELDS - 1] = Game_object("wall", "no drill", "no color", "inanimate")

    # Случайные стены внутри карты
    for i in range(WALLS_MAX_NUMBER):
        wall_x_random = random.randint(1, MAP_WIDTH_IN_FIELDS - 2)
        wall_y_random = random.randint(1, MAP_HEIGHT_IN_FIELDS - 2)
        objects[wall_y_random][wall_x_random] = Game_object("wall", "no drill", "no color", "inanimate")

    return objects


def check_the_possibility_of_drill_placement(objects, drill_x, drill_y, drill_color_text):
    """Проверка возможности размещения бура в заданной позиции"""
    possibility_of_drill_placement = True

    # Проверка что поле пустое
    if objects[drill_y][drill_x].name != "empty field":
        possibility_of_drill_placement = False

    # Проверка соседних клеток (вражеские буры не должны быть рядом)
    if (objects[drill_y - 1][drill_x].name == "drill" and objects[drill_y - 1][drill_x].color != drill_color_text) or (objects[drill_y + 1][drill_x].name == "drill" and objects[drill_y + 1][drill_x].color != drill_color_text) or (objects[drill_y][drill_x - 1].name == "drill" and objects[drill_y][drill_x - 1].color != drill_color_text) or (objects[drill_y][drill_x + 1].name == "drill" and objects[drill_y][drill_x + 1].color != drill_color_text):
        possibility_of_drill_placement = False

    # Проверка буров через одну клетку
    if drill_y > 1:
        if objects[drill_y - 2][drill_x].name == "drill" and objects[drill_y - 2][drill_x].color != drill_color_text:
            possibility_of_drill_placement = False
    if drill_y < MAP_HEIGHT_IN_FIELDS - 2:
        if objects[drill_y + 2][drill_x].name == "drill" and objects[drill_y + 2][drill_x].color != drill_color_text:
            possibility_of_drill_placement = False
    if drill_x > 1:
        if objects[drill_y][drill_x - 2].name == "drill" and objects[drill_y][drill_x - 2].color != drill_color_text:
            possibility_of_drill_placement = False
    if drill_x < MAP_WIDTH_IN_FIELDS - 2:
        if objects[drill_y][drill_x + 2].name == "drill" and objects[drill_y][drill_x + 2].color != drill_color_text:
            possibility_of_drill_placement = False

    # Проверка по диагонали
    if (objects[drill_y - 1][drill_x - 1].name == "drill" and objects[drill_y - 1][drill_x - 1].color != drill_color_text) or (objects[drill_y + 1][drill_x + 1].name == "drill" and objects[drill_y + 1][drill_x + 1].color != drill_color_text) or (objects[drill_y - 1][drill_x + 1].name == "drill" and objects[drill_y - 1][drill_x + 1].color != drill_color_text) or (objects[drill_y + 1][drill_x - 1].name == "drill" and objects[drill_y + 1][drill_x - 1].color != drill_color_text):
        possibility_of_drill_placement = False
    
    return possibility_of_drill_placement


def choose_drill_color_text(player_index):
    """Выбор цвета бура в текстовом формате по индексу игрока"""
    if player_index == 0:
        drill_color_text = "blue"
    else:
        drill_color_text = "red"

    return drill_color_text


def find_enemy_drill(objects, visited_objects, x, y, friendly_drill_color_text):
    """Рекурсивный поиск вражеских буров (для проверки связи)"""
    if objects[y][x].name == "wall" or visited_objects[y][x] != "not visited":
        return visited_objects
    
    visited_objects[y][x] = "visited"

    # Если нашли вражеский бур
    if objects[y][x].name == "drill" and objects[y][x].color != friendly_drill_color_text:
        visited_objects[y][x] = "enemy drill found"
        return visited_objects

    # Рекурсивный поиск в четырех направлениях
    visited_objects = find_enemy_drill(objects, visited_objects, x - 1, y, friendly_drill_color_text)
    visited_objects = find_enemy_drill(objects, visited_objects, x + 1, y, friendly_drill_color_text)
    visited_objects = find_enemy_drill(objects, visited_objects, x, y - 1, friendly_drill_color_text)
    visited_objects = find_enemy_drill(objects, visited_objects, x, y + 1, friendly_drill_color_text)

    return visited_objects


def check_communication_with_enemy_drills(objects, friendly_drill_x, friendly_drill_y, friendly_drill_color_text):
    """Проверка связи с вражескими бурами (чтобы игроки не были изолированы)"""
    visited_objects = [["not visited" for j in range(MAP_WIDTH_IN_FIELDS)] for i in range(MAP_HEIGHT_IN_FIELDS)]
    communication_with_enemy_drills = False
    visited_objects = find_enemy_drill(objects, visited_objects, friendly_drill_x, friendly_drill_y, friendly_drill_color_text)

    # Проверка результатов поиска
    for i in range(MAP_HEIGHT_IN_FIELDS):
        for j in range(MAP_WIDTH_IN_FIELDS):
            if visited_objects[i][j] == "enemy drill found":
                communication_with_enemy_drills = True
    
    return communication_with_enemy_drills


def choose_drill_position():
    """Случайный выбор направления для нового бура"""
    possible_drill_positions = ["left", "right", "up", "down"]
    random_drill_position_index = random.randint(0, len(possible_drill_positions) - 1)
    drill_position = possible_drill_positions[random_drill_position_index]
    return drill_position


def create_drills(players, objects):
    """Создание буров для обоих игроков"""
    for i in range(PLAYER_DRILLS_NUMBER):
        for player_index in range(len(players)):
            drill_created = False
            drill_color_text = choose_drill_color_text(player_index)
            while not drill_created:
                # Случайные координаты
                drill_x_random = random.randint(1, MAP_WIDTH_IN_FIELDS - 2)
                drill_y_random = random.randint(1, MAP_HEIGHT_IN_FIELDS - 2)
                # Проверка возможности размещения
                drill_created = check_the_possibility_of_drill_placement(objects, drill_x_random, drill_y_random, drill_color_text)
                # Для последнего бура проверяем связь с противником
                if drill_created and player_index == len(players) - 1 and i == PLAYER_DRILLS_NUMBER - 1:
                    drill_created = check_communication_with_enemy_drills(objects, drill_x_random, drill_y_random, drill_color_text)

            # Создание бура
            objects[drill_y_random][drill_x_random] = Game_object("drill", choose_drill_position(), drill_color_text, "alive")
    
    return objects


def read_action_in_game(players):
    """Чтение действий игрока с таймером"""
    possible_actions = ["up", "down", "left", "right"]
    # Случайное действие по умолчанию (если время вышло)
    random_action_index = random.randint(0, len(possible_actions) - 1)
    action = possible_actions[random_action_index]
    start_time = pygame.time.get_ticks()
    end_time = start_time + TURN_DELAY
    current_time = start_time

    # Ожидание действия в течение TURN_DELAY
    while action != "quit" and current_time <= end_time:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                action = "quit"
                
            elif event.type == pygame.KEYUP:
                if players[0].turn: # Управление для синего игрока (WASD)
                    if event.key == pygame.K_w:
                        action = "up"
                    elif event.key == pygame.K_s:
                        action = "down"
                    elif event.key == pygame.K_a:
                        action = "left"
                    elif event.key == pygame.K_d:
                        action = "right"
                    
                else: # Управление для красного игрока (стрелки)
                    if event.key == pygame.K_UP:
                        action = "up"
                    elif event.key == pygame.K_DOWN:
                        action = "down"
                    elif event.key == pygame.K_LEFT:
                        action = "left"
                    elif event.key == pygame.K_RIGHT:
                        action = "right"
        
        current_time = pygame.time.get_ticks()

    return action


def move_drill(objects, action, drill_x, drill_y):
    """Перемещение бура в заданном направлении"""
    if action == "up":
        objects[drill_y][drill_x].drill_position = "up" # Меняем направление бура
        # Проверка что целевая клетка свободна
        if objects[drill_y - 1][drill_x].name == "empty field":
             # Перемещение бура
            objects[drill_y - 1][drill_x] = objects[drill_y][drill_x]
            objects[drill_y][drill_x] = Game_object("empty field", "no drill", "no color", "inanimate")

    elif action == "down":
        objects[drill_y][drill_x].drill_position = "down" # Меняем направление бура
        # Проверка что целевая клетка свободна
        if objects[drill_y + 1][drill_x].name == "empty field":
            # Перемещение бура
            objects[drill_y + 1][drill_x] = objects[drill_y][drill_x]
            objects[drill_y][drill_x] = Game_object("empty field", "no drill", "no color", "inanimate")

    elif action == "left":
        objects[drill_y][drill_x].drill_position = "left" # Меняем направление бура
        # Проверка что целевая клетка свободна
        if objects[drill_y][drill_x - 1].name == "empty field":
            # Перемещение бура
            objects[drill_y][drill_x - 1] = objects[drill_y][drill_x]
            objects[drill_y][drill_x] = Game_object("empty field", "no drill", "no color", "inanimate")

    else: # "right"
        objects[drill_y][drill_x].drill_position = "right" # Меняем направление бура
        # Проверка что целевая клетка свободна
        if objects[drill_y][drill_x + 1].name == "empty field":
            # Перемещение бура
            objects[drill_y][drill_x + 1] = objects[drill_y][drill_x]
            objects[drill_y][drill_x] = Game_object("empty field", "no drill", "no color", "inanimate")
            
    return objects


def react_on_actions_in_game(players, objects, action):
    """Обработка действий во время игры"""
    if action == "quit":
        pygame.quit() # Выход из игры
    else:
        # Определение порядка обхода в зависимости от действия
        if action == "up" or action == "left":
            # Обход сверху вниз, слева направо
            start_cycle_in_height = 0
            end_cycle_in_height = MAP_HEIGHT_IN_FIELDS
            step_cycle_in_height = 1
            start_cycle_in_width = 0
            end_cycle_in_width = MAP_WIDTH_IN_FIELDS
            step_cycle_in_width = 1
        else:
            # Обход снизу вверх, справа налево
            start_cycle_in_height = MAP_HEIGHT_IN_FIELDS - 1
            end_cycle_in_height = -1
            step_cycle_in_height = -1
            start_cycle_in_width = MAP_WIDTH_IN_FIELDS - 1
            end_cycle_in_width = -1
            step_cycle_in_width = -1

        # Обход всех клеток в заданном порядке
        for i in range(start_cycle_in_height, end_cycle_in_height, step_cycle_in_height):
            for j in range(start_cycle_in_width, end_cycle_in_width, step_cycle_in_width):
                if objects[i][j].name == "drill" and ((players[0].turn and objects[i][j].color == "blue") or (players[1].turn and objects[i][j].color == "red")):
                    objects = move_drill(objects, action, j, i) # Перемещение

    return objects


def check_drills_on_destruction(objects):
    """Проверка буров на уничтожение"""
    for i in range(1, MAP_HEIGHT_IN_FIELDS - 1):
        for j in range(1, MAP_WIDTH_IN_FIELDS - 1):
            if objects[i][j].name == "drill":
                # Проверка наличия рядом вражеского бура, направленного на текущий
                if (objects[i - 1][j].name == "drill" and objects[i - 1][j].color != objects[i][j].color and objects[i - 1][j].drill_position == "down") or (objects[i + 1][j].name == "drill" and objects[i + 1][j].color != objects[i][j].color and objects[i + 1][j].drill_position == "up") or (objects[i][j - 1].name == "drill" and objects[i][j - 1].color != objects[i][j].color and objects[i][j - 1].drill_position == "right") or (objects[i][j + 1].name == "drill" and objects[i][j + 1].color != objects[i][j].color and objects[i][j + 1].drill_position == "left"):
                    objects[i][j].death = "dead" # Помечаем как уничтоженный

    return objects


def check_players_on_destroyed_drills(players, objects):
    """Подсчет уничтоженных буров для каждого игрока"""
    for i in range(1, MAP_HEIGHT_IN_FIELDS - 1):
        for j in range(1, MAP_WIDTH_IN_FIELDS - 1):
            if objects[i][j].name == "drill" and objects[i][j].death == "dead":
                if objects[i][j].color == "blue":
                    players[0].destroyed_drills += 1 # Синий игрок
                else:
                    players[1].destroyed_drills += 1 # Красный игрок

    return players


def change_players_specifications(players):
    """Обновление состояния игроков после игрового раунда"""
    # Определение победителя по количеству разрушенных буров
    if players[0].destroyed_drills < players[1].destroyed_drills:
        players[0].game_points += 1
        players[0].last_game_result = "won"
        players[1].last_game_result = "lost"
    elif players[0].destroyed_drills > players[1].destroyed_drills:
        players[1].game_points += 1
        players[1].last_game_result = "won"
        players[0].last_game_result = "lost"
    else: # Ничья
        players[0].last_game_result = "draw"
        players[1].last_game_result = "draw"

    # Сброс параметров для нового игрового раунда
    players[0].turn = True
    players[1].turn = False
    
    for i in range(len(players)):
        players[i].destroyed_drills = 0

    return players


def react_on_actions_after_game(screen, players, Menu_text):
    """Обработка действий после окончания игрового раунда"""
    was_action = False
    while not was_action:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Выход
                was_action = True
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONUP: # Отпускание кнопки мыши
                if event.button == 1: # Левая кнопка
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x >= Menu_text.x_left and mouse_x <= Menu_text.x_right and mouse_y >= Menu_text.y_up and mouse_y <= Menu_text.y_down:
                        was_action = True
                        menu(screen, players) # Возврат в меню


def change_players_turns(players):
    """Смена активного игрока"""
    if players[0].turn:
        players[1].turn = True
        players[0].turn = False
    else:
        players[0].turn = True
        players[1].turn = False

    return players                 


def game(screen, players):
    """Основная игровая функция"""
    # Инициализация пустой карты
    objects = [[Game_object("empty field", "no drill", "no color", "inanimate") for j in range(MAP_WIDTH_IN_FIELDS)] for i in range(MAP_HEIGHT_IN_FIELDS)]
    objects = create_walls(objects) # Создание стен
    objects = create_drills(players, objects) # Создание буров
    Menu_text = Text(MAP_WIDTH // 2, MAP_HEIGHT - FIELD_HEIGHT // 2, "Меню", BLACK, None, 70, GREEN) # Кнопка меню
    game_running = True # Флаг работы игры

    while game_running:
        draw_game(screen, players, objects, Menu_text) # Отрисовка
        action = read_action_in_game(players) # Получение действия

        if action == "quit": # Выход
            game_running = False

        objects = react_on_actions_in_game(players, objects, action) # Обработка действия
        objects = check_drills_on_destruction(objects) # Проверка на уничтожение буров
        players = check_players_on_destroyed_drills(players, objects) # Подсчет разрушений

        # Если есть разрушенные буры - завершение игры
        if players[0].destroyed_drills > 0 or players[1].destroyed_drills > 0:
            game_running = False
            draw_game(screen, players, objects, Menu_text) # Финальная отрисовка
            players = change_players_specifications(players) # Обновление статистики
            react_on_actions_after_game(screen, players, Menu_text) # Ожидание действия
        
        players = change_players_turns(players) # Смена хода


def main():
    """Главная функция инициализации"""
    screen = pygame.display.set_mode((MAP_WIDTH, MAP_HEIGHT))
    pygame.display.set_caption("Буры") # Название окна

    # Создание игроков
    players = [Player(0, "the were no matches", True, 0), Player(0, "the were no matches", False, 0)]

    # Запуск меню
    menu(screen, players)


# Запуск программы
main()
