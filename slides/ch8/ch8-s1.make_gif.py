"""把 gyro-both.mp4 转成适合嵌入课件的循环 GIF。"""
import imageio.v2 as imageio
from PIL import Image

from pathlib import Path

MEDIA = Path(__file__).resolve().parent / "ch8-s1-media"
SRC = str(MEDIA / "gyro-both.mp4")
DST = str(MEDIA / "gyro-both.gif")
FPS = 12
WIDTH = 800

reader = imageio.get_reader(SRC, fps=FPS)
frames = []
for frame in reader:
    img = Image.fromarray(frame)
    h = round(img.height * WIDTH / img.width)
    frames.append(img.resize((WIDTH, h), Image.LANCZOS))
reader.close()

# 自适应调色板，扁平配色下 256 色足够
frames[0].save(
    DST,
    save_all=True,
    append_images=frames[1:],
    duration=round(1000 / FPS),
    loop=0,
    optimize=True,
)
import os
print(DST, f"{os.path.getsize(DST)/1e6:.2f} MB", len(frames), "frames")
