import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
random.seed(11)
W,H=2000,700
o="/tmp/claude-0/b3d/"
# paper colour
base=Image.new("RGB",(W,H),(214,196,155))
n=Image.effect_noise((W,H),70).convert("L")
fib=Image.effect_noise((W//4,H//4),90).convert("L").resize((W,H),Image.BICUBIC).filter(ImageFilter.GaussianBlur(6))
stain=Image.effect_noise((W//40,H//40),120).convert("L").resize((W,H),Image.BICUBIC).filter(ImageFilter.GaussianBlur(40))
col=Image.blend(base,Image.merge("RGB",[n]*3),0.06)
col=Image.composite(col,Image.blend(col,Image.new("RGB",(W,H),(150,110,60)),0.45),stain.point(lambda p:255 if p>120 else int(p*1.6)))
d=ImageDraw.Draw(col)
f=ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",300)
d.text((W//2,H//2+10),"Tamám Shud",font=f,fill=(22,18,16),anchor="mm")
# ink texture: slightly broken
col=col.filter(ImageFilter.GaussianBlur(1.2))
dd=ImageDraw.Draw(col)
for _ in range(60):
    x=random.randint(0,W); y=random.randint(0,H); r=random.randint(2,10)
    dd.ellipse([x-r,y-r,x+r,y+r],fill=(150,110,70))
col=col.filter(ImageFilter.GaussianBlur(0.8))
col.save(o+"scrap_col.png")
# torn alpha: organic random-walk edges with multi-scale wobble
import math
m=Image.new("L",(W,H),0); pts=[]
def walk(n, amp_big, amp_small):
    v=0; out=[]
    for i in range(n):
        v+=random.uniform(-amp_big,amp_big); v*=0.92
        out.append(v+random.uniform(-amp_small,amp_small))
    return out
top=walk(W//6+2,7,9); bot=walk(W//6+2,7,9); lf=walk(H//6+2,8,8); rt=walk(H//6+2,8,8)
for i,x in enumerate(range(0,W,6)): pts.append((x,70+top[i]))
for i,y in enumerate(range(0,H,6)): pts.append((W-70+rt[i]+0,y))
for i,x in enumerate(range(W,0,-6)): pts.append((x,H-70+bot[min(i,len(bot)-1)]))
for i,y in enumerate(range(H,0,-6)): pts.append((60+lf[min(i,len(lf)-1)],y))
ImageDraw.Draw(m).polygon(pts,fill=255)
rr=Image.new('L',(W,H),0); ImageDraw.Draw(rr).rounded_rectangle([45,50,W-45,H-50],radius=30,fill=255); m=ImageChops.multiply(m,rr)
# fibrous micro edge
fn=Image.effect_noise((W,H),255).convert("L").filter(ImageFilter.GaussianBlur(1))
m=m.filter(ImageFilter.GaussianBlur(3)); m=ImageChops.multiply(m.point(lambda p:255 if p>100 else p*2), Image.eval(fn,lambda p:255))
m=m.filter(ImageFilter.GaussianBlur(1.5))
m.save(o+"scrap_alpha.png")
# edge mask (for ember glow + burn darkening)
er=m.filter(ImageFilter.MinFilter(15))
edge=ImageChops.subtract(m,er).filter(ImageFilter.GaussianBlur(6))
edge=edge.point(lambda p:min(255,int(p*1.8)))
edge.save(o+"scrap_edge.png")
print("tex ok")
