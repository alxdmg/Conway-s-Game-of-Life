# Conway-s-Game-of-Life
An Object Oriented implementation of Conway's Game of Life, and GIF generator through Matplotlib.

Conway's game of life is a cellular automaton devised by the British mathematician John Horton Conway in 1970.
The game requires only the initial set up of the board, from there on the cells evolve, reproduce and die following 3 simple rules:
- Any live cell with two or three neighbors survives.
- Any dead cell with three live neighbors becomes a live cell.
- All other live cells die in the next generation. Similarly, all other dead cells stay dead.

You can read more about the game on Wikipedia [here:](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)

Here are two example GIFs generated using this program:
<p float="left">
<img src="/two_gliders.gif" width="450" />
<img src="/acorn.gif" width="450 /> 
</p>

GameOfLife.py contains an object oriented implementation of the game, including docstrings, methods to pass your own initial states, methods to add elements/figures anywhere you want and with any orientation, among other things.

Animation.py uses Matplotlib to graph the evolution of the game, and you can optionally save it to the current directory thanks to ImageMagick. [Check here for doc/download.](https://imagemagick.org/)
