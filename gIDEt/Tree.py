class TreeError(Exception):  # TODO: expand with error-code functionality
    """Basic tree exception class"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

#--------------------------------------------------------------------------------

# module constants
_ADD = 0
_DELETE = 1
_INSERT = 2

class Node(object):
    """Class for basic node functionality"""

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.bpointer = None
        self.fpointer = []
        self.expansion = True        

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def setFPointer(self, id, mode, fpointer=None):
        if fpointer is None:
            if mode == _ADD:
                self.fpointer.append(id)
            elif mode == _DELETE:
                self.fpointer.remove(id)
            elif mode == _INSERT:
                self.fpointer = [id]
        else:
            self.fpointer = fpointer

    def getFPointer(self):
        return self.fpointer

    def setBPointer(self, id):
        self.bpointer = id

    def getBPointer(self):
        return self.bpointer

    def getExpansion(self):
        return self.expansion

    def setExpansion(self, expansion):
        self.expansion = expansion

    def listNode(self):  # NOTE: for debugging purposes
        print ["%s: %s" % (k, v) for k, v in self.__dict__.items()]

#--------------------------------------------------------------------------------


class EmbeddedNode(Node):
    """Class that adds 'multi-dimensional' functionality to the Node-class,
       i.e., 'trees within trees'"""

    def __init__(self, id, name, tree=None):
        Node.__init__(self, id, name)  # explicit call to ancestor's __init__ method
        self.embeddedTree = None  # place-holder for embedded tree / lower level
        self.superPath = []  # place-holder for nodes' super path        

    def setTree(self, tree):
        self.embeddedTree = tree

    def getTree(self):
        return self.embeddedTree

    def deleteTree(self):
        self.embeddedTree = None
        
    def addSuperPath(self, path):
        self.superPath.insert(0, path)
        
    def getSuperPath(self):
        return self.superPath

#--------------------------------------------------------------------------------

import string


# module constants
(_ADD, _DELETE, _INSERT) = range(3)
(_ROOT, _DEPTH, _WIDTH) = range(3)

class Tree(object):
    """Class for basic tree functionality"""

    def __init__(self):
        self.tree = []
        self.branches = [[]]

    def clear(self):
        self.tree = []

    def appendNode(self, pos, name):
        """Append a node after the position indicated by the 'pos' parameter"""

        # if self.isUniqueName(name):
        if pos is None:  # root node
            id = _ROOT
        else:
            id = self.__generateId()
        node = EmbeddedNode(id, name)  # create node
        self.tree.append(node)
        self.__updateFPointer(pos, id, _ADD)
        node.setBPointer(pos)
        # else:
            # raise TreeError("Node name is not unique: %s" % (name))
        return node

    def insertNode(self, pos, name):
        """Insert a node between the node indicated by the 'pos' 
           parameter and its parent node"""

        # if self.isUniqueName(name):
            # index = self.getIndex(pos)
        id = self.__generateId()
        # prevPointer = self[index].getBPointer()
        prevPointer = self[pos].getBPointer()
        newNode = EmbeddedNode(id, name)  # create node
        newNode.setBPointer(prevPointer)
        newNode.setFPointer(pos, _ADD)
        self.tree.append(newNode)
        self.__updateFPointer(prevPointer, id, _ADD)
        # self[index].setBPointer(id)
        self[pos].setBPointer(id)
        self.__updateFPointer(prevPointer, pos, _DELETE)
        # else:
            # raise TreeError("Not unique node name: %s" % (name))

    def moveNode(self, src, dest):  # TODO: test method
        """Move a node indicated by the 'src' parameter to the node indicated 
           by the 'dest' parameter"""
        
        # test/debug: '3' is root, and the source and destination node
        if (src != _ROOT and len(self.tree) > 3):  
            previousNode = self[src].getBPointer()
            self.__updateFPointer(previousNode, src, _DELETE)
            self.__updateFPointer(dest, src, _ADD)
            self[src].setBPointer(dest)
        else:
            raise TreeError("Invalid move operation")

    def copyNode(self, src, dest):
        """Copy a node indicated by the 'src' parameter to the 
           node indicated by the 'dest' parameter"""
        pass

    def deleteNode(self, pos):
        """Delete a node in the position indicated by the 'pos' parameter"""

        if pos in self:
            # index = self.getIndex(pos)
            # previousNode = self[index].getBPointer()
            previousNode = self[pos].getBPointer()
            self.__updateFPointer(previousNode, pos, _DELETE)
            # for node in self[index].getFPointer():
            for node in self[pos].getFPointer():
                self.__updateFPointer(previousNode, node, _ADD)
                self.__updateBPointer(node, previousNode)
            # self.tree.remove(self[index])
            self.tree.remove(self[pos])
        else:
            raise TreeError("Node does not exist: %s" % (pos))

    def deleteBranch(self, pos):
        deleteList = [pos]

        def innerDelete(pos):  # inner function to 'deleteBranch'
            # fpointer = self[self.getIndex(pos)].getFPointer()
            fpointer = self[pos].getFPointer()
            if fpointer != []:
                for node in fpointer:
                    # deleteList.append(self[self.getIndex(node)].getId())  # NOTE: verify
                    deleteList.append(self[node].getId())  # NOTE: verify
                    innerDelete(node)
                else:
                    return

        if self.isBranch(pos):
            innerDelete(pos)  # call inner-function
            for node in deleteList:
                self.deleteNode(node)
        else:
            raise TreeError("Node contains no subnodes, i.e., not a branch: %s" % (pos))

    def setName(self, pos, name):
        if pos in self:
            self[pos].setName(name)
        else:
            raise TreeError("Node does not exist: %s" % (pos))
    
    
    def genBPath(self, pos):
        # Python generator. Performs the inverse of 'expandTree'.
        yield (self[pos].getId(), self[pos].getName())
        bpointer = self[pos].getBPointer()
        yield (bpointer, self[bpointer].getName())
        while bpointer:
            bpointer = self[bpointer].getBPointer()
            yield (bpointer, self[bpointer].getName())
    

    def getIndex(self, pos=None):
        if pos is None:
            return _ROOT
        if pos in self:
            for index, node in enumerate(self.tree):
                if node.getId() == pos:
                    break
            return index
        else:
            return  _ROOT

    def connect(child, parent):  # inner function to genBranchLines
        rowStart = parent[0] + 1
        rowEnd = child[0]
        column =  child[1] -1
        if column != -1:
            for y, row in enumerate(self.branches[index]):
                if (y >= rowStart) and (y <= rowEnd):
                    row[column] = 1

        parentY = childY
        parentX = childX
        
        queue = self[pos].getFPointer()
        if queue:  # branch
            self.branches[index].append([0]*(level + 1))
            if level != _ROOT:
                childX += 1            
            childY = len(self.branches[index]) -1
            connect((childY, childX), (parentY, parentX))
            if self[pos].getExpansion():
                level += 1
                for element in queue:
                    # recursive call
                    self.genBranchLines(index, element, level, childX, childY)
        else:  # leaf
            self.branches[index].append([0]*(level + 1))
            if level != _ROOT:
                childX += 1
            childY = len(self.branches[index]) -1
            connect((childY, childX), (parentY, parentX))

    def isLastNode(self, pos):
        result = False
        parentNode = self[pos].getBPointer()
        if parentNode != None:
            branch = self[parentNode].getFPointer()
            if branch.index(self[pos].getId()) == (len(branch) -1):
                result = True
        return result
    
    def expandTree(self, pos=_ROOT, mode=_DEPTH):
        # Python generator. Loosly based on an algorithm from 'Essential LISP' by
        # John R. Anderson, Albert T. Corbett, and Brian J. Reiser, page 239-241
        yield pos
        queue = self[pos].getFPointer()
        while queue:
            yield queue[0]
            expand = self[queue[0]].getFPointer()
            if mode == _DEPTH:
                queue = expand + queue[1:]  # depth-first
            elif mode == _WIDTH:
                queue = queue[1:] + expand  # width-first

    def isBranch(self, pos):
        # return self[self.getIndex(pos)].getFPointer()
        return self[pos].getFPointer()

    def isUniqueName(self, name):
        for node in self.tree:
            if node.getName() == name:
                return False
        return True

    def __updateFPointer(self, pos, id, mode):
        if pos is None:
            return
        else:
            # self[self.getIndex(pos)].setFPointer(id, mode)
            self[pos].setFPointer(id, mode)

    def __updateBPointer(self, pos, id):
        # self[self.getIndex(pos)].setBPointer(id)
        self[pos].setBPointer(id)

    def __generateId(self):
        """Private function that generates an unique node-ID"""

        nodes = [node.getId() for node in self.tree]
        result = max(nodes) +1
        return result

    def __getitem__(self, key):
        return self.tree[self.getIndex(key)]

    def __setitem__(self, key, item):
        self.tree[self.getIndex(key)] = item

    def __len__(self):
        return len(self.tree)

    def __nonzero__(self):
        if self.tree == []:
            return False
        else:
            return True

    def __contains__(self, pos):
        return [node.getId() for node in self.tree if node.getId() == pos]

    def show(self, pos, level=_ROOT):        
        queue = self[pos].getFPointer()
        if queue:  # branch
            if level == _ROOT:
                print ">", str(self[pos].getId()).rjust(3), "-", self[pos].getName(), self.getIndex(pos), self.isLastNode(pos)
            else:
                print "t"*level, ">", str(self[pos].getId()).rjust(3), "-", self[pos].getName(), self.getIndex(pos), self.isLastNode(pos)
            if self[pos].getExpansion():
                level += 1
                for element in queue:
                    self.show(element, level)  # recursive call
        else:  # leaf
            if level == _ROOT:
                print ">", str(self[pos].getId()).rjust(3), "-", self[pos].getName(), self.getIndex(pos), self.isLastNode(pos)
            else:
                print "t"*level, ">", str(self[pos].getId()).rjust(3), "-", self[pos].getName(), self.getIndex(pos), self.isLastNode(pos)

#--------------------------------------------------------------------------------
# module testing
if __name__ == "__main__":
    testTree = Tree()  # instantiate Tree object
    testTree.appendNode(None, "Harry")  # build tree
    testTree.appendNode(0, "Jane")
    testTree.appendNode(0, "Bill")
    testTree.appendNode(1, "Joe")
    testTree.appendNode(1, "Diane")
    testTree.appendNode(4, "George")
    testTree.appendNode(4, "Mary")
    testTree.appendNode(5, "Jill")
    testTree.appendNode(7, "Carol")
    testTree.appendNode(2, "Grace")
    testTree.appendNode(1, "Mark")
    # testTree.deleteNode(1)
#    testTree.show(0)
    print testTree.isLastNode(1)
    # testTree.tree[2].addAttribute(["OS", "Linux"])
    # for node in testTree.tree:
        # print node, node.listNode()

    # for node in testTree.expandTree(mode=_DEPTH):  # generator-based iteration
        # print testTree[node].getName()
    
    """
    path = ""
    for node in testTree.genBPath(8):
        path += "/" + node[1]
    print path
    """
    """
    treeWalk = testTree.getBPath(8)
    print treeWalk
    path = ""
    for node in treeWalk:
        # path += "/" + node[1]
        path += str(node[0])
    print path
    print "".join(["%s" % (node[0]) for node in treeWalk])
    """
