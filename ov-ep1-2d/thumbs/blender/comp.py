import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops
src=sys.argv[1]; title=sys.argv[2]; out=sys.argv[3]
im=Image.open(src).convert("RGB")
W,H=im.size
im=ImageEnhance.Contrast(im).enhance(1.12); im=ImageEnhance.Color(im).enhance(1.15)
# vignette
v=Image.new("L",(W,H),0); ImageDraw.Draw(v).ellipse([-W*0.2,-H*0.3,W*1.2,H*1.3],fill=255); v=v.filter(ImageFilter.GaussianBlur(180))
im=Image.composite(im,Image.blend(im,Image.new("RGB",(W,H),(0,0,0)),0.6),v)
im=im.convert("RGBA")
f=ImageFont.truetype("/tmp/claude-0/fonts/AlfaSlabOne-Regular.ttf",200)
size=200
while f.getlength(title)>W-90: size-=4; f=ImageFont.truetype("/tmp/claude-0/fonts/AlfaSlabOne-Regular.ttf",size)
x=W//2; y=int(H*0.15)
# dark halo
h=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(h).text((x,y+6),title,font=f,fill=(0,0,0,255),anchor="mm",stroke_width=14,stroke_fill=(0,0,0,255))
im.alpha_composite(h.filter(ImageFilter.GaussianBlur(22))); im.alpha_composite(h.filter(ImageFilter.GaussianBlur(8)))
# soft white bloom
g=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(g).text((x,y),title,font=f,fill=(255,235,220,150),anchor="mm")
im.alpha_composite(g.filter(ImageFilter.GaussianBlur(14)))
t=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(t).text((x,y),title,font=f,fill=(250,247,240,255),anchor="mm")
# distress the type slightly
n=Image.effect_noise((W,H),120).convert("L").point(lambda p:255 if p>12 else 190)
t.putalpha(ImageChops.multiply(t.split()[3],n))
im.alpha_composite(t)
im=im.convert("RGB")
# chromatic aberration
r,g_,b=im.split(); r=ImageChops.offset(r,2,0); b=ImageChops.offset(b,-2,0); im=Image.merge("RGB",(r,g_,b))
# film grain
gn=Image.effect_noise((W,H),70).convert("RGB")
im=Image.blend(im,gn,0.055); im=ImageEnhance.Brightness(im).enhance(1.06)
im.save(out); im.resize((320,180),Image.LANCZOS).save(out.replace(".png","_small.png"))
print("ok")
