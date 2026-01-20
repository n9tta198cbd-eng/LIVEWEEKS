# -*- coding: utf-8 -*-
from datetime import date, datetime
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import os
import math


# =========================
# FONT LOADING
# =========================
FONT_PATH = os.path.join(os.path.dirname(__file__), "font.otf")


def get_font(size_px: int):
    try:
        return ImageFont.truetype(FONT_PATH, size_px)
    except Exception:
        return ImageFont.load_default()


def draw_centered_text(draw, text, y_pos, font, color, width):
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (width - text_w) // 2
    draw.text((x, y_pos), text, fill=color, font=font)
    return text_h


def draw_centered_text_two_colors(draw, t1, t2, y, font, c1, c2, w):
    full = t1 + t2
    bbox = draw.textbbox((0, 0), full, font=font)
    full_w = bbox[2] - bbox[0]
    x = (w - full_w) // 2
    draw.text((x, y), t1, fill=c1, font=font)
    w1 = draw.textbbox((0, 0), t1, font=font)[2]
    draw.text((x + w1, y), t2, fill=c2, font=font)


def generate_life_calendar(birth_str, lifespan, w, h, theme, lang, font_size=0):
    birth = datetime.strptime(birth_str, "%Y-%m-%d").date()
    today = date.today()

    lived_weeks = max(0, (today - birth).days // 7)
    total_weeks = int(lifespan * 365.2422 / 7)
    percent = (lived_weeks / total_weeks * 100) if total_weeks else 0

    bg = (185, 185, 185) if theme == "gray" else (0, 0, 0)
    lived_color = (152, 152, 152)
    future_color = (217, 217, 217)
    current_color = (255, 77, 77)
    text_color = (255, 255, 255)

    img = Image.new("RGB", (w, h), bg)
    draw = ImageDraw.Draw(img)

    # =========================
    # TEXT SETUP
    # =========================
    main_px = font_size if font_size > 0 else max(30, min(150, int(w * 0.038)))
    small_px = int(main_px * 0.6)

    main_font = get_font(main_px)
    small_font = get_font(small_px)

    percent_h = small_font.getbbox("100.0% to 90")[3]

    # =========================
    # FIXED LAYOUT
    # =========================
    SIDE_PADDING = 80
    PERCENT_GAP = 20

    BOTTOM_TEXT_OFFSET = 300     # ФИКС: от низа до текста
    TEXT_TO_GRID_GAP = 150       # ФИКС: от текста до сетки

    # =========================
    # TEXT POSITION
    # =========================
    y_main = h - BOTTOM_TEXT_OFFSET

    # =========================
    # GRID CALCULATION (ONLY VERTICAL ALIGN)
    # =========================
    cols = 55
    rows = math.ceil(total_weeks / cols)

    grid_end_y = y_main - TEXT_TO_GRID_GAP   # ЖЕСТКО 150px
    grid_start_y = 0

    grid_w = w - SIDE_PADDING * 2
    grid_h = grid_end_y - grid_start_y

    cell = min(grid_w / cols, grid_h / rows)
    gap = cell * 0.30
    r = (cell - gap) / 2

    used_w = cols * cell
    used_h = rows * cell

    # горизонталь — центр
    ox = SIDE_PADDING + (grid_w - used_w) / 2
    # вертикаль — ПРИЖАТО К НИЗУ
    oy = grid_end_y - used_h

    actual_grid_bottom = oy + used_h

    # =========================
    # LOGO
    # =========================
    logo_img = None
    logo_path = os.path.join(os.path.dirname(__file__), "logo_mini.png")

    if os.path.exists(logo_path):
        logo_img = Image.open(logo_path).convert("RGBA")


    # =========================
    # DRAW GRID
    # =========================
    for row in range(rows):
        for col in range(cols):
            i = row * cols + col
            cx = ox + col * cell + cell / 2
            cy = oy + row * cell + cell / 2

            if i < lived_weeks:
                draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=lived_color)
            elif i == lived_weeks:
                if logo_img:
                    size = int(r * 2.2)
                    logo = logo_img.resize((size, size), Image.Resampling.LANCZOS)
                    img.paste(logo, (int(cx - size / 2), int(cy - size / 2)), logo)
                else:
                    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=current_color)
            else:
                draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=future_color)

    # =========================
    # TEXT DRAW
    # =========================
    line1 = "ДЕЙСТВУЙ СЕЙЧАС" if lang == "ru" else "ACT NOW"
    line2 = "У ТЕБЯ ЕЩЕ ЕСТЬ ВРЕМЯ" if lang == "ru" else "YOU STILL HAVE TIME"

    y_percent = actual_grid_bottom + PERCENT_GAP
    draw_centered_text_two_colors(
        draw,
        f"{percent:.1f}%",
        f" to {lifespan}",
        y_percent,
        small_font,
        lived_color,
        text_color,
        w,
    )

    # Separate line spacing for each language
    if lang == "ru":
        LINE_SPACING = int(main_px * 0.05)
    else:
        LINE_SPACING = int(main_px * 0.20)

    h1 = draw_centered_text(draw, line1, y_main, main_font, text_color, w)
    draw_centered_text(
        draw,
        line2,
        y_main + h1 + LINE_SPACING,
        main_font,
        text_color,
        w
)


    buf = BytesIO()
    img.save(buf, "PNG", optimize=True)
    return buf.getvalue()


def generate_image(params):
    def get(name, default=None):
        return params.get(name, [default])[0]

    # Increase resolution by 1.5x for better quality
    w_base = min(5000, max(300, int(get("w", 1179))))
    h_base = min(5000, max(300, int(get("h", 2556))))
    w_final = int(w_base * 1.5)
    h_final = int(h_base * 1.5)

    return generate_life_calendar(
        get("birth"),
        int(get("lifespan", 90)),
        w_final,
        h_final,
        get("theme", "black"),
        get("lang", "en"),
        int(get("fs", 50)),
    )


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)
            img_bytes = generate_image(params)

            self.send_response(200)
            self.send_header("Content-Type", "image/png")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(img_bytes)
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())
