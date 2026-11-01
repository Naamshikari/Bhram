import bpy, math, sys
from mathutils import Vector
args=dict(a.split("=") for a in sys.argv[1:])
SAMPLES=int(args.get("s","32")); SCALE=int(args.get("pct","50")); OUT=args.get("out","/tmp/claude-0/b3d/prev.png")
T="/tmp/claude-0/b3d/"
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene
def node_mat(name):
    m=bpy.data.materials.new(name); m.use_nodes=True; nt=m.node_tree; nt.nodes.clear(); return m,nt
def link(nt,a,b): nt.links.new(a,b)

# ---------- sand ----------
bpy.ops.mesh.primitive_plane_add(size=24)
sand=bpy.context.object
sub=sand.modifiers.new("sub","SUBSURF"); sub.subdivision_type="SIMPLE"; sub.levels=sub.render_levels=7
tx=bpy.data.textures.new("dunes","CLOUDS"); tx.noise_scale=1.4
dm=sand.modifiers.new("disp","DISPLACE"); dm.texture=tx; dm.strength=0.12; dm.mid_level=0.5
tx2=bpy.data.textures.new("ripples","CLOUDS"); tx2.noise_scale=0.18
dm2=sand.modifiers.new("disp2","DISPLACE"); dm2.texture=tx2; dm2.strength=0.025
m,nt=node_mat("sand"); N=nt.nodes
out=N.new("ShaderNodeOutputMaterial"); bs=N.new("ShaderNodeBsdfPrincipled")
tc=N.new("ShaderNodeTexCoord")
nz=N.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value=160; nz.inputs["Detail"].default_value=2
nz2=N.new("ShaderNodeTexNoise"); nz2.inputs["Scale"].default_value=6; nz2.inputs["Detail"].default_value=6
sp=N.new("ShaderNodeTexNoise"); sp.inputs["Scale"].default_value=420; sp.inputs["Detail"].default_value=0
link(nt,tc.outputs["Object"],sp.inputs["Vector"])
cr=N.new("ShaderNodeValToRGB"); cr.color_ramp.elements[0].color=(0.02,0.017,0.015,1); cr.color_ramp.elements[1].color=(0.13,0.10,0.075,1)
mix=N.new("ShaderNodeMath"); mix.operation="MULTIPLY_ADD"; mix.inputs[1].default_value=0.6; 
link(nt,tc.outputs["Object"],nz.inputs["Vector"]); link(nt,tc.outputs["Object"],nz2.inputs["Vector"])
spm=N.new("ShaderNodeMath"); spm.operation="ADD"; link(nt,nz.outputs["Fac"],spm.inputs[0]); link(nt,sp.outputs["Fac"],spm.inputs[1]); spm2=N.new("ShaderNodeMath"); spm2.operation="MULTIPLY"; spm2.inputs[1].default_value=0.5; link(nt,spm.outputs[0],spm2.inputs[0]); link(nt,spm2.outputs[0],mix.inputs[0]); link(nt,nz2.outputs["Fac"],mix.inputs[2])
link(nt,mix.outputs[0],cr.inputs["Fac"]); link(nt,cr.outputs["Color"],bs.inputs["Base Color"])
bs.inputs["Roughness"].default_value=0.92
bump=N.new("ShaderNodeBump"); bump.inputs["Strength"].default_value=0.8; bump.inputs["Distance"].default_value=0.01
wv=N.new("ShaderNodeTexWave"); wv.inputs["Scale"].default_value=0.9; wv.inputs["Distortion"].default_value=14; wv.inputs["Detail"].default_value=3
link(nt,tc.outputs["Object"],wv.inputs["Vector"])
hm=N.new("ShaderNodeMath"); hm.operation="MULTIPLY_ADD"; hm.inputs[1].default_value=1.0
link(nt,nz.outputs["Fac"],hm.inputs[0]); wm=N.new('ShaderNodeMath'); wm.operation='MULTIPLY'; wm.inputs[1].default_value=0.35; link(nt,wv.outputs['Fac'],wm.inputs[0]); link(nt,wm.outputs[0],hm.inputs[2])
bump.inputs["Distance"].default_value=0.03
link(nt,hm.outputs[0],bump.inputs["Height"]); link(nt,bump.outputs["Normal"],bs.inputs["Normal"])
link(nt,bs.outputs[0],out.inputs["Surface"])
sand.data.materials.append(m)

# ---------- scrap ----------
bpy.ops.mesh.primitive_plane_add(size=1)
p=bpy.context.object; p.scale=(2.0,0.7,1); bpy.ops.object.transform_apply(scale=True)
s=p.modifiers.new("sub","SUBSURF"); s.subdivision_type="SIMPLE"; s.levels=s.render_levels=6
wr=bpy.data.textures.new("wr","CLOUDS"); wr.noise_scale=0.9
d=p.modifiers.new("wr","DISPLACE"); d.texture=wr; d.strength=0.012
bd=p.modifiers.new("bend","SIMPLE_DEFORM"); bd.deform_method="BEND"; bd.angle=math.radians(12); bd.deform_axis="Y"
p.location=(0,0,0.13); p.rotation_euler=(math.radians(-6),math.radians(3),math.radians(-7))
m,nt=node_mat("scrap"); N=nt.nodes
out=N.new("ShaderNodeOutputMaterial")
uv=N.new("ShaderNodeTexCoord")
def img(path,noncolor=False):
    t=N.new("ShaderNodeTexImage"); t.image=bpy.data.images.load(path)
    if noncolor: t.image.colorspace_settings.name="Non-Color"
    link(nt,uv.outputs["UV"],t.inputs["Vector"]); return t
ci=img(T+"scrap_col.png"); ai=img(T+"scrap_alpha.png",True); ei=img(T+"scrap_edge.png",True)
burn=N.new("ShaderNodeMix"); burn.data_type="RGBA"; burn.blend_type="MULTIPLY"
link(nt,ei.outputs["Color"],burn.inputs["Factor"]); link(nt,ci.outputs["Color"],burn.inputs[6]); burn.inputs[7].default_value=(0.12,0.05,0.02,1)
bs=N.new("ShaderNodeBsdfPrincipled"); bs.inputs["Roughness"].default_value=0.75
link(nt,burn.outputs[2],bs.inputs["Base Color"])
tr=N.new("ShaderNodeBsdfTranslucent"); link(nt,burn.outputs[2],tr.inputs["Color"])
mx=N.new("ShaderNodeMixShader"); mx.inputs[0].default_value=0.06
link(nt,bs.outputs[0],mx.inputs[1]); link(nt,tr.outputs[0],mx.inputs[2])
em=N.new("ShaderNodeEmission"); em.inputs["Color"].default_value=(1.0,0.12,0.02,1)
emstr=N.new("ShaderNodeMath"); emstr.operation="MULTIPLY"; emstr.inputs[1].default_value=float(args.get("ember","9"))
link(nt,ei.outputs["Color"],emstr.inputs[0]); link(nt,emstr.outputs[0],em.inputs["Strength"])
add=N.new("ShaderNodeAddShader"); link(nt,mx.outputs[0],add.inputs[0]); link(nt,em.outputs[0],add.inputs[1])
tp=N.new("ShaderNodeBsdfTransparent")
fin=N.new("ShaderNodeMixShader"); link(nt,ai.outputs["Color"],fin.inputs[0]); link(nt,tp.outputs[0],fin.inputs[1]); link(nt,add.outputs[0],fin.inputs[2])
link(nt,fin.outputs[0],out.inputs["Surface"])
p.data.materials.append(m)

# ---------- lights ----------
def light(kind,name,loc,energy,color,target=(0,0,0.1),**kw):
    L=bpy.data.lights.new(name,kind); L.energy=energy; L.color=color
    for k,v in kw.items(): setattr(L,k,v)
    o=bpy.data.objects.new(name,L); sc.collection.objects.link(o); o.location=loc
    dvec=Vector(target)-Vector(loc); o.rotation_euler=dvec.to_track_quat("-Z","Y").to_euler(); return o
light("SPOT","key",(-0.6,-1.3,4.6),float(args.get("key","900")),(1.0,0.86,0.68),spot_size=math.radians(19),spot_blend=0.65,shadow_soft_size=0.03)
light("AREA","rim",(0.3,3.2,0.9),float(args.get("rim","1400")),(1.0,0.06,0.02),target=(0,0,0),size=3.0)
light("POINT","redpool",(2.4,0.8,0.25),float(args.get("pool","120")),(1.0,0.08,0.03),shadow_soft_size=0.3)
light("AREA","cool",(-3,-2,1.5),30,(0.4,0.55,1.0),size=2)

# ---------- camera ----------
cd=bpy.data.cameras.new("cam"); cd.lens=float(args.get("lens","45"))
cam=bpy.data.objects.new("cam",cd); sc.collection.objects.link(cam)
cam.location=(0.05,-2.75,2.55)
aim=Vector((0,0.40,0.0)); cam.rotation_euler=(aim-cam.location).to_track_quat("-Z","Y").to_euler()
cd.dof.use_dof=True; cd.dof.focus_distance=(Vector((0,0,0.13))-cam.location).length; cd.dof.aperture_fstop=float(args.get("f","2.2"))
sc.camera=cam

# ---------- world / render ----------
w=bpy.data.worlds.new("w"); sc.world=w; w.use_nodes=True
w.node_tree.nodes["Background"].inputs[0].default_value=(0.004,0.004,0.006,1)
sc.render.engine="CYCLES"; sc.cycles.device="CPU"; sc.cycles.samples=SAMPLES; sc.cycles.use_denoising=True
sc.render.resolution_x=1280; sc.render.resolution_y=720; sc.render.resolution_percentage=SCALE
try:
    sc.view_settings.view_transform="AgX"; sc.view_settings.look="AgX - Medium High Contrast"
except Exception as e: print("cm",e)
sc.render.filepath=OUT; sc.render.image_settings.file_format="PNG"
bpy.ops.render.render(write_still=True)
print("RENDERED",OUT)
