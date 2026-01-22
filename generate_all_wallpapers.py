#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate wallpapers for all iPhone models
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from api.cal import generate_life_calendar
from datetime import date

# iPhone resolutions (from script.js)
devices = {
    'iPhone 13 mini': {'w': 1080, 'h': 2340},
    'iPhone 13_13 Pro_14_14 Pro': {'w': 1170, 'h': 2532},
    'iPhone 13 Pro Max_14 Plus_14 Pro Max': {'w': 1284, 'h': 2778},
    'iPhone 15_15 Pro_16': {'w': 1179, 'h': 2556},
    'iPhone 15 Plus_15 Pro Max_16 Plus': {'w': 1290, 'h': 2796},
    'iPhone 16 Pro': {'w': 1206, 'h': 2622},
    'iPhone 16 Pro Max': {'w': 1320, 'h': 2868},
    'iPhone 17': {'w': 1179, 'h': 2556},
    'iPhone 17 Pro': {'w': 1206, 'h': 2622},
    'iPhone 17 Pro Max': {'w': 1320, 'h': 2868}
}

# Test birth date
birth_date = "2000-01-01"
lifespan = 90
font_size = 60

# Create output directory
output_dir = "generated_wallpapers"
os.makedirs(output_dir, exist_ok=True)

print("Generating wallpapers for all devices...\n")

for device_name, resolution in devices.items():
    # Apply 1.5x quality multiplier
    w = int(resolution['w'] * 1.5)
    h = int(resolution['h'] * 1.5)

    # Safe filename
    safe_name = device_name.replace(' ', '_').replace('/', '_')

    for theme in ['black', 'gray']:
        for lang in ['eng', 'ru']:
            filename = f"{safe_name}_{theme}_{lang}.png"
            filepath = os.path.join(output_dir, filename)

            print(f"Generating: {filename}")

            try:
                img_data = generate_life_calendar(
                    birth_str=birth_date,
                    lifespan=lifespan,
                    w=w,
                    h=h,
                    theme=theme,
                    lang=lang,
                    font_size=font_size
                )

                with open(filepath, 'wb') as f:
                    f.write(img_data)

                print(f"  OK Saved: {filepath}\n")

            except Exception as e:
                print(f"  ERROR: {e}\n")

print(f"\nAll wallpapers generated in: {output_dir}/")
print(f"Total files: {len(devices) * 2 * 2} (10 devices × 2 themes × 2 languages)")
