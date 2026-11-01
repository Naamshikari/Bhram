import random, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
W,H=1280,720
F="fonts/"  # Anton, Special Elite, Permanent Marker (Google Fonts)
def font(n,s): return ImageFont.truetype(F+n,s)
ANTON=lambda s:font("Anton-Regular.ttf",s)
TYPE=lambda s:font("SpecialElite-Regular.ttf",s)
HAND=lambda s:font("PermanentMarker-Regular.ttf",s)
random.seed(7)

def noise(size, amt, blur=0):
    n=Image.effect_noise(size, amt).convert("L")
    if blur: n=n.filter(ImageFilter.GaussianBlur(blur))
    return n
def paper(size, base, grain=40, mottle=True):
    im=Image.new("RGB",size,base)
    g=noise(size,grain)
    im=Image.blend(im, Image.merge("RGB",[g]*3), 0.08)
    if mottle:
        m=noise((size[0]//16,size[1]//16),80).resize(size,Image.BICUBIC).filter(ImageFilter.GaussianBlur(20))
        dark=Image.new("RGB",size,(60,40,20))
        im=Image.composite(im,Image.blend(im,dark,0.25),m)
    return im
def vignette(im, strength=0.65):
    w,h=im.size
    v=Image.new("L",(w,h),0); d=ImageDraw.Draw(v)
    d.ellipse([-w*0.15,-h*0.25,w*1.15,h*1.25],fill=255)
    v=v.filter(ImageFilter.GaussianBlur(160))
    black=Image.new("RGB",(w,h),(10,8,6))
    return Image.composite(im, Image.blend(im,black,strength), v)
def shadow_paste(bg, fg, pos, angle=0, off=(10,14), blur=14, op=150):
    fg=fg.convert("RGBA")
    if angle: fg=fg.rotate(angle, expand=True, resample=Image.BICUBIC)
    a=fg.split()[3]
    sh=Image.new("RGBA",fg.size,(0,0,0,0)); sh.putalpha(a.point(lambda p:p*op//255))
    pad=blur*3
    shc=Image.new("RGBA",(fg.size[0]+pad*2,fg.size[1]+pad*2),(0,0,0,0)); shc.paste(sh,(pad,pad))
    shc=shc.filter(ImageFilter.GaussianBlur(blur))
    bg.alpha_composite(shc,(pos[0]-pad+off[0],pos[1]-pad+off[1]))
    bg.alpha_composite(fg,pos)
def torn(img, jag=10):
    w,h=img.size
    m=Image.new("L",(w,h),0); d=ImageDraw.Draw(m)
    pts=[]
    for x in range(0,w+1,8): pts.append((x,random.randint(0,jag)))
    for y in range(0,h+1,8): pts.append((w-random.randint(0,jag),y))
    for x in range(w,-1,-8): pts.append((x,h-random.randint(0,jag)))
    for y in range(h,-1,-8): pts.append((random.randint(0,jag),y))
    d.polygon(pts,fill=255)
    img=img.convert("RGBA"); img.putalpha(m); return img
def stroke_text(d, xy, txt, f, fill, sw=0, sf=(0,0,0), anchor="la"):
    d.text(xy, txt, font=f, fill=fill, stroke_width=sw, stroke_fill=sf, anchor=anchor)
def fit(txt, fn, maxw, start):
    s=start
    while fn(s).getlength(txt)>maxw: s-=2
    return fn(s)
def stamp(text, size, color=(170,25,25), angle=-12, border=True):
    f=ANTON(size)
    tw=int(f.getlength(text)); th=int(size*1.25)
    im=Image.new("RGBA",(tw+60,th+40),(0,0,0,0)); d=ImageDraw.Draw(im)
    if border: d.rounded_rectangle([6,6,tw+54,th+34],radius=10,outline=color+(255,),width=7)
    d.text((30,14),text,font=f,fill=color+(255,))
    # ink wear
    n=noise(im.size,120).point(lambda p:255 if p>95 else 0).filter(ImageFilter.GaussianBlur(0.6))
    a=ImageChops.multiply(im.split()[3],n)
    im.putalpha(a.point(lambda p:int(p*0.88)))
    return im.rotate(angle,expand=True,resample=Image.BICUBIC)
def headline_block(bg, lines, x, y, sizes, colors, maxw, gap=0, bar=None):
    d=ImageDraw.Draw(bg)
    for t,s,c in zip(lines,sizes,colors):
        f=fit(t,ANTON,maxw,s)
        bb=d.textbbox((x,y),t,font=f)
        if bar and c==bar[0]:
            d.rectangle([bb[0]-14,bb[1]-10,bb[2]+14,bb[3]+12],fill=bar[1])
            d.text((x,y),t,font=f,fill=c)
        else:
            d.text((x+5,y+6),t,font=f,fill=(0,0,0,200))
            d.text((x,y),t,font=f,fill=c,stroke_width=3,stroke_fill=(15,10,8))
        y=bb[3]+gap+18
    return y

INK=(28,24,30); RED=(178,28,28); CREAM=(244,234,210); YEL=(250,214,70)

# ---------- Variant A: the scrap ----------
def variant_a():
    bg=paper((W,H),(126,92,58),50).convert("RGBA")   # dark kraft desk
    bg=vignette(bg.convert("RGB"),0.7).convert("RGBA")
    # ruled index card behind
    card=paper((520,340),(236,226,200),30,False); dc=ImageDraw.Draw(card)
    for yy in range(70,340,32): dc.line([(0,yy),(520,yy)],fill=(150,175,205),width=2)
    dc.line([(0,48),(520,48)],fill=(200,80,80),width=2)
    dc.text((24,12),"EXHIBIT C  ·  ADELAIDE  ·  1948",font=TYPE(26),fill=INK)
    dc.text((24,80),"Found sewn in a hidden",font=TYPE(28),fill=(60,55,60))
    dc.text((24,112),"fob pocket of the trousers.",font=TYPE(28),fill=(60,55,60))
    shadow_paste(bg,card,(700,330),angle=6)
    # the scrap: torn printed paper with TAMAM SHUD
    scrap=paper((640,220),(240,232,212),25,False); ds=ImageDraw.Draw(scrap)
    f=fit("Tamám Shud",lambda s:font("../fonts/SpecialElite-Regular.ttf",s) if False else TYPE(s),570,170)
    ds.text((320,112),"Tamám Shud",font=f,fill=(20,18,18),anchor="mm")
    scrap=scrap.filter(ImageFilter.GaussianBlur(0.4))
    shadow_paste(bg,torn(scrap,14),(600,110),angle=-5,off=(14,18),blur=18,op=170)
    # evidence tag
    tag=Image.new("RGBA",(260,120),(0,0,0,0)); dt=ImageDraw.Draw(tag)
    dt.polygon([(30,0),(260,0),(260,120),(30,120),(0,60)],fill=(214,190,120,255))
    dt.ellipse([16,50,36,70],fill=(126,92,58,255))
    dt.text((60,16),"EVIDENCE",font=ANTON(36),fill=RED)
    dt.text((60,66),"NO. 48 / 1",font=TYPE(30),fill=INK)
    shadow_paste(bg,tag,(990,560),angle=14)
    # headline left
    d=ImageDraw.Draw(bg)
    y=headline_block(bg,["2 WORDS.","NO NAME."],48,70,[180,180],[CREAM,YEL],500)
    sub="A dead man's last clue"
    d.text((54,y+6),sub,font=TYPE(40),fill=CREAM)
    # red arrow to scrap
    d.line([(500,y+28),(610,y+28),(640,330)],fill=RED,width=9,joint="curve")
    d.polygon([(640,318),(624,350),(660,344)],fill=RED)
    return bg

# ---------- Variant B: the code ----------
def variant_b():
    bg=paper((W,H),(232,222,196),35).convert("RGB")
    bg=vignette(bg,0.55).convert("RGBA")
    # book page
    page=paper((620,600),(246,240,224),20,False); dp=ImageDraw.Draw(page)
    code=["WRGOABABD","MLIAOI","WTBIMPANETP","MLIABOAIAQC"]
    yy=60
    for i,l in enumerate(code):
        f=fit(l,HAND,560,78)
        dp.text((30+ (i%2)*8,yy),l,font=f,fill=(40,40,70))
        yy+=104
    page=page.filter(ImageFilter.GaussianBlur(0.5))
    shadow_paste(bg,page,(620,50),angle=3,off=(14,18),blur=20,op=150)
    d=ImageDraw.Draw(bg)
    # red circle around first line
    cl=Image.new("RGBA",(W,H),(0,0,0,0)); dcl=ImageDraw.Draw(cl)
    for k in range(3):
        dcl.ellipse([640+k*3,118+k*2,1175-k*2,250-k*3],outline=RED+(235,),width=6)
    cl=cl.rotate(-3,center=(905,184),resample=Image.BICUBIC)
    bg.alpha_composite(cl)
    # tape
    tape=Image.new("RGBA",(200,56),(235,225,170,170)); shadow_paste(bg,tape,(820,24),angle=-8,off=(2,3),blur=4,op=60)
    # dark headline panel
    panel=Image.new("RGBA",(620,H),(20,17,16,240))
    bg.alpha_composite(panel,(0,0))
    y=headline_block(bg,["NOBODY","CAN READ","THIS."],50,50,[175,175,175],[CREAM,CREAM,YEL],520,gap=-8)
    d.text((56,y+4),"Found in a dead man's book · 1948",font=TYPE(30),fill=(220,205,175))
    st=stamp("UNSOLVED",70,angle=-8); bg.alpha_composite(st,(860,500))
    return bg

# ---------- Variant C: the case file ----------
def variant_c():
    bg=paper((W,H),(48,40,36),40).convert("RGB")
    bg=vignette(bg,0.5).convert("RGBA")
    # manila folder
    fol=Image.new("RGBA",(760,600),(0,0,0,0)); df=ImageDraw.Draw(fol)
    df.rounded_rectangle([0,40,760,600],radius=14,fill=(214,180,112,255))
    df.rounded_rectangle([40,0,300,70],radius=12,fill=(214,180,112,255))
    tex=paper((760,600),(214,180,112),35); tex=tex.convert("RGBA"); tex.putalpha(fol.split()[3]); fol=tex
    df=ImageDraw.Draw(fol)
    df.text((62,14),"CASE  1948 / SA",font=TYPE(30),fill=INK)
    # typed label
    lab=paper((520,150),(246,240,224),20,False); dl=ImageDraw.Draw(lab)
    dl.text((20,14),"SUBJECT:",font=TYPE(30),fill=INK)
    dl.text((20,58),"UNKNOWN MALE",font=TYPE(54),fill=INK)
    dl.text((20,114),"Somerton Beach, 1 Dec 1948",font=TYPE(24),fill=(80,70,70))
    fol.alpha_composite(lab.convert("RGBA"),(60,120))
    # paperclipped scrap
    sc=paper((300,90),(240,232,212),20,False); ImageDraw.Draw(sc).text((150,46),"Tamám Shud",font=TYPE(48),fill=INK,anchor="mm")
    sc=torn(sc,8).rotate(-7,expand=True,resample=Image.BICUBIC)
    fol.alpha_composite(sc,(400,330))
    df=ImageDraw.Draw(fol)
    df.rounded_rectangle([600,312,626,382],radius=12,outline=(150,150,155,255),width=5)
    # string line
    st=stamp("UNIDENTIFIED",78,angle=-14); fol.alpha_composite(st,(40,330))
    shadow_paste(bg,fol,(520,70),angle=-4,off=(16,20),blur=22,op=190)
    d=ImageDraw.Draw(bg)
    y=headline_block(bg,["WHO","WAS HE?"],46,90,[230,200],[CREAM,YEL],560,gap=-14)
    d.text((52,y+10),"No name. No cause. No one came.",font=TYPE(32),fill=CREAM)
    # red pin + string
    return bg

out="./"
for name,fn in [("ep1_thumb_A_scrap",variant_a),("ep1_thumb_B_code",variant_b),("ep1_thumb_C_casefile",variant_c)]:
    im=fn().convert("RGB"); assert im.size==(W,H)
    im.save(out+name+".png",optimize=True)
    im.resize((320,180),Image.LANCZOS).save("small_"+name+".png")
print("done")
