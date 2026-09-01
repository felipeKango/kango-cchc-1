#!/usr/bin/env python3
"""Genera public/og.png (1200x630) y public/qr.png (1000x1000) para kango-cchc-1."""
import os

from PIL import Image, ImageDraw, ImageFont
import qrcode

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, "public")

BG = "#FAFAFA"
INK = "#0a0f2b"
RED = "#C0001A"
MUTED = (10, 15, 43, 160)

FONT_PATH = "/System/Library/Fonts/Helvetica.ttc"


def font(size, bold=False):
    # Helvetica.ttc: index 0 regular, index 1 bold
    return ImageFont.truetype(FONT_PATH, size, index=1 if bold else 0)


def gen_og():
    img = Image.new("RGB", (1200, 630), BG)
    d = ImageDraw.Draw(img)

    # Barra roja superior
    d.rectangle([0, 0, 1200, 10], fill=RED)

    # Chip
    chip_text = "CLASE #1 - IA EN SIMPLE: TU PUNTO DE PARTIDA"
    f_chip = font(24, bold=True)
    tw = d.textlength(chip_text, font=f_chip)
    cx, cy, pad_x, pad_y = 80, 92, 22, 12
    d.rounded_rectangle([cx, cy, cx + tw + 2 * pad_x, cy + 24 + 2 * pad_y + 4],
                        radius=26, outline=RED, width=2)
    d.text((cx + pad_x, cy + pad_y), chip_text, font=f_chip, fill=RED)

    # Título
    f_title = font(88, bold=True)
    d.text((78, 180), "IA para la construcción", font=f_title, fill=INK)
    d.text((78, 280), "en Chile", font=f_title, fill=INK)

    # Subtítulo
    f_sub = font(32)
    d.text((80, 408), "Programa de formación en Inteligencia Artificial", font=f_sub, fill=(60, 65, 95))
    d.text((80, 452), "para el sector construcción", font=f_sub, fill=(60, 65, 95))

    # Pie: Kango x CChC
    f_foot = font(30, bold=True)
    d.rectangle([80, 545, 86, 585], fill=RED)
    d.text((102, 550), "Kango · CChC · 1 sep 2026", font=f_foot, fill=INK)

    # Logo Kango arriba a la derecha
    try:
        logo = Image.open(os.path.join(PUB, "img", "logo-kango.png")).convert("RGBA")
        ratio = 150 / logo.height
        logo = logo.resize((max(1, int(logo.width * ratio)), 150), Image.LANCZOS)
        img.paste(logo, (1200 - logo.width - 70, 70), logo)
    except Exception as exc:  # el OG sigue siendo válido sin logo
        print(f"AVISO: no se pudo insertar el logo en og.png: {exc}")

    out = os.path.join(PUB, "og.png")
    img.save(out, optimize=True)
    print(f"OK {out} ({os.path.getsize(out) // 1024} KB)")


def gen_qr():
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data("https://kangocchc-1.vercel.app")
    qr.make(fit=True)
    img = qr.make_image(fill_color=INK, back_color="white").convert("RGB")
    img = img.resize((1000, 1000), Image.NEAREST)
    out = os.path.join(PUB, "qr.png")
    img.save(out, optimize=True)
    print(f"OK {out} ({os.path.getsize(out) // 1024} KB)")


if __name__ == "__main__":
    gen_og()
    gen_qr()
