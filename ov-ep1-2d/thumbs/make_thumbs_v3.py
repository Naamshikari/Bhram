import random, math, sys

from PIL import Image, ImageDraw, ImageFont, ImageFilter
exec(open("make_thumbs_v2.py").read().split("# ---- V1")[0])
MUKTA=lambda s:ImageFont.truetype(F+"Mukta-ExtraBold.ttf",s)
def htext(bg, txt, xy, size, fill, maxw, stroke=10):
    f=MUKTA(size)
    while f.getlength(txt)>maxw: size-=4; f=MUKTA(size)
    s=Image.new("RGBA",bg.size,(0,0,0,0)); ImageDraw.Draw(s).text((xy[0]+8,xy[1]+12),txt,font=f,fill=(0,0,0,230),stroke_width=stroke,stroke_fill=(0,0,0,230))
    bg.alpha_composite(s.filter(ImageFilter.GaussianBlur(8)))
    d=ImageDraw.Draw(bg); d.text(xy,txt,font=f,fill=fill,stroke_width=stroke,stroke_fill=BLK)
    return d.textbbox(xy,txt,font=f,stroke_width=stroke)
def badge(bg, txt, xy, angle=-8, col=RED, size=64):
    f=ANTON(size); w=int(f.getlength(txt))+50; h=int(size*1.45)
    b=Image.new("RGBA",(w+20,h+20),(0,0,0,0)); d=ImageDraw.Draw(b)
    d.rounded_rectangle([6,6,w+6,h+6],radius=14,fill=BLK); d.rounded_rectangle([0,0,w,h],radius=14,fill=col,outline=BLK,width=6)
    d.text((w//2,h//2),txt,font=f,fill=WHITE,anchor="mm")
    b=b.rotate(angle,expand=True,resample=Image.BICUBIC); bg.alpha_composite(b,xy)
def code_page(w=600,h=640, n=5):
    p=paper((w,h),(240,230,205)); d=ImageDraw.Draw(p)
    # light falloff for depth
    p=Image.composite(p,Image.blend(p,Image.new("RGB",p.size,(70,50,30)),0.5),radial((w,h),(w//2,h//3),w*0.7,(255,255,255),(0,0,0)).convert("L"))
    d=ImageDraw.Draw(p); y=40
    for i,l in enumerate(["WRGOABABD","MLIAOI","WTBIMPANETP","MLIABOAIAQC","ITTMTSAMSTGAB"][:n]):
        f=HAND(100)
        while f.getlength(l)>w-70: f=HAND(f.size-2)
        d.text((30+(i%2)*10,y),l,font=f,fill=(25,25,60)); y+=(h-60)//n
    return p.convert("RGBA")
def hot_bg(c1,c2,center):
    bg=radial((W,H),center,520,c1,c2).convert("RGBA")
    rays=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(rays)
    for k in range(0,360,15):
        a=math.radians(k); a2=math.radians(k+6)
        d.polygon([center,(center[0]+2000*math.cos(a),center[1]+2000*math.sin(a)),(center[0]+2000*math.cos(a2),center[1]+2000*math.sin(a2))],fill=(255,255,255,18))
    bg.alpha_composite(rays.filter(ImageFilter.GaussianBlur(6)))
    return bg
def circle(bg, box, col=RED, angle=-4):
    c=Image.new("RGBA",(W,H),(0,0,0,0)); dc=ImageDraw.Draw(c)
    dc.ellipse(box,outline=BLK+(255,),width=28); dc.ellipse(box,outline=col+(255,),width=15)
    cx=(box[0]+box[2])//2; cy=(box[1]+box[3])//2
    bg.alpha_composite(c.rotate(angle,center=(cx,cy),resample=Image.BICUBIC))

# A: challenge — CAN YOU READ THIS?
def a():
    bg=hot_bg((150,20,20),(10,4,6),(900,360))
    pg=code_page().rotate(5,expand=True,resample=Image.BICUBIC)
    drop(bg,pg,(650,40),off=(20,30),blur=28,op=240)
    circle(bg,[630,95,1275,250],YEL,angle=5)
    bb=big_text(bg,"CAN YOU",(36,110),190,WHITE,maxw=560)
    big_text(bg,"READ THIS?",(36,bb[3]+4),190,YEL,maxw=600)
    d=ImageDraw.Draw(bg); arrow(d,(420,90),(600,150),col=YEL)
    badge(bg,"75+ YEARS UNSOLVED",(40,560),angle=-4,size=58)
    return bg

# B: hidden pocket
def fabric(size):
    w,h=size; base=Image.new("RGB",size,(38,40,48)); d=ImageDraw.Draw(base)
    for k in range(-h,w,9): d.line([(k,0),(k+h,h)],fill=(52,54,64),width=3)
    n=Image.effect_noise(size,50).convert("RGB"); base=Image.blend(base,n,0.08)
    return base
def b():
    bg=fabric((W,H)).convert("RGBA")
    light=radial((W,H),(880,380),430,(255,200,120),(0,0,0)).convert("L").point(lambda p:p)
    warm=Image.new("RGBA",(W,H),(255,170,80,0)); warm.putalpha(light.point(lambda p:int(p*0.35)))
    bg.alpha_composite(warm)
    dark=Image.new("RGBA",(W,H),(0,0,0,0)); dark.putalpha(light.point(lambda p:int((255-p)*0.75))); bg.alpha_composite(dark)
    d=ImageDraw.Draw(bg)
    # pocket slit with stitches
    d.rounded_rectangle([640,400,1180,440],radius=20,fill=(8,8,12))
    for x in range(640,1180,26): d.line([(x,388),(x+14,388)],fill=(230,200,120),width=4); d.line([(x,456),(x+14,456)],fill=(230,200,120),width=4)
    # scrap emerging from pocket (rolled), lit
    sc=paper((520,170)); ds=ImageDraw.Draw(sc)
    ds.text((260,88),"Tamám Shud",font=TYPE(80),fill=(15,12,12),anchor="mm")
    sc=torn(sc,10).rotate(8,expand=True,resample=Image.BICUBIC)
    halo=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(halo).ellipse([600,120,1220,480],fill=(255,220,140,150))
    bg.alpha_composite(halo.filter(ImageFilter.GaussianBlur(70)))
    crop=Image.new("RGBA",(W,H),(0,0,0,0)); crop.alpha_composite(sc,(650,200))
    m=Image.new("L",(W,H),255); ImageDraw.Draw(m).rectangle([0,420,W,H],fill=0)
    crop.putalpha(Image.composite(crop.split()[3],Image.new("L",(W,H),0),m))
    sh=Image.new("RGBA",(W,H),(0,0,0,0)); sh.putalpha(crop.split()[3].point(lambda p:p*0.8)); bg.alpha_composite(sh.filter(ImageFilter.GaussianBlur(20)),(14,22))
    bg.alpha_composite(crop)
    circle(bg,[610,150,1240,470],RED,angle=-6)
    bb=big_text(bg,"SEWN INTO",(36,120),190,WHITE,maxw=560)
    big_text(bg,"HIS POCKET",(36,bb[3]+4),190,YEL,maxw=580)
    d=ImageDraw.Draw(bg); arrow(d,(470,560),(640,420))
    return bg

# C: Hindi — कोई नहीं पढ़ पाया
def c():
    bg=hot_bg((20,60,140),(3,5,15),(900,360))
    pg=code_page().rotate(-4,expand=True,resample=Image.BICUBIC)
    drop(bg,pg,(660,50),off=(20,30),blur=28,op=240)
    circle(bg,[650,70,1275,240],YEL,angle=-3)
    htext(bg,"ये कोड",(40,-10),150,WHITE,maxw=560)
    htext(bg,"कोई नहीं",(40,175),175,YEL,maxw=580)
    htext(bg,"पढ़ पाया!",(40,395),175,YEL,maxw=580)
    badge(bg,"75+ YEARS",(930,590),angle=-6,size=56)
    return bg

out="./"
names=[("ep1_thumb3_A_canyouread",a),("ep1_thumb3_B_pocket",b),("ep1_thumb3_C_hindi",c)]
sheet=Image.new("RGB",(246*3+40,158),(30,30,30))
for i,(n,fn) in enumerate(names):
    im=grain(fn().convert("RGB"),0.035); im.save(out+n+".png",optimize=True)
    sheet.paste(im.resize((246,138),Image.LANCZOS),(10+i*256,10))
sheet.save("sheet3.png"); print("ok")
