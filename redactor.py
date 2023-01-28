import pygame as pg
from mutagen.mp3 import MP3
from math import floor
from widgets import Slider, Button
import main
import os


class Redactor:
	def __init__(self, w, h, app, lvl=''):
		# values
		self.lvl = lvl
		self.w, self.h = w, h
		self.FPS = 60
		self.cs = 30
		self.mode = 0
		self.map = []
		if lvl != '':
			with open(f'data/lvl/{lvl}/map.txt') as f:
				for i in f:
					if i[-1] == '\n':
						self.map.append(i[:-1])
					else:
						self.map.append(i)
			with open(f'data/lvl/{lvl}/lvl_settings.txt') as f:
				for i in f:
					if i[:3] == 'bpm':
						self.bpm = int(i[4:])
		with open (f'player_settings.txt') as f:
			for i in f:
				if i[:5] == 'speed':
					self.speed = int(i[6:-1])
		self.step = (self.FPS * self.speed) * (self.FPS / self.bpm) / 2
		self.audio_len = floor(MP3(f'data/lvl/{lvl}/music.mp3').info.length)
		for i in range(round(self.audio_len * self.bpm / self.FPS * 2)):
			self.map.append('0')
		self.add_column = None
		self.cur_cir = None
		self.app = app
		self.ent_list = app.ent_list[:2]
		with open (f'player_settings.txt') as f:
			for i in f:
				if i[:12] == 'music_volume':
					self.music_volume = float(i[i.find('=') + 1:-1])
		pg.mixer.music.load(f'data/lvl/{lvl}/music.mp3')
		pg.mixer.music.set_volume(self.music_volume)
		self.play_music = -1

		# images
		self.cir_img = [pg.image.load('data/img/left_circle.bmp'), pg.image.load('data/img/up_circle.bmp'),
			pg.image.load('data/img/right_circle.bmp'), pg.image.load('data/img/down_circle.bmp'),
			pg.image.load('data/img/empty_area_h.bmp'), pg.image.load('data/img/empty_area_v.bmp'),
			pg.transform.flip(pg.image.load('data/img/empty_area_h.bmp'), False, True), pg.transform.flip(pg.image.load('data/img/empty_area_v.bmp'), True, False),
			pg.image.load('data/img/left_circle_br.bmp'), pg.image.load('data/img/up_circle_br.bmp'),
			pg.image.load('data/img/right_circle_br.bmp'), pg.image.load('data/img/down_circle_br.bmp'),
			pg.image.load('data/img/senser_circle_deactivated.bmp')]
		for i in range(len(self.cir_img)):
			self.cir_img[i] = pg.transform.scale(self.cir_img[i], (self.cs * 2, self.cs * 2))
			self.cir_img[i].set_colorkey((0, 0, 0))

		# enteries & sliders
		self.timeline = Slider(0, self.audio_len, 1, 0, 125, self.w + 20, 0)
		self.btn_sets = Button(540, 640, lambda: mode1(app, self), 'data/img/lvl_sets1.jpg', 'data/img/lvl_sets2.jpg', colorkey=False)
		self.save_icon = Button(10, 640, lambda: self.save_lvl(), 'data/img/save_icon1.jpg', 'data/img/save_icon2.jpg', colorkey=False)
		self.btn_close = Button(540, 10, close, 'data/img/btn_close1.bmp', 'data/img/btn_close2.bmp', colorkey=False)
		self.btn_playmus = Button(10, 10, lambda: self.music(), 'data/img/play_music1.bmp', 'data/img/play_music2.bmp', colorkey=False)

	def music(self):
		self.play_music *= -1
		if self.play_music == 1:
			pg.mixer.music.play(start=self.timeline.get_value())
		else:
			pg.mixer.music.pause()

	def render(self, win, mmt):
		for i in range(len(self.map)):
			for j in self.map[i]:
				if round(-i * self.step + mmt) in range(-self.cs, self.w // 2):
					win.blit(self.cir_img[5], (-i * self.step + mmt - self.cs, self.h // 2 - self.cs))
					win.blit(self.cir_img[7], (self.w + i * self.step - mmt - self.cs, self.h // 2 - self.cs))
					win.blit(self.cir_img[4], (self.w // 2 - self.cs, -i * self.step + mmt - self.cs))
					win.blit(self.cir_img[6], (self.w // 2 - self.cs, self.h + i * self.step - mmt - self.cs))
				if j == '1' and round(-i * self.step + mmt) in range(-self.cs, self.w // 2):
					win.blit(self.cir_img[0], (-i * self.step + mmt - self.cs, self.h // 2 - self.cs))
				elif j == '3' and round(self.w + i * self.step - mmt) in range(self.w // 2, self.w + self.cs):
					win.blit(self.cir_img[2], (self.w + i * self.step - mmt - self.cs, self.h // 2 - self.cs))
				elif j == '2' and round(-i * self.step + mmt) in range(-self.cs, self.h // 2):
					win.blit(self.cir_img[1], (self.w // 2 - self.cs, -i * self.step + mmt - self.cs))
				elif j == '4' and round(self.h + i * self.step - mmt) in range(self.h // 2, self.h + self.cs):
					win.blit(self.cir_img[3], (self.w // 2 - self.cs, self.h + i * self.step - mmt - self.cs))
				win.blit(self.cir_img[12], (self.w // 2 - 30, self.h // 2 - 30))

	def render_br(self, win, pos, mmt):
		if self.add_column == 1:
			ind = int((mmt - pos[0] + 29) // self.step)
			if ind in range(0, len(self.map)):
				win.blit(self.cir_img[8], (-ind * self.step + mmt - 30, self.h // 2 - 30))
				self.cur_cir = ind, 1
		elif self.add_column == 3:
			ind = int((mmt + pos[0] - 600 + 29) // self.step)
			if ind in range(0, len(self.map)):
				win.blit(self.cir_img[10], (self.w + ind * self.step - mmt - 30, self.h // 2 - 30))
				self.cur_cir = ind, 3
		elif self.add_column == 2:
			ind = int((mmt - pos[1] + 29) // self.step)
			if ind in range(0, len(self.map)):
				win.blit(self.cir_img[9], (self.w // 2 - 30, -ind * self.step + mmt - 30))
				self.cur_cir = ind, 2
		elif self.add_column == 4:
			ind = int((mmt + pos[1] - 600 + 29) // self.step)
			if ind in range(0, len(self.map)):
				win.blit(self.cir_img[11], (self.w // 2 - 30, self.h + ind * self.step - mmt - 30))
				self.cur_cir = ind, 4

	def render_ui(self, win):
		self.timeline.render(win)
		self.btn_sets.render(win)
		self.save_icon.render(win)
		self.btn_close.render(win)
		self.btn_playmus.render(win)

	def render_sets(self, win):
		win.fill((0, 0, 0))
		win.blit(self.app.nametxt, (50, 50))
		win.blit(self.app.bpmtxt, (75, 150))
		for i in self.ent_list:
			i.render(win)
		self.app.btn_save_red.render(win)
		self.app.btn_return_bw.render(win)

	def check_br_circles(self, pos):
		if pos[0] in range(0, self.w // 2 - 60) and pos[1] in range(270, 331):
			self.add_column = 1
		elif pos[0] in range(self.w // 2 + 60, self.w) and pos[1] in range(270, 331):
			self.add_column = 3
		elif pos[0] in range(270, 331) and pos[1] in range(0, self.h // 2 - 60):
			self.add_column = 2
		elif pos[0] in range(270, 331) and pos[1] in range(self.h // 2 + 60, self.h):
			self.add_column = 4
		else:
			self.add_column = None

	def add_circle(self):
		if self.map[self.cur_cir[0]] == '0':
			self.map[self.cur_cir[0]] = str(self.cur_cir[1])
		elif str(self.cur_cir[1]) not in self.map[self.cur_cir[0]]:
			self.map[self.cur_cir[0]] += str(self.cur_cir[1])

	def del_circle(self):
		if self.map[self.cur_cir[0]] != '0' and str(self.cur_cir[1]) in self.map[self.cur_cir[0]]:
			a = str(self.cur_cir[1])
			b = self.map[self.cur_cir[0]]
			self.map[self.cur_cir[0]] = b[:b.find(a)] + b[b.find(a) + 1:]
		if self.map[self.cur_cir[0]] == '':
			self.map[self.cur_cir[0]] = '0'

	def save_lvl(self):
		for i in range(len(self.map) - 1, 0, -1):
			if self.map[i - 1] == '0':
				self.map = self.map[:-1]
			else:
				break
		with open(f'data/lvl/{self.lvl}/map.txt', 'w') as f:
			for i in range(len(self.map)):
				f.write(self.map[i] + '\n')
			f.close()
		for i in range(round(self.audio_len * self.bpm / self.FPS * 2)):
			self.map.append('0')


def mode1(app, red):
	red.mode = 1
	red.ent_list[0].str = red.lvl
	with open(f'data/lvl/{red.lvl}/lvl_settings.txt') as f:
		for i in f:
			red.ent_list[1].str = i[4:]

def close():
	global run
	run = False

def mode0(red):
	red.mode = 0

def save_lvl_sets(app, red):
	lvl_name = red.ent_list[0].get_value()
	lvl_bpm = red.ent_list[1].get_value()
	if lvl_name != red.lvl:
		os.rename(f'data/lvl/{red.lvl}', lvl_name)
		red.lvl = lvl_name
	with open(f'data/lvl/{red.lvl}/lvl_settings.txt', 'w') as f:
		f.write(f'bpm={lvl_bpm}')
		f.close()
	red.mode = 0

run = True
mmt = 0

def run_redactor(app, lvl=''):
	global run
	run = True
	global mmt
	pg.init()
	w, h = 600, 700
	win = pg.display.set_mode((w, h))
	red = Redactor(w, h - 100, app, lvl=lvl)
	clock = pg.time.Clock()
	delta = 0
	pos = (0, 0)
	pressed = False
	pos = None
	FPS = 60
	stop_mmt = (red.audio_len + 1) * FPS * red.speed
	app.btn_return_bw.func = lambda: mode0(red)
	app.btn_save_red.func = lambda: save_lvl_sets(app, red)
	while run:
		win.fill((255, 255, 255))
		for ev in pg.event.get():
			if ev.type == pg.QUIT:
				run = False
			elif ev.type == pg.KEYDOWN:
				if ev.key == pg.K_RIGHT:
					delta = red.speed
				elif ev.key == pg.K_LEFT:
					delta = -red.speed
				if red.mode == 1:
					if ev.key != pg.K_BACKSPACE:
						for i in red.ent_list:
							if i.choosed:
								i.add_let(ev.key)
					else:
						for i in red.ent_list:
							if i.choosed:
								i.str = i.str[:-1]
			elif ev.type == pg.KEYUP:
				delta = 0
			elif ev.type == pg.MOUSEMOTION:
				if red.mode == 0:
					pos = ev.pos
					red.check_br_circles(ev.pos)
					if ev.pos[0] in range(540, 591) and ev.pos[1] in range(640, 691):
						red.btn_sets.cur_img = 1
					elif ev.pos[0] in range(10, 61) and ev.pos[1] in range(640, 691):
						red.save_icon.cur_img = 1
					elif ev.pos[0] in range(540, 591) and ev.pos[1] in range(10, 61):
						red.btn_close.cur_img = 1
					elif ev.pos[0] in range(10, 61) and ev.pos[1] in range(10, 61):
						red.btn_playmus.cur_img = 1
					else:
						red.btn_sets.cur_img = 0
						red.save_icon.cur_img = 0
						red.btn_close.cur_img = 0
						red.btn_playmus.cur_img = 0
				elif red.mode == 1:
					if ev.pos[0] in range(100, 501) and ev.pos[1] in range(475, 551):
						app.btn_save_red.cur_img = 1
					elif ev.pos[0] in range(540, 591) and ev.pos[1] in range(10, 61):
						app.btn_return_bw.cur_img = 1
					else:
						app.btn_save_red.cur_img = 0
						app.btn_return_bw.cur_img = 0
			elif ev.type == pg.MOUSEBUTTONDOWN:
				if red.mode == 0:
					pressed = True
					pos = ev.pos
					if ev.pos[0] in range(10, 61) and ev.pos[1] in range(10, 61):
						red.btn_playmus.act(app)
					else:
						red.play_music = -1
						pg.mixer.music.pause()
						if red.add_column != None:
							if ev.button == 1:
								red.add_circle()
							elif ev.button == 3:
								red.del_circle()
						elif ev.pos[0] in range(540, 591) and ev.pos[1] in range(640, 691):
							red.btn_sets.act(app)
						elif ev.pos[0] in range(10, 61) and ev.pos[1] in range(640, 691):
							red.save_icon.act(app)
						elif ev.pos[0] in range(540, 591) and ev.pos[1] in range(10, 61):
							red.btn_close.act(app)
							if red.play_music == 1:
								mmt = red.timeline.get_value() * red.speed * red.FPS
				if red.mode == 1:
					app.check_ents(ev.pos[0], ev.pos[1])
					if ev.pos[0] in range(100, 501) and ev.pos[1] in range(475, 551):
						app.btn_save_red.act(app)
					elif ev.pos[0] in range(540, 591) and ev.pos[1] in range(10, 61):
						app.btn_return_bw.act(red)
			elif ev.type == pg.MOUSEBUTTONUP:
				pressed = False
		if pressed:
			if pos[0] in range(red.timeline.x, red.timeline.x + 350) and pos[1] in range(red.timeline.y, red.timeline.y + 45):
				red.timeline.change(pos[0])
				mmt = red.timeline.get_value() * red.speed * red.FPS
		if red.mode == 0:
			red.render(win, mmt)
			if red.add_column != None:
				red.render_br(win, pos, mmt)
			red.render_ui(win)
		elif red.mode == 1:
			red.render_sets(win)
		pg.display.update()
		clock.tick(FPS)
		if red.play_music == -1:
			if delta != 0:
				red.timeline.set_value(floor(mmt / FPS / red.speed))
			if delta > 0 and mmt <= stop_mmt:
				mmt += delta
			elif delta < 0 and mmt > 0:
				mmt += delta
		else:
			mmt += red.speed
			red.timeline.set_value(floor(mmt / FPS / red.speed))
	app.mode = 0

if __name__ == '__main__':
	run_redactor(main.app, lvl='asdasd')
	pg.quit()