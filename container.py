"""This module contains the Container and PriorityQueue classes.

Your only task here is to implement the add method for PriorityQueue,
according to its docstring.
"""

class Container:
    """A container that holds Objects.

    This is an abstract class.  Only child classes should be instantiated.
    """
    def add(self, item):
        """Add <item> to this Container.

        @type self: Container
        @type item: Object
        @rtype: None
        """
        raise NotImplementedError

    def remove(self):
        """Remove and return a single item from this Container.

        @type self: Container
        @rtype: Object
        """
        raise NotImplementedError

    def is_empty(self):
        """Return True iff this Container is empty.

        @type self: Container
        @rtype: bool
        """
        raise NotImplementedError


class PriorityQueue(Container):
    """A queue of items that operates in FIFO-priority order.

    Items are removed from the queue according to priority; the item with the
    highest priority is removed first.  Ties are resolved in first-in-first-out
    (FIFO) order, meaning the item which was inserted *earlier* is the first one
    to be removed.

    Priority is defined by the <less_than> function that is provided at time
    of construction.  If x < y, then x has a *HIGHER* priority than y.
    (Intuitively, something with "priority 1" is more important than something
    with "priority 10".)

    All objects in the container must be of the same type.

    === Private Attributes ===
    @type _queue: List
      The end of the list represents the *front* of the queue, that is,
      the next item to be removed.
    @type _less_than: Callable[[Object, Object], bool]
      If x._less_than(y) is true, then x has higher priority than y
      and should be removed from the queue before y.

    === Representation Invariants ===
    - all elements of _queue are of the same type
    - the elements of _queue are appropriate arguments for function less_than
    - the elements of _queue are in order according to function less_than.
    """

    def __init__(self, less_than):
        """Initialize this to an empty PriorityQueue.

        @type self: PriorityQueue
        @type less_than: Callable[[Object, Object], bool]
            Determines the relative priority of two elements of the queue.
            If x._less_than(y) is true, then x has higher priority than y.
        @rtype: None
        """

        self._queue = []
        self._less_than = less_than
    
    def is_less_than(self, item):
        """Return if this item is less than the item in PriorityQueue
        
        this is a helper function for the A* algorithm
        
        @type self: PriorityQueue
        @rtype: bool
        """
        # run a for loop to find if the item in the list 
        turn = 0
        for i in self._queue:
            #if the item equals a value in a list
            if item.grid_x == i.grid_x and item.grid_y == i.grid_y:
                #and if it's less than that item than return True else return false
                if self._less_than(i, item):
                    return True
                else:
                    return False
        if turn == 0:
            return False
    def add(self, item):
        """Add <item> to this PriorityQueue.

        @type self: PriorityQueue
        @type item: Object
        @rtype: None

        >>> def shorter(a, b):
        ...    return len(a) < len(b)
        ...
        >>>
        >>> # Define a PriorityQueue with priority on shorter strings.
        >>> # I.e., when we remove, we get the shortest remaining string.
        >>> pq = PriorityQueue(shorter)
        >>> pq.add('fred')
        >>> pq.add('arju')
        >>> pq.add('monalisa')
        >>> pq.add('hat')
        >>> pq._queue
        ['monalisa', 'arju', 'fred', 'hat']
        >>> pq.remove()
        'hat'
        >>> pq._queue
        ['monalisa', 'arju', 'fred']
        """
        #set a variable to know when item has been inserted
        switch = 0
        #add the value if the length of the list is 0
        if len(self._queue) == 0:
            self._queue.append(item)
        #otherwise do this
        else:
            #run a for loop in the length of the list
            for i in range(len(self._queue)):
                #if the item is (equal to) the value in the list insert at the end of the list
                if not self._less_than(self._queue[i],item) and not self._less_than(item,self._queue[i]) and switch == 0:
                    self._queue.insert(i-1,item)
                    switch = 1
                #if the value is less than the other values in the loop insert it
                elif self._less_than(self._queue[i], item) and switch == 0:
                    self._queue.insert(i,item)
                    switch = 1
                #or add it at the end of the list if none of the conditions are met
                elif i == len(self._queue)-1 and switch == 0:
                    self._queue.append(item)

    def remove(self):
        """Remove and return the next item from this PriorityQueue.

        Precondition: this priority queue is non-empty.

        @type self: PriorityQueue
        @rtype: Object

        >>> def shorter(a, b):
        ...    return len(a) < len(b)
        ...
        >>>
        >>> # When we hit the tie, the one that was added first will be
        >>> # removed first.
        >>> pq = PriorityQueue(shorter)
        >>> pq.add('fred')
        >>> pq.add('arju')
        >>> pq.add('monalisa')
        >>> pq.add('hat')
        >>> pq.remove()
        'hat'
        >>> pq.remove()
        'fred'
        >>> pq.remove()
        'arju'
        >>> pq.remove()
        'monalisa'
        """
        return self._queue.pop()

    def is_empty(self):
        """Return True iff this PriorityQueue is empty.

        @type self: PriorityQueue
        @rtype: bool

        >>> def lt(a, b):
        ...    return a < b
        ...
        >>>
        >>> pq = PriorityQueue(lt)
        >>> pq.is_empty()
        True
        >>> pq.add('fred')
        >>> pq.is_empty()
        False
        """
        return len(self._queue) == 0


'''if __name__ == '__main__':
    import doctest
    doctest.testmod()
    import python_ta
    python_ta.check_all(config='pylintrc.txt')'''
