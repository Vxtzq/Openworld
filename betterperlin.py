from ursina import *
from noise import pnoise2
import numpy as np
from panda3d.core import DirectionalLight as PandaDirectionalLight, NodePath, Vec4, Vec3, Fog
from ursina.shaders import lit_with_shadows_shader
app = Ursina()

class InfiniteTerrain(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.chunks = {}
        self.chunk_size = 16
        self.chunk_distance = 3
        self.terrain_scale = 20
        self.height_scale = 5
        self.seed = np.random.randint(0, 100)
        self.sun = DirectionalLight(shadow_map_resolution=(256,256))
        self.sun.look_at(Vec3(-10,-1,-10))
        self.sun.position = Vec3(0, 10, 0)
        # Camera setup
        self.camera = EditorCamera()
        self.camera.position = (0, 20, 0)
        self.camera.rotation_x = -30  # Looking slightly downwards

        # Load the shader
        self.shader = lit_with_shadows_shader

        # Add a directional light to the scene
        

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.update_chunks()

    

    def update(self):
        self.update_chunks()

    

    def generate_chunk(self, x, z):
        vertices = []
        triangles = []
        colors = []
        chunk_size_plus_one = self.chunk_size + 1

        for i in range(chunk_size_plus_one):
            for j in range(chunk_size_plus_one):
                world_x = x * self.chunk_size + i
                world_z = z * self.chunk_size + j
                
                # Use different scales for different octaves to create more varied terrain
                height = (
                    pnoise2(world_x / self.terrain_scale, world_z / self.terrain_scale, octaves=4, repeatx=1024, repeaty=1024, base=self.seed) * self.height_scale +
                    pnoise2(world_x / (self.terrain_scale / 2), world_z / (self.terrain_scale / 2), octaves=2, repeatx=1024, repeaty=1024, base=self.seed) * (self.height_scale / 2) +
                    pnoise2(world_x / (self.terrain_scale / 4), world_z / (self.terrain_scale / 4), octaves=8, repeatx=1024, repeaty=1024, base=self.seed) * (self.height_scale / 4)
                )
                
                vertices.append((i, height, j))
                
                # Assign colors based on height
                if height < 1:
                    colors.append(color.yellow)
                else:
                    colors.append(color.green)

        for i in range(self.chunk_size):
            for j in range(self.chunk_size):
                idx = i * chunk_size_plus_one + j
                triangles.append((idx, idx + chunk_size_plus_one, idx + 1))
                triangles.append((idx + 1, idx + chunk_size_plus_one, idx + chunk_size_plus_one + 1))

        return vertices, triangles, colors

    def update_chunks(self):
        player_chunk_x = int(self.camera.x // self.chunk_size)
        player_chunk_z = int(self.camera.z // self.chunk_size)

        new_chunks = {}
        for x in range(player_chunk_x - self.chunk_distance, player_chunk_x + self.chunk_distance + 1):
            for z in range(player_chunk_z - self.chunk_distance, player_chunk_z + self.chunk_distance + 1):
                if (x, z) not in self.chunks:
                    vertices, triangles, colors = self.generate_chunk(x, z)
                    new_chunk = Entity(
                        model=Mesh(vertices=vertices, triangles=triangles, colors=colors, mode='triangle', static=True), 
                        collider='mesh', 
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

        # Update the bounds of the scene to ensure shadows are calculated correctly
        self.sun.update_bounds(entity=scene)

terrain = InfiniteTerrain()
app.run()

