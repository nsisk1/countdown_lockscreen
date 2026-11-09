#!/usr/bin/env python3
"""
T-Minus Lock Screen & Milestone Wallpaper Generator
Generates a customized, high-resolution (1080x1920, 9:16) smartphone lock screen
featuring a telemetry HUD, countdown typography, and 5-stage milestone progress bar.
"""

import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_procedural_background(width=1080, height=1920):
    """Generates a deep matte carbon background with subtle ambient glow."""
    # Base radial gradient
    y, x = np.ogrid[:height, :width]
    
    # Dark carbon background
    base_color = np.array([11, 14, 15], dtype=np.float32)
    center_glow = np.array([16, 26, 24], dtype=np.float32)
    
    # Distance from center-bottom for ambient emerald/amber glow
    cx, cy = width / 2.0, height * 0.72
    dist = np.sqrt((x - cx) ** 2 + ((y - cy) * 0.8) ** 2)
    max_dist = math.sqrt(width ** 2 + height ** 2)
    factor = np.clip(1.0 - (dist / (max_dist * 0.45)), 0.0, 1.0)
    factor = factor[:, :, np.newaxis]
    
    img_arr = base_color + (center_glow - base_color) * factor
    
    # Add subtle circuit / grid noise texture
    noise = np.random.normal(0, 2.5, (height, width, 1))
    img_arr = np.clip(img_arr + noise, 0, 255).astype(np.uint8)
    
    base_img = Image.fromarray(img_arr, mode='RGB')
    return base_img

def find_system_font(font_names, default_size=32):
    """Tries to find a clean system TTF font."""
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, default_size)
            except Exception:
                continue
    return ImageFont.load_default()

def draw_hud_brackets(draw, width, height, margin=50, corner_len=60, color=(36, 180, 126, 180)):
    """Draws sci-fi corner telemetry brackets."""
    # Top-Left
    draw.line([(margin, margin + corner_len), (margin, margin), (margin + corner_len, margin)], fill=color, width=3)
    draw.ellipse([margin + corner_len + 10, margin - 3, margin + corner_len + 16, margin + 3], fill=(234, 150, 40, 220))
    
    # Top-Right
    draw.line([(width - margin - corner_len, margin), (width - margin, margin), (width - margin, margin + corner_len)], fill=color, width=3)
    draw.ellipse([width - margin - 3, margin - 3, width - margin + 3, margin + 3], fill=(234, 150, 40, 220))
    
    # Bottom-Left
    draw.line([(margin, height - margin - corner_len), (margin, height - margin), (margin + corner_len, height - margin)], fill=color, width=3)
    
    # Bottom-Right
    draw.line([(width - margin - corner_len, height - margin), (width - margin, height - margin), (width - margin, height - margin - corner_len)], fill=color, width=3)

def generate_lockscreen(
    output_path="t_minus_lockscreen.png",
    main_text="T-MINUS 40:00:00",
    subtitle="TARGET: FRIDAY • 8H / STAGE",
    active_stage=1,  # 1 to 5 (e.g., 1 = T-5D active)
    base_asset=None,
    width=1080,
    height=1920
):
    """
    Renders the complete 9:16 lock screen wallpaper.
    If base_asset is provided, composites telemetry over the high-res wallpaper.
    Otherwise builds it procedurally.
    """
    if base_asset and os.path.exists(base_asset):
        base_img = Image.open(base_asset).convert("RGBA")
        if base_img.size != (width, height):
            base_img = base_img.resize((width, height), Image.Resampling.LANCZOS)
    else:
        base_img = create_procedural_background(width, height).convert("RGBA")

    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Telemetry framing
    draw_hud_brackets(draw, width, height)

    # Upper 35% is preserved for device lock screen clock/date
    # HUD Elements reside in lower 40% (y = 1100 to 1550)
    cy_text = int(height * 0.62)
    
    # Fonts
    font_main = find_system_font(["DejaVuSans-Bold"], default_size=64)
    font_sub = find_system_font(["DejaVuSans-Bold"], default_size=28)
    font_stages = find_system_font(["DejaVuSans"], default_size=24)

    # 1. Main Title with Glow
    # Glow layer
    glow_color = (0, 255, 170, 70)
    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, 1)]:
        bbox = draw.textbbox((0, 0), main_text, font=font_main)
        w_text = bbox[2] - bbox[0]
        x_text = (width - w_text) // 2 + dx
        draw.text((x_text, cy_text + dy), main_text, fill=glow_color, font=font_main)

    # Main sharp text
    bbox = draw.textbbox((0, 0), main_text, font=font_main)
    w_text = bbox[2] - bbox[0]
    x_text = (width - w_text) // 2
    draw.text((x_text, cy_text), main_text, fill=(220, 255, 240, 255), font=font_main)

    # 2. Subtitle
    cy_sub = cy_text + 90
    bbox_sub = draw.textbbox((0, 0), subtitle, font=font_sub)
    w_sub = bbox_sub[2] - bbox_sub[0]
    x_sub = (width - w_sub) // 2
    draw.text((x_sub, cy_sub), subtitle, fill=(242, 160, 52, 230), font=font_sub)

    # 3. Telemetry Progress Gauge
    cy_bar = cy_sub + 75
    bar_w = 780
    bar_h = 48
    bar_x = (width - bar_w) // 2
    bar_y = cy_bar

    # Gauge ruler marks above the bar
    ruler_y = bar_y - 14
    for i in range(21):
        rx = bar_x + int(i * (bar_w / 20))
        tick_h = 8 if i % 5 == 0 else 4
        tick_color = (0, 230, 150, 160) if i % 5 == 0 else (0, 180, 120, 90)
        draw.line([(rx, ruler_y - tick_h), (rx, ruler_y)], fill=tick_color, width=2 if i % 5 == 0 else 1)

    # Outer pill container
    draw.rounded_rectangle(
        [bar_x, bar_y, bar_x + bar_w, bar_y + bar_h],
        radius=bar_h // 2,
        outline=(0, 230, 150, 140),
        width=2,
        fill=(10, 22, 20, 210)
    )

    # Small status LEDs at sides of pill
    draw.ellipse([bar_x - 24, bar_y + bar_h // 2 - 4, bar_x - 16, bar_y + bar_h // 2 + 4], fill=(242, 160, 52, 220))
    draw.ellipse([bar_x + bar_w + 16, bar_y + bar_h // 2 - 4, bar_x + bar_w + 24, bar_y + bar_h // 2 + 4], fill=(242, 160, 52, 220))

    # 5 Segments: T-5D, T-4D, T-3D, T-2D, T-1D
    num_segments = 5
    padding = 6
    seg_w = (bar_w - (num_segments + 1) * padding) / num_segments
    labels = ["T-5D", "T-4D", "T-3D", "T-2D", "T-1D"]

    for idx in range(num_segments):
        sx1 = bar_x + padding + idx * (seg_w + padding)
        sy1 = bar_y + padding
        sx2 = sx1 + seg_w
        sy2 = bar_y + bar_h - padding
        
        # Fill style depending on active/completed stage
        if idx < active_stage:
            fill_color = (0, 240, 160, 230)
            outline_color = (120, 255, 210, 255)
        elif idx == active_stage:
            fill_color = (0, 160, 110, 150)
            outline_color = (0, 240, 160, 180)
        else:
            fill_color = (20, 36, 32, 140)
            outline_color = (30, 60, 50, 100)

        draw.rounded_rectangle([sx1, sy1, sx2, sy2], radius=6, fill=fill_color, outline=outline_color, width=1)

        # Stage label below segment
        label = labels[idx]
        bbox_l = draw.textbbox((0, 0), label, font=font_stages)
        lw = bbox_l[2] - bbox_l[0]
        lx = int(sx1 + (seg_w - lw) / 2)
        ly = bar_y + bar_h + 18
        lbl_color = (0, 240, 160, 220) if idx <= active_stage else (100, 140, 130, 150)
        draw.text((lx, ly), label, fill=lbl_color, font=font_stages)

    # Merge overlay with base image
    final_img = Image.alpha_composite(base_img, overlay).convert("RGB")
    final_img.save(output_path, quality=95)
    print(f"Generated lock screen saved to: {output_path}")

if __name__ == "__main__":
    generate_lockscreen()