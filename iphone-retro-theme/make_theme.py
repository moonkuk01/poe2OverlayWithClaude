"""컬러 GBA 스타일 아이폰 테마 생성기 (오리지널 픽셀 아트).
실행: python3 make_theme.py  ->  output/ 에 아이콘, 배경화면, 미리보기 생성
직접 구한 이미지를 배경에 넣고 싶다면 custom/ 폴더에 PNG(투명 배경)를 넣으세요.
"""
import os, glob, math, random
from PIL import Image, ImageDraw, ImageFont
from sprites import C as SC, MONSTERS, HERO

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "output")
def rgb(h): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5))

K = rgb("#202830"); WHITE = (255, 255, 255)

def sprite(rows, scale=1):
    rows = [r for r in rows.strip("\n").split("\n")]
    w = max(len(r) for r in rows)
    im = Image.new("RGBA", (w, len(rows)), (0, 0, 0, 0))
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch != ".": im.putpixel((x, y), rgb(SC[ch]) + (255,))
    return im.resize((w*scale, len(rows)*scale), Image.NEAREST) if scale > 1 else im

FONT = ImageFont.load_default_imagefont()

# ======================= 아이콘 (32x32) =======================
def icon_base(c1, c2):
    im = Image.new("RGB", (32, 32), rgb(c1)); d = ImageDraw.Draw(im)
    for y in range(16, 32):           # 아래쪽 디더 그라데이션
        for x in range(32):
            if (x + y) % 2 == 0 or y > 23: d.point((x, y), fill=rgb(c2))
    d.line([(2, 2), (29, 2)], fill=WHITE)   # 상단 하이라이트
    return im, d

def shine(d, pts):
    d.point(pts, fill=WHITE)

def gear_pts(cx, cy, r1, r2, n=8):
    pts = []
    for i in range(n * 2):
        a = math.pi * i / n
        r = r1 if i % 2 == 0 else r2
        for da in (-0.17, 0.17):
            pts.append((cx + r * math.cos(a + da), cy + r * math.sin(a + da)))
    return pts

def ic_phone(d):
    d.rounded_rectangle([6, 18, 25, 26], 3, fill=rgb("#f05048"), outline=K)
    d.rectangle([11, 13, 20, 18], fill=rgb("#f05048"), outline=K)
    d.rounded_rectangle([5, 7, 26, 12], 2, fill=rgb("#b02830"), outline=K)
    for x in (10, 14, 18): d.rectangle([x, 20, x+2, 22], fill=WHITE, outline=K)
    shine(d, [(7, 8), (8, 8), (7, 19)])
def ic_messages(d):
    d.rounded_rectangle([4, 6, 27, 21], 5, fill=WHITE, outline=K)
    d.polygon([(9, 20), (8, 26), (14, 20)], fill=WHITE, outline=K); d.line([(10, 21), (13, 21)], fill=WHITE)
    for x in (9, 15, 21): d.rectangle([x, 12, x+2, 14], fill=rgb("#3878d0"))
def ic_camera(d):
    d.rectangle([10, 7, 17, 10], fill=rgb("#585868"), outline=K)
    d.rounded_rectangle([4, 10, 27, 25], 3, fill=rgb("#686878"), outline=K)
    d.rectangle([5, 11, 26, 13], fill=rgb("#9898a8"))
    d.ellipse([10, 12, 21, 23], fill=rgb("#202830"), outline=K)
    d.ellipse([12, 14, 19, 21], fill=rgb("#3878d0")); shine(d, [(14, 15), (15, 15), (14, 16)])
    d.rectangle([22, 12, 24, 13], fill=rgb("#f8d040"))
def ic_photos(d):
    d.rectangle([5, 5, 26, 27], fill=WHITE, outline=K)
    d.rectangle([7, 7, 24, 21], fill=rgb("#a8e0ff"))
    d.polygon([(7, 21), (13, 12), (18, 18), (21, 15), (24, 19), (24, 21)], fill=rgb("#58c058"))
    d.line([(7, 21), (13, 12), (18, 18)], fill=rgb("#307830"))
    d.ellipse([18, 8, 22, 12], fill=rgb("#f8d040"))
def ic_settings(d):
    d.polygon(gear_pts(15.5, 15.5, 12, 9), fill=rgb("#a8a8b8"), outline=K)
    d.ellipse([9, 9, 22, 22], fill=rgb("#c8c8d8"), outline=K)
    d.ellipse([13, 13, 18, 18], fill=rgb("#585868"), outline=K); shine(d, [(11, 11), (12, 11), (11, 12)])
def ic_safari(d):
    d.ellipse([4, 4, 27, 27], fill=rgb("#f8d040"), outline=K)
    d.ellipse([7, 7, 24, 24], fill=WHITE, outline=rgb("#c89820"))
    d.polygon([(15, 8), (18, 15), (15, 15)], fill=rgb("#f05048")); d.polygon([(16, 23), (13, 16), (16, 16)], fill=rgb("#3858a8"))
    d.point((15, 15), fill=K); shine(d, [(8, 9), (9, 8)])
def ic_mail(d):
    d.rectangle([4, 8, 27, 24], fill=rgb("#fff0d0"), outline=K)
    d.line([(4, 8), (15, 17), (16, 17), (27, 8)], fill=K)
    d.ellipse([12, 14, 19, 21], fill=rgb("#f05048"), outline=rgb("#b02830"))
    shine(d, [(14, 16)])
def ic_music(d):
    d.polygon([(11, 6), (25, 3), (25, 8), (11, 11)], fill=rgb("#a070d8"), outline=K)
    d.rectangle([11, 9, 12, 22], fill=K); d.rectangle([24, 6, 25, 19], fill=K)
    d.ellipse([5, 19, 12, 25], fill=rgb("#a070d8"), outline=K); d.ellipse([18, 16, 25, 22], fill=rgb("#a070d8"), outline=K)
    shine(d, [(7, 20), (20, 17)])
def ic_maps(d):
    d.polygon([(4, 8), (11, 5), (20, 8), (27, 5), (27, 24), (20, 27), (11, 24), (4, 27)], fill=rgb("#f8e0a0"), outline=K)
    d.line([(11, 5), (11, 24)], fill=rgb("#c8a868")); d.line([(20, 8), (20, 27)], fill=rgb("#c8a868"))
    for i in range(0, 8, 2): d.point((7 + i, 20 - i), fill=rgb("#b02830"))
    d.line([(17, 10), (21, 14)], fill=rgb("#f05048"), width=2); d.line([(21, 10), (17, 14)], fill=rgb("#f05048"), width=2)
def ic_calendar(d):
    d.rectangle([5, 7, 26, 26], fill=WHITE, outline=K); d.rectangle([5, 7, 26, 12], fill=rgb("#f05048"), outline=K)
    for x in (9, 21): d.rectangle([x, 4, x+1, 9], fill=K)
    for yy in (15, 19, 23):
        for xx in range(8, 25, 4): d.rectangle([xx, yy, xx+1, yy+1], fill=rgb("#585868"))
    d.rectangle([16, 19, 17, 20], fill=rgb("#f05048"))
def ic_clock(d):
    d.ellipse([4, 4, 27, 27], fill=rgb("#f05048"), outline=K); d.ellipse([7, 7, 24, 24], fill=WHITE, outline=K)
    d.line([(15, 9), (15, 16)], fill=K, width=2); d.line([(15, 16), (20, 16)], fill=K, width=2)
    for p in [(15, 8), (23, 15), (15, 23), (8, 15)]: d.point(p, fill=rgb("#585868"))
    shine(d, [(7, 10), (8, 8)])
def ic_weather(d):
    for i in range(8):
        a = math.pi * i / 4; d.line([(11 + 8*math.cos(a), 11 + 8*math.sin(a)), (11 + 10*math.cos(a), 11 + 10*math.sin(a))], fill=rgb("#f89838"))
    d.ellipse([5, 5, 17, 17], fill=rgb("#f8d040"), outline=rgb("#c86018"))
    d.ellipse([10, 15, 20, 25], fill=WHITE, outline=K); d.ellipse([16, 12, 27, 23], fill=WHITE, outline=K)
    d.rectangle([12, 20, 25, 25], fill=WHITE); d.line([(13, 25), (24, 25)], fill=K)
def ic_notes(d):
    d.rectangle([7, 5, 24, 27], fill=rgb("#fff0d0"), outline=K)
    d.rectangle([7, 5, 24, 8], fill=rgb("#f8d040"), outline=K)
    for yy in range(12, 25, 3): d.line([(10, yy), (21, yy)], fill=rgb("#a8a8b8"))
    d.line([(10, 12), (18, 12)], fill=rgb("#3858a8")); d.line([(10, 15), (20, 15)], fill=rgb("#3858a8"))
def ic_appstore(d):
    d.arc([10, 4, 21, 15], 180, 360, fill=K, width=2)
    d.polygon([(5, 10), (26, 10), (24, 27), (7, 27)], fill=rgb("#58b0f8"), outline=K)
    d.polygon([(6, 10), (25, 10), (25, 13), (6, 13)], fill=rgb("#b8e8ff"))
    d.polygon([(15, 15), (17, 19), (21, 19), (18, 22), (19, 26), (15, 23), (12, 26), (13, 22), (10, 19), (14, 19)], fill=rgb("#f8d040"), outline=K)
def ic_games(d):
    d.rounded_rectangle([8, 3, 23, 28], 3, fill=rgb("#d8d8e0"), outline=K)
    d.rectangle([10, 5, 21, 14], fill=rgb("#585868")); d.rectangle([11, 6, 20, 13], fill=rgb("#9bbc0f"))
    d.rectangle([11, 18, 15, 19], fill=K); d.rectangle([12, 17, 13, 21], fill=K)
    d.ellipse([18, 17, 20, 19], fill=rgb("#b02830")); d.ellipse([16, 20, 18, 22], fill=rgb("#b02830"))
    d.line([(12, 25), (14, 25)], fill=rgb("#585868")); d.line([(17, 25), (19, 25)], fill=rgb("#585868"))
def ic_health(d):
    d.rectangle([13, 4, 18, 8], fill=rgb("#c8a868"), outline=K)
    d.ellipse([6, 9, 25, 28], fill=rgb("#b8e8ff"), outline=K)
    d.chord([7, 10, 24, 27], 10, 170, fill=rgb("#f05048"))
    d.polygon([(11, 16), (13, 14), (15, 16), (17, 14), (19, 16), (15, 21)], fill=WHITE)
    shine(d, [(10, 13), (10, 14), (11, 12)])

ICONS = {  # 이름: (그리기 함수, 배경색, 아래쪽 배경색)
 "phone": (ic_phone, "#78d878", "#58b058"), "messages": (ic_messages, "#68b8f8", "#4890d8"),
 "camera": (ic_camera, "#f8c8a0", "#e0a070"), "photos": (ic_photos, "#f8a8c8", "#e080a8"),
 "settings": (ic_settings, "#b8b8c8", "#9090a8"), "safari": (ic_safari, "#88d0f8", "#58a8e0"),
 "mail": (ic_mail, "#f89878", "#e07058"), "music": (ic_music, "#f8b8e8", "#e090d0"),
 "maps": (ic_maps, "#98d878", "#70b858"), "calendar": (ic_calendar, "#f8e8b8", "#e8c888"),
 "clock": (ic_clock, "#f8d878", "#e8b850"), "weather": (ic_weather, "#78c8f8", "#50a0e0"),
 "notes": (ic_notes, "#c8e898", "#a0c870"), "appstore": (ic_appstore, "#f8a878", "#e08050"),
 "games": (ic_games, "#b898e8", "#9070d0"), "health": (ic_health, "#f8e0e8", "#f0b8c8"),
}

def make_icon(name, size=512):
    fn, c1, c2 = ICONS[name]
    im, d = icon_base(c1, c2); fn(d)
    return im.resize((size, size), Image.NEAREST)

# ======================= 배경화면 (215x466 -> x6) =======================
W, H, S = 215, 466, 6
P = {k: rgb(v) for k, v in {
 "g1": "#88d070", "g2": "#70b858", "g3": "#509838", "t1": "#58a840", "t2": "#387828", "t3": "#205020",
 "path": "#f0d8a0", "path2": "#d8b878", "w1": "#68a8f8", "w2": "#4880d8", "w3": "#b8e0ff",
 "roof": "#e05848", "roof2": "#a83030", "wall": "#f8f0e0", "wall2": "#d0c8b8", "win": "#88c8f8",
 "trunk": "#906038", "sky1": "#88c8f8", "sky2": "#b8e0ff", "sky3": "#e0f4ff"}.items()}

def tree(d, x, y):
    d.rectangle([x+6, y+12, x+9, y+17], fill=P["trunk"], outline=K)
    d.ellipse([x, y, x+15, y+14], fill=P["t2"], outline=K)
    d.ellipse([x+2, y+1, x+12, y+9], fill=P["t1"])
    d.point([(x+4, y+3), (x+5, y+3), (x+4, y+4), (x+9, y+4)], fill=P["g1"])

def house(d, x, y):
    d.rectangle([x+4, y+16, x+44, y+42], fill=P["wall"], outline=K)
    d.rectangle([x+5, y+36, x+43, y+41], fill=P["wall2"])
    d.polygon([(x-2, y+18), (x+8, y), (x+40, y), (x+50, y+18)], fill=P["roof"], outline=K)
    for i in range(4, 18, 4): d.line([(x+8 - i*0.5, y+i), (x+40 + i*0.5, y+i)], fill=P["roof2"])
    d.rectangle([x+20, y+28, x+28, y+42], fill=P["trunk"], outline=K)
    for wx in (x+8, x+33):
        d.rectangle([wx, y+23, wx+7, y+30], fill=P["win"], outline=K); d.point((wx+2, y+25), fill=WHITE)

def pond(d, x, y, w, h):
    d.rounded_rectangle([x-2, y-2, x+w+2, y+h+2], 10, fill=P["path2"])
    d.rounded_rectangle([x, y, x+w, y+h], 9, fill=P["w1"], outline=P["w2"])
    rnd = random.Random(3)
    for _ in range(7):
        rx, ry = x + rnd.randrange(6, w-8), y + rnd.randrange(4, h-4)
        d.line([(rx, ry), (rx+4, ry)], fill=P["w3"])

def tall_grass(d, x0, y0, w, h):
    for yy in range(y0, y0+h, 7):
        for xx in range(x0, x0+w, 7):
            d.polygon([(xx, yy+7), (xx+2, yy+1), (xx+3, yy+4), (xx+5, yy), (xx+7, yy+7)], fill=P["g3"], outline=P["t3"])
            d.point((xx+3, yy+5), fill=P["t1"])

def flower(d, x, y, c):
    d.point([(x+1, y), (x, y+1), (x+2, y+1), (x+1, y+2)], fill=c); d.point((x+1, y+1), fill=rgb("#f8d040"))

def fence(d, x0, x1, y):
    d.rectangle([x0, y+2, x1, y+3], fill=WHITE, outline=K)
    for xx in range(x0, x1+1, 6): d.rectangle([xx, y, xx+2, y+8], fill=WHITE, outline=K)

def grass_field(im, d, rnd):
    d.rectangle([0, 0, W, H], fill=P["g1"])
    for y in range(0, H, 8):
        for x in range(0, W, 8):
            if (x // 8 + y // 8) % 2: d.point([(x+2, y+3), (x+3, y+2), (x+4, y+3)], fill=P["g2"])
    for _ in range(40):
        flower(d, rnd.randrange(W), rnd.randrange(H), rgb(rnd.choice(["#f85858", "#ffffff", "#f8d040"])))

def path(d, pts, wid=20):
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]): d.line([(x0, y0), (x1, y1)], fill=P["path"], width=wid)
    for (x, y) in pts: d.ellipse([x - wid//2, y - wid//2, x + wid//2, y + wid//2], fill=P["path"])

def paste(im, spr, x, y, shadow=True):
    if shadow:
        ImageDraw.Draw(im).ellipse([x+2, y+spr.height-3, x+spr.width-2, y+spr.height+1], fill=P["g3"])
    im.paste(spr, (x, y), spr)

def custom_sprites():
    """custom/ 폴더의 PNG (사용자가 직접 넣은 이미지)를 불러옴."""
    out = []
    for f in sorted(glob.glob(os.path.join(BASE, "custom", "*.png"))):
        s = Image.open(f).convert("RGBA"); s.thumbnail((28, 28), Image.NEAREST); out.append(s)
    return out

def make_home(seed=11):
    rnd = random.Random(seed)
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
    grass_field(im, d, rnd)
    path(d, [(107, -10), (107, 120), (60, 160), (60, 290), (150, 330), (150, 480)])
    pond(d, 128, 175, 58, 40)
    tall_grass(d, 22, 330, 70, 42); tall_grass(d, 120, 400, 70, 35)
    for y in range(-6, H, 15):
        for x in (-7, 6, W-21, W-8): tree(d, x, y)
    for x in range(20, W-20, 15): tree(d, x, -8)
    house(d, 20, 58); fence(d, 120, 175, 95)
    mons = [sprite(m, 2) for m in MONSTERS.values()] + [c.resize((c.width*2, c.height*2), Image.NEAREST) for c in custom_sprites()]
    spots = [(30, 300), (140, 372), (120, 240), (148, 306), (150, 300), (30, 420)]
    for spr, (x, y) in zip(mons, spots): paste(im, spr, x, y)
    paste(im, sprite(HERO, 2), 47, 250)
    return im.resize((W*S, H*S), Image.NEAREST)

def hp_box(d, x, y, w, name, lv, hp, show_num=False):
    d.rounded_rectangle([x, y, x+w, y+34], 4, fill=rgb("#f8f8e8"), outline=K)
    d.rounded_rectangle([x+2, y+2, x+w-2, y+32], 3, outline=rgb("#c8c8b0"))
    d.fontmode = "1"
    d.text((x+6, y+4), name, fill=K, font=FONT); d.text((x+w-30, y+4), f"Lv{lv}", fill=K, font=FONT)
    d.rounded_rectangle([x+8, y+19, x+w-8, y+25], 2, fill=rgb("#404850"))
    d.text((x+10, y+17), "HP", fill=rgb("#f8d040"), font=FONT)
    bx0, bx1 = x+26, x+w-10
    d.rectangle([bx0, y+21, bx1, y+23], fill=rgb("#506058"))
    d.rectangle([bx0, y+21, bx0 + int((bx1-bx0)*hp), y+23], fill=rgb("#58d058" if hp > .5 else "#f8b830"))

def make_lock(monster="MUSHLING"):
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
    # 하늘 (시계 영역) – 디더 그라데이션
    bands = [(0, "sky1"), (70, "sky2"), (140, "sky3")]
    for i, (y0, c) in enumerate(bands):
        d.rectangle([0, y0, W, H], fill=P[c])
        if i: 
            for y in range(y0 - 8, y0):
                for x in range((y % 2), W, 2): d.point((x, y), fill=P[c])
    for cx, cy in [(30, 40), (150, 95), (90, 130)]:   # 구름
        d.ellipse([cx, cy, cx+26, cy+10], fill=WHITE); d.ellipse([cx+8, cy-5, cx+22, cy+7], fill=WHITE)
    # 들판
    d.rectangle([0, 190, W, H], fill=P["g1"])
    for y in range(190, H, 6):
        for x in range((y // 6 % 2) * 3, W, 6): d.point((x, y), fill=P["g2"])
    d.line([(0, 190), (W, 190)], fill=P["g3"])
    for x in range(-5, W, 13): tree(d, x, 176)
    # 배틀 발판
    d.ellipse([110, 262, 205, 290], fill=P["g3"], outline=P["t3"]); d.ellipse([118, 266, 197, 284], fill=P["g2"])
    d.ellipse([5, 342, 110, 372], fill=P["g3"], outline=P["t3"]); d.ellipse([13, 346, 102, 366], fill=P["g2"])
    enemy = sprite(MONSTERS[monster], 3)
    im.paste(enemy, (158 - enemy.width//2, 275 - enemy.height), enemy)
    hero = sprite(HERO, 3)
    im.paste(hero, (57 - hero.width//2, 357 - hero.height), hero)
    hp_box(d, 8, 212, 92, monster, 5, 1.0)
    hp_box(d, 118, 312, 90, "YOU", 12, 0.62)
    # 대화창
    y = 382
    d.rounded_rectangle([4, y, W-5, y+46], 5, fill=rgb("#384858"), outline=K)
    d.rounded_rectangle([8, y+4, W-9, y+42], 3, fill=rgb("#f8f8f0"), outline=rgb("#e05848"))
    d.fontmode = "1"
    d.text((15, y+11), f"A wild {monster} appeared!", fill=K, font=FONT)
    d.text((15, y+25), "Unlock to RUN or FIGHT...", fill=rgb("#586878"), font=FONT)
    d.polygon([(W-22, y+33), (W-14, y+33), (W-18, y+37)], fill=rgb("#e05848"))
    return im.resize((W*S, H*S), Image.NEAREST)

def make_preview(home, icons, path_out):
    wp = home.resize((645, 1398), Image.NEAREST); d = ImageDraw.Draw(wp)
    sz, gx, x0 = 120, 150, 40
    mask = Image.new("L", (sz, sz)); ImageDraw.Draw(mask).rounded_rectangle([0, 0, sz-1, sz-1], 27, fill=255)
    names = [n for n in ICONS if n not in ("phone", "messages", "safari", "music")]
    for i, k in enumerate(names):
        wp.paste(icons[k].resize((sz, sz), Image.NEAREST), (x0 + (i % 4)*gx, 150 + (i // 4)*175), mask)
    dock = Image.new("RGBA", (605, 170), (0, 0, 0, 0))
    ImageDraw.Draw(dock).rounded_rectangle([0, 0, 604, 169], 50, fill=(255, 255, 255, 110))
    wp.paste(dock, (20, 1190), dock)
    for i, k in enumerate(["phone", "messages", "safari", "music"]):
        wp.paste(icons[k].resize((sz, sz), Image.NEAREST), (x0 + i*gx, 1215), mask)
    wp.save(path_out)

if __name__ == "__main__":
    os.makedirs(os.path.join(OUT, "icons"), exist_ok=True)
    icons = {}
    for n in ICONS:
        icons[n] = make_icon(n); icons[n].save(os.path.join(OUT, "icons", f"{n}.png"))
    home = make_home(); home.save(os.path.join(OUT, "wallpaper_home.png"))
    for m in MONSTERS:
        make_lock(m).save(os.path.join(OUT, f"wallpaper_lock_{m.lower()}.png"))
    make_preview(home, icons, os.path.join(OUT, "preview_home.png"))
    print("done ->", OUT)
