import pygame as pg


class Entery:
	def __init__(self, x, y, w, s, mode, text=''):
		self.x, self.y, self.w = x, y, w
		self.s = s
		self.font = pg.font.Font(None, s)
		self.str = text
		self.text = self.font.render(self.str, False, (255, 255, 255))
		if mode == 1:
			self.keys = {pg.K_q: 'q', pg.K_w: 'w', pg.K_e: 'e', pg.K_r: 'r', pg.K_t: 't',
						pg.K_y: 'y', pg.K_u: 'u', pg.K_i: 'i', pg.K_o: 'o', pg.K_p: 'p',
						pg.K_a: 'a', pg.K_s: 's', pg.K_d: 'd', pg.K_f: 'f', pg.K_g: 'g',
						pg.K_h: 'h', pg.K_j: 'j', pg.K_k: 'k', pg.K_l: 'l', pg.K_z: 'z',
						pg.K_x: 'x', pg.K_c: 'c', pg.K_v: 'v', pg.K_b: 'b', pg.K_n: 'n',
						pg.K_m: 'm', pg.K_1: '1', pg.K_2: '2', pg.K_3: '3', pg.K_4: '4',
						pg.K_5: '5', pg.K_6: '6', pg.K_7: '7', pg.K_8: '8', pg.K_9: '9', 
						pg.K_0: '0', pg.K_SPACE: ' ', pg.K_BACKSLASH: '\\', pg.K_PERIOD: '.'}
		else:
			self.keys = {pg.K_1: '1', pg.K_2: '2', pg.K_3: '3', pg.K_4: '4',pg.K_5: '5',
						pg.K_6: '6', pg.K_7: '7', pg.K_8: '8', pg.K_9: '9', pg.K_0: '0'}
		self.choosed = False

	def render(self, win):
		pg.draw.rect(win, (255, 255, 255), (self.x, self.y, self.w, self.s + 10), width=3)
		if self.choosed:
			self.text = self.font.render(f'{self.str}_', False, (255, 255, 255))
		else:
			self.text = self.font.render(self.str, False, (255, 255, 255))
		win.blit(self.text, (self.x + 5, self.y + 12))

	def add_let(self, key):
		if key in self.keys:
			self.str += self.keys[key]

	def get_value(self):
		return self.str


class Slider:
	def __init__(self, first, last, step, start, x, y, clr):
		self.xstep = 350 / (last - first)
		self.last = last
		self.pos = start
		self.font = pg.font.Font(None, 28)
		self.txt = self.font.render(str(self.pos), False, (clr, clr, clr))
		self.x, self.y = x, y
		self.clr = clr

	def render(self, win):
		x, y = self.x, self.y
		pg.draw.rect(win, (self.clr, self.clr, self.clr), (x, y + 20, 350, 5), width=0)
		pg.draw.rect(win, (self.clr, self.clr, self.clr), (x + self.xstep * (self.pos - 1) - 6, y, 11, 45), width=0)
		win.blit(self.txt, (x + self.xstep * (self.pos - 1) - 5, y - 20))

	def change(self, x):
		if self.pos <= self.last:
			self.pos = (x - self.x) // self.xstep + 1
			if self.pos == self.last - 1:
				self.pos = self.last
			elif self.pos == 1:
				self.pos = 0
			self.txt = self.font.render(str(int(self.pos)), False, (self.clr, self.clr, self.clr))

	def get_value(self):
		return int(self.pos)

	def set_value(self, val):
		if val in range(0, self.last + 1):
			self.pos = val
			self.txt = self.font.render(str(int(self.pos)), False, (self.clr, self.clr, self.clr))


class Button:
	def __init__(self, x, y, f, img1, img2, colorkey=True):
		self.crd = (x, y)
		self.func = f
		self.img = (pg.image.load(img1), pg.image.load(img2))
		if colorkey:
			for i in range(2):
				self.img[i].set_colorkey((0, 0, 0))
		self.cur_img = 0

	def act(self, app):
		self.func()

	def render(self, win):
		win.blit(self.img[self.cur_img], self.crd)