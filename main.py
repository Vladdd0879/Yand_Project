import pygame as pg
import game as g
from widgets import *
import os
import shutil
import redactor


class App:
	def __init__(self, w, h, win):
		# values
		self.mode = 0
		self.pady = 110
		self.font = pg.font.Font(None, 36)
		self.infofont = pg.font.Font(None, 25)
		self.lvl_list = os.listdir('data/lvl')

		# reading files
		with open (f'player_settings.txt') as f:
			for i in f:
				if i[:5] == 'speed':
					self.speed = int(i[6:-1])
				elif i[:12] == 'music_volume':
					self.music_volume = float(i[i.find('=') + 1:-1])
				elif i[:14] == 'effects_volume':
					self.effects_volume = float(i[i.find('=') + 1:-1])
		with open(f'data/lvl/{self.lvl_list[0]}/map.txt') as f:
			amount = 0
			duration = 0
			c = 0
			for i in f:
				c += 1
				if i not in ('0', '0\n'):
					amount += len(i) - 1
			duration = c
		with open(f'data/lvl/{self.lvl_list[0]}/lvl_settings.txt') as f:
			for i in f:
				if i[:3] == 'bpm':
					bpm = int(i[5:-1])

		# images
		self.bgimg = pg.transform.scale(pg.image.load('data/img/game_bg.jpg'), (w, h))
		self.info_panel = pg.image.load('data/img/info_panel.bmp')
		self.info_panel.set_colorkey((0, 0, 0))

		# buttons
		self.btn_play = Button(100, 100, lambda: mode1(self), 'data/img/btn_play_unchoosed.bmp', 'data/img/btn_play_choosed.bmp')
		self.btn_return = Button(540, 10, lambda: mode0(self), 'data/img/btn_return_unchoosed.bmp', 'data/img/btn_return_choosed.bmp')
		self.btn_set = Button(100, 200, lambda: mode2(self), 'data/img/btn_set1.bmp', 'data/img/btn_set2.bmp')
		self.btn_save = Button(100, 475, lambda: save_sets(self), 'data/img/btn_save1.bmp', 'data/img/btn_save2.bmp')
		self.btn_save_red = Button(100, 475, lambda: self.check_red_sets(win), 'data/img/btn_save1.bmp', 'data/img/btn_save2.bmp')
		self.btn_red = Button(100, 300, lambda: mode30(self), 'data/img/btn_red1.bmp', 'data/img/btn_red2.bmp')
		self.btn_return_bw = Button(540, 10, lambda: mode30(self), 'data/img/btn_return_bw1.bmp', 'data/img/btn_return_bw2.bmp')
		self.btn_newlvl = Button(0, 0, lambda: mode31(self), 'data/img/newlvl1.jpg', 'data/img/newlvl2.jpg')

		# sliders & entries
		self.sliders = [Slider(1, 11, 1, self.speed, 180, 92, 255),
						Slider(0, 100, 2, int(self.music_volume * 100), 160, 192, 255),
						Slider(0, 100, 2, int(self.effects_volume * 100), 190, 292, 255)]
		self.ent_list = [Entery(175, 40, 300, 36, 1), Entery(175, 140, 300, 36, 0),
						Entery(175, 240, 300, 36, 1), Entery(175, 340, 300, 36, 1)]

		# text
		self.info_name = self.font.render(self.lvl_list[0], False, (255, 255, 255))
		self.info_diff = self.infofont.render(f'{self.get_difficulty(duration, amount, bpm)}*', False, (255, 255, 255))
		self.info_noteamnt = self.infofont.render(f'{amount} нот', False, (255, 255, 255))
		self.info_bpm = self.infofont.render(f'{bpm} bpm', False, (255, 255, 255))
		self.nametxt = self.font.render('Название', False, (255, 255, 255))
		self.bpmtxt = self.font.render('BPM', False, (255, 255, 255))
		self.musictxt = self.font.render('Музыка', False, (255, 255, 255))
		self.imgtxt = self.font.render('Картинка', False, (255, 255, 255))

	def render(self, win):
		if self.mode == 0:
			win.blit(self.bgimg, (0, 0))
			self.btn_play.render(win)
			self.btn_set.render(win)
			self.btn_red.render(win)

		elif self.mode == 1:
			self.lvl_btns = []
			win.blit(self.bgimg, (0, 0))
			self.btn_return.render(win)
			for i in range(len(self.lvl_list)):
				self.lvl_btns.append(Button(10, self.pady + i * 100, lambda x = i: g.play_lvl(self.lvl_list[x], self), 'data/img/lvl1.jpg', 'data/img/lvl1.jpg'))
				self.lvl_btns[i].render(win)
				img = pg.transform.scale(pg.image.load(f'data/lvl/{self.lvl_list[i]}/bg.bmp'), (130, 90))
				self.name = self.font.render(self.lvl_list[i], False, (255, 255, 255))
				win.blit(self.name, (150, self.pady + i * 100 + 33))
				win.blit(img, (10, self.pady + i * 100))
			win.blit(self.info_panel, (0, 0))
			win.blit(self.info_name, (10, 5))
			win.blit(self.info_diff, (10,35))
			win.blit(self.info_noteamnt, (10, 55))
			win.blit(self.info_bpm, (10, 75))

		elif self.mode == 2:
			win.fill((0, 0, 0))
			win.blit(self.speedtxt, (50, 100))
			win.blit(self.musictxt, (50, 200))
			win.blit(self.efftxt, (50, 300))
			self.btn_return_bw.render(win)
			for i in self.sliders:
				i.render(win)
			self.btn_save.render(win)

		elif self.mode == 31:
			win.fill((0, 0, 0))
			win.blit(self.nametxt, (50, 50))
			win.blit(self.bpmtxt, (75, 150))
			win.blit(self.musictxt, (55, 250))
			win.blit(self.imgtxt, (50, 350))
			for i in self.ent_list:
				i.render(win)
			self.btn_save_red.render(win)
			self.btn_return_bw.render(win)

		elif self.mode == 30:
			self.lvl_btns = []
			win.blit(self.bgimg, (0, 0))
			self.btn_return.render(win)
			for i in range(len(self.lvl_list)):
				self.lvl_btns.append(Button(10, self.pady + i * 100, lambda x = i: load_red(app, win, x), 'data/img/lvl1.jpg', 'data/img/lvl1.jpg'))
				self.lvl_btns[i].render(win)
				img = pg.transform.scale(pg.image.load(f'data/lvl/{self.lvl_list[i]}/bg.bmp'), (130, 90))
				self.name = self.font.render(self.lvl_list[i], False, (255, 255, 255))
				win.blit(self.name, (150, self.pady + i * 100 + 33))
				win.blit(img, (10, self.pady + i * 100))
			self.btn_newlvl.crd = (10, self.pady + (i + 1) * 100)
			self.btn_newlvl.render(win)
			win.blit(self.info_panel, (0, 0))
			win.blit(self.info_name, (10, 5))
			win.blit(self.info_diff, (10,35))
			win.blit(self.info_noteamnt, (10, 55))
			win.blit(self.info_bpm, (10, 75))

	def check_red_sets(self, win):
		lvl_name = self.ent_list[0].get_value()
		lvl_bpm = self.ent_list[1].get_value()
		lvl_music = self.ent_list[2].get_value()
		lvl_bg = self.ent_list[3].get_value()
		if os.path.exists(lvl_music) and os.path.exists(lvl_bg) and lvl_name != '' and lvl_bpm != '':
			os.mkdir('data/lvl/' + lvl_name)
			shutil.copy(lvl_music, f'data/lvl/{lvl_name}', follow_symlinks=True)
			os.rename(f'data/lvl/{lvl_name}/{lvl_music}', f'data/lvl/{lvl_name}/music.mp3')
			shutil.copy(lvl_bg, f'data/lvl/{lvl_name}', follow_symlinks=True)
			os.rename(f'data/lvl/{lvl_name}/{lvl_bg}', f'data/lvl/{lvl_name}/bg.bmp')
			f = open(f'data/lvl/{lvl_name}/lvl_settings.txt', 'w')
			f.write(f'bpm={lvl_bpm}')
			f.close()
			f = open(f'data/lvl/{lvl_name}/map.txt', 'w')
			f.close()
			redactor.run_redactor(self, lvl=lvl_name)
			win = pg.display.set_mode((600, 600))

	def check_mouse(self, x, y, clk=False):
		for i in range(len(self.lvl_btns)):
			if not clk:
				if x in range(10, 311) and y in range(self.pady + i * 100, self.pady + i * 100 + 90):
					self.lvl_btns[i].cur_img = 1
					self.change_cur_lvl(i)
				else:
					self.lvl_btns[i].cur_img = 0
			else:
				if x in range(10, 311) and y in range(self.pady + i * 100, self.pady + i * 100 + 90):
					self.lvl_btns[i].act(self)

	def check_sliders(self, x, y):
		for i in range(len(self.sliders)):
			if x in range(self.sliders[i].x, self.sliders[i].x + 350) and y in range(self.sliders[i].y, self.sliders[i].y + 45):
				self.sliders[i].change(x)

	def check_ents(self, x, y):
		for i in range(len(self.ent_list)):
			if x in range(self.ent_list[i].x, self.ent_list[i].x + self.ent_list[i].w) and y in range(self.ent_list[i].y, self.ent_list[i].y + self.ent_list[i].s + 10):
				self.ent_list[i].choosed = True
			else:
				self.ent_list[i].choosed = False

	def change_cur_lvl(self, n):
		self.info_name = self.font.render(self.lvl_list[n], False, (255, 255, 255))
		with open(f'data/lvl/{self.lvl_list[n]}/map.txt') as f:
			amount = 0
			duration = 0
			c = 0
			for i in f:
				c += 1
				if i not in ('0', '0\n'):
					amount += len(i) - 1
			duration = c
		with open(f'data/lvl/{self.lvl_list[n]}/lvl_settings.txt') as f:
			for i in f:
				if i[:3] == 'bpm':
					bpm = int(i[4:])
		self.info_diff = self.infofont.render(f'{self.get_difficulty(duration, amount, bpm)}*', False, (255, 255, 255))
		self.info_noteamnt = self.infofont.render(f'{amount} нот', False, (255, 255, 255))
		self.info_bpm = self.infofont.render(f'{bpm} bpm', False, (255, 255, 255))

	def get_difficulty(self, dur, amount, bpm):
		if dur == 0:
			return 0.0
		return round(amount / dur * bpm / 50, 2)


def mode1(app):
	app.mode = 1
	app.lvl_list = os.listdir('data/lvl')

def mode30(app):
	app.mode = 30
	app.lvl_list = os.listdir('data/lvl')
	app.lvl_btns = []

def mode0(app):
	app.mode = 0

def mode2(app):
	app.mode = 2
	app.speedtxt = app.font.render('Скорость', False, (255, 255, 255))
	app.musictxt = app.font.render('Музыка', False, (255, 255, 255))
	app.efftxt = app.font.render('Эффекты', False, (255, 255, 255))

def mode31(app):
	app.mode = 31
	for i in app.ent_list:
		i.str = ''
	app.btn_save_red.func = lambda: app.check_red_sets(win)

def load_red(app, win, i):
	redactor.run_redactor(app, lvl=app.lvl_list[i])
	win = pg.display.set_mode((600, 600))

def save_sets(app):
	values = [i.get_value() for i in app.sliders]
	with open('player_settings.txt', 'w') as f:
		for i in range(len(values)):
			if i == 0:
				s = f'speed={values[i]}\n'
			elif i == 1:
				s = f'music_volume={values[i] / 100}\n'
			elif i == 2:
				s = f'effects_volume={values[i] / 100}'
			f.write(s)
		f.close()
	mode0(app)

pg.init()
w, h, cs = 600, 600, 30
win = pg.display.set_mode((w, h))
app = App(w, h, win)

def main():
	w, h, cs = 600, 600, 30
	global win
	global app
	run = True
	pressed = False
	app.btn_save_red.func = lambda: app.check_red_sets(win)
	while run:
		app.render(win)
		for ev in pg.event.get():
			if ev.type == pg.QUIT:
				run = False
			elif ev.type == pg.MOUSEMOTION:
				if app.mode == 1:
					app.check_mouse(ev.pos[0], ev.pos[1])
					if ev.pos[0] in range(540, 591) and ev.pos[1] in range(10, 61):
						app.btn_return.cur_img = 1
					else:
						app.btn_return.cur_img = 0
				elif app.mode == 0:
					if ev.pos[0] in range(100, 501) and ev.pos[1] in range(100, 176):
						app.btn_play.cur_img = 1
					elif ev.pos[0] in range(100, 501) and ev.pos[1] in range(200, 276):
						app.btn_set.cur_img = 1
					elif ev.pos[0] in range(100, 501) and ev.pos[1] in range(300, 376):
						app.btn_red.cur_img = 1
					else:
						app.btn_play.cur_img = 0
						app.btn_set.cur_img = 0
						app.btn_red.cur_img = 0
				elif app.mode == 2:
					if ev.pos[0] in range(100, 501) and ev.pos[1] in range(475, 551):
						app.btn_save.cur_img = 1
					elif ev.pos[0] in range(540, 591) and ev.pos[1] in range(10, 61):
						app.btn_return_bw.cur_img = 1
					else:
						app.btn_save.cur_img = 0
						app.btn_return_bw.cur_img = 0
				elif app.mode == 31:
					if ev.pos[0] in range(100, 501) and ev.pos[1] in range(475, 551):
						app.btn_save_red.cur_img = 1
					elif ev.pos[0] in range(540, 591) and ev.pos[1] in range(10, 61):
						app.btn_return_bw.cur_img = 1
					else:
						app.btn_save_red.cur_img = 0
						app.btn_return_bw.cur_img = 0
				if app.mode == 30:
					app.check_mouse(ev.pos[0], ev.pos[1])
					if ev.pos[0] in range(540, 591) and ev.pos[1] in range(10, 61):
						app.btn_return.cur_img = 1
					elif ev.pos[0] in range(app.btn_newlvl.crd[0], app.btn_newlvl.crd[0] + 301) and ev.pos[1] in range(app.btn_newlvl.crd[1], app.btn_newlvl.crd[1] + 91):
						app.btn_newlvl.cur_img = 1
					else:
						app.btn_return.cur_img = 0
						app.btn_newlvl.cur_img = 0
			elif ev.type == pg.MOUSEBUTTONDOWN and ev.button not in (4, 5):
				if app.mode == 1:
					app.check_mouse(ev.pos[0], ev.pos[1], clk=True)
					if ev.pos[0] in range(540, 591) and ev.pos[1] in range(10, 61):
						app.btn_return.act(app)
				elif app.mode == 0:
					if ev.pos[0] in range(100, 501) and ev.pos[1] in range(100, 176):
						app.btn_play.act(app)
					elif ev.pos[0] in range(100, 501) and ev.pos[1] in range(200, 276):
						app.btn_set.act(app)
					elif ev.pos[0] in range(100, 501) and ev.pos[1] in range(300, 376):
						app.btn_red.act(app)
				elif app.mode == 2:
					pressed  = True
					if ev.pos[0] in range(100, 501) and ev.pos[1] in range(475, 551):
						app.btn_save.act(app)
					elif ev.pos[0] in range(540, 591) and ev.pos[1] in range(10, 61):
						app.btn_return_bw.act(app)
				elif app.mode == 31:
					app.check_ents(ev.pos[0], ev.pos[1])
					if ev.pos[0] in range(100, 501) and ev.pos[1] in range(475, 551):
						app.btn_save_red.act(app)
					elif ev.pos[0] in range(540, 591) and ev.pos[1] in range(10, 61):
						app.btn_return_bw.act(app)
				if app.mode == 30:
					app.check_mouse(ev.pos[0], ev.pos[1], clk=True)
					if ev.pos[0] in range(540, 591) and ev.pos[1] in range(10, 61):
						app.btn_return.act(app)
					elif ev.pos[0] in range(app.btn_newlvl.crd[0], app.btn_newlvl.crd[0] + 301) and ev.pos[1] in range(app.btn_newlvl.crd[1], app.btn_newlvl.crd[1] + 91):
						app.btn_newlvl.act(app)
			elif ev.type == pg.KEYDOWN:
				if app.mode == 31:
					if ev.key != pg.K_BACKSPACE:
						for i in app.ent_list:
							if i.choosed:
								i.add_let(ev.key)
					else:
						for i in app.ent_list:
							if i.choosed:
								i.str = i.str[:-1]
			elif ev.type == pg.MOUSEBUTTONDOWN and ev.button == 4 and app.pady != 110 and app.mode in (30, 1):
				app.pady += 10
			elif ev.type == pg.MOUSEBUTTONDOWN and ev.button == 5 and app.mode in (30, 1):
				app.pady -= 10
			elif ev.type == pg.MOUSEBUTTONUP:
				pressed = False
		if pressed:
			app.check_sliders(ev.pos[0], ev.pos[1])
		pg.display.update()
	pg.quit()

if __name__ == '__main__':
	main()