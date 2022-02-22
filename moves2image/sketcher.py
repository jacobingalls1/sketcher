import pygame as pg
from vector import Vector


pg.init()
PAD = 20


class Board:
    def __init__(self, surface, lwidth):
        self.board = surface
        self.mBoard = surface.get_size()
        self.cursor = Vector(PAD, PAD)
        self.color = (0, 0, 0)
        self.lwidth = lwidth

    def normalize(self):
        if self.cursor.x < 0:
            self.cursor.x = 0
        if self.cursor.y < 0:
            self.cursor.y = 0
        if self.cursor.x > self.mBoard[0]:
            self.cursor.x = self.mBoard[0]
        if self.cursor.y > self.mBoard[1]:
            self.cursor.y = self.mBoard[1]

    def draw(self, diff):
        oCursor = self.cursor * 1
        self.cursor += diff
        # self.normalize()
        pg.draw.line(self.board, self.color, (self.cursor.x, self.cursor.y),
                     (oCursor.x, oCursor.y), self.lwidth)

    def save(self, fName):
        pg.image.save(self.board, fName)





