class Vertex:
    def __init__(self, label=0,
                 longitude=0.0, latitude=0.0,
                 adj=[]):
        self.label = label

        self.longitude = longitude
        self.latitude  = latitude

        self.adj = adj

    def __str__(self):
        return str(self.label) + " " + str(self.longitude) + ", " + str(self.latitude) + " :\t" + str(self.adj)

    def __lt__(self, other):
        self.label < other.label

    def __le__(self, other):
        self.label <= other.label

    def __gt__(self, other):
        self.label > other.label

    def __ge__(self, other):
        self.label >= other.label

    def __eq__(self, other):
        self.label == other.label

    def __ne__(self, other):
        self.label != other.label
