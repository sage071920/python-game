import pygame
from PIL import Image, ImageFilter


class Player:
    def __init__(self, game):
        self.game = game
        self.player_x = self.game.width // 2
        self.player_y = self.game.height // 2
        self.radius = 20
        self.speed = 0.5
        self.player_orientation = [0, 0, 0, 0]
        self.RED = (255, 0, 0)
        self.energie = 100
        self.energie_degeneration = 0.09
        self.inventory = []
        self.maxinventory = 5
        self.last_movement_time = pygame.time.get_ticks()
        self.regeneration_time = 5000
        self.regeneration_interval = 200
        self.max_energie = 100
        self.selected_slot = 0
        self.last_drop_time = 0
        self.drop_cooldown = 1000

    def drop_Item(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_drop_time < self.drop_cooldown:
            return
        merged_inventory = self.game.merge_inventory(self)
        if self.selected_slot < len(merged_inventory):
            item_to_drop = list(merged_inventory.keys())[self.selected_slot]
            if item_to_drop == "wood":
                if "wood" not in self.game.itemdata:
                    self.game.itemdata["wood"] = []
                self.game.itemdata["wood"].append([self.player_x, self.player_y + self.radius + 3])
            elif item_to_drop == "stone":
                if "stone" not in self.game.itemdata:
                    self.game.itemdata["stone"] = []
                self.game.itemdata["stone"].append([self.player_x, self.player_y + self.radius + 3])
            elif item_to_drop == "wood_plank":
                if "wood_plank" not in self.game.itemdata:
                    self.game.itemdata["wood_plank"] = []
                self.game.itemdata["wood_plank"].append([self.player_x, self.player_y + self.radius + 3])
            elif item_to_drop == "crafting_table":
                if "crafting_table" not in self.game.itemdata:
                    self.game.itemdata["crafting_table"] = []
                self.game.itemdata["crafting_table"].append([self.player_x, self.player_y + self.radius + 3])
            elif item_to_drop == "stick":
                if "stick" not in self.game.itemdata:
                    self.game.itemdata["stick"] = []
                self.game.itemdata["stick"].append([self.player_x, self.player_y + self.radius + 3])
            if item_to_drop in self.inventory:
                self.inventory.remove(item_to_drop)
            self.last_drop_time = current_time

    def check_key_hold(self, key, max_time):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks() / 1000
        if keys[key] and not hasattr(self, 'start_time'):
            self.start_time = current_time
        elif keys[key] and hasattr(self, 'start_time'):
            duration = current_time - self.start_time
            if duration >= max_time:
                delattr(self, 'start_time')
                return True
        elif not keys[key] and hasattr(self, 'start_time'):
            duration = current_time - self.start_time
            delattr(self, 'start_time')
            return None
        return None

    def handle_energy_regeneration(self):
        current_time = pygame.time.get_ticks()
        self.time_since_last_movement = current_time - self.last_movement_time
        if self.energie < self.max_energie:
            if self.time_since_last_movement >= self.regeneration_time:
                if current_time % self.regeneration_interval == 0:
                    self.energie += 1
                    if self.energie > self.max_energie:
                        self.energie = self.max_energie

    def would_collide_with_item(self, new_x, new_y):
        player_rect = pygame.Rect(new_x - self.radius, new_y - self.radius, self.radius * 2, self.radius * 2)
        for item_key, positions in self.game.itemdata.items():
            for position in positions:
                if isinstance(position, (list, tuple)) and len(position) == 2:
                    item_x, item_y = position
                    item_rect = pygame.Rect(item_x, item_y, 32, 32)
                    if player_rect.colliderect(item_rect):
                        return True
        return False

    def handle_player_input(self):
        keys = pygame.key.get_pressed()
        moved = False
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            new_x = self.player_x - self.speed * 2 if (self.energie > 0 and keys[pygame.K_LSHIFT]) else self.player_x - self.speed
            new_y = self.player_y
            if self.player_x - self.radius > 0 and not self.would_collide_with_item(new_x, new_y):
                if self.energie > 0 and keys[pygame.K_LSHIFT]:
                    self.player_x = new_x
                    self.energie -= self.energie_degeneration
                    moved = True
                else:
                    self.player_x = new_x
                    moved = True
            elif self.player_x - self.radius <= 0:
                self.player_orientation[0] = 1
                self.game.chunk_koordinaten[0] += 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            new_x = self.player_x + self.speed * 2 if (self.energie > 0 and keys[pygame.K_LSHIFT]) else self.player_x + self.speed
            new_y = self.player_y
            if self.player_x + self.radius < self.game.width and not self.would_collide_with_item(new_x, new_y):
                if self.energie > 0 and keys[pygame.K_LSHIFT]:
                    self.player_x = new_x
                    self.energie -= self.energie_degeneration
                    moved = True
                else:
                    self.player_x = new_x
                    moved = True
            elif self.player_x + self.radius >= self.game.width:
                self.player_orientation[1] = 1
                self.game.chunk_koordinaten[0] -= 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            new_x = self.player_x
            new_y = self.player_y - self.speed * 2 if (self.energie > 0 and keys[pygame.K_LSHIFT]) else self.player_y - self.speed
            if self.player_y - self.radius > 60 and not self.would_collide_with_item(new_x, new_y):
                if self.energie > 0 and keys[pygame.K_LSHIFT]:
                    self.player_y = new_y
                    self.energie -= self.energie_degeneration
                    moved = True
                else:
                    self.player_y = new_y
                    moved = True
            elif self.player_y - self.radius <= 60:
                self.player_orientation[2] = 1
                self.game.chunk_koordinaten[1] += 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            new_x = self.player_x
            new_y = self.player_y + self.speed * 2 if (self.energie > 0 and keys[pygame.K_LSHIFT]) else self.player_y + self.speed
            if self.player_y + self.radius < self.game.height and not self.would_collide_with_item(new_x, new_y):
                if self.energie > 0 and keys[pygame.K_LSHIFT]:
                    self.player_y = new_y
                    self.energie -= self.energie_degeneration
                    moved = True
                else:
                    self.player_y = new_y
                    moved = True
            elif self.player_y + self.radius >= self.game.height:
                self.player_orientation[3] = 1
                self.game.chunk_koordinaten[1] -= 1
        if moved:
            self.last_movement_time = pygame.time.get_ticks()

        if keys[pygame.K_q]:
            self.drop_Item()

        if keys[pygame.K_1]:
            self.selected_slot = 0
        if keys[pygame.K_2]:
            self.selected_slot = 1
        if keys[pygame.K_3]:
            self.selected_slot = 2
        if keys[pygame.K_4]:
            self.selected_slot = 3
        if keys[pygame.K_5]:
            self.selected_slot = 4

        if keys[pygame.K_i]:
            self.show_crafting_menu()

        if keys[pygame.K_e]:
            is_near, pos_x, pos_y, item_key = self.get_nearby_item()
            if is_near:
                if item_key == "crafting_table":
                    self.game.crafting_table_item.open_craft_menu(self.game.screen, self)

        self.game.go_through_inventory(self, self.selected_slot, self.game.screen)

        is_near, pos_x, pos_y, item_key = self.get_nearby_item()
        if is_near:
            break_time = self.game.wood_item.wood_break_time if item_key == 'wood' else self.game.stone_item.stone_break_time if item_key == 'stone' else self.game.wood_plank_item.wood_plank_break_time

            if self.selected_slot < len(self.inventory) and self.inventory[self.selected_slot] == "stone_pickaxe":
                if item_key == "stone":
                    break_time /= 3
                else:
                    break_time *= 1.5

            result = self.check_key_hold(pygame.K_e, break_time)
            if result:
                self.interact_with_item()

    def render(self):
        for item_key, positions in self.game.itemdata.items():
            for position in positions:
                item_x, item_y = position
                if item_key == "wood":
                    self.game.wood_item.draw_on_screen(self.game.screen, item_x, item_y)
                elif item_key == "stone":
                    self.game.stone_item.draw_on_screen(self.game.screen, item_x, item_y)
                elif item_key == "wood_plank":
                    self.game.wood_plank_item.draw_on_screen(self.game.screen, item_x, item_y)
                elif item_key == "crafting_table":
                    self.game.crafting_table_item.draw_on_screen(self.game.screen, item_x, item_y)
                elif item_key == "stick":
                    self.game.stick_item.draw_on_screen(self.game.screen, item_x, item_y)
        pygame.draw.circle(self.game.screen, self.RED, (int(self.player_x), int(self.player_y)), self.radius)

    def check_boundaries(self):
        if self.player_orientation[0] == 1:
            self.player_x = self.game.width - self.radius
        if self.player_orientation[1] == 1:
            self.player_x = self.radius
        if self.player_orientation[2] == 1:
            self.player_y = self.game.height - self.radius
        if self.player_orientation[3] == 1:
            self.player_y = 60 + self.radius

    def get_nearby_item(self, distance_threshold=75):
        closest_item = None
        min_distance = float('inf')
        for item_key, positions in self.game.itemdata.items():
            for position in positions:
                if isinstance(position, (list, tuple)) and len(position) == 2:
                    item_x, item_y = position
                    if (self.player_x + self.radius + distance_threshold > item_x and
                        self.player_x - self.radius - distance_threshold < item_x + 32 and
                        self.player_y + self.radius + distance_threshold > item_y and
                        self.player_y - self.radius - distance_threshold < item_y + 32):
                        distance = ((self.player_x - item_x) ** 2 + (self.player_y - item_y) ** 2) ** 0.5
                        if distance < min_distance:
                            min_distance = distance
                            closest_item = (True, item_x, item_y, item_key)
        if closest_item:
            return closest_item
        return False, None, None, None


        
    def show_crafting_menu(self):
        color_light = (170, 170, 170)
        color_dark = (100, 100, 100)
        button_width = 40
        button_height = 40
        button_x = (self.game.width - button_width) // 2
        button_y = (self.game.height - button_height) // 2
        item_x = button_x + (button_width - 32) //2
        item_y = button_y + (button_height - 32) //2
        item_to_craft = None
        item_usedto_craft = None
    
        # Screenshot des aktuellen Bildschirms speichern
        pygame.image.save(self.game.screen, "pngs/screenshot.png")

        # Screenshot laden und unscharf machen
        screenshot = Image.open("pngs/screenshot.png")
        blurred_screenshot = screenshot.filter(ImageFilter.GaussianBlur(2.5))
        blurred_screenshot.save("pngs/blurred_screenshot.png")

        # Unscharfes Bild als Hintergrund laden
        blurred_background = pygame.image.load("pngs/blurred_screenshot.png")

        # Crafting-Menü anzeigen
        Open = True
        while Open:
            self.game.screen.blit(blurred_background, (0, 0))

            if item_usedto_craft in self.inventory:
                if item_to_craft == "wood_plank":
                    # Crafting von Wood Planks
                    if self.inventory.count("wood") >= 1:
                        for _ in range(self.game.wood_plank_item.craft_output):
                            self.inventory.append("wood_plank")
                        self.inventory.remove("wood")
                        break
                elif item_to_craft == "crafting_table":
                    # Crafting von Crafting Table
                    if self.inventory.count("wood_plank") >= 4:  # Überprüfe, ob genügend Wood Planks vorhanden sind
                        for _ in range(4):
                            self.inventory.remove("wood_plank")
                        self.inventory.append("crafting_table")  # Füge den Crafting Table zum Inventar hinzu
                        break
                elif item_to_craft == "stick":
                    # Crafting von Sticks
                    if self.inventory.count("wood_plank") >= 2:
                        for _ in range(4):
                            self.inventory.append("stick")
                        for _ in range(2):
                            self.inventory.remove("wood_plank")
                        break


            # Ereignisse abfragen
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
                    
            mouse = pygame.mouse.get_pos()
            if button_x <= mouse[0] <= button_x + button_width and button_y <= mouse[1] <= button_y + button_height:
                pygame.draw.rect(self.game.screen, color_light, [button_x, button_y, button_width, button_height])
            else:
                pygame.draw.rect(self.game.screen, color_dark, [button_x, button_y, button_width, button_height])
            
            if button_x+5 <= mouse[0] <= button_x + button_width and button_y-55 <= mouse[1] <= button_y-55 + button_height:
                pygame.draw.rect(self.game.screen, color_light, [button_x, button_y-55, button_width, button_height])
            else:
                pygame.draw.rect(self.game.screen, color_dark, [button_x, button_y-55, button_width, button_height])
            if button_x+5 <= mouse[0] <= button_x + button_width and button_y-110 <= mouse[1] <= button_y-110 + button_height:
                pygame.draw.rect(self.game.screen, color_light, [button_x, button_y-110, button_width, button_height])
            else:
                pygame.draw.rect(self.game.screen, color_dark, [button_x, button_y-110, button_width, button_height])

            self.game.wood_plank_item.draw_on_screen(self.game.screen, item_x, item_y)
            self.game.crafting_table_item.draw_on_screen(self.game.screen, item_x, item_y-55)
            self.game.stick_item.draw_on_screen(self.game.screen, item_x, item_y-110)

            # Bildschirm aktualisieren
            pygame.display.update()





    def interact_with_item(self):
        is_near, pos_x, pos_y, item_key = self.get_nearby_item()
        if is_near:
            self.inventory.append(item_key)
            if item_key in self.game.itemdata:
                for i, position in enumerate(self.game.itemdata[item_key]):
                    if position == [pos_x, pos_y]:
                        del self.game.itemdata[item_key][i]
                        break
                if not self.game.itemdata[item_key]:
                    del self.game.itemdata[item_key]
                self.game.chunkdata[tuple(self.game.chunk_koordinaten)] = self.game.itemdata