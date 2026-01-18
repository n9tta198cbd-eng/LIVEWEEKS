# -*- coding: utf-8 -*-
from datetime import date, datetime
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import os

# =========================
# FONT LOADING - NEW MECHANISM
# =========================

# Find available font path ONCE at module load
FONT_PATH = None
POSSIBLE_FONTS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "C:/Windows/Fonts/arial.ttf",
    "C:/Windows/Fonts/Arial.ttf",
]

for fp in POSSIBLE_FONTS:
    if os.path.exists(fp):
        FONT_PATH = fp
        break


def get_font(size_px: int):
    """Create font with exact pixel size"""
    if FONT_PATH:
        return ImageFont.truetype(FONT_PATH, size_px)
    else:
        # Fallback - will not scale but won't crash
        return ImageFont.load_default()


def draw_centered_text(draw, text, y_pos, font, color, width):
    """Draw text centered horizontally"""
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) // 2
    draw.text((x, y_pos), text, fill=color, font=font)
    return text_height


# =========================
# LIFE CALENDAR
# =========================
def generate_life_calendar(
    birth_str: str,
    lifespan: int,
    w: int,
    h: int,
    theme: str,
    lang: str,
    font_size: int = 0  # NEW: explicit font size parameter
) -> bytes:

    birth = datetime.strptime(birth_str, "%Y-%m-%d").date()
    today = date.today()

    lived_days = max(0, (today - birth).days)
    lived_weeks = lived_days // 7
    total_weeks = int(lifespan * 365.2422 / 7)

    percent = (lived_weeks / total_weeks * 100) if total_weeks else 0

    # ===== COLORS =====
    if theme == "white":
        bg = (230, 230, 230)
        lived_color = (60, 60, 60)
        future_color = (255, 255, 255)
        current_color = (255, 77, 77)
        text_main_color = (40, 40, 40)
        text_secondary_color = (110, 110, 110)
    else:
        bg = (0, 0, 0)
        lived_color = (255, 255, 255)
        future_color = (50, 50, 50)
        current_color = (255, 77, 77)
        text_main_color = (230, 230, 230)
        text_secondary_color = (150, 150, 150)

    img = Image.new("RGB", (w, h), bg)
    draw = ImageDraw.Draw(img)

    # ===== GRID =====
    cols = 52
    rows = lifespan

    padding_top = int(h * 0.18)
    padding_bottom = int(h * 0.18)
    padding_x = int(w * 0.08)

    grid_w = w - padding_x * 2
    grid_h = h - padding_top - padding_bottom

    cell = min(grid_w / cols, grid_h / rows)
    gap = cell * 0.25
    r = (cell - gap) / 2

    ox = (w - cols * cell) / 2
    oy = padding_top

    for row in range(rows):
        for col in range(cols):
            i = row * cols + col
            cx = ox + col * cell + cell / 2
            cy = oy + row * cell + cell / 2

            if i < lived_weeks:
                dot_color = lived_color
            elif i == lived_weeks:
                dot_color = current_color
            else:
                dot_color = future_color

            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=dot_color)

    # ===== TEXT - NEW MECHANISM =====
    # Calculate font size: use parameter or calculate from width
    if font_size > 0:
        main_px = font_size
    else:
        # Default: width / 7 = ~168px for iPhone 15 (1179px width)
        main_px = w // 7

    small_px = main_px // 2

    # Clamp sizes to reasonable range (v5 - fixed)
    main_px = max(40, min(350, main_px))
    small_px = max(25, min(175, small_px))

    # Create fonts with exact sizes
    main_font = get_font(main_px)
    small_font = get_font(small_px)

    # Text content
    if lang == "ru":
        line1 = "Действуй сейчас."
        line2 = "У тебя ещё есть время."
    else:
        line1 = "ACT NOW"
        line2 = "YOU STILL HAVE TIME"

    percent_text = f"{percent:.1f}% to {lifespan}"

    # Draw percentage text
    y_percent = int(h * 0.82)
    draw_centered_text(draw, percent_text, y_percent, small_font, text_secondary_color, w)

    # Draw main text lines
    y_main = int(h * 0.865)
    line1_height = draw_centered_text(draw, line1, y_main, main_font, text_main_color, w)
    draw_centered_text(draw, line2, y_main + line1_height + 10, main_font, text_main_color, w)

    # Save
    buf = BytesIO()
    img.save(buf, "PNG", optimize=True)
    return buf.getvalue()


# =========================
# YEAR CALENDAR
# =========================
def generate_year_calendar(w: int, h: int) -> bytes:
    today = date.today()
    start = date(today.year, 1, 1)
    total_days = (date(today.year, 12, 31) - start).days + 1
    passed = (today - start).days

    img = Image.new("RGB", (w, h), (10, 10, 10))
    draw = ImageDraw.Draw(img)

    cols = 53
    rows = 7

    padding_top = int(h * 0.18)
    padding_bottom = int(h * 0.12)
    padding_x = int(w * 0.08)

    grid_w = w - padding_x * 2
    grid_h = h - padding_top - padding_bottom

    cell = min(grid_w / cols, grid_h / rows)
    r = (cell * 0.7) / 2

    ox = (w - cols * cell) / 2
    oy = padding_top

    for d in range(total_days):
        week = d // 7
        day = d % 7

        cx = ox + week * cell + cell / 2
        cy = oy + day * cell + cell / 2

        color = (255, 255, 255) if d < passed else (60, 60, 60)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)

    buf = BytesIO()
    img.save(buf, "PNG", optimize=True)
    return buf.getvalue()


# =========================
# API ENTRY POINT
# =========================
def generate_image(params: dict) -> bytes:
    def get(name, default=None):
        val = params.get(name, [default])
        return val[0] if val else default

    cal_type = get("type", "life")
    theme = get("theme", "black")
    lang = get("lang", "en")

    w = min(5000, max(300, int(get("w", 1179))))
    h = min(5000, max(300, int(get("h", 2556))))

    # NEW: Allow font size override via URL parameter
    font_size = int(get("fs", 0))

    if cal_type == "life":
        birth = get("birth")
        if not birth:
            raise ValueError("birth is required (YYYY-MM-DD)")

        lifespan = int(get("lifespan", 90))

        return generate_life_calendar(
            birth,
            lifespan,
            w,
            h,
            theme,
            lang,
            font_size
        )

    if cal_type == "year":
        return generate_year_calendar(w, h)

    raise ValueError("Unknown calendar type")


# =========================
# VERCEL HANDLER
# =========================
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)

            image_bytes = generate_image(params)

            self.send_response(200)
            self.send_header("Content-Type", "image/png")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("X-Font-Path", str(FONT_PATH))  # Debug: show which font is used
            self.send_header("X-Version", "5.0-force")
            self.end_headers()
            self.wfile.write(image_bytes)

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode())
