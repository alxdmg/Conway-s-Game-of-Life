# Conway-s-Game-of-Life
An Object Oriented implementation of Conway's Game of Life, and GIF generator through Matplotlib.

Conway's game of life is a cellular automaton devised by the British mathematician John Horton Conway in 1970.
The game requires only the initial set up of the board, from there on the cells evolve, reproduce and die following 3 simple rules:
- Any live cell with two or three neighbors survives. (Cells need to live in communities)
- Any dead cell with three live neighbors becomes a live cell. (Cells reproduce if resources are available)
- All other live cells die in the next generation. Similarly, all other dead cells stay dead. (Over/underpopulated cells die due to lack of resources)

You can read more about the game on Wikipedia [here:](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)

Here are two example GIFs generated using this program:

<p align="center">
<img src="https://github.com/alxdmg/Conway-s-Game-of-Life/blob/master/two_gliders.gif" width="450" height="300">
<img src="https://github.com/alxdmg/Conway-s-Game-of-Life/blob/master/acorn.gif" width="450" height="300">
</p>
