import pygame
import numpy as np
import math

"""

Current issues

Y pos is jumping when mouse drag is down
Grid rendering stragely at certain zoom levels


"""


window = None
running = True

windowSize = (1600, 900)

gridSize = 40
wireSize = 10

renderGrid = True
hoverTile = [0, 0]

debugFont = None

def AlignValueLeft(n, b):
	return n - (n % b)


def AlignValueRight(n, b):
	return (n - (n % b)) + b


def Start():
	global debugFont

	debugFont = pygame.font.SysFont("monospace", 14)



def Input():
	global running, renderGrid

	Controller.userMousePos[0], Controller.userMousePos[1] = pygame.mouse.get_pos()

	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			running = False
		elif e.type == pygame.KEYDOWN:
			if e.key == pygame.K_w:
				Controller.userDirectional[0] = True
			elif e.key == pygame.K_d:
				Controller.userDirectional[1] = True
			elif e.key == pygame.K_s:
				Controller.userDirectional[2] = True
			elif e.key == pygame.K_a:
				Controller.userDirectional[3] = True
		elif e.type == pygame.KEYUP:
			if e.key == pygame.K_w:
				Controller.userDirectional[0] = False
			elif e.key == pygame.K_d:
				Controller.userDirectional[1] = False
			elif e.key == pygame.K_s:
				Controller.userDirectional[2] = False
			elif e.key == pygame.K_a:
				Controller.userDirectional[3] = False
			elif e.key == pygame.K_g:
				renderGrid = not renderGrid
		elif e.type == pygame.MOUSEBUTTONDOWN:
			if e.button == 1:
				Controller.userClick[0] = True
			elif e.button == 3:
				Controller.userClick[1] = True
			elif e.button == 2:
				Controller.userClick[2] = True
			elif e.button == 4:
				Controller.userScroll[0] = True
			elif e.button == 5:
				Controller.userScroll[1] = True
		elif e.type == pygame.MOUSEBUTTONUP:
			if e.button == 1:
				Controller.userClick[0] = False
			elif e.button == 3:
				Controller.userClick[1] = False
			elif e.button == 2:
				Controller.userClick[2] = False


# This function is separated from normal input in order to record the previous state of the system for things like click triggers.
# Warning: This function can and will run multiple times between calling Input()
def PostInput():
	Controller.userPrevClick = [Controller.userClick[0], Controller.userClick[1], Controller.userClick[2]]
	Controller.userScroll = [False, False]


def Update():
	global hoverTile


	# this adjusts the camera zoom according to controller
	if (Controller.userScroll[0]):
		Camera.zoom *= 2
	elif (Controller.userScroll[1]):
		Camera.zoom /= 2


	# this updates the camera's zoom positions
	Camera.div_pos = [Camera.pos[0] / Camera.zoom, Camera.pos[1] / Camera.zoom]
	Camera.mult_pos = [Camera.pos[0] * Camera.zoom, Camera.pos[1] * Camera.zoom]


	# Update Mouse Instance Position
	Controller.userMouseInstancePos = [Controller.userMousePos[0] + Camera.mult_pos[0], Controller.userMousePos[1] + Camera.mult_pos[1]]


	# this updates the tile being currently hovered by the mouse
	hoverTile[0] = AlignValueLeft((Controller.userMousePos[0] + Camera.pos[0]), gridSize) / gridSize
	hoverTile[1] = AlignValueLeft((Controller.userMousePos[1] + Camera.pos[1]), gridSize) / gridSize

	# update camera position if any input is registed by the controller
	if not Camera.dragMode:
		if Controller.userDirectional[0]:
			Camera.pos[1] -= Camera.speed
		elif Controller.userDirectional[2]:
			Camera.pos[1] += Camera.speed
		if Controller.userDirectional[3]:
			Camera.pos[0] -= Camera.speed
		elif Controller.userDirectional[1]:
			Camera.pos[0] += Camera.speed

	# function triggers once to enable drag mode and record fixed data about mouse and camera position until dragging is complete
	if (Controller.userClick[2] and not Controller.userPrevClick[2]):
		Camera.dragPin = [Camera.pos[0], Camera.pos[0]]
		Camera.userMousePin = [Controller.userMousePos[0], Controller.userMousePos[1]]
		Camera.dragMode = True

	# function triggers once and disables drag mode, the last updated camera position is recorded
	if ((not Controller.userClick[2]) and Controller.userPrevClick[2]):
		Camera.dragMode = False

	# function updates camera position when in drag mode according to drag data involving camera position at start of drag and mouse position
	if (Camera.dragMode and Controller.userClick[2]):
		Camera.pos = [Camera.dragPin[0] - ((Controller.userMousePos[0] - Camera.userMousePin[0])*Camera.zoom), Camera.dragPin[1] - ((Controller.userMousePos[1] - Camera.userMousePin[1])*Camera.zoom)]
	
	#print("({0}, {1})".format(Camera.pos[0], Camera.pos[1]))


def RenderGrid():
	global gridSize, window, windowSize

	# the nearest chunk boundaries from the edge of the screen is recorded
	left = AlignValueLeft(Camera.div_pos[0], gridSize)
	right = AlignValueRight((Camera.div_pos[0]) + (windowSize[0]), gridSize)
	top = AlignValueLeft(Camera.div_pos[1], gridSize)
	bottom = AlignValueRight((Camera.div_pos[1]) + (windowSize[1]), gridSize)

	# vertical lines are rendered
	for n in np.arange(left, right, gridSize * Camera.zoom):
		pygame.draw.line(window, Colors.white, (n - (Camera.div_pos[0]), top - (Camera.div_pos[1])), (n - (Camera.div_pos[0]), bottom - (Camera.div_pos[1])))

	# horizontal lines are rendered
	for n in np.arange(top, bottom, gridSize * Camera.zoom):
		pygame.draw.line(window, Colors.white, (left - (Camera.div_pos[0]), n - (Camera.div_pos[1])), (right - (Camera.div_pos[0]), n - (Camera.div_pos[1])))


def renderDebugText(str, pos, c):
	global window, debugFont
	fbuffer = debugFont.render(str, 1, c)
	window.blit(fbuffer, pos)


def Render():
	global window, renderGrid, gridSize, hoverTile, debugFont

	window.fill(Colors.darkGray)

	if renderGrid:
		RenderGrid()

	pygame.draw.rect(window, Colors.black, (0,0,300,200))

	renderDebugText("Camera Pos: ({0}, {1})".format(math.floor(Camera.pos[0] / gridSize), math.floor(Camera.pos[1] / gridSize)), (10, 10), Colors.white)
	renderDebugText("Mouse Pos: ({0}, {1})".format(math.floor(Controller.userMouseInstancePos[0] / gridSize), math.floor(Controller.userMouseInstancePos[1]  / gridSize)), (10, 24), Colors.white)

	pygame.display.flip()


class Camera:
	pos = [0, 0]
	speed = 5

	zoom = 1.0
	div_pos = [0, 0]
	mult_pos = [0, 0]

	dragMode = False
	dragPin = [0, 0]

	userMousePin = [0, 0]


class Colors:
	white = (200, 200, 200)
	black = (0, 0, 0)
	darkGray = (50, 50, 50)
	red = (255, 0, 0)


class Controller:
	#NESW
	userDirectional = [False, False, False, False]
	#Lclick Rclick ScrollClick
	userClick = [False, False, False]
	userPrevClick = [False, False, False]

	userMousePos = [0, 0]
	userMouseInstancePos = [0, 0]

	# Scroll up, Scroll down
	userScroll = [False, False]

def main():
	global window, running, windowSize

	pygame.init()
	pygame.font.init()

	window = pygame.display.set_mode(windowSize)

	tps = 60
	tickNS = 1000 / tps

	tickDelta = 0

	lastTick = pygame.time.get_ticks()

	fps = 144
	frameNS = 1000 / fps

	lastFrame = pygame.time.get_ticks()

	Start()

	while running:
		Input()

		nowTick = pygame.time.get_ticks()

		tickDelta += (nowTick - lastTick) / tickNS

		lastTick = nowTick

		while tickDelta > 0.9999:
			tickDelta -= 1
			Update()
			PostInput()

		nowFrame = pygame.time.get_ticks()

		if (nowFrame - lastFrame > frameNS):
			Render()
			lastFrame = nowFrame



	return 0


if __name__ == "__main__":
	main()

