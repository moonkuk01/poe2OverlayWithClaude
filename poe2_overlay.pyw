# -*- coding: utf-8 -*-
"""
PoE2 아이템 분석 오버레이
- 인게임에서 아이템에 커서 올리고 Ctrl+C → 클립보드의 아이템 텍스트를 읽어
  현재 빌드 타겟(슬롯별 노려야 할 옵션)과 대조해서 보여준다.
- 클립보드를 "읽기"만 하므로 GGG 규정 안전지대 (게임 메모리 접근/자동입력 없음).
- 항상 위(topmost) 반투명 창. 외부 라이브러리 불필요 (Python 표준 라이브러리만).

빌드 타겟: Ice Strike 마셜 아티스트 멍크
  (자세한 슬롯별 타겟은 POE2_클래스맞춤_멍크_IceStrike.md 참고)

실행: 이 파일 더블클릭 (.pyw = 콘솔창 없이 실행)
"""

import json
import os
import re

APP_TITLE = "PoE2 아이템 분석"
CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".poe2_overlay_config.json")
CLIP_POLL_MS = 600            # 클립보드 감시 주기(ms)
BUILD_NAME = "Ice Strike 마셜 아티스트"

# ---------------------------------------------------------------------------
# 1) 아이템 클립보드 파싱 + 빌드 타겟 대조
# ---------------------------------------------------------------------------

_DASH_LINE = re.compile(r"^-{3,}$")

# 슬롯별 빌드 타겟 (Ice Strike 마셜 아티스트 멍크 기준)
BUILD_SLOT_TARGETS = {
    "Gloves": ("⭐ 최우선 슬롯 (Way of the Stonefist가 장갑을 무기화)", [
        ("+Melee 스킬 레벨", ["level of all melee", "melee skill"]),
        ("어택에 원소 추가피해", ["damage to attacks"]),
        ("어택 스피드", ["attack speed"]),
        ("크리 데미지 보너스", ["critical damage"]),
        ("크리 확률", ["critical hit chance", "critical strike chance"]),
    ]),
    "Quarterstaves": ("무기 — 크리/원소딜 중심 (Sinister Quarterstaff)", [
        ("어택 원소 피해 %", ["elemental damage with attack", "increased elemental damage"]),
        ("크리 데미지", ["critical damage"]),
        ("어택 스피드", ["attack speed"]),
        ("크리 확률", ["critical hit chance", "critical strike chance"]),
    ]),
    "Amulets": ("목걸이 — Spirit + Melee 레벨", [
        ("Spirit", ["spirit"]),
        ("+Melee 스킬 레벨", ["level of all melee", "melee skill"]),
        ("어택 원소 추가피해", ["damage to attacks"]),
    ]),
    "Rings": ("반지 — 플랫 원소딜/저항/마나 (Amethyst Ring)", [
        ("어택에 플랫 원소 피해", ["damage to attacks"]),
        ("저항", ["resistance"]),
        ("마나", ["mana"]),
    ]),
    "Helmets": ("헬멧 — ES/크리확률/저항", [
        ("에너지 실드", ["energy shield"]),
        ("크리 확률", ["critical hit chance", "critical strike chance"]),
        ("저항", ["resistance"]),
    ]),
    "Body Armours": ("가슴 — 회피/ES 하이브리드", [
        ("회피", ["evasion"]),
        ("에너지 실드", ["energy shield"]),
        ("저항", ["resistance"]),
    ]),
    "Boots": ("신발 — 이동속도 최우선", [
        ("이동 속도", ["movement speed"]),
        ("저항", ["resistance"]),
        ("생명/ES", ["maximum life", "energy shield"]),
    ]),
    "Belts": ("벨트 — 생명/저항", [
        ("생명", ["maximum life", "to life"]),
        ("저항", ["resistance"]),
        ("회피/ES", ["evasion", "energy shield"]),
    ]),
}

_SLOT_ALIASES = {
    "glove": "Gloves", "quarterstaff": "Quarterstaves", "quarterstave": "Quarterstaves",
    "amulet": "Amulets", "ring": "Rings", "helmet": "Helmets",
    "body arm": "Body Armours", "boot": "Boots", "belt": "Belts",
}

_PROP_PREFIXES = ("Quality:", "Evasion Rating:", "Armour:", "Energy Shield:",
                  "Block:", "Requirements:", "Level:", "Str:", "Dex:", "Int:",
                  "Sockets:", "Item Level:", "Note:", "Stack Size:")


def _slot_key(item_class: str):
    ic = (item_class or "").lower()
    for k, v in _SLOT_ALIASES.items():
        if k in ic:
            return v
    return None


def parse_item_clipboard(text: str) -> dict:
    """PoE2 아이템 Ctrl+C 텍스트 파싱. PoE 아이템 아니면 {'ok': False}."""
    lines = [ln.rstrip() for ln in (text or "").splitlines()]
    if not any(ln.startswith(("Item Class:", "Rarity:")) for ln in lines):
        return {"ok": False}

    info = {"ok": True, "item_class": "", "rarity": "", "name": "", "base": "",
            "ilvl": None, "req_level": None, "mods": []}

    # '----' 기준으로 섹션 분리
    sections, cur = [], []
    for ln in lines:
        if _DASH_LINE.match(ln.strip()):
            sections.append(cur)
            cur = []
        else:
            cur.append(ln)
    sections.append(cur)

    # 첫 섹션: class / rarity / 이름 / 베이스
    name_lines = []
    for ln in (sections[0] if sections else []):
        if ln.startswith("Item Class:"):
            info["item_class"] = ln.split(":", 1)[1].strip()
        elif ln.startswith("Rarity:"):
            info["rarity"] = ln.split(":", 1)[1].strip()
        elif ln.strip():
            name_lines.append(ln.strip())
    if name_lines:
        info["name"] = name_lines[0]
        if len(name_lines) > 1:
            info["base"] = name_lines[1]

    # 나머지 섹션: ilvl / 요구레벨 / 모드
    for sec in sections[1:]:
        for ln in sec:
            s = ln.strip()
            if not s:
                continue
            if s.startswith("Item Level:"):
                m = re.search(r"(\d+)", s)
                if m:
                    info["ilvl"] = int(m.group(1))
                continue
            if s.startswith("Level:") and info["req_level"] is None:
                m = re.search(r"(\d+)", s)
                if m:
                    info["req_level"] = int(m.group(1))
                continue
            if s.startswith(_PROP_PREFIXES) or s in ("Corrupted", "Unidentified", "Mirrored"):
                continue
            info["mods"].append(s)
    return info


def analyze_item(info: dict) -> dict:
    """파싱된 아이템을 빌드 타겟과 대조."""
    slot = _slot_key(info.get("item_class", ""))
    out = {"slot": slot, "note": "", "hits": []}
    if not slot or slot not in BUILD_SLOT_TARGETS:
        return out
    note, targets = BUILD_SLOT_TARGETS[slot]
    out["note"] = note
    mods = info.get("mods", [])
    mods_l = [m.lower() for m in mods]
    for label, keys in targets:
        matched = None
        for orig, low in zip(mods, mods_l):
            if any(k in low for k in keys):
                matched = orig
                break
        out["hits"].append((label, matched))
    return out


# ---------------------------------------------------------------------------
# 2) 설정 저장/로드 (창 위치만 유지)
# ---------------------------------------------------------------------------

def load_config() -> dict:
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def save_config(cfg: dict):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
    except OSError:
        pass


# ---------------------------------------------------------------------------
# 3) 오버레이 UI (tkinter)
# ---------------------------------------------------------------------------

BG = "#15161a"
BG2 = "#1e2026"
FG = "#e8e6e3"
DIM = "#8a8f98"
ACCENT = "#d4af37"    # PoE 골드
GOOD = "#9ae66e"      # 타겟 충족
MISS = "#6b7078"      # 타겟 비어있음

RARITY_COLORS = {
    "Normal": "#c8c8c8", "Magic": "#8888ff",
    "Rare": "#e0e000", "Unique": "#af6025",
}


def run_app():
    import tkinter as tk

    cfg = load_config()
    root = tk.Tk()
    root.title(APP_TITLE)
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    try:
        root.attributes("-alpha", 0.94)
    except tk.TclError:
        pass
    root.configure(bg=BG)
    root.geometry(cfg.get("geometry", "380x480+80+80"))

    font_base = ("Malgun Gothic", 10)
    font_small = ("Malgun Gothic", 9)
    font_title = ("Malgun Gothic", 11, "bold")

    state = {"last_clip": None, "collapsed": False}

    # ---- 헤더 (드래그) ----
    header = tk.Frame(root, bg=BG2)
    header.pack(fill="x")
    drag = {"x": 0, "y": 0}

    def on_press(e):
        drag["x"], drag["y"] = e.x_root - root.winfo_x(), e.y_root - root.winfo_y()

    def on_drag(e):
        root.geometry("+{}+{}".format(e.x_root - drag["x"], e.y_root - drag["y"]))

    title_lbl = tk.Label(header, text=APP_TITLE, bg=BG2, fg=ACCENT, font=font_title)
    title_lbl.pack(side="left", padx=10, pady=6)
    for w in (header, title_lbl):
        w.bind("<ButtonPress-1>", on_press)
        w.bind("<B1-Motion>", on_drag)

    def close_app():
        cfg_out = {"geometry": root.geometry()}
        save_config(cfg_out)
        root.destroy()

    tk.Button(header, text="✕", command=close_app, bg=BG2, fg=DIM, bd=0,
              activebackground=BG2, activeforeground=FG).pack(side="right", padx=4)

    def toggle_collapse():
        state["collapsed"] = not state["collapsed"]
        if state["collapsed"]:
            body.pack_forget()
            root.geometry(root.geometry().split("+")[0].split("x")[0] + "x36")
        else:
            body.pack(fill="both", expand=True)
            geo = root.geometry()
            if geo.endswith("x36") or "x36+" in geo:
                root.geometry("380x480")

    tk.Button(header, text="—", command=toggle_collapse, bg=BG2, fg=DIM, bd=0,
              activebackground=BG2, activeforeground=FG).pack(side="right")

    # ---- 본문 ----
    body = tk.Frame(root, bg=BG)
    body.pack(fill="both", expand=True)

    sub = tk.Label(body, text="빌드: {} · 인게임에서 아이템 Ctrl+C".format(BUILD_NAME),
                   bg=BG, fg=DIM, font=font_small, anchor="w", wraplength=350)
    sub.pack(fill="x", padx=12, pady=(6, 2))

    content = tk.Frame(body, bg=BG)
    content.pack(fill="both", expand=True, padx=4, pady=2)

    status = tk.Label(body, text="클립보드 감시 중…", bg=BG, fg=DIM, font=font_small,
                      anchor="w")
    status.pack(fill="x", padx=12, pady=(0, 2))

    bottom = tk.Frame(body, bg=BG)
    bottom.pack(fill="x", pady=(0, 8))
    tk.Button(bottom, text="🔍 지금 분석", command=lambda: force_analyze(), bg=BG2,
              fg=FG, bd=0, padx=12, pady=3, activebackground=BG2).pack(side="left", padx=12)

    # ---- 렌더링 ----
    def clear_content():
        for w in content.winfo_children():
            w.destroy()

    def show_placeholder(msg):
        clear_content()
        tk.Label(content, text=msg, bg=BG, fg=DIM, font=font_base, justify="left",
                 wraplength=350, anchor="nw").pack(fill="both", expand=True,
                                                   padx=10, pady=10)

    def render(info):
        clear_content()
        ana = analyze_item(info)
        rcol = RARITY_COLORS.get(info.get("rarity", ""), FG)

        # 헤더 (이름 + 희귀도)
        tk.Label(content, text="{}".format(info.get("name") or "?"), bg=BG, fg=rcol,
                 font=font_title, wraplength=350, justify="left",
                 anchor="w").pack(fill="x", padx=8, pady=(4, 0))
        meta = []
        if info.get("ilvl"):
            meta.append("ilvl {}".format(info["ilvl"]))
        if info.get("req_level"):
            meta.append("요구 Lv {}".format(info["req_level"]))
        if info.get("item_class"):
            meta.append(info["item_class"])
        subtxt = info.get("base", "")
        if meta:
            subtxt = (subtxt + "   " + " · ".join(meta)).strip()
        tk.Label(content, text=subtxt, bg=BG, fg=DIM, font=font_small,
                 wraplength=350, justify="left", anchor="w").pack(fill="x", padx=8)

        # 빌드 타겟 대조
        if ana["slot"] and ana["hits"]:
            tk.Label(content, text=ana["note"], bg=BG, fg=FG, font=font_small,
                     wraplength=350, justify="left", anchor="w").pack(
                fill="x", padx=8, pady=(8, 2))
            hit_n = 0
            for label, matched in ana["hits"]:
                mark = "✅" if matched else "⬜"
                color = GOOD if matched else MISS
                if matched:
                    hit_n += 1
                txt = "{} {}".format(mark, label)
                if matched:
                    txt += "   ({})".format(matched[:40])
                tk.Label(content, text=txt, bg=BG, fg=color, font=font_small,
                         wraplength=350, justify="left", anchor="w").pack(
                    fill="x", padx=8)
            tk.Label(content, text="→ 타겟 {}/{} 충족".format(hit_n, len(ana["hits"])),
                     bg=BG, fg=ACCENT, font=font_small, anchor="w").pack(
                fill="x", padx=8, pady=(2, 0))
        else:
            tk.Label(content, text="이 슬롯({})은 빌드 타겟 데이터가 없어요.".format(
                info.get("item_class", "?")), bg=BG, fg=DIM, font=font_small,
                wraplength=350, justify="left", anchor="w").pack(fill="x", padx=8, pady=6)

        # 원문 모드
        tk.Label(content, text="─ 아이템 옵션 ─", bg=BG, fg=DIM, font=font_small,
                 anchor="w").pack(fill="x", padx=8, pady=(8, 0))
        for m in (info.get("mods") or ["(모드 없음)"]):
            tk.Label(content, text="· " + m, bg=BG, fg=FG, font=font_small,
                     wraplength=350, justify="left", anchor="w").pack(fill="x", padx=8)

    # ---- 클립보드 처리 ----
    def read_clip():
        try:
            return root.clipboard_get()
        except tk.TclError:
            return ""

    def force_analyze():
        raw = read_clip()
        state["last_clip"] = raw
        info = parse_item_clipboard(raw)
        if info.get("ok"):
            render(info)
            status.config(text="분석 완료 · 클립보드 감시 중")
        else:
            show_placeholder("클립보드에 PoE2 아이템이 없어요.\n\n인게임에서 아이템에 커서를 "
                             "올리고 Ctrl+C 한 뒤\n'🔍 지금 분석'을 누르거나, 그냥 복사만 해도 "
                             "자동으로 떠요.")
            status.config(text="PoE2 아이템 아님 · 클립보드 감시 중")

    def poll_clip():
        raw = read_clip()
        if raw != state["last_clip"]:
            state["last_clip"] = raw
            info = parse_item_clipboard(raw)
            if info.get("ok"):
                render(info)
                status.config(text="자동 분석됨 · 클립보드 감시 중")
        root.after(CLIP_POLL_MS, poll_clip)

    # ---- 시작 ----
    show_placeholder("인게임에서 아이템에 커서를 올리고 Ctrl+C 하면\n여기에 빌드 타겟 대조가 "
                     "자동으로 뜹니다.\n\n(클립보드를 읽기만 하므로 게임 규정상 안전)")
    poll_clip()
    root.mainloop()


if __name__ == "__main__":
    run_app()
