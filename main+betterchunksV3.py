from ursina import *
from ursina.shaders import lit_with_shadows_shader
from ursina.shaders import colored_lights_shader

from noise import pnoise2
import numpy as np
import random
from ursina.prefabs.first_person_controller import FirstPersonController

from ursina.lights import DirectionalLight

512
rand_state = random.Random()

class InfiniteTerrain(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.chunks = {}
        self.chunk_size = 16
        self.terrain_scale = 100
        self.height_scale = 10
        self.chunk_distance = 5

        # Perlin noise settings for additional detail
        self.detail_scale = 20
        self.detail_height = 2

        # Perlin noise settings for mountains
        self.mountain_scale = 200
        self.mountain_height = 50

        self.octaves = 4
        self.persistence = 0.5
        self.lacunarity = 2.0
        self.seed = np.random.randint(0, 100)
        self.sun = DirectionalLight(shadow_map_resolution=(4096,4096))
        self.sun.look_at(Vec3(-10,-1,-10))
        self.sun.position = Vec3(0, 10, 0)
        self.water = Entity(model='plane', color=color.color(160,1,.8,.5), position=(0,-1,0), scale=200, rotation=(0,0,0), double_sided=True,)
        # Camera setup
        self.camera = EditorCamera()
        self.camera.position = (0, 20, 0)
        self.camera.rotation_x = -30  # Looking slightly downwards
        blob=Entity(parent=self.model,model="assets",position=(0,2,0),scale=1,shader=lit_with_shadows_shader)
        # Load the shader
        self.shader = lit_with_shadows_shader

        # Add a directional light to the scene
        

        self.setup_fog()

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.update_chunks()

    def update(self):
        self.update_chunks()
        self.camera.x += .3
    def setup_fog(self):
        from panda3d.core import Fog

        fog = Fog("SceneFog")
        fog.setColor(0.5, 0.5, 0.5)  # Grey fog color
        fog.setExpDensity(0.1)  # Adjust density for desired effect

        render.setFog(fog)

        # Set the background color of the scene to match the fog
        base.win.setClearColor(Vec4(0.5, 0.5, 0.5, 1))

    def generate_chunk(self, x, z):       
            
        vertices = []
        triangles = []
        uvs = []
        colors = []
        normals = []
        chunk_size_plus_one = self.chunk_size + 1

        for i in range(chunk_size_plus_one):
            for j in range(chunk_size_plus_one):
                world_x = x * self.chunk_size + i
                world_z = z * self.chunk_size + j

                # Base terrain layer
                base_height = pnoise2(world_x / self.terrain_scale, world_z / self.terrain_scale, 
                                      octaves=self.octaves, persistence=self.persistence, lacunarity=self.lacunarity, 
                                      repeatx=1024, repeaty=1024, base=self.seed) * self.height_scale

                # Detail layer
                detail_height = pnoise2(world_x / self.detail_scale, world_z / self.detail_scale, 
                                        octaves=self.octaves, persistence=self.persistence, lacunarity=self.lacunarity, 
                                        repeatx=1024, repeaty=1024, base=self.seed) * self.detail_height

                # Mountain layer
                mountain_height = pnoise2(world_x / self.mountain_scale, world_z / self.mountain_scale, 
                                          octaves=self.octaves, persistence=self.persistence, lacunarity=self.lacunarity, 
                                          repeatx=1024, repeaty=1024, base=self.seed) * self.mountain_height

                # Combine the heights
                height = base_height + detail_height + mountain_height*0.1

                vertices.append((i, height, j))
                uvs.append((i / self.chunk_size, j / self.chunk_size))
                normals.append((0, 1, 0))  # Placeholder normals, you may want to calculate actual normals

                toappend = None
                    # Assign colors based on height
                if  height < -.3:
                    
                    toappend = color.rgb32(255, 230, 146)
                
                if height > 4:
                    
                    toappend = color.gray
                if height > 5:
                    
                    toappend = color.white
                
                if height >  -.3 and height < 4:
                    
                    toappend = color.green
                
                colors.append(toappend)
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
                    new_chunk.scale = (1, 2, 1)
                    new_chunk.set_shader_input("light_direction", Vec3(1, -1, -1))
                    self.chunks[(x, z)] = new_chunk
                new_chunks[(x, z)] = self.chunks[(x, z)]
        self.water.position=(self.camera.x,-1,self.camera.z)
        # Remove old chunks
        for chunk in list(self.chunks.keys()):
            if chunk not in new_chunks:
                destroy(self.chunks[chunk])
                del self.chunks[chunk]

        self.chunks = new_chunks
        self.sun.update_bounds(entity=scene)



app = Ursina()
'''Terrain using an RGB texture as input'''



Sky(color=color.cyan)


#player = Entity(model='sphere', color=color.azure, scale=.2, origin_y=-.5)

terrain = InfiniteTerrain()







app.run()
