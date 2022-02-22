import cv2
import numpy as np
import time
import kdtree
from vector import Vector
from vector2moves.pathComponent import Dots


def doBorders(image):
    _, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10,10))
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,4))
    image = cv2.morphologyEx(image, cv2.MORPH_ERODE, kernel)
    return image
    # return cv2.flip(image, 0)

def points(image):
    tree = kdtree.create(dimensions=2)
    for r in range(len(image)):
        for c in range(len(image[r])):
            if image[r][c]:
                tree.add(Vector(c, r))
    tree = tree.rebalance()
    return tree

def nearest(tree, point, threshold=10):
    nn = tree.search_nn(point)[0].data
    if point.distance(nn) < threshold:
        tree = tree.remove(nn)
        return nn, tree
    return nn, False

def shapes(tree):
    ret = []
    while tree:
        tree = tree.rebalance()
        nn = tree.search_nn((0,0))[0].data
        tree = tree.remove(nn)
        shape = Dots([])
        nTree = tree
        while nTree:
            shape.addPoint(nn)
            tree = nTree
            nn, nTree = nearest(tree, shape.end())
        ret.append(shape)
    return ret

def image2pathComponents(image):
    image = cv2.imread(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = doBorders(image)
    p = points(image)
    s = shapes(p)
    return s
