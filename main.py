import os
import sys
import time
import select
import tty
import termios
import random

WIDTH = 50
HEIGHT = 40
LENTH = 8
BTYPE = "-<>=~"



printc = sys.stdout.write


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])



class canvas(object):
	def __init__(self, players=1, hardness=1):
		self.width = WIDTH
		self.hight = HEIGHT
		self.player1 = man()
		self.score = 0
		with open("best.txt") as f:
			self.bestscore = int(f.read())
		self.init_boards()
		self.init_canvas()
		self.display()
		self.start()

	def init_boards(self):

		self.boards = []
		b1 = board("-")
		self.boards.append(b1)

		# btest = board('<',20,20)
		# self.boards.append(btest)

		x = random.sample(range(0,WIDTH-LENTH),4)
		y = random.sample(range(11,HEIGHT),4)
		for i in range(0,4):
			b = board(random.choice(BTYPE),x[i],y[i])
			self.boards.append(b)

	def allup(self):
		self.player1.isstand(self.boards)
		flag1 = self.player1.stand

		for i, b in enumerate(self.boards):
			b.moveup()
			if b.y == 0:
				del self.boards[i]

		self.player1.isstand(self.boards)
		flag2 = self.player1.stand

		if flag1 == False and flag2==False:
			self.player1.falling()
		elif flag1 == False and flag2 == True:
			pass
		else:
			self.player1.moveup()

		if random.random() > 0.45:
			# random.choice("-^<>")
			x = random.randint(1,WIDTH-LENTH)
			b = board(random.choice(BTYPE), x, HEIGHT-1)
			self.boards.append(b)


	def display_txt(self, text):
		i = 20
		for t in text:
			self.screen[20][i] = t
			i +=1

	def display(self):
		os.system("clear")
		self.init_canvas()

		for b in self.boards:
			b.output(self.screen)

		if self.player1.live:
			self.screen[self.player1.y][self.player1.x] = "$"
		else:
			if self.score > self.bestscore:
				with open("best.txt", 'w') as f:
					f.write(str(self.score))
				self.display_txt("game over~ good job")
			else:
				self.display_txt("game over~")

		print "score: %d\t\t best:%d"% (self.score, self.bestscore)
		
		# for i in self.screen:
		# 	print "".join(i)

		for i in self.screen:
			for j in i :
				if j == '^':
					printc(bcolors.FAIL + j + bcolors.ENDC)
				# elif j == '|':
				# 	printc(bcolors.HEADER + j + bcolors.ENDC)
				# elif j == '-':
					# printc(bcolors.FAIL + j + bcolors.ENDC)
				elif j == '>' or j == '<':
					printc(bcolors.OKGREEN + j + bcolors.ENDC)
				elif j == '=':
					printc(bcolors.OKBLUE + j + bcolors.ENDC)
				elif j == '~':
					printc(bcolors.HEADER + j + bcolors.ENDC)
				else:
					printc(j)
			print ""


	def start(self):
		old_settings = termios.tcgetattr(sys.stdin)
		try:
		    tty.setcbreak(sys.stdin.fileno())
		    i = 0
		    while 1:
		    	# score system
		        i += 1
		        if i > 10 and self.player1.live:
		        	self.score += 1
		        	i = 0
		        time.sleep(0.1)

		        self.allup()


		        if isData():
		            c = sys.stdin.read(1)
		            print c
		            if c == 'A' or c == 'a':
		            	self.player1.moveleft()
		            if c == 'D' or c == 'd':
		            	self.player1.moveright()
		            if c == '\x1b':         # x1b is ESC
		                break
		        self.display()

		finally:
		    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

	def init_canvas(self):
		self.screen = [([' '] * self.width) for i in range(self.hight)]
		for i in xrange(self.width):
			self.screen[0][i] = "^"
		for i in xrange(self.hight):
			self.screen[i][0] = "|"
			self.screen[i][self.width-1] = "|"
		pass

	def init_player(self, players):
		self.players = []
		for x in xrange(players):
			player = man()
			self.players.append(player)  

# muti static
class man(object):
	def __init__(self):
		self.x = 25
		self.y = 15
		self.stand = False
		self.live = True

	def isstand(self, boards):
		self.stand = False
		for i, b in enumerate(boards):
			if b.y == self.y+1 and self.x < b.x+b.lenth and self.x >= b.x:
				self.stand = True
				if b.btype != '-':
					b.affect(self)
				if b.btype == '~':
					del boards[i]
				break

	def moveright(self):
		if self.x < WIDTH-2:
			self.x += 1
		
	def moveleft(self):
		if self.x > 1:
			self.x -= 1

	def moveup(self):
		if self.y > 0:
			self.y -= 1
		else:
			self.live = False

	def falling(self):
		if self.y < HEIGHT-1:
			self.y += 1
		else:
			self.live = False


	# def stand(self):


class board(object):
	def __init__(self, btype, x=23, y=17):
		self.x = x
		self.y = y
		self.btype = btype
		self.lenth = LENTH
		self.live = True

	def affect(self, player):
		if self.btype == '^':
			player.live = False
		if self.btype == '<':
			player.moveleft()
		if self.btype == '>':
			player.moveright()
		if self.btype == '~':
			# del self
			player.moveup()
		if self.btype == '=':
			player.moveup()
			player.moveup()

	def moveup(self):
		if self.y > 0:
			self.y -= 1

	def output(self, screen):
		for i in xrange(self.lenth):
			screen[self.y][self.x+i] = self.btype
		pass


if __name__ == '__main__':
	game = canvas()
