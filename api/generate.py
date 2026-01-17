from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timedelta
from io import BytesIO
import math

def generate_life_calendar(birth_date_str, lifespan, width, height):
    """
    Генерирует календарь жизни в неделях
    """
    # Парсим дату рождения
    birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d')
    today = datetime.now()

    # Цвета
    bg_color = (0, 0, 0)  # Черный фон
    lived_color = (255, 255, 255)  # Белый для прожитых недель
    future_color = (60, 60, 60)  # Темно-серый для будущих недель
    grid_color = (40, 40, 40)  # Цвет сетки

    # Создаем изображение
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Рассчитываем параметры сетки
    total_weeks = lifespan * 52
    weeks_per_row = 52
    total_rows = lifespan

    # Паддинги и размеры
    padding_top = 100
    padding_bottom = 100
    padding_left = 50
    padding_right = 50

    # Доступная область для календаря
    available_width = width - padding_left - padding_right
    available_height = height - padding_top - padding_bottom

    # Размер ячейки
    cell_width = available_width / weeks_per_row
    cell_height = available_height / total_rows
    cell_size = min(cell_width, cell_height)

    # Размер кружка (с зазором)
    gap = cell_size * 0.3
    circle_radius = (cell_size - gap) / 2

    # Рассчитываем количество прожитых недель
    weeks_lived = math.floor((today - birth_date).days / 7)

    # Центрируем календарь
    grid_width = weeks_per_row * cell_size
    grid_height = total_rows * cell_size
    start_x = (width - grid_width) / 2
    start_y = (height - grid_height) / 2

    # Рисуем кружки
    for year in range(total_rows):
        for week in range(weeks_per_row):
            week_number = year * weeks_per_row + week

            # Центр кружка
            cx = start_x + week * cell_size + cell_size / 2
            cy = start_y + year * cell_size + cell_size / 2

            # Определяем цвет
            if week_number < weeks_lived:
                color = lived_color
            else:
                color = future_color

            # Рисуем кружок
            draw.ellipse(
                [cx - circle_radius, cy - circle_radius,
                 cx + circle_radius, cy + circle_radius],
                fill=color
            )

    # Добавляем текст (возраст)
    try:
        font_large = ImageFont.truetype("arial.ttf", 60)
        font_small = ImageFont.truetype("arial.ttf", 30)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    age = math.floor((today - birth_date).days / 365.25)
    age_text = f"{age} years"

    # Рисуем возраст в верхней части
    text_bbox = draw.textbbox((0, 0), age_text, font=font_large)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (width - text_width) / 2
    draw.text((text_x, 30), age_text, fill=lived_color, font=font_large)

    # Конвертируем в байты
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return buffer.getvalue()


def generate_year_calendar(width, height):
    """
    Генерирует календарь текущего года по дням
    """
    today = datetime.now()
    year = today.year

    # Цвета
    bg_color = (0, 0, 0)
    lived_color = (255, 255, 255)
    future_color = (60, 60, 60)

    # Создаем изображение
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Параметры сетки
    days_in_year = 366 if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) else 365
    weeks_per_row = 52
    total_rows = math.ceil(days_in_year / 7)

    # Паддинги
    padding_top = 100
    padding_bottom = 100
    padding_left = 50
    padding_right = 50

    available_width = width - padding_left - padding_right
    available_height = height - padding_top - padding_bottom

    cell_width = available_width / weeks_per_row
    cell_height = available_height / total_rows
    cell_size = min(cell_width, cell_height)

    gap = cell_size * 0.3
    circle_radius = (cell_size - gap) / 2

    # День года
    day_of_year = today.timetuple().tm_yday

    # Центрируем
    grid_width = weeks_per_row * cell_size
    grid_height = total_rows * cell_size
    start_x = (width - grid_width) / 2
    start_y = (height - grid_height) / 2

    # Рисуем дни
    for day in range(days_in_year):
        week = day // 7
        day_in_week = day % 7

        cx = start_x + day_in_week * cell_size + cell_size / 2
        cy = start_y + week * cell_size + cell_size / 2

        color = lived_color if day < day_of_year else future_color

        draw.ellipse(
            [cx - circle_radius, cy - circle_radius,
             cx + circle_radius, cy + circle_radius],
            fill=color
        )

    # Добавляем год
    try:
        font_large = ImageFont.truetype("arial.ttf", 60)
    except:
        font_large = ImageFont.load_default()

    year_text = str(year)
    text_bbox = draw.textbbox((0, 0), year_text, font=font_large)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (width - text_width) / 2
    draw.text((text_x, 30), year_text, fill=lived_color, font=font_large)

    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return buffer.getvalue()


def generate_goal_calendar(goal_name, start_date_str, deadline_str, width, height):
    """
    Генерирует календарь обратного отсчета до цели
    """
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
    today = datetime.now()

    # Цвета
    bg_color = (0, 0, 0)
    completed_color = (255, 255, 255)
    remaining_color = (60, 60, 60)

    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Вычисляем дни
    total_days = (deadline - start_date).days
    days_passed = max(0, (today - start_date).days)
    days_passed = min(days_passed, total_days)

    # Параметры сетки
    days_per_row = 30
    total_rows = math.ceil(total_days / days_per_row)

    padding_top = 150
    padding_bottom = 100
    padding_left = 50
    padding_right = 50

    available_width = width - padding_left - padding_right
    available_height = height - padding_top - padding_bottom

    cell_width = available_width / days_per_row
    cell_height = available_height / total_rows
    cell_size = min(cell_width, cell_height)

    gap = cell_size * 0.3
    circle_radius = (cell_size - gap) / 2

    grid_width = days_per_row * cell_size
    grid_height = total_rows * cell_size
    start_x = (width - grid_width) / 2
    start_y = (height - grid_height) / 2 + 50

    # Рисуем дни
    for day in range(total_days):
        row = day // days_per_row
        col = day % days_per_row

        cx = start_x + col * cell_size + cell_size / 2
        cy = start_y + row * cell_size + cell_size / 2

        color = completed_color if day < days_passed else remaining_color

        draw.ellipse(
            [cx - circle_radius, cy - circle_radius,
             cx + circle_radius, cy + circle_radius],
            fill=color
        )

    # Добавляем название цели и дни до цели
    try:
        font_large = ImageFont.truetype("arial.ttf", 50)
        font_small = ImageFont.truetype("arial.ttf", 30)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    days_remaining = max(0, total_days - days_passed)

    goal_text = goal_name
    text_bbox = draw.textbbox((0, 0), goal_text, font=font_large)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (width - text_width) / 2
    draw.text((text_x, 30), goal_text, fill=completed_color, font=font_large)

    days_text = f"{days_remaining} days remaining"
    text_bbox = draw.textbbox((0, 0), days_text, font=font_small)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (width - text_width) / 2
    draw.text((text_x, 90), days_text, fill=completed_color, font=font_small)

    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return buffer.getvalue()


class handler(BaseHTTPRequestHandler):
    """
    Vercel serverless handler
    """
    def do_GET(self):
        # Парсим URL и параметры
        parsed_url = urlparse(self.path)
        params = parse_qs(parsed_url.query)

        # Получаем параметры
        cal_type = params.get('type', ['life'])[0]
        width = int(params.get('w', ['1179'])[0])
        height = int(params.get('h', ['2556'])[0])

        try:
            if cal_type == 'life':
                birth = params.get('birth', ['2000-01-01'])[0]
                lifespan = int(params.get('lifespan', ['90'])[0])
                image_bytes = generate_life_calendar(birth, lifespan, width, height)

            elif cal_type == 'year':
                image_bytes = generate_year_calendar(width, height)

            elif cal_type == 'goal':
                goal = params.get('goal', ['My Goal'])[0]
                start = params.get('start', ['2024-01-01'])[0]
                deadline = params.get('deadline', ['2024-12-31'])[0]
                image_bytes = generate_goal_calendar(goal, start, deadline, width, height)
            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Invalid calendar type')
                return

            # Отправляем изображение
            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.send_header('Content-Length', str(len(image_bytes)))
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.end_headers()
            self.wfile.write(image_bytes)

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f'Error: {str(e)}'.encode())
