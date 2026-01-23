#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from api.cal import generate_life_calendar

# Test iPhone 15
name = 'iPhone_15'
width, height = 1179, 2556
w, h = int(width * 1.5), int(height * 1.5)

print(f"\nGenerating {name}: {w}x{h}")

# English
img_data = generate_life_calendar('2000-01-01', 90, w, h, 'black', 'eng', 60)
filename = f'test_{name}_eng.png'
with open(filename, 'wb') as f:
    f.write(img_data)
print(f'  Saved: {filename}')

# Russian
img_data_ru = generate_life_calendar('2000-01-01', 90, w, h, 'black', 'ru', 60)
filename_ru = f'test_{name}_ru.png'
with open(filename_ru, 'wb') as f:
    f.write(img_data_ru)
print(f'  Saved: {filename_ru}')

print('\nDone!')
