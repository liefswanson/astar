from priorityQueue import PriorityQueue
from math import sqrt


class PathFind:
    def __init__(self, vertices=[]):
        self.vertices = vertices

    def djisktra(self, a, b):
        distances = [float("inf") for _ in self.vertices]
        distances[a] = 0
        predecessors = [None for _ in self.vertices]
        # queue = PriorityQueue()
        queue = PriorityQueue()
        queue.enqueue((distances[a], self.vertices[a].label))

        while True:
            # print(queue)
            _, current = queue.dequeue()
            # dequeue a node we already looked at
            # this may not be necessary because it will just not decrease any travel times anyway
            if current is b:
                break
            else:
                # traverse adj list, and see if any are shorter than current dist
                for v in self.vertices[current].adj:
                    temp = distances[current] + weight(self.vertices[current],
                                                       self.vertices[v])
                    if distances[v] > temp:
                        distances[v] = temp
                        predecessors[v] = current
                        queue.enqueue((distances[a], v))

        print((distances, predecessors))
        return (distances, predecessors)

    def aStar(self, a, b):
        distances = [float("inf") for _ in self.vertices]
        return distances


def weight(a, b):
    return sqrt((a.longitude - b.longitude)**2 +
                (a.latitude  - b.latitude )**2)

# list of distance
# DONE

# set all to inf
# DONE

# set the source vertex distance to 0
# DONE

## create a priority queue of all the distances  call it H
# DONE

##while H is not empty
# DONE

# U=  min from H
# DONE
#remove min from H
# DONE

# check is U vertex the destination
# DONE
# if so return distance
# DONE

#else go through Adjancey list for the vertex
# DONE

#if new distance which is distance to current vertex + distance to next vertex < old distance
# DONE
# change the distance to the new shorter one
# DONE
# update piroirty queue
#if vertix not found return inf
#
