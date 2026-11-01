import bpy, math, sys
from mathutils import Vector
args=dict(a.split("=") for a in sys.argv[1:])
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene
def mat(name,col,rough=0.8,sheen=0.0):
    m=bpy.data.materials.new(name); m.use_nodes=True
    b=m.node_tree.nodes["Principled BSDF"]; b.inputs["Base Color"].default_value=col+(1,); b.inputs["Roughness"].default_value=rough
    try: b.inputs["Sheen Weight"].default_value=sheen
    except: pass
    return m
COAT=mat("coat",(0.025,0.024,0.027),0.85,0.6); FELT=mat("felt",(0.02,0.018,0.018),0.9,0.5)
SKIN=mat("skin",(0.12,0.07,0.05),0.6); SHIRT=mat("shirt",(0.35,0.33,0.3),0.7); TIE=mat("tie",(0.35,0.01,0.01),0.5)
def sub(o,l=3):
    m=o.modifiers.new("s","SUBSURF"); m.levels=m.render_levels=l
    bpy.ops.object.shade_smooth()
def put(o,m): o.data.materials.append(m)
# real proportions (metres)
import bmesh
prof=[(1.49,0.075,0.068),(1.465,0.13,0.095),(1.44,0.20,0.12),(1.405,0.28,0.135),(1.36,0.305,0.142),(1.28,0.315,0.148),(1.15,0.30,0.15),(0.95,0.29,0.15),(0.6,0.285,0.15)]
me=bpy.data.meshes.new("torso"); bm=bmesh.new(); N=48; rings=[]
for z,rx,ry in prof:
    rings.append([bm.verts.new((rx*math.cos(2*math.pi*i/N), ry*math.sin(2*math.pi*i/N), z)) for i in range(N)])
for r0,r1 in zip(rings,rings[1:]):
    for i in range(N): bm.faces.new((r0[i],r0[(i+1)%N],r1[(i+1)%N],r1[i]))
bm.faces.new(rings[-1][::-1]); bm.to_mesh(me); bm.free()
t=bpy.data.objects.new("torso",me); sc.collection.objects.link(t); bpy.context.view_layer.objects.active=t; t.select_set(True)
sub(t,2); put(t,COAT)
bpy.ops.mesh.primitive_cylinder_add(radius=0.06,depth=0.12,location=(0,0.01,1.52)); n=bpy.context.object; sub(n,1); put(n,SKIN)
bpy.ops.mesh.primitive_cylinder_add(radius=0.08,depth=0.07,location=(0,0.0,1.49)); c=bpy.context.object; sub(c,2); put(c,SHIRT)
bpy.ops.mesh.primitive_uv_sphere_add(radius=1,location=(0,0.01,1.63),segments=64,ring_count=32); h=bpy.context.object; h.scale=(0.088,0.105,0.118); bpy.ops.object.shade_smooth(); put(h,SKIN)
bpy.ops.mesh.primitive_uv_sphere_add(radius=1,location=(0,-0.025,1.56),segments=48,ring_count=24); j=bpy.context.object; j.scale=(0.07,0.075,0.06); bpy.ops.object.shade_smooth(); put(j,SKIN)
for x in (-0.088,0.088):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1,location=(x,0.02,1.62)); e=bpy.context.object; e.scale=(0.012,0.022,0.032); bpy.ops.object.shade_smooth(); put(e,SKIN)
bpy.ops.mesh.primitive_cylinder_add(radius=0.19,depth=0.01,location=(0,0,1.715),vertices=96); br=bpy.context.object; br.scale=(1,0.93,1)
bd=br.modifiers.new("b","SIMPLE_DEFORM"); bd.deform_method="BEND"; bd.angle=math.radians(-22); bd.deform_axis="Y"
sub(br,2); put(br,FELT)
bpy.ops.mesh.primitive_cylinder_add(radius=0.105,depth=0.13,location=(0,0,1.78),vertices=64); cr=bpy.context.object; cr.scale=(1,0.9,1)
for v in cr.data.vertices:
    if v.co.z>0: v.co.x*=0.88; v.co.y*=0.82; v.co.z-=0.035*(1-abs(v.co.y)/0.105)
sub(cr,1); put(cr,FELT)
bpy.ops.mesh.primitive_cylinder_add(radius=0.106,depth=0.025,location=(0,0,1.735),vertices=64); bn=bpy.context.object; bn.scale=(1.01,0.91,1); put(bn,mat("band",(0.004,0.004,0.004),0.35))
for o in (br,cr,bn): o.rotation_euler=(math.radians(-7),math.radians(4),0)
bpy.ops.mesh.primitive_cube_add(location=(0,-0.15,1.38)); sv=bpy.context.object; sv.scale=(0.065,0.006,0.1)
for v in sv.data.vertices:
    if v.co.z<0: v.co.x*=0.1
put(sv,SHIRT)
bpy.ops.mesh.primitive_cube_add(location=(0,-0.156,1.25)); ti=bpy.context.object; ti.scale=(0.022,0.006,0.17)
for v in ti.data.vertices:
    if v.co.z>0: v.co.x*=0.65
put(ti,TIE)
# lights: no key on the face. red rim left-back, cool-warm rim right-back, faint front fill
def L(kind,loc,e,col,tgt=(0,0,1.5),**kw):
    d=bpy.data.lights.new("l",kind); d.energy=e; d.color=col
    for k,v in kw.items(): setattr(d,k,v)
    o=bpy.data.objects.new("l",d); sc.collection.objects.link(o); o.location=loc
    o.rotation_euler=(Vector(tgt)-Vector(loc)).to_track_quat("-Z","Y").to_euler()
L("AREA",(-1.3,2.6,1.9),float(args.get("red","1600")),(1,0.05,0.02),size=1.2)
L("AREA",(1.3,2.8,1.9),float(args.get("warm","500")),(1,0.75,0.55),size=1.0)
L("AREA",(0.4,-4,1.4),float(args.get("fill","8")),(1,0.3,0.25),size=4)
L("SPOT",(0,0.3,3.2),float(args.get("top","40")),(1,0.8,0.65),tgt=(0,0,1.75),spot_size=math.radians(30),spot_blend=0.5)
cd=bpy.data.cameras.new("c"); cd.lens=85
cam=bpy.data.objects.new("c",cd); sc.collection.objects.link(cam); cam.location=(0,-3.4,1.45)
cam.rotation_euler=(Vector((0,0,1.42))-cam.location).to_track_quat("-Z","Y").to_euler(); sc.camera=cam
w=bpy.data.worlds.new("w"); sc.world=w; w.use_nodes=True; w.node_tree.nodes["Background"].inputs[0].default_value=(0,0,0,1)
sc.render.engine="CYCLES"; sc.cycles.samples=int(args.get("s","48")); sc.cycles.use_denoising=True
sc.render.film_transparent=True
sc.render.resolution_x=1280; sc.render.resolution_y=720; sc.render.resolution_percentage=int(args.get("pct","100"))
sc.view_settings.view_transform="AgX"
sc.render.image_settings.file_format="PNG"; sc.render.image_settings.color_mode="RGBA"
sc.render.filepath=args.get("out","/tmp/claude-0/v5/man.png")
bpy.ops.render.render(write_still=True); print("RENDERED")
