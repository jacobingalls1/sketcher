from vector import Vector
from arrangePath.organizer import CoverGraphOrganizer


class Moves:  # MAKE ROOM FOR REAL MEN
    def __init__(self):
        self.points = []
        self.paths = []
        self.organizer = CoverGraphOrganizer()

    def addPath(self, path):
        self.paths.append(path)

    def doPoints(self):
        self.paths = self.organizer.organize(self.paths)
        for path in self.paths:
            for point in path:
                self.points.append(point)

    def sNext(self):
        self.doPoints()
        yield self.points[0]
        for i in range(len(self.points) - 1):
            yield self.points[i + 1] - self.points[i]

    def __iter__(self):
        return self.sNext()
