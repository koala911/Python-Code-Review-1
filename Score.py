class Score:
    def __init__(self):
        self.points = 0

    def increase(self, points):
        self.points += points

    def __str__(self):
        return str(self.points)
