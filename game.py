import pygame as pg
import main

run = True


class Game:
	def __init__(self, lvl, w, h, cs):
		# values
		self.FPS = 60
		self.w, self.h, self.cs = w, h, cs
		self.score = 0
		self.map = []
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
				elif i[:12] == 'music_volume':
					self.music_volume = float(i[i.find('=') + 1:-1])
				elif i[:14] == 'effects_volume':
					self.effects_volume = float(i[i.find('=') + 1:-1])
		self.amount = 0
		for i in self.map:
			if i != '0':
				self.amount += len(i)
		self.plus_score = 1000000 // self.amount
		self.font = pg.font.Font(None, 36)
		self.clicked = []
		self.bgcolor = (255, 255, 255)
		self.stat = []
		self.step = (self.FPS * self.speed) * (self.FPS / self.bpm) / 2

		# images
		self.cir_img = [pg.image.load('data/img/left_circle.bmp'), pg.image.load('data/img/up_circle.bmp'),
			pg.image.load('data/img/right_circle.bmp'), pg.image.load('data/img/down_circle.bmp')]
		for i in range(4):
			self.cir_img[i] = pg.transform.scale(self.cir_img[i], (cs * 2, cs * 2))
			self.cir_img[i].set_colorkey((0, 0, 0))

		# other
		self.text = self.font.render(f'Очки: {self.score}', False, (0, 0, 0))
		self.hitsound = pg.mixer.Sound('data/sounds/hitsound.wav')
		self.hitsound.set_volume(self.effects_volume)

	def render(self, win, mmt):
		win.blit(self.text, (0, 0))
		self.cur_circles = [None, None, None, None]
		for i in range(len(self.map)):
			for j in self.map[i]:
				if (int(j), i) not in self.clicked:
					if j == '1' and round(-i * self.step + mmt) in range(-self.cs, self.w // 2 + self.cs):
						win.blit(self.cir_img[0], (-i * self.step + mmt - self.cs, self.h // 2 - self.cs))
						if self.cur_circles[0] == None:
							self.cur_circles[0] = i
					elif j == '3' and round(self.w + i * self.step - mmt) in range(self.w // 2 - self.cs, self.w + self.cs):
						win.blit(self.cir_img[2], (self.w + i * self.step - mmt - self.cs, self.h // 2 - self.cs))
						if self.cur_circles[2] == None:
							self.cur_circles[2] = i
					elif j == '2' and round(-i * self.step + mmt) in range(-self.cs, self.h // 2 + self.cs):
						win.blit(self.cir_img[1], (self.w // 2 - self.cs, -i * self.step + mmt - self.cs))
						if self.cur_circles[1] == None:
							self.cur_circles[1] = i
					elif j == '4' and round(self.h + i * self.step - mmt) in range(self.h // 2 - self.cs, self.h + self.cs):
						win.blit(self.cir_img[3], (self.w // 2 - self.cs, self.h + i * self.step - mmt - self.cs))
						if self.cur_circles[3] == None:
							self.cur_circles[3] = i

	def click(self, single_clicks, keys, mmt):
		for i in range(len(single_clicks)):
			if single_clicks[i] and self.cur_circles[i] != None:
				self.clicked.append((i + 1, self.cur_circles[i]))
				self.hitsound.play()
				if i + 1 == 1:
					res = self.w // 2 - round(-self.cur_circles[i] * self.step + mmt)
				elif i + 1 == 3:
					res = self.w // 2 - round(self.w + self.cur_circles[i] * self.step - mmt)
				elif i + 1 == 2:
					res = self.h // 2 - round(-self.cur_circles[i] * self.step + mmt)
				elif i + 1 == 4:
					res = self.h // 2 - round(self.h + self.cur_circles[i] * self.step - mmt)
				if res in range(-1 * self.speed, 1 * self.speed + 1):
					self.score += self.plus_score
					self.bgcolor = (255, 255, 255)
					self.stat.append(100)
				elif res in range(-2 * self.speed, 2 * self.speed + 1):
					self.score += round(self.plus_score * 0.9375)
					self.bgcolor = (244, 244, 244)
					self.stat.append(100)
				elif res in range(-3 * self.speed, 3 * self.speed + 1):
					self.score += round(self.plus_score * 0.6666)
					self.bgcolor = (233, 233, 233)
					self.stat.append(66)
				elif res in range(-5 * self.speed, 5 * self.speed + 1):
					self.score += round(self.plus_score * 0.3125)
					self.bgcolor = (211, 211, 211)
					self.stat.append(31)
				else:
					self.bgcolor = (200, 200, 200)
					self.stat.append(0)
				self.text = self.font.render(f'Очки: {self.score}', False, (0, 0, 0))


class Player:
	def __init__(self, w, h, cs):
		self.w, self.h, self.cs = w, h, cs
		self.keys = [False, False, False, False]
		self.single_clicks = [False, False, False, False]
		self.imgs = [pg.image.load('data/img/senser_circle_activated.bmp'), pg.image.load('data/img/senser_circle_deactivated.bmp')]
		for i in range(2):
			self.imgs[i] = pg.transform.scale(self.imgs[i], (self.cs * 2, self.cs * 2))
			self.imgs[i].set_colorkey((0, 0, 0))

	def render(self, win):
		if self.keys != [False, False, False, False]:
			win.blit(self.imgs[0], (self.w // 2 - self.cs, self.h // 2 - self.cs))
		else:
			win.blit(self.imgs[1], (self.w // 2 - self.cs, self.h // 2 - self.cs))

	def click_check(self, game, mmt):
		if [False, False, False, False] != self.keys:
			game.click(self.single_clicks, self.keys, mmt)


def rtrn():
		global run
		run = False

def play_lvl(lvl, app):
	global run
	run = 1
	pg.init()
	w, h, cs = 600, 600, 30
	win = pg.display.set_mode((w, h))
	# run = True
	mmt = 0
	game = Game(lvl, w, h, cs)
	player = Player(w, h, cs)
	clock = pg.time.Clock()
	single = False
	stop_mmt = len(game.map) * game.step  + w // 2 + 400
	pg.mixer.music.load(f'data/lvl/{lvl}/music.mp3')
	pg.mixer.music.set_volume(game.music_volume)
	pg.mixer.music.play()
	# game
	while run:
		win.fill(game.bgcolor)
		if single:
			player.single_clicks = [False, False, False, False]
			single = False
		if mmt >= stop_mmt:
			run = False
		for ev in pg.event.get():
			if ev.type == pg.QUIT:
				run = False
			if ev.type == pg.KEYDOWN:
				if ev.key in (pg.K_a, pg.K_LEFT):
					player.keys[0] = True
					player.single_clicks[0] = True
					single = True
				elif ev.key in (pg.K_w, pg.K_UP):
					player.keys[1] = True
					player.single_clicks[1] = True
					single = True
				elif ev.key in (pg.K_d, pg.K_RIGHT):
					player.keys[2] = True
					player.single_clicks[2] = True
					single = True
				elif ev.key in (pg.K_s, pg.K_DOWN):
					player.keys[3] = True
					player.single_clicks[3] = True
					single = True
			elif ev.type == pg.KEYUP:
				if ev.key in (pg.K_a, pg.K_LEFT):
					player.keys[0] = False
				elif ev.key in (pg.K_w, pg.K_UP):
					player.keys[1] = False
				elif ev.key in (pg.K_d, pg.K_RIGHT):
					player.keys[2] = False
				elif ev.key in (pg.K_s, pg.K_DOWN):
					player.keys[3] = False
		player.render(win)
		game.render(win, mmt)
		player.click_check(game, mmt)
		pg.display.update()
		mmt += game.speed
		clock.tick(game.FPS)
	# result
	if len(game.stat) != 0:
		accuracy = round(sum(game.stat) / len(game.stat), 2)
	else:
		accuracy = 100
	pg.mixer.music.pause()
	run = True
	score = game.score
	if score >= 900000:
		img = pg.image.load('data/img/S.jpg')
	elif score >= 800000:
		img = pg.image.load('data/img/A.jpg')
	elif score >= 700000:
		img = pg.image.load('data/img/B.jpg')
	elif score >= 500000:
		img = pg.image.load('data/img/C.jpg')
	else:
		img = pg.image.load('data/img/D.jpg')
	img.set_colorkey((0, 0, 0))
	bg = pg.transform.scale(pg.image.load(f'data/lvl/{lvl}/bg.bmp'), (w, h))
	btn_return = main.Button(10, 10, rtrn, 'data/img/btn_return_unchoosed.bmp', 'data/img/btn_return_choosed.bmp')
	res_pan = pg.image.load('data/img/result_panel.bmp')
	res_pan.set_colorkey((0, 0, 0))
	scoretxt = game.font.render(f'Очки: {game.score} / 1000000', False, (255, 255, 255))
	acctxt = game.font.render(f'Точность: {accuracy}%', False, (255, 255, 255))
	while run:
		win.blit(bg, (0, 0))
		for ev in pg.event.get():
			if ev.type == pg.QUIT:
				run = False
			elif ev.type == pg.MOUSEMOTION:
				if ev.pos[0] in range(10, 61) and ev.pos[1] in range(10, 61):
					btn_return.cur_img = 1
				else:
					btn_return.cur_img = 0
			elif ev.type == pg.MOUSEBUTTONDOWN and ev.button in (1, 2, 3):
				if ev.pos[0] in range(10, 61) and ev.pos[1] in range(10, 61):
					btn_return.act(app)
		win.blit(img, (350, 0))
		win.blit(res_pan, (0, 0))
		win.blit(scoretxt, (10, 220))
		win.blit(acctxt, (10, 260))
		btn_return.render(win)
		pg.display.update()


if __name__ == '__main__':
	play_lvl('lvl_test', main.app)