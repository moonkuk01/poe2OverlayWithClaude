"""레트로 휴대용 게임기 풍 아이폰 테마 생성기 (오리지널 픽셀 아트).
실행: python3 make_theme.py  ->  output/ 폴더에 아이콘/배경화면/미리보기 생성
"""
import os, random
from PIL import Image, ImageDraw, ImageFont

PALETTES = {
    "classic": ["#9bbc0f", "#8bac0f", "#306230", "#0f380f"],   # 초록 액정
    "pocket":  ["#e0dbcd", "#a89f94", "#706b66", "#2b2b26"],   # 흑백 액정
}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")

# ---------- 아이콘 (16x16, 0=가장 밝음 ~ 3=가장 어두움) ----------
ICONS = {
"phone": """
0000000000000000
0000000000000000
0003300000000000
0032230000000000
0032230000000000
0032230000000000
0003223000000000
0000322300000000
0000032230000000
0000003223003300
0000000322232230
0000000032222230
0000000003333300
0000000000000000
0000000000000000
0000000000000000""",
"messages": """
0000000000000000
0000000000000000
0333333333333330
0311111111111130
0311111111111130
0311331331331130
0311331331331130
0311111111111130
0311111111111130
0333333333333330
0000003300000000
0000003000000000
0000030000000000
0000000000000000
0000000000000000
0000000000000000""",
"camera": """
0000000000000000
0000000000000000
0000000000000000
0000033333000000
0333332223333330
0322222222221230
0322223333222230
0322232112322230
0322231111322230
0322231111322230
0322223333222230
0322222222222230
0333333333333330
0000000000000000
0000000000000000
0000000000000000""",
"photos": """
0000000000000000
0000000000000000
0333333333333330
0311111111111130
0311111111133130
0311111111133130
0311111111111130
0311111311111130
0311113231111130
0311132223113130
0311322222332230
0313222222222230
0333333333333330
0000000000000000
0000000000000000
0000000000000000""",
"settings": """
0000000000000000
0000000330000000
0000000330000000
0003303333033000
0003333223333000
0000332222330000
0003322112233000
0333221001223330
0333221001223330
0003322112233000
0000332222330000
0003333223333000
0003303333033000
0000000330000000
0000000330000000
0000000000000000""",
"safari": """
0000000000000000
0000033333300000
0000311111130000
0003111311113000
0031111311111300
0031111121111300
0311111222111130
0313112232113130
0311111222111130
0031111121111300
0031111311111300
0003111311113000
0000311111130000
0000033333300000
0000000000000000
0000000000000000""",
"mail": """
0000000000000000
0000000000000000
0000000000000000
0333333333333330
0331111111111330
0313111111113130
0311311111131130
0311133113311130
0311111331111130
0311111111111130
0311111111111130
0333333333333330
0000000000000000
0000000000000000
0000000000000000
0000000000000000""",
"music": """
0000000000000000
0000000000000000
0000000333333300
0000000333333300
0000000300000300
0000000300000300
0000000300000300
0000000300000300
0000000300000300
0000333300033330
0003333300333330
0003333300333330
0000333000033300
0000000000000000
0000000000000000
0000000000000000""",
"maps": """
0000000000000000
0000003333000000
0000032222300000
0000322332230000
0000322332230000
0000032222300000
0000003223000000
0000000330000000
0011111331111100
0122221111222210
0122222112222210
0011111111111100
0000000000000000
0000000000000000
0000000000000000
0000000000000000""",
"calendar": """
0000000000000000
0000300000030000
0333333333333330
0322222222222230
0322222222222230
0311111111111130
0313131313131130
0311111111111130
0313131313131130
0311111111111130
0313131313133130
0311111111111130
0333333333333330
0000000000000000
0000000000000000
0000000000000000""",
"clock": """
0000000000000000
0000033333300000
0000311111130000
0003111311113000
0031111311111300
0031111311111300
0311111311111130
0311111333331130
0311111111111130
0031111111111300
0031111111111300
0003111111113000
0000311111130000
0000033333300000
0000000000000000
0000000000000000""",
"weather": """
0000000000000000
0003000300000000
0000303000000000
0003111300000000
0331111133000000
0003111333330000
0000303111113000
0003033111111300
0000311111111130
0000311111111130
0000033333333300
0000000000000000
0000300300300000
0003003003000000
0000000000000000
0000000000000000""",
"notes": """
0000000000000000
0000000000000000
0003333333333000
0003111111113000
0003133333113000
0003111111113000
0003133331113000
0003111111113000
0003133333313000
0003111111113000
0003133311113000
0003111111113000
0003333333333000
0000000000000000
0000000000000000
0000000000000000""",
"appstore": """
0000000000000000
0000000000000000
0000003333000000
0000032222300000
0000320000230000
0000320000230000
0333333333333330
0322222222222230
0322223333222230
0322223003222230
0322223333222230
0322222222222230
0333333333333330
0000000000000000
0000000000000000
0000000000000000""",
"games": """
0000000000000000
0000000000000000
0000000000000000
0003333333333000
0032222222222300
0322322222232230
0323332222333230
0322322222232230
0322222222222230
0322333223322230
0322222222222230
0032222222222300
0003330000333000
0000000000000000
0000000000000000
0000000000000000""",
"health": """
0000000000000000
0000000000000000
0000000000000000
0003330000333000
0032223003222300
0322122332222230
0321222222222230
0322222222222230
0322222222222230
0032222222222300
0003222222223000
0000322222230000
0000032222300000
0000003223000000
0000000330000000
0000000000000000""",
}

def hexrgb(h): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5))

def render_icon(rows, pal, size=512):
    rows = rows.strip().split("\n")
    im = Image.new("RGB", (16, 16))
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            im.putpixel((x, y), hexrgb(pal[int(c)]))
    # 1px 여백을 둔 18x18 캔버스로 아이콘 중앙 정렬
    canvas = Image.new("RGB", (18, 18), hexrgb(pal[0]))
    canvas.paste(im, (1, 1))
    return canvas.resize((size, size), Image.NEAREST)

# ---------- 배경화면 (215x466 픽셀 -> x6 = 1290x2796) ----------
W, H, S = 215, 466, 6

def draw_tree(d, x, y, P):
    d.ellipse([x+1, y, x+14, y+11], fill=P[2], outline=P[3])
    d.point([(x+4, y+3), (x+5, y+3), (x+4, y+4), (x+9, y+5), (x+10, y+6)], fill=P[1])
    d.rectangle([x+6, y+11, x+9, y+15], fill=P[3])

def draw_house(d, x, y, P):
    d.polygon([(x-2, y+12), (x+20, y), (x+42, y+12)], fill=P[3])
    for i in range(3, 12, 3):
        d.line([(x+20 - i*1.8, y+i), (x+20 + i*1.8, y+i)], fill=P[2])
    d.rectangle([x+2, y+12, x+38, y+34], fill=P[0], outline=P[3])
    d.rectangle([x+17, y+22, x+24, y+34], fill=P[2], outline=P[3])
    for wx in (x+6, x+29):
        d.rectangle([wx, y+17, wx+6, y+23], fill=P[1], outline=P[3])
        d.line([(wx+3, y+17), (wx+3, y+23)], fill=P[3])

def draw_grass_tuft(d, x, y, P, c=1):
    d.point([(x, y), (x+2, y), (x+1, y+1)], fill=P[c])

def draw_tall_grass(d, x0, y0, w, h, P):
    for yy in range(y0, y0+h, 6):
        for xx in range(x0, x0+w, 6):
            d.polygon([(xx, yy+5), (xx+1, yy+1), (xx+2, yy+5)], fill=P[2])
            d.polygon([(xx+3, yy+5), (xx+4, yy), (xx+5, yy+5)], fill=P[3])

def draw_flower(d, x, y, P):
    d.point([(x+1, y), (x, y+1), (x+2, y+1), (x+1, y+2)], fill=P[0])
    d.point((x+1, y+1), fill=P[3])

def draw_fence(d, x0, x1, y, P):
    d.line([(x0, y+2), (x1, y+2)], fill=P[3])
    d.line([(x0, y+5), (x1, y+5)], fill=P[3])
    for xx in range(x0, x1+1, 6):
        d.rectangle([xx, y, xx+1, y+8], fill=P[0], outline=P[3])

def draw_sign(d, x, y, P):
    d.rectangle([x, y, x+14, y+9], fill=P[1], outline=P[3])
    d.line([(x+3, y+3), (x+11, y+3)], fill=P[3]); d.line([(x+3, y+6), (x+9, y+6)], fill=P[3])
    d.rectangle([x+6, y+10, x+8, y+15], fill=P[3])

def draw_pond(d, x, y, w, h, P):
    d.rounded_rectangle([x, y, x+w, y+h], radius=8, fill=P[2], outline=P[3])
    for i in range(6):
        rx = x + 8 + (i * 13) % (w - 14); ry = y + 6 + (i * 7) % (h - 10)
        d.line([(rx, ry), (rx+4, ry)], fill=P[1])

def draw_textbox(d, y, text, P):
    d.rectangle([6, y, W-7, y+44], fill=P[0], outline=P[3])
    d.rectangle([8, y+2, W-9, y+42], outline=P[3])
    d.fontmode = "1"
    font = ImageFont.load_default_imagefont() if hasattr(ImageFont, "load_default_imagefont") else ImageFont.load_default()
    for i, line in enumerate(text.split("\n")):
        d.text((16, y+9 + i*14), line, fill=P[3], font=font)
    d.polygon([(W-22, y+34), (W-14, y+34), (W-18, y+38)], fill=P[3])  # ▼ 다음 표시

def make_wallpaper(pal, lock=False, seed=7):
    P = [hexrgb(c) for c in pal]
    rnd = random.Random(seed)
    im = Image.new("RGB", (W, H), P[1]); d = ImageDraw.Draw(im)
    # 잔디 질감
    for _ in range(420):
        draw_grass_tuft(d, rnd.randrange(W), rnd.randrange(H), P, 2)
    # 굽이진 흙길
    path = [(100, -5), (100, 150), (60, 190), (60, 300), (130, 340), (130, 470)]
    for (x0, y0), (x1, y1) in zip(path, path[1:]):
        d.line([(x0, y0), (x1, y1)], fill=P[0], width=22)
    for (x, y) in path: d.ellipse([x-11, y-11, x+11, y+11], fill=P[0])
    for _ in range(90):
        px, py = rnd.randrange(W), rnd.randrange(H)
        if im.getpixel((px, py)) == P[0]: d.point((px, py), fill=P[1])
    # 테두리 나무 숲
    for y in range(0, H, 14):
        for x in (-6, 8, W-22, W-8):
            draw_tree(d, x, y, P)
    if not lock:
        for x in range(22, W-22, 14):
            draw_tree(d, x, -4, P)
    # 오브젝트
    draw_house(d, 128, 120 if lock else 40, P)
    draw_fence(d, 26, 70, 250, P)
    draw_sign(d, 82, 210, P)
    draw_pond(d, 140, 230, 50, 36, P)
    draw_tall_grass(d, 26, 330, 60, 36, P)
    draw_tall_grass(d, 150, 380, 40, 30, P)
    for _ in range(14):
        fx, fy = rnd.randrange(28, W-34), rnd.randrange(60, H-60)
        if im.getpixel((fx, fy)) == P[1]: draw_flower(d, fx, fy, P)
    if lock:
        draw_textbox(d, H-86, "A wild notification\nappeared!", P)
    return im.resize((W*S, H*S), Image.NEAREST)

def make_preview(name, pal, icons):
    """홈 화면 적용 예시 미리보기 (iPhone 비율, 절반 크기)."""
    wp = make_wallpaper(pal).resize((645, 1398), Image.NEAREST)
    d = ImageDraw.Draw(wp)
    order = list(icons)[:16]
    sz, gx, gy, x0, y0 = 120, 150, 175, 40, 150
    mask = Image.new("L", (sz, sz)); ImageDraw.Draw(mask).rounded_rectangle([0, 0, sz-1, sz-1], 27, fill=255)
    for i, k in enumerate(order):
        x, y = x0 + (i % 4) * gx, y0 + (i // 4) * gy
        wp.paste(icons[k].resize((sz, sz), Image.NEAREST), (x, y), mask)
    # 독(Dock)
    d.rounded_rectangle([20, 1190, 625, 1360], 50, fill=hexrgb(pal[2]), outline=hexrgb(pal[3]), width=4)
    for i, k in enumerate(["phone", "messages", "safari", "music"]):
        wp.paste(icons[k].resize((sz, sz), Image.NEAREST), (x0 + i * gx, 1215), mask)
    wp.save(os.path.join(OUT, f"preview_{name}.png"))

if __name__ == "__main__":
    for name, pal in PALETTES.items():
        idir = os.path.join(OUT, name, "icons"); os.makedirs(idir, exist_ok=True)
        icons = {}
        for k, rows in ICONS.items():
            icons[k] = render_icon(rows, pal); icons[k].save(os.path.join(idir, f"{k}.png"))
        make_wallpaper(pal).save(os.path.join(OUT, name, "wallpaper_home.png"))
        make_wallpaper(pal, lock=True).save(os.path.join(OUT, name, "wallpaper_lock.png"))
        make_preview(name, pal, icons)
    print("done ->", OUT)
