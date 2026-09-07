# Kontaktbogen aus mehreren Screenshots: sheet.py <ausgabe.jpg> <bild1> [bild2 ...]
import sys
from PIL import Image, ImageDraw
out, files = sys.argv[1], sys.argv[2:]
ims = [Image.open(f).convert("RGB") for f in files]
cols = 2 if len(ims) > 1 else 1
w = 1500; th = [int(im.height * w / im.width) for im in ims]
rows = (len(ims) + cols - 1) // cols
rh = [max(th[r * cols:(r + 1) * cols]) for r in range(rows)]
sheet = Image.new("RGB", (w * cols, sum(rh) + 26 * rows), "black"); d = ImageDraw.Draw(sheet)
y = 0
for r in range(rows):
    for c in range(cols):
        i = r * cols + c
        if i >= len(ims): break
        sheet.paste(ims[i].resize((w, th[i])), (c * w, y)); d.text((c * w + 8, y + rh[r] + 4), files[i], fill="yellow")
    y += rh[r] + 26
sheet.save(out, "JPEG", quality=74); print("sheet", out, sheet.size)
