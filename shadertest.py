from ursina import *

app = Ursina()

# Load the custom shader
custom_shader = Shader(language=Shader.GLSL,
                       vertex=open("custom_shader.glsl").read(),
                       fragment=open("custom_shader.glsl").read())

# Create an entity with the custom shader
entity = Entity(model='cube', color=color.white,scale = (1000,1,1000), shader=custom_shader)

# Set shader uniforms (you might need to adjust these to match your scene)
entity.set_shader_input("lightPos", Vec3(1, 1, 1))
entity.set_shader_input("viewPos", camera.world_position)
entity.set_shader_input("lightColor", Vec3(1, 1, 1))
entity.set_shader_input("objectColor", Vec3(1, 1, 1))
entity.set_shader_input("ambientStrength", 0.1)
entity.set_shader_input("specularStrength", 0.5)
entity.set_shader_input("shininess", 32)
entity.set_shader_input("fogColor", Vec3(0.5, 0.5, 0.5))
entity.set_shader_input("fogDensity", 1)
camera = EditorCamera()
Sky(color = color.cyan)
# Set up the camera and light
camera.position = (0, 0, -5)
directional_light = DirectionalLight(y=2, z=3, shadows=True)
directional_light.look_at(Vec3(10, -10,10))

app.run()