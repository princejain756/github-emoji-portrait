#!/usr/bin/env python3
"""Turn a photo into an emoji mosaic for your GitHub profile README.

Usage:
    python emoji_portrait.py photo.jpg > portrait.txt
    python emoji_portrait.py photo.jpg --size 32 --crop 0.7 --out portrait.txt

Then paste the output into a fenced code block in your README.
"""
import argparse

from PIL import Image, ImageFilter, ImageOps

# emoji -> approximate rendered color on GitHub
PALETTE = [
    ("⬛", (35, 35, 35)),
    ("🟫", (140, 85, 55)),
    ("🏿", (68, 46, 37)),
    ("🏾", (97, 63, 46)),
    ("🏽", (137, 90, 63)),
    ("🏼", (188, 133, 96)),
    ("🏻", (236, 188, 150)),
    ("⬜", (240, 240, 240)),
    ("🟧", (247, 139, 30)),
    ("🟨", (253, 203, 55)),
    ("🟥", (221, 46, 68)),
    ("🟩", (121, 178, 80)),
    ("🟦", (85, 172, 238)),
]


def nearest(pixel, palette=PALETTE):
    best_i, best_d = 0, float("inf")
    for i, (_, rgb) in enumerate(palette):
        d = sum((pixel[k] - rgb[k]) ** 2 for k in range(3))
        if d < best_d:
            best_i, best_d = i, d
    return best_i


def make_portrait(src, size=28, crop=0.56, top=0.04):
    img = Image.open(src).convert("RGB")
    w, h = img.size
    side = int(min(w, h) * crop)
    left = (w - side) // 2
    img = img.crop((left, int(h * top), left + side, int(h * top) + side))
    img = img.filter(ImageFilter.GaussianBlur(1.0))
    img = ImageOps.autocontrast(img, cutoff=1)
    img = img.resize((size, size), Image.LANCZOS)
    return "\n".join(
        "".join(PALETTE[nearest(img.getpixel((x, y)))][0] for x in range(size))
        for y in range(size)
    )


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("photo", help="input image (a centered headshot works best)")
    p.add_argument("--size", type=int, default=28, help="mosaic width/height in emoji (default 28)")
    p.add_argument("--crop", type=float, default=0.56, help="fraction of the frame to keep (default 0.56)")
    p.add_argument("--top", type=float, default=0.04, help="vertical offset of the crop (default 0.04)")
    p.add_argument("--out", help="write to file instead of stdout")
    args = p.parse_args()

    art = make_portrait(args.photo, args.size, args.crop, args.top)
    if args.out:
        with open(args.out, "w") as f:
            f.write(art + "\n")
    else:
        print(art)
