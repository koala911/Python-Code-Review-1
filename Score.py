class Score:
    def __init__(self):
        self.points = 0
        self.point_per_sec = 0

    def increase(self, points):
        self.points += points

    def update_points_per_sec(self, points_per_sec):
        self.point_per_sec += points_per_sec

    def __str__(self):
        return str(round(self.points, 2))
