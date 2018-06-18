import pygame, sys, math, time 
from pygame.locals import *

DisplayMistakes = True  
DisplayPossible = True  

FPS = 60
SleepTime = 0.1
CellSize = 72
FontSize = CellSize / 20 * 6
LargeFontSize = CellSize
MediumFontSize = CellSize / 7 * 5
CellsX = 9
CellsY = 9
SmallCellSize = CellSize / 3
ThinLineWidth = 4
ThickLineWidth = 6
CellPadding = CellSize / 12
TopLeftGrid = CellSize, CellSize

OffWhite   = (200, 220, 240)
White      = (220, 240, 240)
LightGray  = (150, 150, 150)
Black      = (0  , 0  , 0  )
Blue       = (102, 194, 255)
Green      = (0  , 255, 0  )
Red        = (255, 0  , 0  )
DarkBlue   = (0  , 115, 153)
AlphaValue = 100

FullCell = [1, 2, 3, 4, 5, 6, 7, 8, 9]
FullCellQuantities = [9, 9, 9, 9, 9, 9, 9, 9, 9]
Labels = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
RomanNumerals = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]

NumberKeyValues = [49, 50, 51, 52, 53, 54, 55, 56, 57]

TopLeft = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]
MidLeft = [[3,0],[3,1],[3,2],[4,0],[4,1],[4,2],[5,0],[5,1],[5,2]]
BotLeft = [[6,0],[6,1],[6,2],[7,0],[7,1],[7,2],[8,0],[8,1],[8,2]]

TopMid = [[0,3],[0,4],[0,5],[1,3],[1,4],[1,5],[2,3],[2,4],[2,5]]
MidMid = [[3,3],[3,4],[3,5],[4,3],[4,4],[4,5],[5,3],[5,4],[5,5]]
BotMid = [[6,3],[6,4],[6,5],[7,3],[7,4],[7,5],[8,3],[8,4],[8,5]]

TopRight = [[0,6],[0,7],[0,8],[1,6],[1,7],[1,8],[2,6],[2,7],[2,8]]
MidRight = [[3,6],[3,7],[3,8],[4,6],[4,7],[4,8],[5,6],[5,7],[5,8]]
BotRight = [[6,6],[6,7],[6,8],[7,6],[7,7],[7,8],[8,6],[8,7],[8,8]]

BigCells = [TopLeft, MidLeft, BotLeft, TopMid, MidMid, BotMid, TopRight, MidRight, BotRight]


class Interface:
	def __init__(self):
		pygame.init()

		if DisplayPossible:
			self.WindowWidth = (CellsX  + 4) * CellSize + (ThinLineWidth / 2)
			self.WindowHeight = (CellsY + 2) * CellSize + (ThinLineWidth / 2)
		else:
			self.WindowWidth = (CellsX + 1) * CellSize + (ThinLineWidth / 2)
			self.WindowHeight = (CellsY + 1) * CellSize + (ThickLineWidth / 2) 

		self.DisplayScreen = pygame.display.set_mode((self.WindowWidth,self.WindowHeight))

		self.clock = pygame.time.Clock()

		self.initInterFace()

	def initInterFace(self):
		self.running = True
		self.initCells()
		self.startingCells = self.currentGrid
		self.mistakeCells = []
		self.initColumnValues()
		self.initRowValues()
		self.initBoxValues()

		self.displayCurrentCell = False 
		self.currentCell = [0,0]

		self.basicFont = pygame.font.Font('freesansbold.ttf', FontSize)
		self.largeFont = pygame.font.Font('freesansbold.ttf', LargeFontSize)
		self.mediumFont = pygame.font.Font('freesansbold.ttf', MediumFontSize)

	def initCells(self):
		self.currentGrid = {}
		for x in range(CellsX):
			for y in range(CellsY):
				self.currentGrid[x,y] = list(FullCell)

	def initColumnValues(self):
		self.columnValues = []
		for x in range(9):
			self.columnValues.append(list(FullCellQuantities))

	def initRowValues(self):
		self.rowValues = []
		for y in range(9):
			self.rowValues.append(list(FullCellQuantities))

	def initBoxValues(self):
		self.boxValues = []
		for z in range(9):
			self.boxValues.append(list(FullCellQuantities))

	def drawGrid(self):
		for x in range(0, self.WindowWidth, CellSize):
			pygame.draw.line(self.DisplayScreen, LightGray, (x, 0), (x, self.WindowHeight), ThinLineWidth)
		for y in range(0, self.WindowHeight, CellSize):
			pygame.draw.line(self.DisplayScreen, LightGray, (0, y), (self.WindowWidth, y), ThinLineWidth)

		for x in range(CellSize, self.WindowWidth, CellSize * 3):
			pygame.draw.line(self.DisplayScreen, Black, (x, 0), (x, self.WindowHeight), ThickLineWidth)
		for y in range(CellSize, self.WindowHeight, CellSize * 3):
			pygame.draw.line(self.DisplayScreen, Black, (0, y), (self.WindowWidth, y), ThickLineWidth)

	def drawPossibleValues(self):
		for cell in self.currentGrid:
			if isinstance(self.currentGrid[cell], list):
				if DisplayPossible:
					for number in self.currentGrid[cell]:
						if number != "":
							self.drawSmallNumbers(number, cell)
				else:
					for x in range(1,10):
						self.drawSmallNumbers(x, cell)
			else: 
				self.drawLargeNumbers(cell)


	def roundFunction(self, number, base):
		return int(base * round(float(number)/base))

	def drawLargeNumbers(self, cell): 
		if not isinstance(self.startingCells[cell], list):
			color = Black
		else:
			color = Blue
		textSurf = self.largeFont.render("%s" %(self.currentGrid[cell]), True, color)
		textRect = textSurf.get_rect()
		textRect.topleft = (((cell[0] + 1) * CellSize) + CellSize / 4, ((cell[1] + 1) * CellSize) + CellSize / 12)
		self.DisplayScreen.blit(textSurf, textRect)

	def drawSmallNumbers(self, number, cell):
		offSetX = ((number + 2) % 3) * CellSize / 3
		offSetY = ((self.roundFunction((number + 1), 3) / 3) - 1) * CellSize / 3
		textSurf = self.basicFont.render("%s" %(number), True, Black)
		textRect = textSurf.get_rect()
		textRect.topleft = (((cell[0] + 1) * CellSize + offSetX + CellPadding), ((cell[1] + 1) * CellSize + offSetY + CellPadding - CellPadding / 2))
		self.DisplayScreen.blit(textSurf, textRect)

	def drawSelectBox(self):
		currentMouseXPos = (self.mousePositionX + ThickLineWidth / 2) / (SmallCellSize)
		currentMouseYPos = (self.mousePositionY + ThickLineWidth / 2) / (SmallCellSize)

		xCoord = currentMouseXPos * (SmallCellSize)
		yCoord = currentMouseYPos * (SmallCellSize)

		if xCoord >= CellSize and yCoord >= CellSize and xCoord < CellSize * 10 and yCoord < CellSize * 10:
			pygame.draw.rect(self.DisplayScreen, Blue, (xCoord + ThickLineWidth / 2, yCoord + ThickLineWidth / 2, FontSize, FontSize), 3)

	def drawLabels(self):
		for n in range(1,10):
			textSurf = self.largeFont.render("%s" %(n), True, DarkBlue)
			textRect = textSurf.get_rect()
			textRect.topleft = (n * CellSize + CellSize / 6 + ThickLineWidth,0)
			self.DisplayScreen.blit(textSurf, textRect)

		for x in range(len(Labels)):
			textSurf = self.largeFont.render("%s" %(Labels[x]), True, DarkBlue)
			textRect = textSurf.get_rect()
			textRect.midtop = (CellSize / 2, (x + 1) * CellSize + ThickLineWidth)
			self.DisplayScreen.blit(textSurf, textRect)

		for z in range(len(RomanNumerals)):
			textSurf = self.mediumFont.render("%s" %(RomanNumerals[z]), True, DarkBlue)
			textRect = textSurf.get_rect()
			textRect.midtop = (CellSize * 11 + CellSize / 2, (z + 1) * CellSize + ThickLineWidth + (CellSize / 8))
			self.DisplayScreen.blit(textSurf, textRect)

	def drawPossibleColumns(self):
		for x in range(len(self.columnValues)):
			value = 0
			for number in self.columnValues[x]:
				value += 1 
				if number != 0:
					cell = [x, 9]
					offSetX = ((value + 2) % 3) * CellSize / 3
					offSetY = ((self.roundFunction((value + 1), 3) / 3) - 1) * CellSize / 3
					textSurf = self.basicFont.render("%s" %(number), True, Black)
					textRect = textSurf.get_rect()
					textRect.topleft = (((cell[0] + 1) * CellSize + offSetX + CellPadding), ((cell[1] + 1) * CellSize + offSetY + CellPadding - CellPadding / 2))
					self.DisplayScreen.blit(textSurf, textRect)

	def drawPossibleRows(self):
		for y in range(len(self.rowValues)):
			value = 0
			for number in self.rowValues[y]:
				value += 1 
				if number != 0:
					cell = [9, y]
					offSetX = ((value + 2) % 3) * CellSize / 3
					offSetY = ((self.roundFunction((value + 1), 3) / 3) - 1) * CellSize / 3
					textSurf = self.basicFont.render("%s" %(number), True, Black)
					textRect = textSurf.get_rect()
					textRect.topleft = (((cell[0] + 1) * CellSize + offSetX + CellPadding), ((cell[1] + 1) * CellSize + offSetY + CellPadding - CellPadding / 2))
					self.DisplayScreen.blit(textSurf, textRect)

	def drawPossibleBoxes(self):
		for y in range(len(self.boxValues)):
			value = 0
			for number in self.boxValues[y]:
				value += 1 
				if number != 0:
					cell = [9, y]
					offSetX = ((value + 2) % 3) * CellSize / 3
					offSetY = ((self.roundFunction((value + 1), 3) / 3) - 1) * CellSize / 3
					textSurf = self.basicFont.render("%s" %(number), True, Black)
					textRect = textSurf.get_rect()
					textRect.topleft = (((cell[0] + 3) * CellSize + offSetX + CellPadding), ((cell[1] + 1) * CellSize + offSetY + CellPadding - CellPadding / 2))
					self.DisplayScreen.blit(textSurf, textRect)

	def drawMistakes(self):
		for cell in self.mistakeCells:
			pygame.draw.rect(self.DisplayScreen, Red, ((cell[0] + 1) * CellSize, (cell[1] + 1) * CellSize, CellSize, CellSize),0)

	def drawCurrentBox(self):
		selectBox = pygame.Surface((CellSize, CellSize))
		selectBox.set_alpha(AlphaValue)
		selectBox.fill(Black)
		self.DisplayScreen.blit(selectBox, ((self.currentCell[0] + 1) * CellSize, (self.currentCell[1] + 1) * CellSize))

	def submitValue(self):
		currentPosSmallX = (self.mousePositionX + ThickLineWidth / 2) / (SmallCellSize)
		currentPosSmallY = (self.mousePositionY + ThickLineWidth / 2) / (SmallCellSize)

		currentPosLargeX = ((self.mousePositionX - CellSize) + ThickLineWidth / 2) / (SmallCellSize * 3)
		currentPosLargeY = ((self.mousePositionY - CellSize) + ThickLineWidth / 2) / (SmallCellSize * 3)

		selectedValue = currentPosSmallX % 3 + (currentPosSmallY % 3 * 3) + 1

		if currentPosLargeX < 9 and currentPosLargeY < 9 and currentPosLargeX > -1 and currentPosLargeY > -1:
			if isinstance(self.currentGrid[currentPosLargeX, currentPosLargeY], list):
				if selectedValue in self.currentGrid[currentPosLargeX, currentPosLargeY]:
					self.currentGrid[currentPosLargeX, currentPosLargeY] = selectedValue
					self.displayCurrentCell = True 
					self.currentCell = [currentPosLargeX, currentPosLargeY]
					self.removeImpossible()

	def removeValue(self):
		currentPosLargeX = ((self.mousePositionX - CellSize) + ThickLineWidth / 2) / (SmallCellSize * 3)
		currentPosLargeY = ((self.mousePositionY - CellSize) + ThickLineWidth / 2) / (SmallCellSize * 3)

		if not isinstance(self.currentGrid[currentPosLargeX, currentPosLargeY], list):
			self.displayCurrentCell = True
			self.currentCell = [currentPosLargeX, currentPosLargeY]

			self.currentGrid[currentPosLargeX, currentPosLargeY] = list(FullCell)
			self.refreshCells()


	def refreshCells(self):
		for cell in self.currentGrid:
			if isinstance(self.currentGrid[cell], list):
				self.currentGrid[cell] = list(FullCell)

		self.removeImpossible()

	def removeImpossible(self):
		for cell in self.currentGrid:
			if not isinstance(self.currentGrid[cell], list):
				for x in range(9):
					if isinstance(self.currentGrid[x, cell[1]], list):
						self.currentGrid[x, cell[1]][self.currentGrid[cell] - 1] = ""

				for y in range(9):
					if isinstance(self.currentGrid[cell[0], y], list):
						self.currentGrid[cell[0], y][self.currentGrid[cell] - 1] = ""

				for bigCell in BigCells:
					if [cell[0], cell[1]] in bigCell:
						for smallCell in bigCell:
							if isinstance(self.currentGrid[smallCell[0], smallCell[1]], list):
								self.currentGrid[smallCell[0], smallCell[1]][self.currentGrid[cell] -1] = ""

		self.updatePossibilities()
		self.checkForPointingPairs()
		self.checkForNakedPairs()
		# self.checkForXWings()
		self.checkForMistakes()

	def updatePossibilities(self):
		for x in range(9):
			quantitiesColumn = [0,0,0,0,0,0,0,0,0]
			for y in range(9):
				if isinstance(self.currentGrid[x,y], list):
					for z in range(1,10):
						if z in self.currentGrid[x,y]:
							quantitiesColumn[z-1] += 1 
			self.columnValues[x] = quantitiesColumn 	

		
		for y in range(9):
			quantitiesRow = [0,0,0,0,0,0,0,0,0]	
			for x in range(9):
				if isinstance(self.currentGrid[x,y], list):
					for z in range(1,10):
						if z in self.currentGrid[x,y]:
							quantitiesRow[z-1] += 1

			self.rowValues[y] = quantitiesRow


		for x in range(len(BigCells)):
			quantitiesBox = [0,0,0,0,0,0,0,0,0]	
			for z in range(9):
				index = BigCells[x][z]
				if isinstance(self.currentGrid[index[0], index[1]], list):
					for z in range(1,10):
						if z in self.currentGrid[index[0], index[1]]:
							quantitiesBox[z-1] += 1

			self.boxValues[x] = quantitiesBox

	def checkForPointingPairs(self):
		for x in range(len(self.boxValues)):
			for y in range(len(self.boxValues[x])):
				if self.boxValues[x][y] > 0 and self.boxValues[x][y] < 4 and self.boxValues[x][y] != 1:
					inLine, coloumn, row, value, coords = self.checkInLine(x,y)
					if inLine:
						if coloumn != None:
							for y in range(9):
								if isinstance(self.currentGrid[coloumn, y], list) and not [coloumn, y] in coords:
									self.currentGrid[coloumn, y][value - 1] = ""
						else:
							for x in range(9):
								if isinstance(self.currentGrid[x, row], list) and not [x, row] in coords:
									self.currentGrid[x, row][value - 1] = ""


	def checkForNakedPairs(self): # Currents only working in x axis 
		for cell in self.currentGrid:
			if isinstance(self.currentGrid[cell], list):
				if self.currentGrid[cell].count("") == 7:
					for x in range(9):
						if isinstance(self.currentGrid[cell], list):
							if self.currentGrid[x, cell[1]] == self.currentGrid[cell] and not x == cell[0]:
								values = []
								for value in self.currentGrid[cell]:
									if value != "":
										values.append(value)
								for z in range(9):
									if isinstance(self.currentGrid[z, cell[1]], list) and self.currentGrid[z, cell[1]] != self.currentGrid[cell]:
										self.currentGrid[z, cell[1]][values[0] -1] = ""
										self.currentGrid[z, cell[1]][values[1] -1] = ""


	def checkForXWings(self): # Currently Only Does Rows # Change for columns 
		for x in range(len(self.columnValues)):
			for y in range(len(self.columnValues[x])):
				if self.columnValues[x][y] == 2:
					value = y + 1
					yCoords = []
					for z in range(9):
						if isinstance(self.currentGrid[x, z], list):
							if value in self.currentGrid[x, z]:
								yCoords.append(z)
					for n in range(9): 
						if self.columnValues[z][y] == 2:
							if isinstance(self.currentGrid[n, yCoords[0]], list) and isinstance(self.currentGrid[n, yCoords[1]], list) and n != x:
								if value in self.currentGrid[n, yCoords[0]] and value in self.currentGrid[n, yCoords[1]]:
									print value, x, n, yCoords

	def checkInLine(self, x,  y):
		coords = []
		bigCell = BigCells[x]
		for cell in bigCell:
			if isinstance(self.currentGrid[cell[0], cell[1]], list):
				if y + 1 in self.currentGrid[cell[0], cell[1]]:
					coords.append(cell)

		if len(coords) >= 2:

			inLineX = True 
			xCoord = coords[0][0]

			

			for z in range(len(coords)):
				if coords[z][0] != xCoord:
					inLineX = False

			inLineY = True 
			yCoord = coords[0][0]
			for z in range(len(coords)):
				if coords[z][1] != yCoord:
					inLineY = False



			if inLineX:
				return True, coords[0][0], None, y + 1, coords

			elif inLineY:
				return True, None, coords[0][1], y + 1, coords

			else:
				return False, None, None, None, None
		else:
			return False, None, None, None, None 


	def checkForMistakes(self):
		mistakes = []
		for cell in self.currentGrid:
			if isinstance(self.currentGrid[cell], list):
				if self.currentGrid[cell].count("") == 9:
					mistakes.append(cell)


		self.mistakeCells = mistakes

	def solveLoop(self):
		successful = False 
		for cell in self.currentGrid:
			if isinstance(self.currentGrid[cell], list):
				if self.currentGrid[cell].count("") == 8:
					for value in self.currentGrid[cell]:
						if value != "":
							self.currentGrid[cell] = value 
							self.removeImpossible()
							successful = True
							self.updateScreen()
							time.sleep(SleepTime)

		for x in range(len(self.columnValues)):
			if 1 in self.columnValues[x]:
				value = self.columnValues[x].index(1) + 1
				for y in range(9):
					if isinstance(self.currentGrid[x,y], list):
						if value in self.currentGrid[x,y]:
							self.currentGrid[x,y] = value
							self.removeImpossible()
							successful = True
							self.updateScreen()
							time.sleep(SleepTime)

		for y in range(len(self.rowValues)):
			if 1 in self.rowValues[y]:
				value = self.rowValues[y].index(1) + 1
				for x in range(9):
					if isinstance(self.currentGrid[x,y], list):
						if value in self.currentGrid[x,y]:
							self.currentGrid[x,y] = value
							self.removeImpossible()
							successful = True
							self.updateScreen()
							time.sleep(SleepTime)


		return successful

	def solve(self):
		successful = self.solveLoop()
		while successful:
			successful = self.solveLoop()		

	def checkSolve(self):
		if len(self.mistakeCells) >= 1:
			return False
		else:
			for cell in self.currentGrid:
				if isinstance(self.currentGrid[cell], list):		
					return False

		return True 

		
	def solveStep(self):
		for cell in self.currentGrid:
			if isinstance(self.currentGrid[cell], list):
				if self.currentGrid[cell].count("") == 8:
					for value in self.currentGrid[cell]:
						if value != "":
							self.currentGrid[cell] = value 
							self.removeImpossible()
							self.updateScreen()
							return None 

		for x in range(len(self.columnValues)):
			if 1 in self.columnValues[x]:
				value = self.columnValues[x].index(1) + 1
				for y in range(9):
					if isinstance(self.currentGrid[x,y], list):
						if value in self.currentGrid[x,y]:
							self.currentGrid[x,y] = value
							self.removeImpossible()
							self.updateScreen()
							return None 

		for y in range(len(self.rowValues)):
			if 1 in self.rowValues[y]:
				value = self.rowValues[y].index(1) + 1
				for x in range(9):
					if isinstance(self.currentGrid[x,y], list):
						if value in self.currentGrid[x,y]:
							self.currentGrid[x,y] = value
							self.removeImpossible()
							self.updateScreen()
							return None 

	def updateScreen(self):
		self.DisplayScreen.fill(White)
		pygame.draw.rect(self.DisplayScreen, OffWhite, (CellSize, CellSize, CellSize * 9, CellSize * 9), 0)

		if DisplayMistakes:
			self.drawMistakes()
		self.drawGrid()
		if DisplayPossible:
			self.drawPossibleColumns()
			self.drawPossibleRows()
			self.drawPossibleBoxes()
		self.drawPossibleValues()
		self.drawLabels()
		self.drawSelectBox()
		if self.displayCurrentCell:
			self.drawCurrentBox()
		pygame.display.flip()		

	def terminate(self):
		pygame.quit()
		sys.exit()

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					self.terminate()
				elif event.type == MOUSEMOTION:
					self.mousePositionX, self.mousePositionY = event.pos
				elif event.type == MOUSEBUTTONDOWN:
					self.mousePositionX, self.mousePositionY = event.pos
					if pygame.mouse.get_pressed()[0]: 
						self.submitValue()
					elif pygame.mouse.get_pressed()[2]:
						self.removeValue()
				elif event.type == KEYDOWN:
					if event.key == K_SPACE:
						self.currentGrid = {(7, 3): [1, 2, '', '', '', '', 7, 8, 9], (4, 7): 3, (1, 3): 5, (4, 8): 2, (3, 0): 6, (2, 8): 8, (8, 0): [1, 2, '', '', '', '', '', '', ''], (7, 8): ['', '', 3, 4, '', '', 7, '', 9], (5, 4): ['', 2, '', '', 5, '', 7, '', 9], (0, 7): ['', 2, '', '', 5, '', '', '', 9], (5, 6): ['', '', '', 4, '', '', '', '', 9], (2, 6): [1, 2, 3, 4, '', '', '', '', 9], (1, 6): ['', 2, 3, 4, '', '', '', '', 9], (5, 1): ['', 2, 3, 4, '', '', 7, 8, ''], (8, 6): 5, (3, 7): ['', '', '', 4, 5, '', 7, 8, ''], (0, 3): 6, (8, 5): 4, (2, 5): ['', 2, 3, '', '', '', '', '', 9], (5, 8): 6, (4, 0): 5, (1, 2): ['', 2, '', 4, '', '', '', '', 9], (7, 4): 6, (6, 4): ['', 2, '', '', '', '', 7, 8, ''], (3, 3): [1, 2, 3, 4, '', '', '', 8, ''], (0, 6): 7, (8, 1): ['', 2, '', '', '', 6, 7, '', ''], (7, 6): ['', 2, 3, 4, '', '', '', 8, 9], (4, 4): ['', '', '', '', '', '', 7, 8, 9], (6, 3): ['', 2, '', '', '', '', 7, 8, ''], (1, 5): ['', 2, 3, '', '', '', 7, 8, 9], (8, 8): ['', '', '', '', '', '', 7, '', 9], (7, 2): [1, 2, '', 4, '', '', 7, '', ''], (3, 6): ['', '', '', 4, '', '', '', 8, ''], (2, 2): 6, (7, 7): ['', 2, '', 4, '', '', 7, 8, 9], (5, 7): 1, (5, 3): ['', 2, '', 4, '', '', 7, '', 9], (4, 1): 1, (1, 1): ['', 2, '', 4, '', '', '', 8, ''], (2, 7): ['', 2, '', 4, 5, '', '', '', 9], (3, 2): ['', 2, '', 4, '', '', '', '', ''], (0, 0): [1, 2, '', '', '', '', '', 8, ''], (6, 6): 6, (5, 0): ['', 2, 3, 4, '', '', '', 8, ''], (7, 1): ['', 2, '', 4, '', '', 7, '', ''], (4, 5): ['', '', '', '', '', 6, 7, 8, 9], (0, 4): 4, (5, 5): ['', 2, '', '', '', '', 7, '', 9], (1, 4): 1, (6, 0): 9, (7, 5): 5, (2, 3): ['', 2, 3, '', '', '', '', '', 9], (2, 1): ['', 2, '', 4, 5, '', '', '', ''], (8, 7): ['', 2, '', '', '', '', 7, '', 9], (6, 8): 1, (4, 2): ['', '', '', 4, '', '', 7, '', ''], (1, 0): ['', 2, '', 4, '', '', '', 8, ''], (0, 8): ['', '', '', '', 5, '', '', '', 9], (6, 5): ['', 2, '', '', '', '', 7, 8, ''], (3, 5): [1, 2, 3, '', '', '', '', 8, ''], (0, 1): ['', 2, '', '', 5, '', '', 8, ''], (8, 3): [1, 2, '', '', '', '', 7, '', 9], (7, 0): [1, 2, '', 4, '', '', '', '', ''], (4, 6): ['', '', '', 4, '', '', '', 8, 9], (6, 7): ['', 2, '', 4, '', '', 7, 8, ''], (5, 2): ['', 2, '', 4, '', '', 7, '', ''], (6, 1): ['', 2, 3, 4, 5, '', 7, '', ''], (3, 1): 9, (8, 2): 8, (2, 4): ['', 2, '', '', '', '', '', '', 9], (3, 8): ['', '', '', 4, 5, '', 7, '', ''], (2, 0): 7, (1, 8): ['', '', 3, 4, '', '', '', '', 9], (6, 2): ['', 2, '', 4, 5, '', 7, '', ''], (4, 3): ['', '', '', 4, '', '', 7, 8, 9], (1, 7): ['', 2, '', 4, '', 6, '', '', 9], (0, 5): ['', 2, '', '', '', '', '', 8, 9], (3, 4): ['', 2, '', '', '', '', '', 8, ''], (0, 2): 3, (8, 4): 3}
						self.currentGrid = {(7, 3): ['', '', 3, '', '', 6, '', '', 9], (4, 7): 6, (1, 3): [1, 2, '', '', '', 6, 7, '', ''], (4, 8): [1, 2, '', '', '', '', '', '', ''], (3, 0): 1, (2, 8): [1, 2, '', '', '', '', '', '', ''], (8, 0): 9, (7, 8): 5, (5, 4): 9, (0, 7): [1, 2, '', '', '', '', 7, '', ''], (5, 6): 8, (2, 6): 5, (1, 6): ['', 2, 3, '', '', '', 7, '', ''], (5, 1): ['', 2, '', '', 5, '', 7, '', ''], (8, 6): 1, (3, 7): ['', 2, '', 4, 5, '', '', '', ''], (0, 3): [1, 2, '', '', 5, '', 7, '', ''], (8, 5): ['', 2, 3, '', 5, 6, '', '', ''], (2, 5): 9, (5, 8): 3, (4, 0): ['', '', '', '', '', '', 7, '', ''], (1, 2): [1, 2, 3, '', '', '', '', '', ''], (7, 4): 7, (6, 4): ['', 2, '', '', 5, '', '', '', ''], (3, 3): ['', 2, 3, '', 5, '', '', '', ''], (0, 6): 6, (8, 1): ['', '', '', 4, 5, 6, '', '', ''], (7, 6): ['', '', 3, 4, '', '', '', '', ''], (4, 4): [1, 2, '', 4, 5, '', '', '', ''], (6, 3): 4, (1, 5): ['', 2, '', '', '', 6, 7, '', ''], (8, 8): ['', '', '', '', '', 6, '', '', ''], (7, 2): [1, '', 3, '', '', '', '', '', ''], (3, 6): 9, (2, 2): [1, 2, 3, '', '', '', '', '', ''], (7, 7): ['', '', 3, 4, '', '', '', 8, ''], (5, 7): [1, 2, '', '', 5, '', '', '', ''], (5, 3): [1, 2, '', '', 5, '', 7, '', ''], (4, 1): 3, (1, 1): 9, (2, 7): [1, 2, 3, '', '', '', 7, '', ''], (3, 2): 8, (0, 0): ['', '', '', '', '', '', 7, 8, ''], (6, 6): ['', 2, 3, '', '', '', 7, '', ''], (5, 0): 4, (7, 1): [1, '', '', 4, '', 6, '', 8, ''], (4, 5): 8, (0, 4): 3, (5, 5): ['', 2, '', '', 5, '', 7, '', ''], (1, 4): [1, 2, '', '', '', '', '', '', ''], (6, 0): ['', '', 3, '', '', 6, '', 8, ''], (7, 5): ['', '', 3, '', '', 6, '', '', ''], (2, 3): 8, (2, 1): [1, 2, '', '', '', 6, 7, '', ''], (8, 7): ['', 2, 3, 4, '', '', '', '', ''], (6, 8): ['', '', '', '', '', 6, '', 8, ''], (4, 2): ['', 2, '', '', 5, '', '', '', 9], (1, 0): 5, (0, 8): ['', '', '', '', '', '', '', '', 9], (6, 5): 1, (3, 5): ['', 2, 3, 4, 5, '', '', '', ''], (0, 1): [1, 2, '', '', '', '', 7, 8, ''], (8, 3): ['', 2, 3, '', 5, 6, '', '', ''], (7, 0): 2, (4, 6): ['', 2, '', 4, '', '', '', '', ''], (6, 7): 9, (5, 2): 6, (6, 1): ['', '', '', '', 5, 6, '', 8, ''], (3, 1): ['', 2, '', '', 5, '', '', '', ''], (8, 2): 7, (2, 4): [1, 2, '', 4, '', '', '', '', ''], (3, 8): 7, (2, 0): ['', '', 3, '', '', 6, 7, '', ''], (1, 8): 4, (6, 2): ['', '', 3, '', 5, '', '', '', ''], (4, 3): [1, 2, '', '', 5, '', 7, '', ''], (1, 7): [1, 2, 3, '', '', '', 7, 8, ''], (0, 5): ['', 2, '', '', 5, '', 7, '', ''], (3, 4): 6, (0, 2): 4, (8, 4): 8}
						self.startingCells = dict(self.currentGrid)

						self.removeImpossible()
					elif event.key == K_ESCAPE:
						self.terminate()

					elif event.key == K_RETURN:
						if not self.displayCurrentCell:
							self.startingCells = dict(self.currentGrid)
							self.solve()
						else:
							self.currentCell[0] += 1
							if self.currentCell[0] >= 9:
								self.currentCell[0] = 0
								self.currentCell[1] += 1
							self.updateScreen()
							if self.currentCell[1] >= 9:
								self.displayCurrentCell = False

					elif event.key == K_s:
						self.solveStep()
					elif event.key == K_p:
						print self.currentGrid
					elif event.key == K_t:
						# self.checkForNakedPairs()
						self.checkForXWings()
					elif event.key == K_b:
						self.initCells()
						self.startingCells = self.currentGrid
						self.mistakeCells = []
						self.initColumnValues()
						self.initRowValues()

						self.removeImpossible()

					elif event.key == K_BACKSPACE:
						if self.displayCurrentCell:
							self.currentGrid[self.currentCell[0], self.currentCell[1]] = list(FullCell)
							self.refreshCells()

					elif event.key == 48:
						self.displayCurrentCell = False 

					elif event.key <= 57 and event.key > 48:
						if self.displayCurrentCell == False:
							self.displayCurrentCell = True 
							self.currentCell = [0,0]
						else:
							numberKeyPressed = NumberKeyValues.index(event.key) + 1
							if isinstance(self.currentGrid[self.currentCell[0], self.currentCell[1]], list):
								if numberKeyPressed in self.currentGrid[self.currentCell[0], self.currentCell[1]]:
									self.currentGrid[self.currentCell[0], self.currentCell[1]] = numberKeyPressed
									self.currentCell[0] += 1
									if self.currentCell[0] >= 9:
										self.currentCell[0] = 0
										self.currentCell[1] += 1
									if self.currentCell[1] >= 9:
										self.displayCurrentCell = False
									self.removeImpossible()
									self.updateScreen()
									
					if event.key == K_UP or event.key == K_w:
						if self.currentCell[1] > 0:
							self.currentCell[1] -= 1
						else:
							self.currentCell[1] = 8
					if event.key == K_DOWN or event.key == pygame.K_s:
						if self.currentCell[1] < 8:
							self.currentCell[1] += 1
						else:
							self.currentCell[1] = 0
					if event.key == K_LEFT or event.key == pygame.K_a:
						if self.currentCell[0] > 0:
							self.currentCell[0] -= 1
						else:
							self.currentCell[0] = 8
					if event.key == K_RIGHT or event.key == pygame.K_d:
						if self.currentCell[0] < 8:
							self.currentCell[0] += 1
						else:
							self.currentCell[0] = 0

					if event.key == K_t:
						print self.checkSolve()


	
			self.clock.tick(FPS)
			self.updateScreen()

if __name__ == '__main__':
	Interface().run()
