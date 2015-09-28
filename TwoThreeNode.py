# Lief Swanson
# liefs@sfu.ca


class TwoThreeNode:
    def __init__(self,
                 parent=None,
                 count=0,
                 smallest=None, largest=None,
                 left=None, middle=None, right=None):
        self.parent = parent
        self.count  = count

        self.smallest = smallest
        self.largest = largest

        self.left   = left
        self.middle = middle
        self.right  = right

    ########################
    # comparison operators #
    ########################

    def __lt__(self, other):
        if self.largest == other.largest:
            return self.smallest < other.smallest
        else:
            return self.largest < other.largest

    def __le__(self, other):
        if self.largest == other.largest:
            return self.smallest <= other.smallest
        else:
            return self.largest <= other.largest

    def __gt__(self, other):
        if self.largest == other.largest:
            return self.smallest > other.smallest
        else:
            return self.largest > other.largest

    def __ge__(self, other):
        if self.largest == other.largest:
            return self.smallest >= other.smallest
        else:
            return self.largest >= other.largest

    def __eq__(self, other):
        return (self.largest == other.largest and
                self.smallest == other.smallest)

    def __ne__(self, other):
        return (self.largest != other.largest or
                self.smallest != other.smallest)

    #############
    # to string #
    #############

    # delegates to recursive depth-first search "treeToStr"

    def __str__(self):
        return self.str(self, "")

    def str(self, node, indent=""):
        if isInterior(node):
            cargo = indent + "(v " + str(node.smallest) + \
                " : ^ " + str(node.largest) + \
                " : # " + str(node.count) + ')\n'
        else:
            return indent + str(node) + '\n'

        left   = node.str(node.left,   indent + " |")
        middle = node.str(node.middle, indent + " |")
        right  = ""
        if hasThreeChildren(node):
            right = node.str(node.right, indent + " |")

        return cargo + left + middle + right

    def list(self):
        if isInterior(self.left):
            if hasThreeChildren(self):
                output = (self.left.list() +
                          self.middle.list() +
                          self.right.list())
            else:
                output = (self.left.list() +
                          self.middle.list())
            return output
        else:
            if hasThreeChildren(self):
                output = [self.left,
                          self.middle,
                          self.right]
            else:
                output = [self.left,
                          self.middle]
            return output

    #########################
    # search implementation #
    #########################

    def search(self, value, index):
        if isInterior(self.left):
            # do recursions based on values
            if value <= self.left.largest:
                return self.left.search(value, index)

            index += self.left.count
            if value <= self.middle.largest:
                return self.middle.search(value, index)

            index += self.middle.count
            if (hasThreeChildren(self) and
                value <= self.right.largest):
                return self.right.search(value, index)
            return None
        else:
            # do inserts based on values
            if value == self.left:
                return index

            index += 1
            if value == self.middle:
                return index

            index += 1
            if value == self.right:
                return index

            return None

    #########################
    # select implementation #
    #########################

    def select(self, index):
        if isInterior(self.left):
            if index < self.left.count:
                return self.left.select(index)

            index -= self.left.count
            if index < self.middle.count:
                return self.middle.select(index)

            index -= self.middle.count
            if (hasThreeChildren(self) and
                index < self.right.count):
                return self.right.select(index)
            else:
                return None
        else:
            if index == 0:
                return self.left
            elif index == 1:
                return self.middle
            else:
                return self.right

    #########################
    # insert implementation #
    #########################

    # deals with everything to do with leaf level insertion
    # - traversal to leaf level
    # - insertion at leaf level
    # - splitting if two many leaves
    # - call recursive splitting algorithm to repair tree

    def insert(self, value):
        # check if we are one level above leaves
        if isInterior(self.left):
            # do recursions based on values
            if value <= self.left.largest:
                self.left.insert(value)
            elif (value <= self.middle.largest or
                  not hasThreeChildren(self)):
                self.middle.insert(value)
            else:
                self.right.insert(value)
        else:
            # do inserts based on values
            if not hasThreeChildren(self):
                self.pinNode(value)
            else:
                newNode = self.splitNode(value)
                self.rippleSplit(newNode)

    # recursive splitting algorithm that traverses the tree backwards
    # deals with:
    # traversal
    # insertion
    # identifying when a new root needs to be constructed

    def rippleSplit(self, overflow):
        if isRoot(self):
            self.makeNewRoot(overflow)
            return
        else:
            current = self.parent

        if not hasThreeChildren(current):
            current.pinNode(overflow)
            return
        else:
            newNode = current.splitNode(overflow)
            current.rippleSplit(newNode)

    # places a node as a child of a node with two children
    # determines by itself which child it should be given ordering

    def pinNode(self, overflow):
        if overflow <= self.left:
            self.right  = self.middle
            self.middle = self.left
            self.left   = overflow
        elif overflow <= self.middle:
            self.right  = self.middle
            self.middle = overflow
        else:
            self.right  = overflow

        # ensure the node is not one above the leaves
        if isInterior(self.left):
            self.count    = self.left.count + self.middle.count + self.right.count
            self.smallest = self.left.smallest
            self.largest  = self.right.largest

            overflow.parent = self
        else:
            self.count    = 3
            self.smallest = self.left
            self.largest  = self.right

        self.correctHeuristics()

    # takes one node with three children, and one extra child
    # makes a new node and adjusts the old node
    # returns the new node

    def splitNode(self, overflow):
            temp = sorted([self.left, self.middle, self.right, overflow])
            self.left   = temp[0]
            self.middle = temp[1]

            if isInterior(self.left):
                self.count    = self.left.count + self.middle.count
                self.smallest = self.left.smallest
                self.largest  = self.middle.largest
                newNode = TwoThreeNode(self.parent,
                                       temp[2].count + temp[3].count,
                                       temp[2].smallest, temp[3].largest,
                                       temp[2], temp[3], None)
                newNode.left.parent   = newNode
                newNode.middle.parent = newNode

            else:
                self.count    = 2
                self.smallest = self.left
                self.largest  = self.middle
                newNode = TwoThreeNode(self.parent,
                                       2,
                                       temp[2], temp[3],
                                       temp[2], temp[3], None)
            self.right = None
            return newNode

    # creates a new root using two nodes as children
    # takes the old root and an addition node as the children

    def makeNewRoot(self, overflow):
        if isInterior(overflow):
            newRoot = TwoThreeNode(None,
                                   self.count + overflow.count,
                                   self.smallest, overflow.largest,
                                   self, overflow, None)
        else:
            newRoot = TwoThreeNode(None,
                                   self.count + overflow.count,
                                   self, overflow,
                                   self, overflow, None)
        self.parent     = newRoot
        overflow.parent = newRoot

    #########################
    # delete implementation #
    #########################

    def delete(self, value):
        if isInterior(self.left):
            # descend tree
            if value <= self.left.largest:
                return self.left.delete(value)
            elif value <= self.middle.largest:
                return self.middle.delete(value)
            elif (hasThreeChildren(self) and
                  value <= self.right.largest):
                return self.right.delete(value)
            else:  # the value does not exist in the tree
                return False
        else:
            # self.unPinNode(value)
            # self.rippleMerge()
            # self.correctHeuristics()
            # return True

            # one above leaf level
            if hasThreeChildren(self):
                deleted = self.unPinNode(value)
                if deleted:
                    self.correctHeuristics()
                return deleted
            else:
                deleted = self.unPinNode(value)
                if deleted:
                    self.rippleMerge()
                return deleted

    def unPinNode(self, target):
        if target == self.left:
            self.left   = self.middle
            self.middle = self.right
        elif target == self.middle:
            self.middle = self.right
        elif target == self.right:
            pass
        else:
            return False

        self.right    = None
        self.smallest = self.left
        self.largest  = self.middle
        self.count    = 2

        return True

    # only work when sibling has 3 children
    def takeFromLeft(self, sibling):
        self.middle      = self.left
        self.left        = sibling.right
        if not isLeaf(self.left):
            self.left.parent = self
        sibling.right    = None

        if not isLeaf(self.left):
            self.count    = self.left.count + self.middle.count
            self.smallest = self.left.smallest
            self.largest  = self.middle.largest

            sibling.count    = sibling.left.count + sibling.middle.count
            sibling.smallest = sibling.left.smallest
            sibling.largest  = sibling.middle.largest
        else:
            self.count    = 2
            self.smallest = self.left
            self.largest  = self.middle

            sibling.count    = 2
            sibling.smallest = sibling.left
            sibling.largest  = sibling.middle

    def takeFromRight(self, sibling):
        self.middle        = sibling.left
        if not isLeaf(self.middle):
            self.middle.parent = self
        sibling.left       = sibling.middle
        sibling.middle     = sibling.right
        sibling.right      = None

        if not isLeaf(self.left):
            self.count    = self.left.count + self.middle.count
            self.smallest = self.left.smallest
            self.largest  = self.middle.largest

            sibling.count    = sibling.left.count + sibling.middle.count
            sibling.smallest = sibling.left.smallest
            sibling.largest  = sibling.middle.largest
        else:
            self.count    = 2
            self.smallest = self.left
            self.largest  = self.middle

            sibling.count    = 2
            sibling.smallest = sibling.left
            sibling.largest  = sibling.middle

    def rippleMerge(self):
        if isRoot(self):
            if hasOneChild(self):
                self.collapseRoot()
            return
        else:
            current = self.parent

        if isLeftChild(self):
            if hasThreeChildren(current.middle):
                self.takeFromRight(current.middle)
            else:
                current.middle.pinNode(self.left)
                current.left   = current.middle
                current.middle = current.right
                current.right  = None
        elif isMiddleChild(self):
            if hasThreeChildren(current.left):
                self.takeFromLeft(current.left)
            else:
                current.left.pinNode(self.left)
                current.middle = current.right
                current.right  = None
        else:
            if hasThreeChildren(current.middle):
                self.takeFromLeft(current.middle)
            else:
                current.middle.pinNode(self.left)
                current.right = None

        if hasOneChild(current):
            current.rippleMerge()
        else:
            self.correctHeuristics()

    def collapseRoot(self):
        self.left.parent = None

    # travels up the path used to reach this location,
    # fixes the heuristics inside the nodes along the path
    # only fixes the heuristics of ancestors, not the current node

    def correctHeuristics(self):

        current = self.parent
        while isInterior(current):
            current.count    = (current.left.count +
                                current.middle.count)
            current.smallest = current.left.smallest

            if(hasThreeChildren(current)):
                current.count  += current.right.count
                current.largest = current.right.largest
            else:
                current.largest = current.middle.largest

            current = current.parent


####################
# Friend functions #
####################

def isLeaf(node):
    return type(node) is not TwoThreeNode


def isInterior(node):
    return type(node) is TwoThreeNode


def hasThreeChildren(node):
    return node.right is not None


def hasTwoChildren(node):
    return (node.right is None and
            node.middle is not None)


def hasOneChild(node):
    return (node.right is None and
            node.middle is None and
            node.left is not None)


def isLeftChild(node):
    return node.parent.left is node


def isMiddleChild(node):
    return node.parent.middle is node


def isRightChild(node):
    return node.parent.right is node


def isRoot(node):
    return node.parent is None
