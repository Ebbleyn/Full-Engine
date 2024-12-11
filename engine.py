import pygame
import sys
import os
import importlib.util
import warnings
import json

# Отключаем вывод предупреждений
warnings.filterwarnings("ignore", category=UserWarning)

class Game:
    def __init__(self, width, height, caption):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self.mods = []
        self.load_config()  # Загрузка конфигурации
        self.background_image = pygame.image.load(os.path.join("images", "image.png")).convert()  # Загрузка заставки
        self.background_image = pygame.transform.scale(self.background_image, (width // 2, height // 2))  # Уменьшение размера заставки
        self.alpha = 255  # Прозрачность заставки
        self.studio_name_text = None
        self.studio_name_alpha = 255  # Прозрачность названия студии

    def load_config(self):
        with open('config.json') as config_file:
            config = json.load(config_file)
            self.studio_name = config.get('studio_name', 'Название студии')
            self.width = config.get('screen_width', self.width)
            self.height = config.get('screen_height', self.height)
            self.screen = pygame.display.set_mode((self.width, self.height))
            window_title = config.get('window_title', 'Default Window Title')
            pygame.display.set_caption(window_title)

            # Загрузка и установка иконки окна, если она указана в конфигурации
            window_icon_path = config.get('window_icon')
            if window_icon_path:
                window_icon = pygame.image.load(os.path.join("icons", window_icon_path))
                pygame.display.set_icon(window_icon)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        for mod in self.mods:
            mod.handle_events()  # Передача обработки событий модам
        return True

    def update(self):
        for mod in self.mods:
            mod.update()

    def render(self):
        self.screen.fill((0, 0, 0))
        # Отрисовка заставки с учетом прозрачности
        self.background_image.set_alpha(self.alpha)
        self.screen.blit(self.background_image, (self.width // 4, self.height // 4))  # Центрирование заставки
        for mod in self.mods:
            mod.render()

        # Отображение названия студии
        if self.studio_name_text:
            text_width, text_height = self.studio_name_text.get_size()
            x = (self.width - text_width) // 2  # Центрирование текста по горизонтали
            y = self.height // 5 - text_height  # Размещение текста над заставкой
            self.studio_name_text.set_alpha(self.studio_name_alpha)
            self.screen.blit(self.studio_name_text, (x, y))

        pygame.display.flip()

    def load_mods(self):
        mods_folder = "mods"
        if not os.path.exists(mods_folder):
            return

        for filename in os.listdir(mods_folder):
            if filename.endswith(".py"):
                mod_name = os.path.splitext(filename)[0]
                spec = importlib.util.spec_from_file_location(mod_name, os.path.join(mods_folder, filename))
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                mod_instance = mod.load(self)
                print(f"Loaded mod: {mod_name}")
                self.add_mod(mod_instance)

    def add_mod(self, mod):
        self.mods.append(mod)

    def run(self):
        running = True
        while running:
            # Плавное исчезновение заставки
            if self.alpha > 0:
                self.alpha -= 4  # Увеличение скорости скрытия
                if self.studio_name_alpha > 0:
                    self.studio_name_alpha -= 4  # Изменение прозрачности названия студии
            else:
                # Загрузка модов после того, как заставка полностью исчезла
                self.load_mods()
                while running:
                    running = self.handle_events()
                    self.update()
                    self.render()
                    self.clock.tick(60)
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Отображение названия студии
            font = pygame.font.Font(None, 40)
            self.studio_name_text = font.render(self.studio_name, True, (255, 255, 255))

            self.render()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game(800, 600, "Простой 2D движок на Pygame")
    game.run()
