from vector import Vector
import random


def pMid(t, p1, p2):
    return p2 * t + p1 * (1 - t)


class Component:
    def __init__(self, timestep, coords):
        self.timestep = timestep
        self.coords = coords

    def point(self, time):
        raise NotImplementedError

    def start(self):
        raise NotImplementedError

    def end(self):
        raise NotImplementedError

    def sample(self, n):  # n points
        raise NotImplementedError

    def sNext(self):
        for time in range(self.timestep + 1):
            t = time / self.timestep
            yield self.point(t)

    def __iter__(self):
        return self.sNext()


class CCurve(Component):
    def start(self):
        return self.coords[0]

    def end(self):
        return self.coords[1]

    def point(self, time):
        return pMid(time, pMid(time, self.coords[0], self.coords[2]), pMid(time, self.coords[2], self.coords[1]))


class SCurve(CCurve):
    def __init__(self, timestep, coords, startPoint):
        super().__init__(timestep, coords)
        self.coords = [startPoint] + coords


class Dots(Component):
    num = 0

    def __init__(self, points, timestep=0, coords=0):
        super().__init__(timestep, coords)
        self.points = points
        Dots.num += 1
        self.num = Dots.num

    def __repr__(self):
        return str(self.num)

    def start(self):
        return self.points[0]

    def end(self):
        return self.points[-1]

    def point(self, time):
        pass

    def addPoint(self, point):
        self.points.append(point)

    def sNext(self):
        factor = 1
        for p in range(len(self.points) // factor):
            yield self.points[p * factor]
        # yield self.points[0]

    def sample(self, n):
        if n > len(self.points):
            return self.points
        return random.sample(self.points, n)


        