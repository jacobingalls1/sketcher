import pygame.image

from moves2image.sketcher import Board
import pygame as pg
from vector2moves.moves import Moves
from vector2moves.path import Path
from vector2moves.pathComponent import CCurve
from vector import Vector
import time
from image2moves.image2borders import image2pathComponents

image = '/home/ophiuchus/PycharmProjects/etchASketch/images/che.png'
im = pygame.image.load(image)
im.set_alpha(127)
(WIDTH, HEIGHT) = im.get_rect().size
screen = pg.display.set_mode((WIDTH, HEIGHT))
screen.fill((255, 255, 255))
screen.blit(im, (20,20))
lWidth = 3

samplePoints = 10

m = Moves()
p = Path()
for part in image2pathComponents(image):
    m.addPath(part)
# p.addPart(CCurve(samplePoints, (Vector(200, 200), Vector(400, 200), Vector(300, 300))))
# m.addPath(p)

print(len(m.points))
print(len(m.paths))

while True:
    b = Board(screen, lWidth)
    for move in m:
        b.draw(move)
        pg.display.update()
        # time.sleep(.01)
    screen.fill((255, 255, 255))
    time.sleep(5)

# while True:
#     x, y = int(input()), int(input())
#     b.draw((x, y))
#     pg.display.update()


