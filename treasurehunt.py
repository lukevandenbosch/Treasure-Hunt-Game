"""Assignment 1 - TreasureHunt 

This module contains the TreasureHunt class.

Your only task here is to implement the methods
where indicated, according to their docstring. 
Also complete the missing doctests.
"""
from grid import Grid

class TreasureHunt:
    """
    Represents an instance of the treasure hunt game.
    
    === Attributes: ===
    @type grid_path: str 
        pathname to a text file that contains the grid map
        see Grid and Node classes for the format
	@type grid: Grid
	    a representation of the game world
    @type sonars: int
       the number of sonars the boat can drop
    @type so_range: int
       the range of sonars
    @type state: str
       the state of the game:
          STARTED, OVER, WON 
    """

    def __init__(self, grid_path, sonars, so_range):
        """
        Initialize a new game with map data stored in the file grid_path
        and commands to be used to play the game in game_path file.
        
        @type grid_path: str
           pathname to a text file that contains the grid map
           see Grid and Node classes for the format
        @type sonars: int
        @type so_range: int      
        """
        self.grid_path = grid_path
        self.sonars = sonars
        self.so_range = so_range
        self.grid = Grid(grid_path)
        self.state = self.grid.state

    def process_command(self, command):
        """
        Process a command, set and return the state of the game 
        after processing this command
        @type command: str
           a command that can be used to play, as follows:
    SONAR, drops a sonar
           PLOT, plots the shortest path from the boat to the treasure
           (on condition the SONAR has discovered the treasure and
           the optimal oath has already been determined)
           QUIT, quit the game
        @rtype: str 
           the state of the game  
        """
        #if the sonar command is taken
        if command == "SONAR":
            #decrease sonars by 1
            self.sonars -= 1
            # if the type of the treasure is not None ie is in range then plot the path
            if type(self.grid.get_treasure(self.so_range)) != type(None):
                print(self.grid.plot_path(self.grid.boat,self.grid.get_treasure(self.so_range)))
        #if the command is quit set the state value to over and print it
        elif command == "QUIT":
            self.state = "OVER"
            print(self.state)

'''if __name__ == '__main__':
    import doctest
    doctest.testmod()
    import python_ta
    python_ta.check_all(config='pylintrc.txt')
'''