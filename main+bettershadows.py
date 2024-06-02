from ursina import *
from ursina.shaders import lit_with_shadows_shader
from noise import pnoise2
import numpy as np
import random
from ursina.prefabs.first_person_controller import FirstPersonController

from ursina.lights import DirectionalLight


rand_state = random.Random()

class InfiniteTerrain(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.chunks = {}
        self.chunk_size = 16
        self.chunk_distance = 3
        self.terrain_scale = 20
        self.height_scale = 5
        self.seed = np.random.randint(0, 100)

        # Camera setup
        self.camera = EditorCamera()
        self.camera.position = (0, 20, 0)
        self.camera.rotation_x = -30  # Looking slightly downwards

        # Load the shader
        self.shader = lit_with_shadows_shader

        # Add a directional light to the scene
        self.setup_light()

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.update_chunks()

    def setup_light(self):
        # Create the directional light and attach it to a NodePath
        self.sun_np = NodePath(PandaDirectionalLight('sun'))
        self.sun_np.node().setColor(Vec4(1, 1, 1, 1))
        self.sun_np.node().setShadowCaster(True, 4096, 4096)  # Enable shadows and set resolution
        self.sun_np.node().get_lens().setFilmSize(100, 100)  # Adjust the frustum size
        self.sun_np.node().get_lens().setNearFar(1, 200)  # Adjust the near and far plane
        self.sun_np.set_hpr(45, -45, 0)
        self.sun_np.reparentTo(render)

        # Attach the light to the render
        render.set_light(self.sun_np)

    def update(self):
        self.update_chunks()

    
    def generate_chunk(self, x, z):
        vertices = []
        triangles = []
        chunk_size_plus_one = self.chunk_size + 1

        for i in range(chunk_size_plus_one):
            for j in range(chunk_size_plus_one):
                world_x = x * self.chunk_size + i
                world_z = z * self.chunk_size + j
                height = pnoise2(world_x / self.terrain_scale, world_z / self.terrain_scale, octaves=4, repeatx=1024, repeaty=1024, base=self.seed) * self.height_scale
                vertices.append((i, height, j))

        for i in range(self.chunk_size):
            for j in range(self.chunk_size):
                idx = i * chunk_size_plus_one + j
                triangles.append((idx, idx + chunk_size_plus_one, idx + 1))
                triangles.append((idx + 1, idx + chunk_size_plus_one, idx + chunk_size_plus_one + 1))

        return vertices, triangles

    def update_chunks(self):
        player_chunk_x = int(self.camera.x // self.chunk_size)
        player_chunk_z = int(self.camera.z // self.chunk_size)

        new_chunks = {}
        for x in range(player_chunk_x - self.chunk_distance, player_chunk_x + self.chunk_distance + 1):
            for z in range(player_chunk_z - self.chunk_distance, player_chunk_z + self.chunk_distance + 1):
                if (x, z) not in self.chunks:
                    vertices, triangles = self.generate_chunk(x, z)
                    new_chunk = Entity(
                        model=Mesh(vertices=vertices, triangles=triangles, mode='triangle', static=True), 
                        collider='mesh', 
                        color=color.green, 
                        position=(x * self.chunk_size, 0, z * self.chunk_size), 
                        shader=self.shader,
                        shadow_receiver=True
                    )
                    new_chunk.set_shader_input("light_direction", Vec3(1, -1, -1))
                    self.chunks[(x, z)] = new_chunk
                new_chunks[(x, z)] = self.chunks[(x, z)]

        # Remove old chunks
        for chunk in list(self.chunks.keys()):
            if chunk not in new_chunks:
                destroy(self.chunks[chunk])
                del self.chunks[chunk]

        self.chunks = new_chunks



app = Ursina()
'''Terrain using an RGB texture as input'''



Sky(color=color.cyan)


#player = Entity(model='sphere', color=color.azure, scale=.2, origin_y=-.5)

terrain = InfiniteTerrain()







app.run()
