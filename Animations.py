import matplotlib.pyplot as plt
import matplotlib.animation as animation
from GameOfLife_parse import GameOfLife
# from GameOfLife_dense import GameOfLife


game = GameOfLife(130, 150)
print("available figures:")
print(game.list_elems())
game.new_elem(figure="acorn", top_left_x=70, top_left_y=100)

NumGen = 500  # Number of generations of the game

fig = plt.figure(dpi=150)
plt.axis('off')
plt.title(f"Acorn seed evolution")
ims = []
for i in range(NumGen):
    im = plt.imshow(255 * game.next_gen(), animated=True)
    ims.append([im])

ani = animation.ArtistAnimation(fig, ims, interval=30, blit=True)
# ani.save('Acorn_500gen_150dpi.gif', dpi=150, writer='imagemagick')
# ani.save('dynamic_images.mp4')

plt.show()
