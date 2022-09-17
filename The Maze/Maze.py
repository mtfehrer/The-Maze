import pygame, sys, os, json, time

screen_size = (1200, 900)
screen = pygame.display.set_mode(screen_size)
screen_center = (screen_size[0] / 2, screen_size[1] / 2)
screen_rect = pygame.Rect((0, 0), screen_size)
pygame.display.set_caption("The Maze")
clock = pygame.time.Clock()
lock_img = pygame.image.load("lock image.png")
lock_img = pygame.transform.scale(lock_img, (110, 100))
lock_img_rect = lock_img.get_rect(center=screen_center)
saving_time = 2
framerate = 144
editor_cell_num = 15
editor_cell_size = (screen_size[0] / editor_cell_num, screen_size[1] / editor_cell_num)
button_size = (200, 150)
white = (255, 255, 255)
gray = (100, 100, 100)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
pygame.init()

title_font = pygame.font.SysFont("arial", int(screen_size[0] / 12))
default_font = pygame.font.SysFont(None, 40)
big_default_font = pygame.font.SysFont(None, 60)
text_box_font = pygame.font.SysFont("consolas", int(screen_size[0] / 14))

title_text = title_font.render("The Maze", True, white)
title_text_rect = title_text.get_rect(center=(screen_center[0], screen_center[1] / 2))

button1_text_pos = screen_center
button1_surf = pygame.Surface(button_size)
button1_rect = button1_surf.get_rect(center=button1_text_pos)

left_arrow_points = [(300, screen_center[1]), (400, screen_center[1] - 100), (400, screen_center[1] + 100)]
right_arrow_points = [(900, screen_center[1]), (800, screen_center[1] - 100), (800, screen_center[1] + 100)]

#for buttons
left_arrow_rect = pygame.Rect((300, screen_center[1] - 100), (100, 200))
right_arrow_rect = pygame.Rect((800, screen_center[1] - 100), (100, 200))

editor_button_text = default_font.render("Level Editor", True, black)
editor_button_text_rect = editor_button_text.get_rect(center=(screen_center[0], screen_center[1] * 1.6))
editor_button_surf = pygame.Surface(button_size)
editor_button_rect = editor_button_surf.get_rect(center=(screen_center[0], screen_center[1] * 1.6))

text_box_surf = pygame.Surface((screen_size[0] * .75, screen_center[1] / 4))
text_box_surf.fill(white)
text_box_rect = text_box_surf.get_rect(center=screen_center)
text_box_text_rect = text_box_surf.get_rect(center=(screen_center[0], screen_center[1] + 17))

box_info_text_rendered = default_font.render("Type the name of your file; Press enter when finished", True, white)
box_info_text_pos = (screen_center[0], screen_center[1] - (screen_center[1] / 6))
box_info_text_rect = box_info_text_rendered.get_rect(center=box_info_text_pos)

saved_text_rendered = title_font.render("Saving To File", True, white)
saved_text_rect = saved_text_rendered.get_rect(center=(screen_center[0], screen_center[1] - 300))

help_background = pygame.Surface((screen_size[0] * .9, screen_size[1] * .9))
help_background_rect = help_background.get_rect(center=screen_center)

preview_help_text = default_font.render("Press 'H' for help", True, white)
preview_help_text_rect = preview_help_text.get_rect(center=(1085, 20))

help_text1 = big_default_font.render("Press 'Left Click' to draw", True, white)
help_text1_rect = help_text1.get_rect(center=(screen_center[0], 150))
help_text2 = big_default_font.render("Press 'Right Click' to erase", True, white)
help_text2_rect = help_text2.get_rect(center=(screen_center[0], 250))
help_text3 = big_default_font.render("Press 'Middle Click' to place start/end", True, white)
help_text3_rect = help_text3.get_rect(center=(screen_center[0], 350))
help_text4 = big_default_font.render("Press 'SPACE' to clear the screen", True, white)
help_text4_rect = help_text4.get_rect(center=(screen_center[0], 450))
help_text5 = big_default_font.render("Press 'ENTER' to save", True, white)
help_text5_rect = help_text5.get_rect(center=(screen_center[0], 550))
help_text6 = big_default_font.render("Press 'ESC' to exit", True, white)
help_text6_rect = help_text6.get_rect(center=(screen_center[0], 650))
help_text7 = big_default_font.render("Press 'H' to close this window", True, yellow)
help_text7_rect = help_text7.get_rect(center=(screen_center[0], 750))

win_text = title_font.render("You Won!", True, green)
win_text_rect = win_text.get_rect(center=(screen_center[0], 100))

class Main:
	def __init__(self):
		self.mode = "title"
		self.title = Title()
		self.editor = Editor()
		self.event = None
		self.key_update = False
		self.cell_num = 10
		self.cell_size = (screen_size[0] / self.cell_num, screen_size[1] / self.cell_num)
		self.current_level = 0

	def fill_screen(self):
		screen.fill(blue)

	def draw_lines(self):
		if self.mode == "editor" or self.mode == "editor_help" or self.mode == "editor_text":
			for num in range(editor_cell_num):
				pygame.draw.line(screen, white, (0, num * editor_cell_size[1]), (screen_size[0], num * editor_cell_size[1]))
				pygame.draw.line(screen, white, (num * editor_cell_size[0], 0), (num * editor_cell_size[0], screen_size[1]))
		else:
			for num in range(self.cell_num):
				pygame.draw.line(screen, white, (0, num * self.cell_size[1]), (screen_size[0], num * self.cell_size[1]))
				pygame.draw.line(screen, white, (num * self.cell_size[0], 0), (num * self.cell_size[0], screen_size[1]))
	
	def editor_key_update(self, event):
		self.event = event
		self.key_update = True

	def editor_key_check(self):
		if self.key_update == True:
			if self.mode == "editor" or self.mode == "editor_help":
				self.mode = self.editor.key_press(self.event.key, self.mode)
			elif self.mode == "editor_text":
				self.mode = self.editor.input_text((self.event.unicode, self.event.key))

	def game_update_check(self, scancode):
		tup = self.game.update_player(scancode)
		if tup[0] == "win":
			self.title.availible_levels.append(self.current_level)
		self.mode = tup[1]

	def run_title(self):
		self.title.get_button_text()
		self.title.display_title()
		self.title.get_mouse_details()
		mode_and_level = self.title.determine_button_press()
		self.mode = mode_and_level[0]
		if mode_and_level[1] != None:
			self.game = Game()
			self.cell_num = self.game.load_level(mode_and_level[1])
			self.cell_size = (screen_size[0] / self.cell_num, screen_size[1] / self.cell_num)
			self.current_level += 1

	def run_editor(self):
		self.editor.edit()
		self.editor.display_cells()
		self.editor.display_help_preview()
		self.draw_lines()

	def display_editor_text(self):
		self.editor.display_cells()
		self.draw_lines()
		if self.editor.display_text_box() != None:
			self.mode = "editor"

	def display_editor_help(self):
		self.editor.display_cells()
		self.draw_lines()
		self.editor.display_help()

	def display_game(self):
		self.game.display_cells()
		self.game.draw_player()
		self.draw_lines()

class Title:
	def __init__(self):
		self.editor_button_color = yellow
		self.button1_color = yellow
		self.left_arrow_color = black
		self.right_arrow_color = black
		self.levels = []
		self.screen_levels = []
		self.title_part = 0
		self.availible_levels = [0]
		self.switch = False
		self.last_press = False
		for filename in os.listdir():
			if filename.endswith(".json"):
				filename = filename[:-5]
				self.levels.append([filename, False])
		del self.levels[1]
		del self.levels[1]
		self.levels.append(["Level 10", False])
		self.levels.append(["Final Boss", False])

	def get_button_text(self):
		self.button1_text = default_font.render(self.levels[self.title_part][0], True, black)
		self.button1_text_rect = self.button1_text.get_rect(center=button1_text_pos)

	def display_title(self):
		screen.blit(title_text, title_text_rect)

		#level editor
		editor_button_surf.fill(self.editor_button_color)
		screen.blit(editor_button_surf, editor_button_rect)
		screen.blit(editor_button_text, editor_button_text_rect)

		#button1
		button1_surf.fill(self.button1_color)
		screen.blit(button1_surf, button1_rect)
		screen.blit(self.button1_text, self.button1_text_rect)
		if self.title_part not in self.availible_levels:
			screen.blit(lock_img, lock_img_rect)

		#arrows
		pygame.draw.polygon(screen, self.left_arrow_color, left_arrow_points)
		pygame.draw.polygon(screen, self.right_arrow_color, right_arrow_points)

		if 11 in self.availible_levels:
			screen.blit(win_text, win_text_rect)

	def get_mouse_details(self):
		self.mouse_pos = pygame.mouse.get_pos()
		self.mouse_press = pygame.mouse.get_pressed()
		if self.mouse_press[0] == True and self.last_press == False:
			self.switch = True
		elif self.mouse_press[0] == True and self.last_press == True:
			self.switch = False
		self.last_press = self.mouse_press[0]

	def determine_button_press(self):
		if (self.mouse_pos[0] > editor_button_rect.left and 
		    self.mouse_pos[0] < editor_button_rect.right and 
		    self.mouse_pos[1] > editor_button_rect.top and 
		    self.mouse_pos[1] < editor_button_rect.bottom):
			self.editor_button_color = green
			if self.switch == True:
				self.switch = False
				return ("editor", None)
		elif (self.mouse_pos[0] > button1_rect.left and 
			  self.mouse_pos[0] < button1_rect.right and 
			  self.mouse_pos[1] > button1_rect.top and 
			  self.mouse_pos[1] < button1_rect.bottom):
			self.button1_color = green
			if self.switch == True:
				self.switch = False
				if self.title_part in self.availible_levels:
					return ("game", self.title_part + 1)
		elif (self.mouse_pos[0] > left_arrow_rect.left and 
			  self.mouse_pos[0] < left_arrow_rect.right and 
			  self.mouse_pos[1] > left_arrow_rect.top and 
			  self.mouse_pos[1] < left_arrow_rect.bottom):
			self.left_arrow_color = white
			if self.switch == True:
				if self.title_part != 0:
					self.title_part -= 1
		elif (self.mouse_pos[0] > right_arrow_rect.left and 
			  self.mouse_pos[0] < right_arrow_rect.right and 
			  self.mouse_pos[1] > right_arrow_rect.top and 
			  self.mouse_pos[1] < right_arrow_rect.bottom):
			self.right_arrow_color = white
			if self.switch == True:
				if self.title_part != len(self.levels) - 1:
					self.title_part += 1
		else:
			self.editor_button_color = yellow
			self.button1_color = yellow
			self.left_arrow_color = black
			self.right_arrow_color = black
		return ("title", None)

class Editor:
	def __init__(self):
		self.main_dict = {"grid_size": 10,
						  "spawn_pos": (0, 0), 
						  "end_pos": (screen_size[0] - editor_cell_size[0], screen_size[1] - editor_cell_size[1]), 
						  "cell_list": []}
		self.not_pressed = False
		self.mid_click = "spawn"
		self.saving = False
		self.text_list = []
		self.text = ""
		self.text_rendered = pygame.Surface((0, 0))
		self.start_time = None

	def edit(self):
		mouse_pos = pygame.mouse.get_pos()
		mouse_press = pygame.mouse.get_pressed()
		x = int(mouse_pos[0] / editor_cell_size[0]) * editor_cell_size[0]
		y = int(mouse_pos[1] / editor_cell_size[1]) * editor_cell_size[1]
		self.highlight_cell_pos = (x, y)
		if self.not_pressed == False:
			if mouse_press[0] == False:
				self.not_pressed = True
		if mouse_press[0] == True and self.not_pressed == True:
			if (self.highlight_cell_pos not in self.main_dict["cell_list"] and 
				self.highlight_cell_pos != self.main_dict["spawn_pos"] and
				self.highlight_cell_pos != self.main_dict["end_pos"]):
				self.main_dict["cell_list"].append(self.highlight_cell_pos)
		elif mouse_press[2] == True:
			if self.highlight_cell_pos in self.main_dict["cell_list"]:
				self.main_dict["cell_list"].remove(self.highlight_cell_pos)
		elif mouse_press[1] == True:
			if (self.highlight_cell_pos not in self.main_dict["cell_list"] and 
				self.highlight_cell_pos != self.main_dict["spawn_pos"] and 
				self.highlight_cell_pos != self.main_dict["end_pos"]):
				if self.mid_click == "spawn":
					self.main_dict["spawn_pos"] = self.highlight_cell_pos
					self.mid_click = "end"
				else:
					self.main_dict["end_pos"] = self.highlight_cell_pos
					self.mid_click = "spawn"

	def key_press(self, key, mode):
		if mode == "editor_help":
			if key == 27:
				return "editor"
		else:
			if key == 27:
				self.main_dict["cell_list"].clear()
				self.not_pressed = False
				return "title"
			elif key == 32:
				self.main_dict["cell_list"].clear()
			elif key == 13:
				return "editor_text"
			elif key == 104:
				return "editor_help"
		return "editor"

	def save_to_file(self):
		filename = self.text + ".json"
		data = json.dumps(self.main_dict, indent=2)
		with open(filename, "w") as f:
			f.write(data)

	def input_text(self, key_and_code):
		if key_and_code[1] == 27:
			return "editor"
		elif key_and_code[1] == 8:
			self.text_list = self.text_list[:-1]
		elif key_and_code[1] == 13:
			self.save_to_file()
			self.start_time = pygame.time.get_ticks()
			return "editor_text"
		else:
			if len(self.text_list) < 19:
				self.text_list.append(key_and_code[0])
		self.set_up_text()
		return "editor_text"

	def set_up_text(self):
		self.text = ""
		for char in self.text_list:
			self.text += char
		self.text_rendered = text_box_font.render(self.text, True, black)

	def display_text_box(self):
		screen.blit(box_info_text_rendered, box_info_text_rect)
		screen.blit(text_box_surf, text_box_rect)
		screen.blit(self.text_rendered, text_box_text_rect)
		end_time = pygame.time.get_ticks()
		if self.start_time == None:
			pass
		elif end_time < self.start_time + (saving_time * framerate):
			screen.blit(saved_text_rendered, saved_text_rect)
		else:
			return "editor"

	def display_help(self):
		screen.blit(help_background, help_background_rect)
		screen.blit(help_text1, help_text1_rect)
		screen.blit(help_text2, help_text2_rect)
		screen.blit(help_text3, help_text3_rect)
		screen.blit(help_text4, help_text4_rect)
		screen.blit(help_text5, help_text5_rect)
		screen.blit(help_text6, help_text6_rect)
		screen.blit(help_text7, help_text7_rect)

	def display_help_preview(self):
		screen.blit(preview_help_text, preview_help_text_rect)

	def display_cells(self):
		for cell_pos in self.main_dict["cell_list"]:
			pygame.draw.rect(screen, black, (cell_pos, editor_cell_size))
		pygame.draw.rect(screen, gray, (self.highlight_cell_pos, editor_cell_size))
		pygame.draw.rect(screen, yellow, (self.main_dict["spawn_pos"], editor_cell_size))
		pygame.draw.rect(screen, green, (self.main_dict["end_pos"], editor_cell_size))

class Game:
	def __init__(self):
		pass

	def load_level(self, level):
		filename = "level " + str(level) + ".json"
		with open(filename) as f:
			self.main_dict = json.load(f)
			self.cell_num = self.main_dict["grid_size"]
			self.cell_size = (screen_size[0] / self.cell_num, screen_size[1] / self.cell_num)
		self.player = Player(self.main_dict, self.cell_num)
		return self.cell_num

	def display_cells(self):
		for cell_pos in self.main_dict["cell_list"]:
			pygame.draw.rect(screen, black, (cell_pos, self.cell_size))
		pygame.draw.rect(screen, yellow, (self.main_dict["spawn_pos"], self.cell_size))
		pygame.draw.rect(screen, green, (self.main_dict["end_pos"], self.cell_size))

	def update_player(self, scancode):
		if self.player.update(scancode) == "win":
			return ("win", "title")
		if scancode == 41:
			return (None, "title")
		return (None, "game")

	def draw_player(self):
		screen.blit(self.player.image, self.player.rect)

class Player:
	def __init__(self, main_dict, cell_num):
		self.cell_num = cell_num
		self.cell_size = (screen_size[0] / self.cell_num, screen_size[1] / self.cell_num)
		self.main_dict = main_dict
		self.image = pygame.Surface(self.cell_size)
		self.image.fill(red)
		self.rect = self.image.get_rect(topleft=self.main_dict["spawn_pos"])

	def determine_moveset(self):
		self.moveset = {"left": True, "right": True, "up": True, "down": True}
		small_player_pos = [self.rect.x / self.cell_size[0], self.rect.y / self.cell_size[1]]
		for cell_pos in self.main_dict["cell_list"]:
			new_pos = [cell_pos[0] / self.cell_size[0], cell_pos[1] / self.cell_size[1]]
			if (new_pos[0] == small_player_pos[0] - 1 and 
			    new_pos[1] == small_player_pos[1]):
				self.moveset["left"] = False
			elif (new_pos[0] == small_player_pos[0] + 1 and
				  new_pos[1] == small_player_pos[1]):
				self.moveset["right"] = False
			elif (new_pos[1] == small_player_pos[1] - 1 and
				  new_pos[0] == small_player_pos[0]):
				self.moveset["up"] = False
			elif (new_pos[1] == small_player_pos[1] + 1 and
				  new_pos[0] == small_player_pos[0]):
				self.moveset["down"] = False

	def move(self, scancode):
		if scancode == 82 and self.moveset["up"] == True:
			self.rect.y -= self.cell_size[1]
		elif scancode == 79 and self.moveset["right"] == True:
			self.rect.x += self.cell_size[0]
		elif scancode == 81 and self.moveset["down"] == True:
			self.rect.y += self.cell_size[1]
		elif scancode == 80 and self.moveset["left"] == True:
			self.rect.x -= self.cell_size[0]
		self.rect.clamp_ip(screen_rect)

	def check_for_win(self):
		x = self.rect.x
		y = self.rect.y
		if [x, y] == self.main_dict["end_pos"]:
			return "win"

	def update(self, scancode):
		self.determine_moveset()
		self.move(scancode)
		return self.check_for_win()

main = Main()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if main.mode == "editor" or main.mode == "editor_text" or main.mode == "editor_help":
				main.editor_key_update(event)
			elif main.mode == "game":
				main.game_update_check(event.scancode)

	main.fill_screen()

	if main.mode == "title":
		main.run_title()
	elif main.mode == "editor":
		main.editor_key_check()
		main.run_editor()
	elif main.mode == "editor_text":
		main.editor_key_check()
		main.display_editor_text()
	elif main.mode == "editor_help":
		main.editor_key_check()
		main.display_editor_help()
	elif main.mode == "game":
		main.display_game()

	main.key_update = False

	pygame.display.update()
	clock.tick(framerate)