import random, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
W,H=1280,720
F="fonts/"  # Anton, Special Elite, Permanent Marker (Google Fonts)
ANTON=lambda s:ImageFont.truetype(F+"Anton-Regular.ttf",s)
TYPE=lambda s:ImageFont.truetype(F+"SpecialElite-Regular.ttf",s)
HAND=lambda s:ImageFont.truetype(F+"PermanentMarker-Regular.ttf",s)
random.seed(3)
YEL=(255,214,0); RED=(232,28,36); WHITE=(255,255,255); BLK=(0,0,0)

def radial(size, center, r, inner, outer):
    w,h=size; m=Image.new("L",size,0); d=ImageDraw.Draw(m)
    d.ellipse([center[0]-r,center[1]-r,center[0]+r,center[1]+r],fill=255)
    m=m.filter(ImageFilter.GaussianBlur(r*0.45))
    return Image.composite(Image.new("RGB",size,inner),Image.new("RGB",size,outer),m)
def grain(im,a=0.05):
    n=Image.effect_noise(im.size,60).convert("RGB"); return Image.blend(im,n,a)
def glow(bg, layer, radius=30, strength=1.6):
    a=layer.split()[3].filter(ImageFilter.GaussianBlur(radius))
    col=layer.convert("RGB").filter(ImageFilter.GaussianBlur(radius))
    g=Image.new("RGBA",bg.size,(0,0,0,0)); g.paste(col,(0,0)); g.putalpha(a.point(lambda p:min(255,int(p*strength))))
    bg.alpha_composite(g); bg.alpha_composite(layer)
def big_text(bg, txt, xy, size, fill, maxw=None, stroke=10, anchor="la", shadow=True):
    f=ANTON(size)
    if maxw:
        while f.getlength(txt)>maxw: size-=4; f=ANTON(size)
    d=ImageDraw.Draw(bg)
    if shadow:
        s=Image.new("RGBA",bg.size,(0,0,0,0)); ImageDraw.Draw(s).text((xy[0]+8,xy[1]+12),txt,font=f,fill=(0,0,0,230),anchor=anchor,stroke_width=stroke,stroke_fill=(0,0,0,230))
        bg.alpha_composite(s.filter(ImageFilter.GaussianBlur(8)))
    d.text(xy,txt,font=f,fill=fill,anchor=anchor,stroke_width=stroke,stroke_fill=BLK)
    return d.textbbox(xy,txt,font=f,anchor=anchor,stroke_width=stroke)
def torn(img, jag=12):
    w,h=img.size; m=Image.new("L",(w,h),0); pts=[]
    for x in range(0,w+1,10): pts.append((x,random.randint(0,jag)))
    for y in range(0,h+1,10): pts.append((w-random.randint(0,jag),y))
    for x in range(w,-1,-10): pts.append((x,h-random.randint(0,jag)))
    for y in range(h,-1,-10): pts.append((random.randint(0,jag),y))
    ImageDraw.Draw(m).polygon(pts,fill=255); img=img.convert("RGBA"); img.putalpha(m); return img
def paper(size,base=(244,236,214)):
    im=Image.new("RGB",size,base); n=Image.effect_noise(size,40).convert("RGB"); return Image.blend(im,n,0.07)
def drop(bg, fg, pos, off=(16,22), blur=22, op=200):
    a=fg.split()[3]; pad=blur*3
    sh=Image.new("RGBA",(fg.size[0]+2*pad,fg.size[1]+2*pad),(0,0,0,0))
    s=Image.new("RGBA",fg.size,(0,0,0,255)); s.putalpha(a.point(lambda p:p*op//255)); sh.paste(s,(pad,pad))
    bg.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)),(pos[0]-pad+off[0],pos[1]-pad+off[1]))
    bg.alpha_composite(fg,pos)
def arrow(d, p0, p1, col=RED, w=22):
    d.line([p0,p1],fill=BLK,width=w+12); 
    ang=math.atan2(p1[1]-p0[1],p1[0]-p0[0]); L=70
    tip=(p1[0]+math.cos(ang)*40,p1[1]+math.sin(ang)*40)
    a=(p1[0]+math.cos(ang+2.5)*L*0.2,p1[1]+math.sin(ang+2.5)*L*0.2)
    pts=[tip,(p1[0]+math.cos(ang+2.4)*L,p1[1]+math.sin(ang+2.4)*L),(p1[0]+math.cos(ang-2.4)*L,p1[1]+math.sin(ang-2.4)*L)]
    d.polygon(pts,fill=BLK,outline=BLK,width=10)
    d.line([p0,p1],fill=col,width=w); d.polygon(pts,fill=col)

# ---- V1: the scrap under a spotlight, "IT MEANS 'THE END'" ----
def v1():
    bg=radial((W,H),(860,380),420,(120,70,30),(8,6,10)).convert("RGBA")
    sc=paper((640,250)); d=ImageDraw.Draw(sc)
    f=TYPE(150)
    while f.getlength("Tamám Shud")>580: f=TYPE(f.size-4)
    d.text((320,128),"Tamám Shud",font=f,fill=(15,12,12),anchor="mm")
    sc=torn(sc).rotate(-6,expand=True,resample=Image.BICUBIC)
    # warm light glow behind
    halo=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(halo).ellipse([520,150,1220,620],fill=(255,190,90,120))
    bg.alpha_composite(halo.filter(ImageFilter.GaussianBlur(90)))
    drop(bg,sc,(540,220),off=(20,30),blur=26,op=230)
    d=ImageDraw.Draw(bg)
    # red circle around the scrap
    c=Image.new("RGBA",(W,H),(0,0,0,0)); dc=ImageDraw.Draw(c)
    dc.ellipse([505,175,1225,560],outline=(0,0,0,255),width=26); dc.ellipse([505,175,1225,560],outline=RED+(255,),width=14)
    bg.alpha_composite(c.rotate(-5,center=(865,368),resample=Image.BICUBIC))
    bb=big_text(bg,"IT MEANS",(40,70),170,WHITE,maxw=480)
    big_text(bg,"\"THE END\"",(40,bb[3]+10),190,YEL,maxw=500)
    return bg

# ---- V2: the code, glowing, "75 YEARS UNCRACKED" ----
def v2():
    bg=radial((W,H),(820,360),460,(40,10,12),(4,3,6)).convert("RGBA")
    lay=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(lay)
    lines=["WRGOABABD","MLIAOI","WTBIMPANETP","MLIABOAIAQC","ITTMTSAMSTGAB"]
    y=40
    for i,l in enumerate(lines):
        f=HAND(96)
        while f.getlength(l)>580: f=HAND(f.size-2)
        d.text((660+(i%2)*14,y),l,font=f,fill=(255,70,60,255)); y+=132
    glow(bg,lay,radius=22,strength=2.2)
    # dark fade on left for text
    fade=Image.linear_gradient("L").rotate(90).resize((W,H)); fade=fade.point(lambda p: max(0,min(255,int((p-95)*5))))
    bg.alpha_composite(Image.composite(Image.new("RGBA",(W,H),(0,0,0,0)),Image.new("RGBA",(W,H),(0,0,0,235)),fade))
    c=Image.new("RGBA",(W,H),(0,0,0,0)); dc=ImageDraw.Draw(c)
    dc.ellipse([630,20,1260,185],outline=(0,0,0,255),width=24); dc.ellipse([630,20,1260,185],outline=YEL+(255,),width=12)
    bg.alpha_composite(c.rotate(-3,center=(945,102),resample=Image.BICUBIC))
    bb=big_text(bg,"NOBODY",(40,150),210,WHITE,maxw=560)
    big_text(bg,"CRACKED IT",(40,bb[3]+4),210,YEL,maxw=580)
    d=ImageDraw.Draw(bg); arrow(d,(470,140),(600,110),col=YEL)
    return bg

# ---- V3: the suitcase, labels cut out ----
def suitcase():
    s=Image.new("RGBA",(620,460),(0,0,0,0)); d=ImageDraw.Draw(s)
    d.rounded_rectangle([200,0,420,90],radius=30,outline=(40,24,14,255),width=26)   # handle
    body=Image.new("RGB",(620,380),(130,72,34))
    shade=Image.linear_gradient("L").resize((620,380))
    body=Image.composite(Image.new("RGB",(620,380),(60,32,14)),body,shade.point(lambda p:int(p*0.7)))
    m=Image.new("L",(620,380),0); ImageDraw.Draw(m).rounded_rectangle([0,0,619,379],radius=40,fill=255)
    s.paste(body,(0,70),m); d=ImageDraw.Draw(s)
    d.rounded_rectangle([0,70,619,449],radius=40,outline=(30,16,8,255),width=8)
    d.line([(0,150),(619,150)],fill=(40,22,10,255),width=8)
    for x in (150,470):
        d.rectangle([x-24,70,x+24,449],fill=(70,40,18,255)); d.rectangle([x-30,190,x+30,240],fill=(200,170,90,255),outline=(60,40,10,255),width=4)
    # cut label rectangles: pale patches with ragged edges + dashed cut lines
    for (x,y,w,h) in [(230,250,170,110),(40,300,90,70)]:
        d.rectangle([x,y,x+w,y+h],fill=(176,120,70,255))
        for k in range(x,x+w,18): d.line([(k,y),(k+10,y)],fill=WHITE+(255,),width=5); d.line([(k,y+h),(k+10,y+h)],fill=WHITE+(255,),width=5)
        for k in range(y,y+h,18): d.line([(x,k),(x,k+10)],fill=WHITE+(255,),width=5); d.line([(x+w,k),(x+w,k+10)],fill=WHITE+(255,),width=5)
    return s
def v3():
    bg=radial((W,H),(900,420),430,(30,60,90),(3,6,12)).convert("RGBA")
    beam=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(beam).polygon([(820,-20),(990,-20),(1240,720),(560,720)],fill=(200,230,255,55))
    bg.alpha_composite(beam.filter(ImageFilter.GaussianBlur(30)))
    sc=suitcase().rotate(4,expand=True,resample=Image.BICUBIC)
    drop(bg,sc,(640,190),off=(10,40),blur=30,op=220)
    # scissors cue: red X cuts / tag
    bb=big_text(bg,"EVERY LABEL",(40,150),200,WHITE,maxw=560)
    big_text(bg,"CUT OUT",(40,bb[3]+4),250,YEL,maxw=560)
    d=ImageDraw.Draw(bg); arrow(d,(560,560),(800,520))
    return bg

out="./"
import os; os.makedirs(out,exist_ok=True)
for n,fn in [("ep1_thumb2_A_theend",v1),("ep1_thumb2_B_code",v2),("ep1_thumb2_C_suitcase",v3)]:
    im=grain(fn().convert("RGB"),0.04); im.save(out+n+".png",optimize=True)
    im.resize((246,138),Image.LANCZOS).save("s_"+n+".png")
# contact sheet at mobile size
sheet=Image.new("RGB",(246*3+40,158),(30,30,30))
for i,n in enumerate(["ep1_thumb2_A_theend","ep1_thumb2_B_code","ep1_thumb2_C_suitcase"]):
    sheet.paste(Image.open("s_"+n+".png"),(10+i*256,10))
sheet.save("sheet.png"); print("ok")
