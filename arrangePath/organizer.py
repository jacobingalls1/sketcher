from vector import Vector
from collections import defaultdict
import kdtree
from vector2moves.pathComponent import Dots
import random

SAMPLES = 100


def closestPoints(pc1, pc2):  # return 2 closest points from cloud 1 then cloud 2
    ret = (None, 9999999999999999)
    for p1 in pc1:
        for p2 in pc2:
            if (d := p1.distance(p2)) < ret[1]:
                ret = ((p1, p2), d)
    if not ret[0]:
        exit()
    return ret

class Organizer:
    def organize(self, paths, cursor):
        raise NotImplementedError

    @staticmethod
    def rotate(path, startPoint):
        ind = path.points.index(startPoint)
        path.points = path.points[ind:] + path.points[:ind]

    @staticmethod
    def backTrack(path, endPoint):
        ind = path.points.index(endPoint)
        path.points += path.points[ind:][::-1]


class TSMOrganizer(Organizer):
    def __init__(self):
        self.distances = defaultdict(lambda: {})
        self.origin = (99999999999999999999, None, None)

    def tsmMetric(self, p):
        return lambda point: self.distances[p][point][1] ** 2

    def travelingSalesman(self, cities):  # return the list in the order of traversal,starts closest to the origin
        ret = [self.origin[1]]
        cities.remove(self.origin[1])
        while cities:
            ret.append(min(cities, key=self.tsmMetric(ret[-1])))
            cities.remove(ret[-1])
        return ret

    def checkOrigin(self, cloud, cursor):  # (path, points)
        for point in cloud[1]:
            if (d := cursor.distance(point)) < self.origin[0]:
                self.origin = (d, cloud[0], point)

    def doDists(self, clouds, cursor):
        for p1 in range(len(clouds)):
            self.checkOrigin(clouds[p1], cursor)
            for p2 in range(p1):
                c1, c2 = clouds[p1], clouds[p2]
                cpo = closestPoints(c1[1], c2[1])
                self.distances[c1[0]][c2[0]] = cpo
                self.distances[c2[0]][c1[0]] = (cpo[0][::-1], cpo[1])

    def organize(self, paths, cursor=Vector(20, 20)):  # return paths
        print(len(paths))
        paths = [p for p in paths if len(p.points) > 1]
        pathSamples = [(p, p.sample(SAMPLES)) for p in paths]
        self.doDists(pathSamples, cursor)
        order = self.travelingSalesman(paths)
        self.rotate(order[0], self.origin[2])
        self.backTrack(order[0], self.distances[order[0]][order[1]][0][0])
        for i in range(1, len(order) - 1):
            self.rotate(order[i], self.distances[order[i]][order[i-1]][0][0])
            self.backTrack(order[i], self.distances[order[i]][order[i+1]][0][0])
        self.rotate(order[-1], self.distances[order[-1]][order[-2]][0][0])
        print(len(order))
        return order

class CurvePoint(Vector):
    def __init__(self, x, y, curve):
        super().__init__(x, y)
        self.curve = curve

class CoverGraphOrganizer(Organizer):
    def __init__(self):
        self.dots = Dots([])
        self.connections = defaultdict(lambda: [])
        self.distances = defaultdict(lambda: {})
        self.origin = (99999999999999999999, None, None)
        self.pathCount = 0

    def checkOrigin(self, cloud, cursor):  # (path, points)
        for point in cloud[1]:
            if (d := cursor.distance(point)) < self.origin[0]:
                self.origin = (d, cloud[0], point)

    def doDists(self, clouds, cursor):
        for p1 in range(len(clouds)):
            self.checkOrigin(clouds[p1], cursor)
            for p2 in range(p1):
                c1, c2 = clouds[p1], clouds[p2]
                cpo = closestPoints(c1[1], c2[1])
                self.distances[c1[0]][c2[0]] = cpo
                self.distances[c2[0]][c1[0]] = (cpo[0][::-1], cpo[1])

    def graphWalk(self, current, visited):
        if current in visited:
            return visited
        visited |= {current}
        # print(visited)
        for p in self.connections[current]:
            visited |= self.graphWalk(p, visited | {current})
        return visited

    def fullGraph(self):
        # print(len(self.graphWalk(list(self.distances.keys())[0], set())))
        return len(self.graphWalk(list(self.distances.keys())[0], set())) == len(list(self.distances.keys()))

    def makeFullGraph(self):
        edges = []
        done = []
        for k in self.distances.keys():
            done.append(k)
            for k2 in self.distances[k].keys():
                if k2 not in done:
                    edges.append((k, k2, self.distances[k][k2]))
        while not self.fullGraph():
            mn = min(edges, key=lambda e: e[2][1])
            self.connections[mn[0]].append(mn[1])
            self.connections[mn[1]].append(mn[0])
            edges.remove(mn)
        while sum([len(v) for v in self.connections.values()]) / 2 > len(list(self.connections.keys())) - 1:
            p1, p2 = random.choice(list(self.connections.keys())), random.choice(list(self.connections.keys()))
            if p1 not in self.connections[p2]:
                continue
            self.connections[p1].remove(p2)
            self.connections[p2].remove(p1)
            if not self.fullGraph():
                self.connections[p1].append(p2)
                self.connections[p2].append(p1)

    def doPath(self, path, startPoint, seen):
        self.pathCount += 1
        if not self.pathCount % 10:
            print(self.pathCount)
        seen += [path]
        self.rotate(path, startPoint)
        watchPaths = list(self.distances[path].keys())
        watchPoints = [self.distances[path][k][0][0] for k in watchPaths]
        for point in path:
            self.dots.addPoint(point)
            if point in watchPoints:
                nPath = watchPaths[watchPoints.index(point)]
                if nPath not in seen:
                    self.doPath(nPath, self.distances[nPath][path][0][0], seen)
            self.dots.addPoint(point)

    def organize(self, paths, sample=10, cursor=Vector(20, 20)):
        paths = [p for p in paths if len(p.points) > 10]
        pathSamples = [(p, p.sample(SAMPLES)) for p in paths]
        self.doDists(pathSamples, cursor)
        self.makeFullGraph()
        self.doPath(self.origin[1], self.origin[2], [])
        return [self.dots]
