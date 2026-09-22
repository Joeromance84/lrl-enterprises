#!/usr/bin/env python3
"""
make_qr.py - QR code for the Nourishology page.

Usage:  python make_qr.py [url] [stem]
Writes: assets/<stem>.png  and  assets/<stem>.svg   (stem defaults to "qr-code")

Error correction H (~30% recoverable) so it survives print and compression.
Requires: pip install "qrcode[pil]"
"""

import sys
from pathlib import Path

import qrcode
from qrcode.constants import ERROR_CORRECT_H
from qrcode.image.svg import SvgPathImage

DEFAULT_URL = "https://joeromance84.github.io/nourishology/"
BOX_SIZE = 30
BORDER = 4


def build(url, out_dir, stem="qr-code"):
    out_dir.mkdir(parents=True, exist_ok=True)

    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=BOX_SIZE, border=BORDER)
    qr.add_data(url)
    qr.make(fit=True)
    png = out_dir / (stem + ".png")
    qr.make_image(fill_color="black", back_color="white").save(png)

    s = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=BOX_SIZE, border=BORDER)
    s.add_data(url)
    s.make(fit=True)
    svg = out_dir / (stem + ".svg")
    s.make_image(image_factory=SvgPathImage).save(svg)

    size = (qr.modules_count + BORDER * 2) * BOX_SIZE
    print("URL  " + url)
    print("PNG  " + str(png) + "  (" + str(size) + "x" + str(size) + ")")
    print("SVG  " + str(svg))
    print("")
    print("Scan it with a phone before printing it.")


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    stem = sys.argv[2] if len(sys.argv) > 2 else "qr-code"
    build(target, Path(__file__).resolve().parent.parent / "assets", stem)
