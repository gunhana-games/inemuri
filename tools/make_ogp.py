"""X などでリンクを貼ったときに表示されるカード画像（ogp.png, 1200x630）と、
アイコン（icon.png, 180x180）を作るスクリプト。
使い方: python tools/make_ogp.py   （inemuri-game フォルダで実行）
背景は、ゲーム画面のスクリーンショット tools/ogp_src.jpg（まぶたが半分閉じた教室）を使う。
上下の黒いまぶたの部分に、題名と一言をのせる。
"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
FONT_B = "C:/Windows/Fonts/BIZ-UDGothicB.ttc"
FONT_R = "C:/Windows/Fonts/BIZ-UDGothicR.ttc"
TITLE = "うとうと学園"
TAG = "先生にバレずに、居眠りしろ。"
SUB = "長押しで目を閉じる ── ブラウザで遊べる無料ゲーム"
YELLOW = (255, 215, 94)
LID = (13, 11, 10)


def font(path, size):
    return ImageFont.truetype(path, size)


def center_text(d, y, text, f, fill, W):
    w = d.textlength(text, font=f)
    d.text(((W - w) / 2, y), text, font=f, fill=fill)


def make_ogp():
    W, H = 1200, 630
    src = Image.open(os.path.join(HERE, "ogp_src.jpg")).convert("RGB")
    # 横幅に合わせて拡大し、真ん中を切り出す
    s = W / src.width
    bg = src.resize((W, round(src.height * s)), Image.LANCZOS)
    top = (bg.height - H) // 2
    bg = bg.crop((0, top, W, top + H)).filter(ImageFilter.GaussianBlur(0.6))
    d = ImageDraw.Draw(bg)
    # 上下のまぶた（スクリーンショットのまぶたより少し大きく、まるく）
    d.ellipse([-200, -330, W + 200, 170], fill=LID)
    d.ellipse([-200, H - 150, W + 200, H + 330], fill=LID)
    # 題名（上のまぶた）と一言（下のまぶた）
    center_text(d, 18, TITLE, font(FONT_B, 104), (255, 255, 255), W)
    center_text(d, H - 118, TAG, font(FONT_B, 50), YELLOW, W)
    center_text(d, H - 52, SUB, font(FONT_R, 26), (230, 230, 230), W)
    # Zzz
    f = font(FONT_B, 44)
    for i, (x, y) in enumerate([(1020, 170), (1070, 130), (1112, 96)]):
        d.text((x, y), "Z", font=font(FONT_B, 34 + i * 10), fill=(255, 255, 255), stroke_width=3, stroke_fill=LID)
    bg.save(os.path.join(OUT, "ogp.png"), optimize=True)


def make_icon():
    S = 180
    img = Image.new("RGB", (S, S), (44, 79, 60))   # 黒板の緑
    d = ImageDraw.Draw(img)
    # 閉じかけの目
    d.ellipse([22, 50, 158, 130], fill=(255, 255, 255), outline=(20, 20, 20), width=6)
    d.ellipse([70, 68, 110, 108], fill=(43, 38, 34))
    d.chord([22, 50, 158, 130], 180, 360, fill=(239, 207, 174), outline=(20, 20, 20), width=6)   # まぶた（上半分）
    d.line([30, 90, 150, 90], fill=(20, 20, 20), width=6)
    d.text((120, 8), "Z", font=font(FONT_B, 40), fill=YELLOW)
    d.text((146, 0), "z", font=font(FONT_B, 28), fill=YELLOW)
    img.save(os.path.join(OUT, "icon.png"), optimize=True)


if __name__ == "__main__":
    make_ogp()
    make_icon()
    print("ogp.png / icon.png を作りました")
