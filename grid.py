"""Assignment 1 - Node and Grid

This module contains the Node and Grid classes.

Your only task here is to implement the methods
where indicated, according to their docstring.
Also complete the missing doctests.
"""

import functools
import sys
import copy
from container import PriorityQueue


@functools.total_ordering
class Node:
    """
    Represents a node in the grid. A node can be navigable 
    (that is located in water)
    or it may belong to an obstacle (island).

    === Attributes: ===
    @type navigable: bool
       navigable is true if and only if this node represents a 
       grid element located in the sea
       else navigable is false
    @type grid_x: int
       represents the x-coordinate (counted horizontally, left to right) 
       of the node
    @type grid_y: int
       represents the y-coordinate (counted vertically, top to bottom) 
       of the node
    @type parent: Node
       represents the parent node of the current node in a path
       for example, consider the grid below:
        012345
       0..+T..
       1.++.++
       2..B..+
       the navigable nodes are indicated by dots (.)
       the obstacles (islands) are indicated by pluses (+)
       the boat (indicated by B) is in the node with 
       x-coordinate 2 and y-coordinate 2
       the treasure (indicated by T) is in the node with 
       x-coordinate 3 and y-coordinate 0
       the path from the boat to the treasure if composed of the sequence 
       of nodes with coordinates:
       (2, 2), (3,1), (3, 0)
       the parent of (3, 0) is (3, 1)
       the parent of (3, 1) is (2, 2)
       the parent of (2, 2) is of course None
    @type in_path: bool
       True if and only if the node belongs to the path plotted by A-star 
       path search
       in the example above, in_path is True for nodes with coordinates 
       (2, 2), (3,1), (3, 0)
       and False for all other nodes
    @type gcost: float
       gcost of the node, as described in the handout
       initially, we set it to the largest possible float
    @type hcost: float
       hcost of the node, as described in the handout
       initially, we set it to the largest possible float
    """
    def __init__(self, navigable, grid_x, grid_y):
        """
        Initialize a new node

        @type self: Node
        @type navigable: bool
        @type grid_x: int
        @type grid_y: int
        @rtype: None

        Preconditions: grid_x, grid_y are non-negative

        >>> n = Node(True, 2, 3)
        >>> n.grid_x
        2
        >>> n.grid_y
        3
        >>> n.navigable
        True
        """
        self.navigable = navigable
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.in_path = False
        self.parent = None
        self.gcost = sys.float_info.max
        self.hcost = sys.float_info.max

    def set_gcost(self, gcost):
        """
        Set gcost to a given value

        @type gcost: float
        @rtype: None

        Precondition: gcost is non-negative

        >>> n = Node(True, 1, 2)
        >>> n.set_gcost(12.0)
        >>> n.gcost
        12.0
        """
        self.gcost = gcost

    def set_hcost(self, hcost):
        """
        Set hcost to a given value

        @type hcost: float
        @rtype: None

        Precondition: gcost is non-negative

        >>> n = Node(True, 1, 2)
        >>> n.set_hcost(12.0)
        >>> n.hcost
        12.0
        """
        self.hcost = hcost

    def fcost(self):
        """
        Compute the fcost of this node according to the handout

        @type self: Node
        @rtype: float
        """
        return self.gcost + self.hcost

    def set_parent(self, parent):
        """
        Set the parent to self
        @type self: Node
        @type parent: Node
        @rtype: None
        """
        self.parent = parent

    def distance(self, other):
        """
        Compute the distance from self to other
        @self: Node
        @other: Node
        @rtype: int
        """
        dstx = abs(self.grid_x - other.grid_x)
        dsty = abs(self.grid_y - other.grid_y)
        if dstx > dsty:
            return 14 * dsty + 10 * (dstx - dsty)
        return 14 * dstx + 10 * (dsty - dstx)

    def __eq__(self, other):
        """
        Return True if self equals other, and false otherwise.

        @type self: Node
        @type other: Node
        @rtype: bool
        """
        return self.grid_x == other.grid_x and self.grid_y == other.grid_y
            

    def __lt__(self, other):
        """
        Return True if self less than other, and false otherwise.

        @type self: Node
        @type other: Node
        @rtype: bool
        """
        return self.fcost() < other.fcost()

    def __str__(self):
        """
        Return a string representation.

        @type self: Node
        @rtype: str
        """
        if self.navigable == True:
            dot = "."
        else:
            dot = "+"
        return dot

class Grid:
    """
    Represents the world where the action of the game takes place.
    You may define helper methods as you see fit.

    === Attributes: ===
    @type width: int
       represents the width of the game map in characters
       the x-coordinate runs along width
       the leftmost node has x-coordinate zero
    @type height: int
       represents the height of the game map in lines
       the y-coordinate runs along height; the topmost
       line contains nodes with y-coordinate 0
    @type map: List[List[Node]]
       map[x][y] is a Node with x-coordinate equal to x
       running from 0 to width-1
       and y-coordinate running from 0 to height-1
    @type treasure: Node
       a navigable node in the map, the location of the treasure
    @type boat: Node
       a navigable node in the map, the current location of the boat
    @type path: PriorityQueue
        a closed list of all the daughter Nodes in the A* algorithm

    === Representation invariants ===
    - width and height are positive integers
    - map has dimensions width, height
    """

    def __init__(self, file_path, text_grid=None):
        """
        If text_grid is None, initialize a new Grid assuming file_path
        contains pathname to a text file with the following format:
        ..+..++
        ++.B..+
        .....++
        ++.....
        .T....+
        where a dot indicates a navigable Node, a plus indicates a
        non-navigable Node, B indicates the boat, and T the treasure.
        The width of this grid is 7 and height is 5.
        If text_grid is not None, it should be a list of strings
        representing a Grid. One string element of the list represents
        one row of the Grid. For example the grid above, should be
        stored in text_grid as follows:
        ["..+..++", "++.B..+", ".....++", "++.....", ".T....+"]

        @type file_path: str
           - a file pathname. See the above for the file format.
           - it should be ignored if text_grid is not None.
           - the file specified by file_path should exists, so there
             is no need for error handling
           Please call open_grid to open the file
        @type text_grid: List[str]
        @rtype: None
        """
        self.state = "STARTED"
        self.file_path = file_path
        self.text_grid = text_grid
        #set up
        self.path = PriorityQueue(Node.__lt__)
        #set up map using open_grid() function and then splitting it if it is a file path
        if self.text_grid == None:
            self.map = self.open_grid(self.file_path).read().split("\n")
        #set up map if it is a text grid
        else:
            self.map = self.text_grid
        #y length of the map
        self.height = len(self.map)
        #break up the map into a 2 dimensional list of strings
        for i in range(len(self.map)):
            self.map[i] = list(self.map[i])
        #set width to be the horizontal length of the map
        self.width = len(self.map[0][:])
        #find the treasure located in the map
        g = copy.copy(self.map)
        for i, x in enumerate(g):
            if "T" in x:
                self.treasure = Node(True, x.index("T"),i)
        #change x and y values
        self.map  = [list(i) for i in zip(*self.map)]
        self.boat = self.set_boat()
        for i,x in enumerate(self.map):
            for j in range(len(x)):
                self.map[i][j] = Node(self.map[i][j] != "+",i,j)
        

    @classmethod
    def open_grid(self, file_path):
        """
        @rtype TextIOWrapper: 
        """
        return open(file_path)
    
    def __str__(self):
        """
        Return a string representation.

        @type self: Grid
        @rtype: str

        >>> g = Grid("", ["B.++", ".+..", "...T"])
        >>> print(g)
        B.++
        .+..
        ...T
        """
        #join the 2d list twice, once with nothing and the other with linebreaks
        lst = []
        g = self.convert()
        for i in g:
            lst.append("".join(i))
        return"\n".join(lst)

    def move(self, direction):
        """
        Move the boat in a specific direction, if the node
        corresponding to the direction is navigable
        Else do nothing

        @type self: Grid
        @type direction: str
        @rtype: None

        direction may be one of the following:
        N, S, E, W, NW, NE, SW, SE
        (north, south, ...)
        123
        4B5
        678
        1=NW, 2=N, 3=NE, 4=W, 5=E, 6=SW, 7=S, 8=SE
        >>> g = Grid("", ["B.++", ".+..", "...T"])
        >>> g.move("S")
        >>> print(g)
        ..++
        B+..
        ...T
        """
        #create moving direction vectors if the N S E W or a combination is entered
        if direction == "N":
            new = (0,-1)
        elif direction == "S":
            new = (0,1)
        elif direction == "E":
            new = (1,0)
        elif direction == "W":
            new = (-1,0)
        elif direction == "NW":
            new = (-1,-1)
        elif direction == "NE":
            new = (1,-1)
        elif direction == "SE":
            new = (1,1)
        elif direction == "SW":
            new = (-1,1)
        else:
            print("Invalid Command")
            
        #create a copy of the map so as not to disturb the original 
        g = copy.copy(self.map)
        #find the boat's index
        B = (self.boat.grid_x,self.boat.grid_y)
        #if the boat (x,y) + the new direction(x,y) is in the bounds of the map
        if B[0]+new[0] >= 0 and B[0]+new[0] < self.height and B[1]+new[1] >= 0 and B[1]+new[1] < self.width:
            #if the new position of the boat is navigable
            if g[B[0]+new[0]][B[1]+new[1]].navigable == True or g[B[0]+new[0]][B[1]+new[1]] == self.treasure:
                #if the new position is the target position then you win
                if g[B[0]+new[0]][B[1]+new[1]] == self.treasure:
                    self.state = "WON"
                    print(self.state)
                #move change the map's position to an dot on the old one and B on the new
                self.boat = g[B[0]+new[0]][B[1]+new[1]]
                #join the list back together the list we have been working on
                #set the map equal to the new one set boat  equal to new position
                self.map = g
            else:
                print("Cannot Move here")
        else:
            print("Cannot Move here")
        

    def find_path(self, start_node, target_node):
        """
        Implement the A-star path search algorithm
        If you will add a new node to the path, don't forget to set the parent.
        You can find an example in the docstring of Node class
        Please note the shortest path between two nodes may not be unique.
        However all of them have same length!

        @type self: Grid
        @type start_node: Node
           The starting node of the path
        @type target_node: Node
           The target node of the path
        @rtype: None
        """
        #create a copy of the original map
        g = copy.copy(self.map)
        #make an open PriorityQueue to store children
        opens = PriorityQueue(Node.__lt__)
        #set the starting node's g and h costs to be 0 or else it starts around infinity
        start_node.gcost = 0
        start_node.hcost = 0
        #add the starting node to the open Queue
        opens.add(start_node)
        #loop while the open set is not empty
        while not opens.is_empty():
            #remove the value with the lowest fcost built into the PriorityQueue class
            q = opens.remove()
            #create a list of successors
            suc = []
            #add each new successor node in the 8 surrounding points to the list if the index is in range and the point is navigable
            if q.grid_y-1 >= 0 and q.grid_y - 1 < self.height and q.grid_x-1 >= 0 and q.grid_x - 1 < self.width and g[q.grid_x-1][q.grid_y-1].navigable == True:
                suc.append(Node(g[q.grid_x-1][q.grid_y-1].navigable,q.grid_x-1,q.grid_y-1))
            if q.grid_y-1 >= 0 and q.grid_y - 1 < self.height and q.grid_x >= 0 and q.grid_x < self.width and g[q.grid_x][q.grid_y-1].navigable == True:
                suc.append(Node(g[q.grid_x][q.grid_y-1].navigable,q.grid_x,q.grid_y-1))
            if q.grid_y-1 >= 0 and q.grid_y - 1 < self.height and q.grid_x + 1 >= 0 and q.grid_x + 1 < self.width and g[q.grid_x+1][q.grid_y-1].navigable == True:
                suc.append(Node(g[q.grid_x+1][q.grid_y-1].navigable,q.grid_x+1,q.grid_y-1))
            if q.grid_y >= 0 and q.grid_y < self.height and q.grid_x-1 >= 0 and q.grid_x - 1 < self.width and g[q.grid_x-1][q.grid_y].navigable == True:
                suc.append(Node(g[q.grid_x-1][q.grid_y].navigable,q.grid_x-1,q.grid_y))
            if q.grid_y >= 0 and q.grid_y < self.height and q.grid_x+1 >= 0 and q.grid_x + 1 < self.width and g[q.grid_x+1][q.grid_y].navigable == True:
                suc.append(Node(g[q.grid_x+1][q.grid_y].navigable,q.grid_x+1,q.grid_y))
            if q.grid_y+1 >= 0 and q.grid_y + 1 < self.height and q.grid_x-1 >= 0 and q.grid_x - 1 < self.width and g[q.grid_x-1][q.grid_y+1].navigable == True:
                suc.append(Node(g[q.grid_x-1][q.grid_y+1].navigable,q.grid_x-1,q.grid_y+1))
            if q.grid_y+1 >= 0 and q.grid_y + 1 < self.height and q.grid_x >= 0 and q.grid_x < self.width and g[q.grid_x][q.grid_y+1].navigable == True:
                suc.append(Node(g[q.grid_x][q.grid_y+1].navigable,q.grid_x,q.grid_y+1))
            if q.grid_y+1 >= 0 and q.grid_y + 1 < self.height and q.grid_x+1 >= 0 and q.grid_x + 1 < self.width and g[q.grid_x+1][q.grid_y+1].navigable == True:
                suc.append(Node(g[q.grid_x+1][q.grid_y+1].navigable,q.grid_x+1,q.grid_y+1))
            #for each successor
            for i in range(len(suc)):
                #set the parent to be the one that was just removed
                suc[i].set_parent(q)
                #stop the search if the target node is found
                if suc[i] == target_node:
                    #also add the successor to the closed set
                    self.path.add(suc[i])
                    return None
                #set the target's g, h, and f costs
                suc[i].set_gcost(q.gcost + q.distance(suc[i]))
                suc[i].set_hcost(target_node.distance(suc[i]))
                suc[i].fcost()
                #if the successor is in the open set and is lower f than the value in the successor then skip the successsor
                if opens.is_less_than(suc[i]):
                    pass
                #if the successor is in the closed set and is lower f than the value in the successor then skip the successsor
                if self.path.is_less_than(suc[i]):
                    pass
                #otherwise add the successor to the open set
                else:
                    opens.add(suc[i])
                #add the q value to the closed set
                self.path.add(q)
            
    def convert(self):
        """converts the map of nodes into a list of strings
        
        @type self: Grid
        @rtype: list
        """
        #create a copy of the map
        g = copy.copy(self.map)
        #invert the map back to y and x
        g = [list(i) for i in zip(*self.map)]
        #loop for each x y in map set the original value that was given as an input
        for i,x in enumerate(g):
            for j in range(len(x)):
                if g[i][j].navigable and g[i][j] != self.boat and g[i][j] != self.treasure:
                    g[i][j] = "."
                elif g[i][j] == self.boat:
                    g[i][j] = "B"
                elif g[i][j] == self.treasure:
                    g[i][j] = "T"
                else:
                    g[i][j] = "+"
        return g

    def retrace_path(self, start_node, target_node):
        """
        Return a list of Nodes, starting from start_node,
        ending at target_node, tracing the parent
        Namely, start from target_node, and add its parent
        to the list. Keep going until you reach the start_node.
        If the chain breaks before reaching the start_node,
        return an empty list.

        @type self: Grid
        @type start_node: Node
        @type target_node: Node
        @rtype: list[Node]
        """
        #run the find_path function
        self.find_path(start_node,target_node)
        #create an empty list
        lst = []
        #copy the closed set
        nodel = copy.copy(self.path)
        #add the closed set into a list
        while not nodel.is_empty():
            lst.append(nodel.remove())
        #find the target node in the list
        for i in range(len(lst)):
            if lst[i] == target_node:
                tar = i
        #create the path from the target to the starting node by adding the all n parents to the list then return it
        lst2 = []
        lst2.append(lst[tar])
        node = lst[tar]
        while not node == start_node:
            lst2.append(node)
            node = node.parent
        return lst2
        
    def set_boat(self):
        """set the position of the boat
        @type self: Grid
        @rtype: Node
        """
        #create a copy of the map
        g = copy.copy(self.map)
        #search throught the values in the node for the boat
        for i, x in enumerate(g):
            if "B" in x:
                #return a node of the boat
                return Node(True, i, x.index("B"))
        
    def get_treasure(self, s_range):
        """
        Return treasure node if it is located at a distance s_range or
        less from the boat, else return None
        @type s_range: int
        @rtype: Node, None
        """
        #make a copy of the map
        g = copy.copy(self.map)
        #go through all of g to find the value T and set the treasure at that value = node at that point
        for i, x in enumerate(g):
            if "T" in x:
                Treasure = Node(True, i, x.index("T"))
        #return the value if it is <= s_range or else don't
        if self.boat.distance(Treasure) <= s_range:
            return Treasure
        else:
            return None


    def plot_path(self, start_node, target_node):
        """
        Return a string representation of the grid map,
        plotting the shortest path from start_node to target_node
        computed by find_path using "*" characters to show the path
        @type self: Grid
        @type start_node: Node
        @type target_node: Node
        @rtype: str
        >>> g = Grid("", ["B.++", ".+..", "...T"])
        >>> print(g.plot_path(g.boat, g.treasure))
        B*++
        .+*.
        ...T
        """
        #create a copy of the map
        g = copy.copy(self.map)
        #make a path using A*
        paths = self.retrace_path(start_node,target_node)
        #write the path on the grid 
        g = self.convert()
        for p in paths:
            if p != start_node and p!= target_node:
                g[p.grid_y][p.grid_x] = "*"
        new = []
        for i, x in enumerate(g):
            new.append("".join(x))
        return "\n".join(new)


'''if __name__ == '__main__':
    import doctest
    doctest.testmod()
    import python_ta
    python_ta.check_all(config='pylintrc.txt')'''
