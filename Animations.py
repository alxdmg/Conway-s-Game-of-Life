
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from GameOfLife import GameOfLife


# set up game
game = GameOfLife(32, 32)

# Acorn Oscillator
game.new_elem(figure="acorn", top_left_x=12, top_left_y=14)

# # Two gliders block
# game.new_elem(figure="glider", top_left_x=3, top_left_y=3)
# game.new_elem(figure="glider", top_left_x=22, top_left_y=22, x_dir=-1, y_dir=-1)

m = game.Board.astype(int)


def update(i):
    m = 255 * game.next_gen().astype(int)
    matrice.set_array(m)

fig, ax = plt.subplots()
plt.axis('off')
ax.set_title("50 generations of Acorn")
matrice = ax.matshow(m)

anim = animation.FuncAnimation(fig, update, frames=50, interval=100, blit=False)


# Comment/Uncomment either line to save or show the GIF
# anim.save('acorn.gif', dpi=80, writer='imagemagick')
plt.show()
