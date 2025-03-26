import pygame
import random
from PIL import Image, ImageFilter

class Item:
    def __init__(self):
        self.darkgreen = (0, 100, 0)
        self.last_inv_slot = None
        self.available_item_dic = {
            "wood": {
                "id": 1,
                "image": pygame.image.load("pngs/wood.png"),
                "highlighted_image": pygame.image.load("pngs/wood_highlighted.png")
            },
            "stone": {
                "id": 2,
                "image": pygame.image.load("pngs/stone.png"),
                "highlighted_image": pygame.image.load("pngs/stone_highlighted.png")
            },
            "wood_plank": {
                "id": 3,
                "image": pygame.image.load("pngs/wood_plank.png"),
                "highlighted_image": pygame.image.load("pngs/wood_plank_highlighted.png")
            },
            "crafting_table": {
                "id": 4,
                "image": pygame.image.load("pngs/craftingtabel.png"),
                "highlighted_image": pygame.image.load("pngs/craftingtabel_highlighted.png")
            },
            "stick": {
                "id": 5,
                "image": pygame.image.load("pngs/stick.png"),
                "highlighted_image": pygame.image.load("pngs/stick_highlighted.png")
            },
            "stone_pickaxe": {
                "id": 6,
                "image": pygame.image.load("pngs/stone_pickaxe.png"),
                "highlighted_image": pygame.image.load("pngs/stone_pickaxe_highlighted.png")
            }
        }

    def add_to_inventory(self, player, item):
        if item in self.available_item_dic:
            if len(player.inventory) < player.maxinventory:
                player.inventory.append(item)

    def merge_inventory(self, player):
        item_list = player.inventory
        count_dict = {}
        for item in item_list:
            if item in count_dict:
                count_dict[item] += 1
            else:
                count_dict[item] = 1
        return count_dict

    def go_through_inventory(self, player, slot_number, screen):
        inventory_width = player.maxinventory * 45 - 5
        screen_width = screen.get_width()
        inventory_x = (screen_width - inventory_width) // 2
        slot_size = 40
        slot_margin = 5
        inventory_y = 10
        self.last_inv_slot = slot_number

        slot_x = inventory_x + slot_number * (slot_size + slot_margin)
        pygame.draw.rect(screen, (0, 255, 0), (slot_x, inventory_y, slot_size, slot_size), 2)

    def draw_inventory(self, screen, player):
        self.merge_inventory(player)
        screen_width = screen.get_width()
        inventory_width = player.maxinventory * 45 - 5
        inventory_x = (screen_width - inventory_width) // 2
        inventory_y = 10
        pygame.draw.rect(screen, (200, 200, 200), (inventory_x - 5, inventory_y - 5, inventory_width + 10, 50), 2)

        slot_size = 40
        slot_margin = 5

        for i in range(player.maxinventory):
            slot_x = inventory_x + i * (slot_size + slot_margin)
            pygame.draw.rect(screen, (255, 255, 255), (slot_x, inventory_y, slot_size, slot_size), 2)

        selected_x = inventory_x + player.selected_slot * (slot_size + slot_margin)
        pygame.draw.rect(screen, (0, 255, 0), (selected_x, inventory_y, slot_size, slot_size), 3)

        x = inventory_x
        y = inventory_y
        for item, count in self.merge_inventory(player).items():
            if item in self.available_item_dic:
                image = self.available_item_dic[item]["image"]
                image_width, image_height = image.get_size()
                item_x = x + (slot_size - image_width) // 2
                item_y = y + (slot_size - image_height) // 2
                screen.blit(image, (item_x, item_y))
                font = pygame.font.SysFont('Arial', 12)
                text = font.render(str(count), True, (255, 255, 255))
                text_x = x + (slot_size - text.get_width() - 1) // 2 - 13
                text_y = y + (slot_size - text.get_height() - 1) // 2 + 15
                screen.blit(text, (text_x, text_y))
            x += slot_size + slot_margin

    def draw_highlighed_on_screen(self, screen, item_key, rect_x, rect_y):
        if item_key in self.available_item_dic:
            highlighted_image = self.available_item_dic[item_key]["highlighted_image"]
            screen.blit(highlighted_image, (rect_x, rect_y))

class wood(Item):
    def __init__(self, screen_width=800, screen_height=600, rect_x=None, rect_y=None):
        super().__init__()
        self.image = pygame.image.load("pngs/wood.png")
        self.highlighted_image = pygame.image.load("pngs/wood_highlighted.png")
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = rect_x if rect_x is not None else random.randint(0, screen_width - self.rect.width)
        self.rect.y = rect_y if rect_y is not None else random.randint(0, screen_height - self.rect.height + 100)
        self.wood_break_time = 2

    def draw_on_screen(self, screen, rect_x=None, rect_y=None):
        if rect_x is not None:
            self.rect.x = rect_x
        if rect_y is not None:
            self.rect.y = rect_y
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return self.rect.x, self.rect.y

class stone(Item):
    def __init__(self, screen_width=800, screen_height=600, rect_x=None, rect_y=None):
        super().__init__()
        self.image = pygame.image.load("pngs/stone.png")
        self.highlighted_image = pygame.image.load("pngs/stone_highlighted.png")
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = rect_x if rect_x is not None else random.randint(0, screen_width - self.rect.width)
        self.rect.y = rect_y if rect_y is not None else random.randint(0, screen_height - self.rect.height + 100)
        self.stone_break_time = 3

    def draw_on_screen(self, screen, rect_x=None, rect_y=None):
        if rect_x is not None:
            self.rect.x = rect_x
        if rect_y is not None:
            self.rect.y = rect_y
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return self.rect.x, self.rect.y

class wood_plank(Item):
    def __init__(self, screen_width=800, screen_height=600, rect_x=None, rect_y=None):
        super().__init__()
        self.image = pygame.image.load("pngs/wood_plank.png")
        self.highlighted_image = pygame.image.load("pngs/wood_plank_highlighted.png")
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = rect_x if rect_x is not None else random.randint(0, screen_width - self.rect.width)
        self.rect.y = rect_y if rect_y is not None else random.randint(0, screen_height - self.rect.height + 100)
        self.wood_plank_break_time = 1
        self.craft_output = 4

    def draw_on_screen(self, screen, rect_x=None, rect_y=None):
        if rect_x is not None:
            self.rect.x = rect_x
        if rect_y is not None:
            self.rect.y = rect_y
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return self.rect.x, self.rect.y

class crafting_table(Item):
    def __init__(self, screen_width=800, screen_height=600, rect_x=None, rect_y=None):
        super().__init__()
        self.image = pygame.image.load("pngs/craftingtabel.png")
        self.highlighted_image = pygame.image.load("pngs/craftingtabel_highlighted.png")
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = rect_x if rect_x is not None else random.randint(0, screen_width - self.rect.width)
        self.rect.y = rect_y if rect_y is not None else random.randint(0, screen_height - self.rect.height + 100)
        self.crafting_table_break_time = 2
    
    def draw_on_screen(self, screen, rect_x=None, rect_y=None):
        if rect_x is not None:
            self.rect.x = rect_x
        if rect_y is not None:
            self.rect.y = rect_y
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return self.rect.x, self.rect.y
    
    def open_craft_menu(self, screen, player):
        color_light = (170, 170, 170)
        color_dark = (100, 100, 100)
        button_width = 40
        button_height = 40
        button_x = (800 - button_width) // 2
        button_y = (600 - button_height) // 2
        item_x = button_x + (button_width - 32) // 2
        item_y = button_y + (button_height - 32) // 2
        item_to_craft = None
        item_usedto_craft = None
        self.player = player
        wood_plank_instance = wood_plank()
        crafting_table_instance = crafting_table()
        stick_instance = stick()
        stone_pickaxe_instance = stone_pickaxe()

        pygame.image.save(screen, "pngs/screenshot.png")
        screenshot = Image.open("pngs/screenshot.png")
        blurred_screenshot = screenshot.filter(ImageFilter.GaussianBlur(2.5))
        blurred_screenshot.save("pngs/blurred_screenshot.png")
        blurred_background = pygame.image.load("pngs/blurred_screenshot.png")

        Open = True
        while Open:
            screen.blit(blurred_background, (0, 0))

            if item_usedto_craft in self.player.inventory:
                if item_to_craft == "wood_plank":
                    if self.player.inventory.count("wood") >= 1:
                        for _ in range(wood_plank_instance.craft_output):
                            self.player.inventory.append("wood_plank")
                        self.player.inventory.remove("wood")
                        break
                elif item_to_craft == "crafting_table":
                    if self.player.inventory.count("wood_plank") >= 4:
                        for _ in range(4):
                            self.player.inventory.remove("wood_plank")
                        self.player.inventory.append("crafting_table")
                        break
                elif item_to_craft == "stick":
                    if self.player.inventory.count("wood_plank") >= 2:
                        for _ in range(stick_instance.craft_output):
                            self.player.inventory.append("stick")
                        for _ in range(2):
                            self.player.inventory.remove("wood_plank")
                        break
                elif item_to_craft == "stone_pickaxe":
                    if self.player.inventory.count("stick") >= 2 and self.player.inventory.count("stone") >= 3:
                        for _ in range(stone_pickaxe_instance.craft_output):
                            self.player.inventory.append("stone_pickaxe")
                        for _ in range(2):
                            self.player.inventory.remove("stick")
                        for _ in range(3):
                            self.player.inventory.remove("stone")
                        break

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    Open = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if button_x <= mouse[0] <= button_x + button_width and button_y <= mouse[1] <= button_y + button_height:
                        item_to_craft = "wood_plank"
                        item_usedto_craft = "wood"
                    elif button_x <= mouse[0] <= button_x + button_width and button_y-55 <= mouse[1] <= button_y-55 + button_height:
                        item_to_craft = "crafting_table"
                        item_usedto_craft = "wood_plank"
                    elif button_x <= mouse[0] <= button_x + button_width and button_y-110 <= mouse[1] <= button_y-110 + button_height:
                        item_to_craft = "stick"
                        item_usedto_craft = "wood_plank"
                    elif button_x <= mouse[0] <= button_x + button_width and button_y-165 <= mouse[1] <= button_y + button_height:
                        item_to_craft = "stone_pickaxe"
                        item_usedto_craft = "stick"
                    
            mouse = pygame.mouse.get_pos()
            if button_x <= mouse[0] <= button_x + button_width and button_y <= mouse[1] <= button_y + button_height:
                pygame.draw.rect(screen, color_light, [button_x, button_y, button_width, button_height])
            else:
                pygame.draw.rect(screen, color_dark, [button_x, button_y, button_width, button_height])
            
            if button_x <= mouse[0] <= button_x + button_width and button_y-55 <= mouse[1] <= button_y-55 + button_height:
                pygame.draw.rect(screen, color_light, [button_x, button_y-55, button_width, button_height])
            else:
                pygame.draw.rect(screen, color_dark, [button_x, button_y-55, button_width, button_height])
            
            if button_x <= mouse[0] <= button_x + button_width and button_y-110 <= mouse[1] <= button_y-110 + button_height:
                pygame.draw.rect(screen, color_light, [button_x, button_y-110, button_width, button_height])
            else:
                pygame.draw.rect(screen, color_dark, [button_x, button_y-110, button_width, button_height])

            if button_x <= mouse[0] <= button_x + button_width and button_y-165 <= mouse[1] <= button_y-165 + button_height:
                pygame.draw.rect(screen, color_light, [button_x, button_y-165, button_width, button_height])
            else:
                pygame.draw.rect(screen, color_dark, [button_x, button_y-165, button_width, button_height])

            # Verwende Instanzen statt Klassennamen

            wood_plank_instance.draw_on_screen(screen, item_x, item_y)      
            crafting_table_instance.draw_on_screen(screen, item_x, item_y-55)
            stick_instance.draw_on_screen(screen, item_x, item_y-110)
            stone_pickaxe_instance.draw_on_screen(screen, item_x, item_y-165)

            pygame.display.update()

class stick(Item):
    def __init__(self, screen_width=800, screen_height=600, rect_x=None, rect_y=None):
        super().__init__()
        self.image = pygame.image.load("pngs/stick.png")
        self.highlighted_image = pygame.image.load("pngs/stick_highlighted.png")
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = rect_x if rect_x is not None else random.randint(0, screen_width - self.rect.width)
        self.rect.y = rect_y if rect_y is not None else random.randint(0, screen_height - self.rect.height + 100)
        self.stick_break_time = 1
        self.craft_output = 4

    def draw_on_screen(self, screen, rect_x=None, rect_y=None):
        if rect_x is not None:
            self.rect.x = rect_x
        if rect_y is not None:
            self.rect.y = rect_y
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return self.rect.x, self.rect.y

class stone_pickaxe(Item):
    def __init__(self, screen_width=800, screen_height=600, rect_x=None, rect_y=None):
        super().__init__()
        self.image = pygame.image.load("pngs/stone_pickaxe.png")
        self.highlighted_image = pygame.image.load("pngs/stone_pickaxe_highlighted.png")
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = rect_x if rect_x is not None else random.randint(0, screen_width - self.rect.width)
        self.rect.y = rect_y if rect_y is not None else random.randint(0, screen_height - self.rect.height + 100)
        self.stone_pickaxe_break_time = 1
        self.craft_output = 1

    def draw_on_screen(self, screen, rect_x=None, rect_y=None):
        if rect_x is not None:
            self.rect.x = rect_x
        if rect_y is not None:
            self.rect.y = rect_y
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return self.rect.x, self.rect.y

class allItems:
    def __init__(self, screen_width=800, screen_height=600):
        self.wood_item = wood(screen_width, screen_height)
        self.stone_item = stone(screen_width, screen_height)
        self.wood_plank_item = wood_plank(screen_width, screen_height)
        self.crafting_table_item = crafting_table(screen_width, screen_height)
        self.stick_item = stick(screen_width, screen_height)
        self.stone_pickaxe_item = stone_pickaxe(screen_width, screen_height)