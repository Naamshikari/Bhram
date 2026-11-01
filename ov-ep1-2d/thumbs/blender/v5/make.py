import random, math, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops, ImageEnhance
random.seed(5)
S=2; W,H=1280*S,720*S
FD="/tmp/claude-0/fonts/"
def F(n,s): return ImageFont.truetype(FD+n,int(s*S))
def P(*pts): return [(x*S,y*S) for x,y in pts]
TITLE=sys.argv[1] if len(sys.argv)>1 else "UNKNOWN MAN"
OUT=sys.argv[2] if len(sys.argv)>2 else "/tmp/claude-0/v5/out.png"

def noise(size,amt,blur=0,down=1):
    n=Image.effect_noise((size[0]//down,size[1]//down),amt).convert("L")
    if down>1: n=n.resize(size,Image.BICUBIC)
    return n.filter(ImageFilter.GaussianBlur(blur)) if blur else n

# ---------- right: dark charcoal with faint chalk writing ----------
bg=Image.new("RGB",(W,H),(22,20,21))
bg=Image.composite(bg,Image.new("RGB",(W,H),(40,36,36)),noise((W,H),90,30,8))
ch=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(ch)
lines=["the unknown man was found","on Somerton beach, 1 Dec 1948","WRGOABABD   MLIAOI","Tamam Shud ... it is ended","no name   no labels   no cause","WTBIMPANETP  MLIABOAIAQC","who was he?  who knew him?","ITTMTSAMSTGAB","the book was handed in","a phone number in pencil"]
y=40
for i,l in enumerate(lines*2):
    d.text((560*S,y*S),l,font=F("NothingYouCouldDo.ttf",38),fill=(225,220,210,70))
    y+=64
    if y>720: break
ch=ch.rotate(-3,resample=Image.BICUBIC)
bg=bg.convert("RGBA"); bg.alpha_composite(ch)

# ---------- left: aged paper with the pencil code ----------
pw=Image.new("RGB",(W,H),(226,214,186))
pw=Image.composite(pw,Image.new("RGB",(W,H),(176,150,108)),noise((W,H),110,40,10).point(lambda p:255 if p>110 else int(p*2.2)))
pw=Image.blend(pw,Image.merge("RGB",[noise((W,H),60)]*3),0.06)
dp=ImageDraw.Draw(pw)
code=[("WRGOABABD",False),("MRGOABABD",True),("MLIAOI",False),("WTBIMPANETP",False),("MLIABOAIAQC",False),("ITTMTSAMSTGAB",False)]
y=95
for t,strike in code:
    f=F("ReenieBeanie.ttf",104)
    dp.text((48*S,y*S),t,font=f,fill=(48,46,50))
    if strike:
        bb=dp.textbbox((48*S,y*S),t,font=f)
        dp.line([(bb[0]-10,(bb[1]+bb[3])//2+8),(bb[2]+20,(bb[1]+bb[3])//2-4)],fill=(40,38,40),width=11*S)
    y+=100
# heavy marker strikes like the ref
for yy in (318,620):
    dp.line([(20*S,yy*S),(330*S,(yy-6)*S)],fill=(45,50,40),width=9*S)
pw=pw.filter(ImageFilter.GaussianBlur(1.2))
# torn edge mask: diagonal rip from x~520 (top) to x~430 (bottom)
m=Image.new("L",(W,H),0); pts=[(0,0)]
x0,x1=545,450; v=0
for i,yy in enumerate(range(0,721,4)):
    v+=random.uniform(-4,4); v*=0.9
    x=x0+(x1-x0)*yy/720+v+random.uniform(-3,3)
    pts.append((x*S,yy*S))
pts+= [(0,H)]
ImageDraw.Draw(m).polygon(pts,fill=255); m=m.filter(ImageFilter.GaussianBlur(1.5))
edge=ImageChops.subtract(m,m.filter(ImageFilter.MinFilter(9*S+1)))
# paper: white fibrous edge then burn
paper=pw.convert("RGBA"); paper.putalpha(m)
# shadow of paper on dark side
sh=Image.new("RGBA",(W,H),(0,0,0,0)); sh.putalpha(m.filter(ImageFilter.GaussianBlur(18*S)).point(lambda p:int(p*0.8)))
bg.alpha_composite(sh,(10*S,0))
bg.alpha_composite(paper)
fib=Image.new("RGBA",(W,H),(250,244,230,0)); fib.putalpha(edge.point(lambda p:min(255,p*2)))
bg.alpha_composite(fib)
# red glow along the rip
glow=Image.new("RGBA",(W,H),(255,40,20,0)); glow.putalpha(edge.filter(ImageFilter.GaussianBlur(14*S)).point(lambda p:min(255,p*4)))
bg.alpha_composite(glow)
hot=Image.new("RGBA",(W,H),(255,150,90,0)); hot.putalpha(edge.filter(ImageFilter.GaussianBlur(2*S)).point(lambda p:min(255,int(p*1.3))))
bg.alpha_composite(hot)
# embers / sparks along the rip
sp=Image.new("RGBA",(W,H),(0,0,0,0)); ds=ImageDraw.Draw(sp)
for _ in range(70):
    yy=random.uniform(250,720); x=x0+(x1-x0)*yy/720+random.uniform(-40,120); r=random.uniform(1,3.2)
    ds.ellipse([(x-r)*S,(yy-r)*S,(x+r)*S,(yy+r)*S],fill=(255,random.randint(90,190),60,random.randint(150,255)))
bg.alpha_composite(sp.filter(ImageFilter.GaussianBlur(1))); bg.alpha_composite(sp.filter(ImageFilter.GaussianBlur(6)))

# ---------- the man: Blender render, face in total shadow ----------
man=Image.open("/tmp/claude-0/v5/man_full.png").convert("RGBA")
sc_=float(__import__("os").environ.get("MANSCALE","1.12"))
man=man.resize((int(W*sc_),int(H*sc_)),Image.LANCZOS)
ox=int((W-man.size[0])/2+int(__import__("os").environ.get("MANDX","40"))*S); oy=int(H-man.size[1]+int(__import__('os').environ.get('MANDY','150'))*S)
layer=Image.new("RGBA",(W,H),(0,0,0,0)); layer.alpha_composite(man,(max(ox,0),oy) if ox>=0 else (0,oy)) if ox>=0 else None
if ox<0:
    layer.alpha_composite(man.crop((-ox,0,-ox+W,man.size[1])),(0,oy))
fig=layer.split()[3]
fs=Image.new("RGBA",(W,H),(0,0,0,0)); fs.putalpha(fig.filter(ImageFilter.GaussianBlur(30*S)).point(lambda p:int(p*0.85)))
bg.alpha_composite(fs,(18*S,8*S))
bg.alpha_composite(layer)
def rim(mask,dx,col,blur,amt):
    e=ImageChops.subtract(mask,ImageChops.offset(mask,dx*S,0)).filter(ImageFilter.GaussianBlur(blur*S))
    l=Image.new("RGBA",(W,H),col+(0,)); l.putalpha(e.point(lambda p:min(255,int(p*amt)))); return l
bg.alpha_composite(rim(fig,10,(255,45,25),16,1.0))
# red light spill over left of frame / figure
spill=Image.new("L",(W,H),0); ImageDraw.Draw(spill).ellipse(P((300,120),(760,820)),fill=255); spill=spill.filter(ImageFilter.GaussianBlur(120*S))
rl=Image.new("RGBA",(W,H),(255,30,15,0)); rl.putalpha(spill.point(lambda p:int(p*0.33))); bg.alpha_composite(rl)

# ---------- title ----------
fsz=196
f=F("AlfaSlabOne-Regular.ttf",fsz)
while f.getlength(TITLE)>1210*S: fsz-=4; f=F("AlfaSlabOne-Regular.ttf",fsz)
tx,ty=W//2,92*S
h=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(h).text((tx,ty+5*S),TITLE,font=f,fill=(0,0,0,255),anchor="mm",stroke_width=10*S,stroke_fill=(0,0,0,255))
bg.alpha_composite(h.filter(ImageFilter.GaussianBlur(18*S))); bg.alpha_composite(h.filter(ImageFilter.GaussianBlur(5*S)))
t=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(t).text((tx,ty),TITLE,font=f,fill=(252,250,246,255),anchor="mm")
t.putalpha(ImageChops.multiply(t.split()[3],noise((W,H),120).point(lambda p:255 if p>10 else 170)))
bg.alpha_composite(t)

# ---------- finish ----------
im=bg.convert("RGB").resize((1280,720),Image.LANCZOS)
v=Image.new("L",(1280,720),0); ImageDraw.Draw(v).ellipse([-260,-220,1540,940],fill=255); v=v.filter(ImageFilter.GaussianBlur(150))
im=Image.composite(im,Image.blend(im,Image.new("RGB",im.size,(0,0,0)),0.55),v)
im=ImageEnhance.Contrast(im).enhance(1.1); im=ImageEnhance.Color(im).enhance(1.12)
r,g,b=im.split(); im=Image.merge("RGB",(ImageChops.offset(r,2,0),g,ImageChops.offset(b,-2,0))).crop((4,2,1276,718)).resize((1280,720),Image.LANCZOS)
im=Image.blend(im,Image.effect_noise((1280,720),80).convert("RGB"),0.06)
im.save(OUT); im.resize((320,180),Image.LANCZOS).save(OUT.replace(".png","_small.png")); print("ok")
