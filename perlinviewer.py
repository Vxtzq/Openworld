from noise import pnoise2
import numpy as np
import matplotlib.pyplot as plt

perlin = np.zeros([16,16])
tree_positions = {}
tree_seed = 42
tree_noise_scale = 20
octaves = 2
persistence = 0.3
lacunarity = 1.5
tree_threshold = 0.2 


for i in range(16):
    for j in range(16):
            noise_value = pnoise2(i/tree_noise_scale, j/tree_noise_scale,
                                      octaves=octaves, persistence=persistence, lacunarity=lacunarity,
                                      repeatx=1024, repeaty=1024, base=tree_seed)
            perlin[i,j] = noise_value
print(perlin)
plt.imshow(perlin)
plt.show()