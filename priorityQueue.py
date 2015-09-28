from TwoThreeTree import TwoThreeTree


class PriorityQueue:
    def __init__(self):
        self.tree = TwoThreeTree()

    def __len__(self):
        return self.tree.count

    def __str__(self):
        return str(self.tree.root)

    def enqueue(self, val):
        self.tree.insert(val)

    def dequeue(self):
        temp = self.tree.min()
        self.tree.delete(temp)
        return temp
