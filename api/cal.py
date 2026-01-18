# -*- coding: utf-8 -*-
from datetime import date, datetime
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import os

# =========================
# FONT LOADING
# =========================
FONT_PATH = os.path.join(os.path.dirname(__file__), "font.otf")



def get_font(size_px: int):
    if FONT_PATH:
        try:
            return ImageFont.truetype(FONT_PATH, size_px)
        except Exception:
            pass
    try:
        return ImageFont.load_default(size=max(size_px // 8, 10))
    except TypeError:
        return ImageFont.load_default()


def draw_centered_text(draw, text, y_pos, font, color, width):
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) // 2
    draw.text((x, y_pos), text, fill=color, font=font)
    return text_height


def draw_centered_text_two_colors(draw, text_part1, text_part2, y_pos, font, color1, color2, width):
    """Draw text with two colors, centered as a whole"""
    full_text = text_part1 + text_part2
    bbox = draw.textbbox((0, 0), full_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x_start = (width - text_width) // 2
    
    # Draw first part
    draw.text((x_start, y_pos), text_part1, fill=color1, font=font)
    
    # Calculate position for second part
    bbox_part1 = draw.textbbox((0, 0), text_part1, font=font)
    part1_width = bbox_part1[2] - bbox_part1[0]
    x_part2 = x_start + part1_width
    
    # Draw second part
    draw.text((x_part2, y_pos), text_part2, fill=color2, font=font)
    
    return text_height


def generate_life_calendar(birth_str, lifespan, w, h, theme, lang, font_size=0):
    birth = datetime.strptime(birth_str, "%Y-%m-%d").date()
    today = date.today()

    lived_days = max(0, (today - birth).days)
    lived_weeks = lived_days // 7
    total_weeks = int(lifespan * 365.2422 / 7)
    percent = (lived_weeks / total_weeks * 100) if total_weeks else 0

    # Colors
    if theme == "white":
        bg = (185, 185, 185)
        lived_color = (152, 152, 152)
        future_color = (217, 217, 217)
        current_color = (255, 77, 77)
        text_main = (217, 217, 217)
        text_sec = (217, 217, 217)
    else:
        bg = (0, 0, 0)
        lived_color = (152, 152, 152)
        future_color = (217, 217, 217)
        current_color = (255, 77, 77)
        text_main = (217, 217, 217)
        text_sec = (217, 217, 217)

    img = Image.new("RGB", (w, h), bg)
    draw = ImageDraw.Draw(img)

    # Grid - 70 circles in one row, very small circles
    cols, rows = 70, lifespan
    pad_top = int(h * 0.20)
    pad_bot = int(h * 0.18)
    pad_x = int(w * 0.04)

    grid_w = w - pad_x * 2
    grid_h = h - pad_top - pad_bot
    cell = min(grid_w / cols, grid_h / rows)
    gap = cell * 0.50  # Much bigger gap = much smaller circles
    r = (cell - gap) / 2

    ox = (w - cols * cell) / 2
    oy = pad_top

    # Try to load logo for current week
    logo_img = None
    # Try multiple possible paths
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "..", "public", "img", "logo_mini.png"),
        os.path.join(os.path.dirname(__file__), "public", "img", "logo_mini.png"),
        "/var/task/public/img/logo_mini.png",  # Vercel path
        "public/img/logo_mini.png"
    ]
    
    for logo_path in possible_paths:
        if os.path.exists(logo_path):
            try:
                logo_img = Image.open(logo_path).convert("RGBA")
                break
            except Exception:
                continue

    for row in range(rows):
        for col in range(cols):
            i = row * cols + col
            cx = ox + col * cell + cell / 2
            cy = oy + row * cell + cell / 2
            if i < lived_weeks:
                c = lived_color
                draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
            elif i == lived_weeks:
                # Draw logo instead of red circle
                if logo_img:
                    logo_size = int(r * 2.2)
                    logo_resized = logo_img.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
                    logo_x = int(cx - logo_size / 2)
                    logo_y = int(cy - logo_size / 2)
                    img.paste(logo_resized, (logo_x, logo_y), logo_resized)
                else:
                    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=current_color)
            else:
                c = future_color
                draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)

    # Adaptive font size based on screen width
    # If fs param provided, use it; otherwise calculate from width
    if font_size > 0:
        main_px = font_size
    else:
        # ~4.2% of width (50px for 1179px width)
        main_px = int(w * 0.042)
        main_px = max(30, min(150, main_px))  # Clamp 30-150px

    small_px = int(main_px * 0.6)

    main_font = get_font(main_px)
    small_font = get_font(small_px)

    # Text - ALL UPPERCASE
    if lang == "ru":
        line1 = "ДЕЙСТВУЙ СЕЙЧАС"
        line2 = "У ТЕБЯ ЕЩЕ ЕСТЬ ВРЕМЯ"
    else:
        line1 = "ACT NOW"
        line2 = "YOU STILL HAVE TIME"

    percent_part1 = f"{percent:.1f}%"
    percent_part2 = f" to {lifespan}"

    y_percent = int(h * 0.82)
    draw_centered_text_two_colors(draw, percent_part1, percent_part2, y_percent, small_font, 
                                   (152, 152, 152), text_sec, w)

    y_main = int(h * 0.865)
    h1 = draw_centered_text(draw, line1, y_main, main_font, text_main, w)
    draw_centered_text(draw, line2, y_main + h1 + 10, main_font, text_main, w)

    buf = BytesIO()
    img.save(buf, "PNG", optimize=True)
    return buf.getvalue()


def generate_image(params):
    def get(name, default=None):
        val = params.get(name, [default])
        return val[0] if val else default


    theme = get("theme", "black")
    lang = get("lang", "en")
    w = min(5000, max(300, int(get("w", 1179))))
    h = min(5000, max(300, int(get("h", 2556))))
    font_size = int(get("fs", 50))  # Default 50px
    birth = get("birth")
    if not birth:
        raise ValueError("birth required")
    lifespan = int(get("lifespan", 90))

    return generate_life_calendar(birth, lifespan, w, h, theme, lang, font_size)


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
            self.send_header("X-Version", "6.0-cal")
            self.end_headers()
            self.wfile.write(image_bytes)
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode())
