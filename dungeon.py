import random
import pygame
from player import Player
from Items import allItems, Item
from PIL import Image, ImageFilter


class dungeons(allItems,Item):
        
    def __init__(self, game):
        Item.__init__(self)  # Initialisiere Item
        self.player = Player(game)
        self.game = game
        allItems.__init__(self, self.game.width, self.game.height)  # Initialisiere allItems
        self.width = self.game.width
        self.height = self.game.height
        self.chunkdata = {}  # Speichert die Inhalte der Dungeon-Chunks
        self.chunk_koordinaten = [0, 0]
        self.background = pygame.image.load("pngs/background_dungeon.png")
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        self.itemdata = {}
        self.pressed = False
        self.last_drop_time = 0
        self.drop_cooldown = 100
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font(None, 36)
        self.last_energy = None
        self.energy_text_surface = None

    def load_chunk(self):
        if tuple(self.chunk_koordinaten) not in self.chunkdata:
            self.itemdata = {
                "wood": [[random.randint(0, self.width - 32), random.randint(60, self.height - 32)]],
                "stone": [[random.randint(0, self.width - 32), random.randint(60, self.height - 32)]]
            }
            self.chunkdata[tuple(self.chunk_koordinaten)] = self.itemdata
        else:
            self.itemdata = self.chunkdata[tuple(self.chunk_koordinaten)]

    def show_quitmenu(self):
        color_light = (170, 170, 170)
        color_dark = (100, 100, 100)
        color = (255, 255, 255)
        smallfont = pygame.font.SysFont('Corbel', 35)
        text = smallfont.render('quit', True, color)
        text_resum = smallfont.render('resum', True, color)
        button_width = 140
        button_height = 40
        button_x = (self.width - button_width) // 2
        button_y = (self.height - button_height) // 2

        pygame.image.save(self.screen, "pngs/screenshot.png")
        screenshot = Image.open("pngs/screenshot.png")
        blurred_screenshot = screenshot.filter(ImageFilter.GaussianBlur(10))
        blurred_screenshot.save("pngs/blurred_screenshot.png")
        blurred_background = pygame.image.load("pngs/blurred_screenshot.png")

        while True:
            self.screen.blit(blurred_background, (0, 0))
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    return False
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if button_x <= mouse[0] <= button_x + button_width and button_y <= mouse[1] <= button_y + button_height:
                        return False
                    if button_x <= mouse[0] <= button_x + button_width and button_y-55 <= mouse[1] <= button_y-55 + button_height:
                        return True

            mouse = pygame.mouse.get_pos()
            if button_x <= mouse[0] <= button_x + button_width and button_y <= mouse[1] <= button_y + button_height:
                pygame.draw.rect(self.screen, color_light, [button_x, button_y, button_width, button_height])
            else:
                pygame.draw.rect(self.screen, color_dark, [button_x, button_y, button_width, button_height])
            if button_x+5 <= mouse[0] <= button_x + button_width and button_y-55 <= mouse[1] <= button_y-55 + button_height:
                pygame.draw.rect(self.screen, color_light, [button_x, button_y-55, button_width, button_height])
            else:
                pygame.draw.rect(self.screen, color_dark, [button_x, button_y-55, button_width, button_height])
            text_x = button_x + (button_width - text.get_width()) // 2
            text_y = button_y + (button_height - text.get_height()) // 2
            self.screen.blit(text, (text_x, text_y))
            self.screen.blit(text_resum, (text_x, text_y-55))
            pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return self.show_quitmenu()
        return True

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.load_chunk()
        if self.last_energy != int(self.player.energie):
            self.last_energy = int(self.player.energie)
            self.energy_text_surface = self.font.render(f"Energie: {self.last_energy}", True, (255, 255, 255))
        self.screen.blit(self.font.render(str(self.chunk_koordinaten), True, (255, 255, 255)), (700, 10))
        if self.energy_text_surface:
            self.screen.blit(self.energy_text_surface, (10, 10))
        self.player.render()
        self.draw_inventory(self.screen, self.player)
        is_near, pos_x, pos_y, item_key = self.player.get_nearby_item()
        if is_near:
            self.draw_highlighed_on_screen(self.screen, item_key, pos_x, pos_y)
        pygame.display.flip()

    def main(self):

        running = True
        while running:
            self.player.handle_energy_regeneration()
            self.player.player_orientation = [0, 0, 0, 0]
            running = self.handle_events()
            self.player.handle_player_input()
            self.player.check_boundaries()
            self.render()
        pygame.quit()

if __name__ == "__main__":
    dungeon = dungeons()
    dungeon.main()
