from ursina import *
from ursina.shaders import lit_with_shadows_shader
from noise import pnoise2
import numpy as np
import random

rand_state = random.Random()

def Noise(x):
  rand_state.seed(x)
  return rand_state.random()*200
app = Ursina()
'''Terrain using an RGB texture as input'''
terrain_from_list= Entity(model=Terrain('noise.png', skip=8), scale=(200,10,200), texture='tex.png',shader=lit_with_shadows_shader)

'''
I'm just getting the height values from the previous terrain as an example, but you can provide your own.
It should be a list of lists, where each value is between 0 and 255.
'''
hv = terrain_from_list.model.height_values.tolist()
#terrain_from_list = Entity(model=Terrain(height_values=hv), scale=(40,5,20), texture='heightmap_1', x=40)
#terrain_bounds = Entity(model='wireframe_cube', origin_y=-.5, scale=(40,5,20), color=color.lime)

def input(key):
    if key == 'space':  # randomize the terrain
        terrain_from_list.model.height_values = [[Noise(a) for a in column] for column in terrain_from_list.model.height_values]
        terrain_from_list.model.generate()

EditorCamera(rotation_x=90)
camera.orthographic = False
Sky(color=color.cyan)
from ursina.lights import DirectionalLight
sun = DirectionalLight(shadow_map_resolution=(2048,2048))
sun.look_at(Vec3(-1,-1,-10))
scene.fog_density = (1, 50)
#player = Entity(model='sphere', color=color.azure, scale=.2, origin_y=-.5)

def update():
    direction = Vec3(held_keys['d'] - held_keys['a'], 0, held_keys['w'] - held_keys['s']).normalized()
    #player.position += direction * time.dt * 8
    """
    y = terraincast(player.world_position, terrain_from_list, terrain_from_list.model.height_values)
    if y is not None:
        player.y = y
        """







app.run()