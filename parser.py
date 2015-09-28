from sys import argv
from Vertex import Vertex
from PathFind import *

path = argv[1]

f = open(path, 'r')

vertices = [Vertex()]

lines = f.read().split('\n')

intoPos = True
for line in lines:
    if line == "":
        intoPos = False
        continue
    if intoPos:
        num, coord = line.split(':')
        longitude, latitude = coord.split(',')
        vertices.append(
            Vertex(int(num),
                   float(longitude), float(latitude)
            )
        )
    else:
        num, temp = line.split(':')
        adj = temp.split(',')
        if adj[-1].strip() == "":
            adj.pop()  # remove trailing empty val
        adj = [int(x) for x in adj]
        vertices[int(num)].adj = adj

# for v in vertices:
#     print(v)

graph = PathFind(vertices)

graph.djisktra(1, 100)
