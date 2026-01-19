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

    bg = (185, 185, 185) if theme == "white" else (0, 0, 0)
    lived_color = (152, 152, 152)
    future_color = (217, 217, 217)
    current_color = (255, 77, 77)
    text_color = (217, 217, 217)

    img = Image.new("RGB", (w, h), bg)
    draw = ImageDraw.Draw(img)

    # =========================
    # TEXT SETUP
    # =========================
    main_px = font_size if font_size > 0 else max(30, min(150, int(w * 0.042)))
    small_px = int(main_px * 0.6)

    main_font = get_font(main_px)
    small_font = get_font(small_px)

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

    # Логотип для текста
    logo_text_img = None
    logo_text_path = os.path.join(os.path.dirname(__file__), "logo_text.png")
    if os.path.exists(logo_text_path):
        logo_text_img = Image.open(logo_text_path).convert("RGBA")


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
    # Тексты в два ряда
    if lang == "ru":
        text_left_1 = "ДЕЙСТВУЙ"
        text_left_2 = "СЕЙЧАС."
        text_right_1 = "У ТЕБЯ ЕЩЁ"
        text_right_2 = "ЕСТЬ ВРЕМЯ."
    else:
        text_left_1 = "ACT"
        text_left_2 = "NOW."
        text_right_1 = "YOU STILL"
        text_right_2 = "HAVE TIME."

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

    # =========================
    # THREE BLOCK TEXT WITH LOGO (2 LINES EACH SIDE)
    # =========================
    LINE_SPACING = int(main_px * 0.2)  # межстрочный интервал

    # Вычисляем размеры текстов
    bbox_left_1 = draw.textbbox((0, 0), text_left_1, font=main_font)
    text_left_1_w = bbox_left_1[2] - bbox_left_1[0]
    text_left_1_h = bbox_left_1[3] - bbox_left_1[1]

    bbox_left_2 = draw.textbbox((0, 0), text_left_2, font=main_font)
    text_left_2_w = bbox_left_2[2] - bbox_left_2[0]
    text_left_2_h = bbox_left_2[3] - bbox_left_2[1]

    bbox_right_1 = draw.textbbox((0, 0), text_right_1, font=main_font)
    text_right_1_w = bbox_right_1[2] - bbox_right_1[0]
    text_right_1_h = bbox_right_1[3] - bbox_right_1[1]

    bbox_right_2 = draw.textbbox((0, 0), text_right_2, font=main_font)
    text_right_2_w = bbox_right_2[2] - bbox_right_2[0]

    # Максимальные ширины для выравнивания
    max_left_w = max(text_left_1_w, text_left_2_w)
    max_right_w = max(text_right_1_w, text_right_2_w)

    # Высота текстового блока (2 строки)
    text_block_h = text_left_1_h + LINE_SPACING + text_left_2_h

    # Размер логотипа - по высоте текстового блока
    logo_text_size = int(text_block_h)

    # Отступ между текстом и логотипом (плотно)
    LOGO_MARGIN = int(main_px * 0.5)

    # Общая ширина композиции
    total_width = max_left_w + LOGO_MARGIN + logo_text_size + LOGO_MARGIN + max_right_w

    # Стартовая позиция для центрирования всей композиции
    start_x = (w - total_width) // 2

    # === РИСУЕМ ЛЕВЫЙ ТЕКСТ (выравнивание вправо) ===
    left_1_x = start_x + max_left_w - text_left_1_w
    left_2_x = start_x + max_left_w - text_left_2_w

    draw.text((left_1_x, y_main), text_left_1, fill=text_color, font=main_font)
    draw.text((left_2_x, y_main + text_left_1_h + LINE_SPACING), text_left_2, fill=text_color, font=main_font)

    # === РИСУЕМ ЛОГОТИП ===
    logo_x = start_x + max_left_w + LOGO_MARGIN
    logo_y = y_main  # выравниваем по верхней линии текста

    logo_rendered = None

    # Загружаем PNG логотип для текста
    if logo_text_img:
        logo_resized = logo_text_img.resize((logo_text_size, logo_text_size), Image.Resampling.LANCZOS)
        # Меняем цвет логотипа на цвет текста
        logo_colored = Image.new("RGBA", logo_resized.size)
        for x in range(logo_resized.width):
            for y in range(logo_resized.height):
                _, _, _, a = logo_resized.getpixel((x, y))
                if a > 0:  # если пиксель не прозрачный
                    logo_colored.putpixel((x, y), (*text_color, a))
                else:
                    logo_colored.putpixel((x, y), (0, 0, 0, 0))
        logo_rendered = logo_colored

    # Вставляем логотип
    if logo_rendered:
        img.paste(logo_rendered, (int(logo_x), int(logo_y)), logo_rendered)
    else:
        # Если логотипа нет, рисуем заглушку (круг)
        cx = logo_x + logo_text_size // 2
        cy = logo_y + logo_text_size // 2
        r_circle = logo_text_size // 2
        draw.ellipse([cx - r_circle, cy - r_circle, cx + r_circle, cy + r_circle], fill=text_color)

    # === РИСУЕМ ПРАВЫЙ ТЕКСТ (выравнивание влево) ===
    right_x = logo_x + logo_text_size + LOGO_MARGIN

    draw.text((right_x, y_main), text_right_1, fill=text_color, font=main_font)
    draw.text((right_x, y_main + text_right_1_h + LINE_SPACING), text_right_2, fill=text_color, font=main_font)


    buf = BytesIO()
    img.save(buf, "PNG", optimize=True)
    return buf.getvalue()


def generate_image(params):
    def get(name, default=None):
        return params.get(name, [default])[0]

    return generate_life_calendar(
        get("birth"),
        int(get("lifespan", 90)),
        min(5000, max(300, int(get("w", 1179)))),
        min(5000, max(300, int(get("h", 2556)))),
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
