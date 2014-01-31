from graphics import *
class TicTacToe:
	"""Simple self managing TicTacToe class"""
	def __init__(self):
		self.grid=[0 for _ in range(9)]
		self.player=1
		self.wonBy=None
		self.moves=0
		self.elements=[]
		if not hasattr(self, 'win'):
			self.text=["Click to restart","X's move", "O's move"]
			self.winCombos=[ (0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6) ]
			self.windowSize=300
			self.win = GraphWin('TicTacToe', self.windowSize, self.windowSize+20)
			instPt = Point(self.windowSize/2, 20)
			self.instructions = Text(instPt, "")
			self.instructions.draw(self.win)
			self.win.setCoords(0,0,3,3.5)
			Line(Point(1,0), Point(1,3)).draw(self.win)
			Line(Point(2,0), Point(2,3)).draw(self.win)
			Line(Point(0,1), Point(3,1)).draw(self.win)
			Line(Point(0,2), Point(3,2)).draw(self.win)

		self.instructions.setText(self.text[self.player])

	def go(self):
		while self.wonBy == None and self.win.isOpen():
			self.getMove()

	def makeSelection(self, point):
		selection=convert2Selection(point)
		self.grid[selection] = self.player
		self.moves += 1
		if self.player==1:
			self.drawX(point)
		else:
			self.drawO(point)

		for combo in self.winCombos:
			if selection in combo:
				self.checkWin(combo)

		if self.moves == 9 or self.wonBy != None:
			self.reset()

		self.swapPlayer()
		#self.show()

	def checkWin(self, combo):
		if self.grid[combo[0]] == self.grid[combo[1]] == self.grid[combo[2]]:
			self.wonBy=combo
			self.drawWinningLine()
			#self.win.close()

	def swapPlayer(self):
		self.player%=2
		self.player+=1
		self.instructions.setText(self.text[self.player])

	def show(self):
		for i in range(3):
			line = ""
			for j in range(3):
				line += str(self.grid[i*3 + j])
			print(line)

	def getMove(self):
		p=self.win.getMouse()
		if p.getX() >= 3.0 or p.getY() >= 3.0:
			return
		else:
			p.setX(int(p.getX()))
			p.setY(int(p.getY()))
			if self.grid[convert2Selection(p)] == 0:
				self.makeSelection(p)

	def drawX(self, point):
		x=point.getX()+0.05
		y=point.getY()+0.05
		a=Line(Point(x,y), Point(x+0.9,y+0.9))
		a.draw(self.win)
		b=Line(Point(x, y+0.9), Point(x+0.9, y))
		b.draw(self.win)
		self.elements.append(a)
		self.elements.append(b)

	def drawO(self, point):
		point.move(0.5, 0.5)
		c=Circle(point, .45)
		c.draw(self.win)
		self.elements.append(c)

	def drawWinningLine(self):
		a=convert2Point(self.wonBy[0])
		b=convert2Point(self.wonBy[2])
		rise=(a.getY()-b.getY())/4
		run = (a.getX()-b.getX())/4
		a.move(run, rise)
		b.move(-run, -rise)
		line=Line(a,b)
		line.setOutline('red')
		line.setWidth(3)
		line.draw(self.win)
		self.elements.append(line)
		#print("a: {},{}\tb: {},{}\trise: {}\trun: {}".format(a.getX(), a.getY(), b.getX(), b.getY(), rise, run))

	def reset(self):
		self.instructions.setText(('Click to restart'))
		self.win.getMouse()
		for e in self.elements:
			e.undraw()
		self.__init__()
		self.go()


def convert2Selection(Point):
	return Point.getX() + (2-Point.getY())*3
def convert2Point(selection):
	x=(selection%3)
	y=2-int((selection-x)/3)
	return Point(x+0.5,y+0.5)