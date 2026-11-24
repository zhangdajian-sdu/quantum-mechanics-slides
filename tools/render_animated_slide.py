"""Composite one embedded GIF over a slide PNG for the online viewer.

Requires Pillow and FFmpeg. Example, from the repository root:
python tools/render_animated_slide.py slides/ch8/ch8-s1.pptx 7 \
    docs/viewer/slides/ch8/ch8-s1/page-7.png
"""
import argparse
import io
from pathlib import Path
import posixpath
import subprocess
import tempfile
import xml.etree.ElementTree as ET
import zipfile

from PIL import Image

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pptx", type=Path)
    parser.add_argument("slide", type=int)
    parser.add_argument("image", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--ffmpeg", default="ffmpeg")
    args = parser.parse_args()
    output = args.output or args.image.with_suffix(".mp4")
    with Image.open(args.image) as image:
        width, height = image.size
    with zipfile.ZipFile(args.pptx) as archive:
        size = ET.fromstring(archive.read("ppt/presentation.xml")).find("p:sldSz", NS)
        root = ET.fromstring(archive.read(f"ppt/slides/slide{args.slide}.xml"))
        rels = ET.fromstring(archive.read(f"ppt/slides/_rels/slide{args.slide}.xml.rels"))
        targets = {rel.get("Id"): rel.get("Target") for rel in rels}
        animations = []
        for picture in root.findall(".//p:pic", NS):
            blip = picture.find(".//a:blip", NS)
            target = targets.get(blip.get(f"{{{NS['r']}}}embed"), "") if blip is not None else ""
            if target.lower().endswith(".gif"):
                animations.append((picture, target))
        if len(animations) != 1:
            raise ValueError("Expected exactly one embedded GIF on this slide")
        picture, target = animations[0]
        transform = picture.find(".//a:xfrm", NS)
        crop = picture.find(".//a:srcRect", NS)
        if transform is None or transform.get("rot") or (crop is not None and any(int(v) for v in crop.attrib.values())):
            raise ValueError("Only uncropped, unrotated picture placement is supported")
        offset, extent = transform.find("a:off", NS), transform.find("a:ext", NS)
        x = round(int(offset.get("x")) * width / int(size.get("cx")))
        y = round(int(offset.get("y")) * height / int(size.get("cy")))
        w = round(int(extent.get("cx")) * width / int(size.get("cx")))
        h = round(int(extent.get("cy")) * height / int(size.get("cy")))
        gif_bytes = archive.read(posixpath.normpath(posixpath.join("ppt/slides", target)))
    with Image.open(io.BytesIO(gif_bytes)) as gif:
        duration_ms = 0
        for frame in range(gif.n_frames):
            gif.seek(frame)
            duration_ms += gif.info.get("duration", 100)
    with tempfile.TemporaryDirectory(prefix="animated-slide-") as temporary:
        gif_path = Path(temporary) / "embedded.gif"
        gif_path.write_bytes(gif_bytes)
        subprocess.run([
            args.ffmpeg, "-y", "-hide_banner", "-loglevel", "error",
            "-loop", "1", "-i", str(args.image),
            "-ignore_loop", "1", "-i", str(gif_path),
            "-filter_complex",
            f"[1:v]scale={w}:{h}:flags=lanczos[animation];"
            f"[0:v][animation]overlay={x}:{y}:shortest=1,fps=25,format=yuv420p[video]",
            "-map", "[video]", "-an", "-t", str(duration_ms / 1000),
            "-c:v", "libx264", "-crf", "18", "-preset", "medium",
            "-movflags", "+faststart", str(output),
        ], check=True)
    print(f"Created {output} ({duration_ms / 1000:.2f} s)")


if __name__ == "__main__":
    main()
