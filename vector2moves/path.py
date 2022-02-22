

class Path:
    def __init__(self):
        self.parts = []

    def sNext(self):
        for part in self.parts:
            for point in part:
                yield point

    def addPart(self, part):
        self.parts.append(part)

    def __iter__(self):
        return self.sNext()
