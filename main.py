import pygame
import numpy as np

window = None
running = True

windowSize = (1600, 900)

gridSize = 40
wireSize = 10


def AlignValueLeft(n, b):
	return n - (n % b)


def AlignValueRight(n, b):
	return (n - (n % b)) + b


def Input():
	global running

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
		elif e.type == pygame.MOUSEBUTTONDOWN:
			if e.button == 1:
				Controller.userClick[0] = True
			elif e.button == 3:
				Controller.userClick[1] = True
			elif e.button == 2:
				Controller.userClick[2] = True
		elif e.type == pygame.MOUSEBUTTONUP:
			if e.button == 1:
				Controller.userClick[0] = False
			elif e.button == 3:
				Controller.userClick[1] = False
			elif e.button == 2:
				Controller.userClick[2] = False


NODE_WIRE = 0
NODE_INVERTER = 1
NODE_LOCKER = 2
NODE_SWITCH = 3
NODE_BUTTON = 4
NODE_OUTPUT = 5
NODE_LIGHTGUN = 6
NODE_CAPACITOR = 7
NODE_DIODE = 8
NODE_CROSSWIRE = 9


class Node:
	def __init__(self):
		self.inputNodes = []
		self.outputNodes = []
		self.sharedNodes = []
		self.horizontalNodes = []
		self.verticalNodes = []


def PostInput():
	Controller.userPrevClick = [Controller.userClick[0], Controller.userClick[1], Controller.userClick[2]]


def Update():
	if not Camera.dragMode:
		if Controller.userDirectional[0]:
			Camera.pos[1] -= Camera.speed
		elif Controller.userDirectional[2]:
			Camera.pos[1] += Camera.speed
		if Controller.userDirectional[3]:
			Camera.pos[0] -= Camera.speed
		elif Controller.userDirectional[1]:
			Camera.pos[0] += Camera.speed

	if (Controller.userClick[2] and not Controller.userPrevClick[2]):
		Camera.dragPos = [Camera.pos[0], Camera.pos[1]]
		Camera.userMousePin = [Controller.userMousePos[0], Controller.userMousePos[1]]
		Camera.dragMode = True

	if ((not Controller.userClick[2]) and Controller.userPrevClick[2]):
		Camera.dragMode = False

	if (Camera.dragMode and Controller.userClick[2]):
		Camera.pos = [Camera.dragPos[0] - (Controller.userMousePos[0] - Camera.userMousePin[0]), Camera.dragPos[1] - (Controller.userMousePos[1] - Camera.userMousePin[1])]


def RenderGrid():
	global aspect, gridSize, window, windowSize

	left = AlignValueLeft(Camera.pos[0], gridSize)
	right = AlignValueRight(Camera.pos[0] + (windowSize[0] / Camera.zoom), gridSize)
	top = AlignValueLeft(Camera.pos[1], gridSize)
	bottom = AlignValueRight(Camera.pos[1] + (windowSize[1] / Camera.zoom), gridSize)

	for n in np.arange(left, right, gridSize):
		pygame.draw.line(window, Colors.white, (n - Camera.pos[0], top - Camera.pos[1]), (n - Camera.pos[0], bottom - Camera.pos[1]))

	for n in np.arange(top, bottom, gridSize):
		pygame.draw.line(window, Colors.white, (left - Camera.pos[0], n - Camera.pos[1]), (right - Camera.pos[0], n - Camera.pos[1]))


def Render():
	global window

	window.fill(Colors.darkGray)

	RenderGrid()

	pygame.display.flip()


class Camera:
	pos = [0, 0]
	zoom = 1
	speed = 5

	dragMode = False
	dragPos = [0, 0]

	userMousePin = [0, 0]


class Colors:
	white = (255, 255, 255)
	black = (0, 0, 0)
	darkGray = (50, 50, 50)


class Controller:
	#NESW
	userDirectional = [False, False, False, False]
	#Lclick Rclick ScrollClick
	userClick = [False, False, False]
	userPrevClick = [False, False, False]

	userMousePos = [0, 0]

def main():
	global window, running, windowSize

	pygame.init()

	window = pygame.display.set_mode(windowSize)

	tps = 60
	tickNS = 1000 / tps

	tickDelta = 0

	lastTick = pygame.time.get_ticks()

	fps = 60
	frameNS = 1000 / fps

	lastFrame = pygame.time.get_ticks()

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

