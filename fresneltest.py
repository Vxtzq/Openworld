from ursina import *
app = Ursina()

b = Entity(model='sphere', color=color.black, shader=fresnel_shader)
ground = Entity(model='plane', color=color.gray, shader=fresnel_shader, y=-1, scale=64, texture='grass', texture_scale=Vec2(32,32))
ground.set_shader_input('fresnel_color', color.gray)
ground.set_shader_input('fresnel_texture', load_texture('white_cube'))
EditorCamera()

for i in range(16):
    e = Entity(model='cube', origin_y=-.5, scale=2, texture='brick', texture_scale=(1,2),
        x=random.uniform(-8,8),
        z=random.uniform(-8,8) + 8,
        scale_y = random.uniform(2,3),
        color=color.hsv(0, 0, random.uniform(.9, 1)),
        shader=fresnel_shader,
        )
    e.set_shader_input('fresnel_texture', load_texture('brick'))

def update():
    for e in scene.entities:
        if hasattr(e, 'shader') and e.shader == fresnel_shader:
            e.set_shader_input('camera_world_position', camera.world_position)





app.run()