#!/usr/bin/env python3
"""Render ZecHub 0xramp carousel slides (1080x1350 PNG) from slides_es.md with Pillow.
Usage: python3 -I render_slides.py <slides_es.md> <outdir> [shots_dir]
shots_dir (optional): slide1.png..slide6.png app screenshots, pasted in the lower half.
Brand colors from zechub.wiki/visual-identity page: #F4B728 (Zcash yellow), #0b1520 (dark)."""
import sys, os, re, textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
YEL, DARK, WHITE = (244, 183, 40), (11, 31, 63), (255, 255, 255)  # navy #0B1F3F per brand guide p32-50
CROP = {int(a): int(b) for a, b in (x.split(":") for x in os.environ.get("CROP", "").split(",") if x)}  # per-slide crop divisor; bigger = shorter crop
F = "/usr/share/fonts/truetype/dejavu/"
fb = lambda s: ImageFont.truetype(F + "DejaVuSans-Bold.ttf", s)
fr = lambda s: ImageFont.truetype(F + "DejaVuSans.ttf", s)


def slides(md):
    out = []
    for line in open(md, encoding="utf-8"):
        m = re.match(r"^(\d)\.\s+(.*)$", line.strip())
        if m:
            head, _, body = m.group(2).partition(": ")
            body = body[:1].upper() + body[1:]
            out.append((head.strip(), body.strip()))
    return out


def render(i, n, head, body, shot, path):
    im = Image.new("RGB", (W, H), DARK)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 18], fill=YEL)
    d.text((80, 70), f"0xramp  ·  {i}/{n}", font=fr(34), fill=YEL)
    y = 150
    for ln in textwrap.wrap(head, 20):
        d.text((80, y), ln, font=fb(78), fill=WHITE); y += 95
    y += 30
    d.rectangle([80, y, 240, y + 8], fill=YEL); y += 50
    for ln in textwrap.wrap(body, 34):
        d.text((80, y), ln, font=fr(44), fill=WHITE); y += 60
    if shot and os.path.exists(shot):
        s = Image.open(shot).convert("RGB")
        room = H - y - 200
        if room > 200:
            s = s.crop((0, 0, s.width, min(s.height, int(s.width * room / CROP.get(i, 600)))))
            s = s.resize((int(s.width * room / s.height), room))
            ImageDraw.Draw(im).rectangle([(W - s.width) // 2 - 6, y + 34, (W + s.width) // 2 + 6, y + 46 + s.height], fill=YEL)
            im.paste(s, ((W - s.width) // 2, y + 40))
    d.text((80, H - 90), "ZecHub  ·  Zcash en Español", font=fb(34), fill=YEL)
    d.text((W - 300, H - 90), "zechub.wiki", font=fr(34), fill=WHITE)
    im.save(path)


if __name__ == "__main__":
    md, outd = sys.argv[1], sys.argv[2]
    shots = sys.argv[3] if len(sys.argv) > 3 else None
    os.makedirs(outd, exist_ok=True)
    S = slides(md)
    for k, (h, b) in enumerate(S, 1):
        p = os.path.join(outd, f"slide{k}.png")
        render(k, len(S), h, b, shots and os.path.join(shots, f"slide{k}.png"), p)
        print(p)
