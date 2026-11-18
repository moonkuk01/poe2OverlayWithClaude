# 레트로 휴대용 게임기 스타일 아이폰 테마

90년대 휴대용 게임기 액정 느낌의 4색 픽셀 아트 테마입니다. 그림은 모두 직접 그린 오리지널이에요.

## 구성 (`output/`)
| 파일 | 설명 |
|---|---|
| `classic/` | 초록 액정 팔레트 |
| `pocket/` | 흑백 액정 팔레트 |
| `*/icons/*.png` | 앱 아이콘 16종 (512×512) |
| `*/wallpaper_home.png` | 홈 화면 배경 (1290×2796) |
| `*/wallpaper_lock.png` | 잠금 화면 배경, 대화창 포함 |
| `preview_*.png` | 적용 예시 미리보기 |

아이콘: phone, messages, camera, photos, settings, safari, mail, music, maps, calendar, clock, weather, notes, appstore, games, health

## 아이폰에 적용하기
1. 아이콘과 배경 PNG를 아이폰 사진 앱에 저장합니다. (AirDrop, iCloud Drive, 카카오톡 나에게 보내기 등)
2. **배경화면**: 설정 → 배경화면 → 새로운 배경화면 추가 → 사진에서 `wallpaper_lock.png` / `wallpaper_home.png`를 고릅니다.
3. **아이콘**: 단축어 앱 → `+` → 동작 추가 → "앱 열기" → 앱 선택
   → 상단 공유(또는 이름 옆 ▼) → **홈 화면에 추가** → 아이콘을 눌러 "사진 선택"으로 PNG 지정 → 이름 입력 → 추가
4. 원래 앱 아이콘은 길게 눌러 → 앱 제거 → **홈 화면에서 제거**를 고릅니다. 앱은 앱 보관함에 남아 있어요.

> 팁: 단축어 아이콘은 실행할 때 잠깐 단축어 배너가 떴다가 사라지는 iOS 제약이 있어요.

## 다시 만들기 / 수정
```bash
pip install pillow
python3 make_theme.py
```
`make_theme.py`의 `PALETTES`에 색 4개를 추가하면 새 색상 테마가 만들어지고, `ICONS`에 16×16 도트 맵(0~3)을 추가하면 아이콘이 늘어나요.
