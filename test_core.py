# -*- coding: utf-8 -*-
"""핵심 로직 테스트: 아이템 클립보드 파싱 + 빌드 타겟 대조"""
import importlib.util
import os
import sys
from importlib.machinery import SourceFileLoader

HERE = os.path.dirname(os.path.abspath(__file__))
loader = SourceFileLoader("overlay", os.path.join(HERE, "poe2_overlay.pyw"))
spec = importlib.util.spec_from_loader("overlay", loader)
ov = importlib.util.module_from_spec(spec)
loader.exec_module(ov)

fails = []


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (" | " + detail if detail else ""))
    if not cond:
        fails.append(name)


# ---------- 1) 레어 아이템 파싱 ----------
GLOVES = """Item Class: Gloves
Rarity: Rare
Behemoth Hand
Grand Bracers
--------
Evasion Rating: 122
--------
Requirements:
Level: 70
Dex: 87
--------
Item Level: 82
--------
Adds 19 to 28 Fire Damage to Attacks
Adds 2 to 42 Lightning Damage to Attacks
+2 to Level of all Melee Skills
27% increased Critical Damage Bonus
100% increased effect of Socketed Items
Adds 9 to 16 Cold Damage to Attacks"""

g = ov.parse_item_clipboard(GLOVES)
check("parse ok", g["ok"])
check("item_class", g["item_class"] == "Gloves", g["item_class"])
check("rarity", g["rarity"] == "Rare")
check("name", g["name"] == "Behemoth Hand", g["name"])
check("base", g["base"] == "Grand Bracers", g["base"])
check("ilvl", g["ilvl"] == 82, str(g["ilvl"]))
check("req_level", g["req_level"] == 70, str(g["req_level"]))
check("mods count", len(g["mods"]) == 6, str(len(g["mods"])))
check("no property lines in mods",
      all(not m.startswith(("Evasion", "Requirements", "Dex")) for m in g["mods"]))

# ---------- 2) 빌드 타겟 대조 ----------
ana = ov.analyze_item(g)
check("slot detected", ana["slot"] == "Gloves", str(ana["slot"]))
hit_labels = [l for l, m in ana["hits"] if m]
miss_labels = [l for l, m in ana["hits"] if not m]
check("melee level hit", any("Melee" in l for l in hit_labels))
check("ele damage hit", any("원소 추가피해" in l for l in hit_labels))
check("crit damage hit", any("크리 데미지" in l for l in hit_labels))
check("attack speed miss", any("어택 스피드" in l for l in miss_labels))
check("crit chance miss", any("크리 확률" in l for l in miss_labels))

# ---------- 3) 슬롯 감지 (다양한 클래스) ----------
check("slot amulet", ov._slot_key("Amulets") == "Amulets")
check("slot ring", ov._slot_key("Rings") == "Rings")
check("slot quarterstaff", ov._slot_key("Quarterstaves") == "Quarterstaves")
check("slot body", ov._slot_key("Body Armours") == "Body Armours")
check("slot boots", ov._slot_key("Boots") == "Boots")
check("slot unknown", ov._slot_key("Sceptres") is None)

# ---------- 4) 매직 아이템 + 비-아이템 ----------
MAGIC = """Item Class: Gloves
Rarity: Magic
Reliable Grand Bracers of the Newt
--------
Item Level: 74
--------
+2 to Level of all Melee Skills"""
mg = ov.parse_item_clipboard(MAGIC)
check("magic ok", mg["ok"] and mg["rarity"] == "Magic")
check("magic mods", mg["mods"] == ["+2 to Level of all Melee Skills"], str(mg["mods"]))

check("non-item rejected", ov.parse_item_clipboard("hello world")["ok"] is False)
check("empty rejected", ov.parse_item_clipboard("")["ok"] is False)

# 알 수 없는 슬롯 → note 비어있고 hits 없음
sceptre = ov.parse_item_clipboard("Item Class: Sceptres\nRarity: Rare\nX\nY")
sa = ov.analyze_item(sceptre)
check("unknown slot no hits", sa["slot"] is None and sa["hits"] == [])

# ---------- 5) 앱 파일 문법 체크 ----------
import py_compile
try:
    py_compile.compile(os.path.join(HERE, "poe2_overlay.pyw"), doraise=True)
    check("py_compile", True)
except py_compile.PyCompileError as e:
    check("py_compile", False, str(e))

print("\n%d failures" % len(fails))
sys.exit(1 if fails else 0)
