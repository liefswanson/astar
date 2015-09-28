# Lief Swanson
# liefs@sfu.ca

# The purpose of this module is to create a layer of indirection
# Allowing the patching up of problems
# difficult to solve from inside the node class
# most of these have to do with when the root is a leaf,
# or could become a leaf after the operation
# also solves problems to do with empty trees

from TwoThreeNode import TwoThreeNode


class TwoThreeTree:
    def __init__(self):
        self.root  = None
        self.count = 0

    def __str__(self):
        return str(self.root)

    def list(self):
        if self.count == 0:
            return []
        if self.count == 1:
            return [self.root]
        else:
            return self.root.list()

    def insert(self, value):
        if self.count == 0:
            self.root = value
        elif self.count == 1:
            temp   = self.root
            left   = min(temp, value)
            middle = max(temp, value)
            self.root = TwoThreeNode(None,
                                     2,
                                     left, middle,
                                     left, middle, None)
        else:
            self.root.insert(value)
            if self.root.parent is not None:
                self.root = self.root.parent
        self.count += 1

    def delete(self, value):
        deleted = True
        if self.count == 0:
            # throw error, cannot delete from empty tree
            # or simply say that the desired value did not exist
            deleted = False
        elif self.count == 1:
            if self.root == value:
                # just delete the root
                self.root = None
                deleted = True
            else:
                deleted = False
        elif self.count == 2:
            # a child, and make the other the root
            if self.root.left == value:
                self.root = self.root.middle
                deleted = True
            elif self.root.middle == value:
                self.root = self.root.left
                deleted = True
            else:
                deleted = False
        elif self.count == 3:
            deleted = self.root.unPinNode(value)
        else:
            # delegate to TwoThreeNode
            deleted = self.root.delete(value)
            # check if the root has been collapsed
            if (self.root.left.parent is None):
                self.root = self.root.left

        if deleted:
            self.count -= 1
        return deleted

    def select(self, index):
        if index < 0:
            index = self.count + index

        if self.count == 1 and index == 0:
            return self.root
        else:
            return self.root.select(index)

    def __getitem__(self, index):
        return self.select(index)

    def search(self, value):
        if self.count == 1 and value == self.root:
            return self.root
        else:
            return self.root.search(value, 0)

    def min(self):
        return self.select(0)

    def max(self):
        return self.select(-1)
