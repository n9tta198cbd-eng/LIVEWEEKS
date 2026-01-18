from datetime import date, datetime
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import os


def load_font(size: int):
    """Load font with Cyrillic support"""
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]

    for path in font_paths:
        if os.path.exists(path):
            try:
                # DO NOT use encoding parameter - it breaks Cyrillic!
                return ImageFont.truetype(path, size)
            except Exception:
                continue

    # Fallback to default
    return ImageFont.load_default()


# =========================
# LIFE CALENDAR
# =========================
def generate_life_calendar(
    birth_str: str,
    lifespan: int,
    w: int,
    h: int,
    theme: str,
    lang: str
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
        lived = (60, 60, 60)
        future = (255, 255, 255)
        current = (255, 77, 77)
        text_main = (40, 40, 40)
        text_secondary = (110, 110, 110)
    else:
        bg = (0, 0, 0)
        lived = (255, 255, 255)
        future = (50, 50, 50)
        current = (255, 77, 77)
        text_main = (230, 230, 230)
        text_secondary = (150, 150, 150)

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

    for y in range(rows):
        for x in range(cols):
            i = y * cols + x
            cx = ox + x * cell + cell / 2
            cy = oy + y * cell + cell / 2

            if i < lived_weeks:
                color = lived
            elif i == lived_weeks:
                color = current
            else:
                color = future

            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)

    # ===== TEXT =====
    # Use fixed pixel sizes based on iPhone screen height
    # iPhone 15: h=2556 -> main=110px, small=70px
    # iPhone 11: h=1792 -> main=77px, small=49px
    main_size = max(60, min(140, int(w / 10.5)))  # Scale with width: ~112px for 1179px
    small_size = max(40, min(90, int(w / 16.5)))   # Scale with width: ~71px for 1179px

    main_font = load_font(main_size)
    small_font = load_font(small_size)





    # Text content based on language
    if lang == "ru":
        line1 = "Действуй сейчас."  # Act now.
        line2 = "У тебя ещё есть время."  # You still have time.
        percent_text = f"{percent:.1f}% to {lifespan}"
    else:
        line1 = "ACT NOW"
        line2 = "YOU STILL HAVE TIME"
        percent_text = f"{percent:.1f}% to {lifespan}"

    bw = draw.textbbox((0, 0), percent_text, font=small_font)
    draw.text(
        ((w - bw[2]) / 2, h * 0.82),
        percent_text,
        text_secondary,
        small_font
    )

    b1 = draw.textbbox((0, 0), line1, font=main_font)
    b2 = draw.textbbox((0, 0), line2, font=main_font)

    y = h * 0.865
    draw.text(((w - b1[2]) / 2, y), line1, text_main, main_font)
    draw.text(((w - b2[2]) / 2, y + b1[3] + 4), line2, text_main, main_font)

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
        return params.get(name, [default])[0]

    cal_type = get("type", "life")
    theme = get("theme", "black")
    lang = get("lang", "en")

    w = min(5000, max(300, int(get("w", 1179))))
    h = min(5000, max(300, int(get("h", 2556))))

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
            lang
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
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")  # Disable cache for testing
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(image_bytes)

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode())
