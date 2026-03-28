#!/usr/bin/env python3
"""Generate OG image for transmacros.com — 1200x630 PNG using Pillow."""

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630

BG = "#0d0f14"
TRANS_BLUE = "#5BCEFA"
TRANS_PINK = "#F5A9B8"
TRANS_WHITE = "#FFFFFF"
WHITE = "#FFFFFF"
MUTED = "#7a8099"
BORDER = "#2a3050"
PILL_BG = "#141824"
GLOW1 = "#1E3458"
GLOW2 = "#1A2D52"
GLOW3 = "#131B30"

STRIPE_COLORS = [TRANS_BLUE, TRANS_PINK, TRANS_WHITE, TRANS_PINK, TRANS_BLUE]

img = Image.new("RGBA", (W, H), BG)
draw = ImageDraw.Draw(img)

# Radial glow — concentric ellipses with reduced opacity
cx, cy = W // 2, H // 2 + 10
for r, color, alpha in [(140, GLOW3, 40), (100, GLOW2, 30), (60, GLOW1, 20)]:
    glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    # Parse hex color and add alpha
    rgb = tuple(int(color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
    glow_draw.ellipse([cx - r * 2, cy - r, cx + r * 2, cy + r], fill=(*rgb, alpha))
    img = Image.alpha_composite(img, glow_layer)
draw = ImageDraw.Draw(img)

# Top trans stripe (20px)
sw = W / 5
for i, color in enumerate(STRIPE_COLORS):
    x0 = int(sw * i)
    x1 = int(sw * (i + 1)) + 1
    draw.rectangle([x0, 0, x1, 20], fill=color)

# Bottom trans stripe (20px)
for i, color in enumerate(STRIPE_COLORS):
    x0 = int(sw * i)
    x1 = int(sw * (i + 1)) + 1
    draw.rectangle([x0, H - 20, x1, H], fill=color)

# Use system fonts — try to find a bold and regular sans-serif
def get_font(size, bold=False):
    """Try system fonts, fall back to default."""
    names = []
    if bold:
        names = [
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/SFNSDisplay-Bold.otf",
            "/Library/Fonts/Arial Bold.ttf",
        ]
    else:
        names = [
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/SFNSDisplay.otf",
            "/Library/Fonts/Arial.ttf",
        ]
    for name in names:
        try:
            return ImageFont.truetype(name, size, index=1 if bold and name.endswith(".ttc") else 0)
        except (IOError, OSError):
            continue
    return ImageFont.load_default()


font_title = get_font(54, bold=True)
font_sub = get_font(22)
font_pill = get_font(14, bold=True)
font_footer = get_font(12)

# "TRANSMACROS.COM" centered
text = "TRANSMACROS.COM"
bbox = draw.textbbox((0, 0), text, font=font_title)
tw = bbox[2] - bbox[0]
draw.text(((W - tw) // 2, H // 2 - 80), text, fill=TRANS_BLUE, font=font_title)

# Subtitle
sub = "The only macro calculator built for trans bodies."
bbox = draw.textbbox((0, 0), sub, font=font_sub)
tw = bbox[2] - bbox[0]
draw.text(((W - tw) // 2, H // 2 - 20), sub, fill=WHITE, font=font_sub)

# Feature pills
pills = ["HRT-Aware", "Trans-Affirming", "Free, Always"]
pill_w, pill_h = 180, 38
pill_gap = 24
total_w = len(pills) * pill_w + (len(pills) - 1) * pill_gap
start_x = (W - total_w) // 2
pill_y = H // 2 + 40

for i, label in enumerate(pills):
    px = start_x + i * (pill_w + pill_gap)
    # Pill background with border
    draw.rounded_rectangle(
        [px, pill_y, px + pill_w, pill_y + pill_h],
        radius=pill_h // 2,
        fill=PILL_BG,
        outline=BORDER,
        width=2
    )
    # Dot accent
    dot_color = [TRANS_BLUE, TRANS_PINK, TRANS_WHITE][i]
    dot_cx = px + 22
    dot_cy = pill_y + pill_h // 2
    draw.ellipse([dot_cx - 4, dot_cy - 4, dot_cx + 4, dot_cy + 4], fill=dot_color)
    # Label
    bbox = draw.textbbox((0, 0), label, font=font_pill)
    lw = bbox[2] - bbox[0]
    lh = bbox[3] - bbox[1]
    draw.text((px + 34, pill_y + (pill_h - lh) // 2 - 1), label, fill=MUTED, font=font_pill)

# Footer text
footer = "Transform Fitness Coaching by Trey Sheidler"
bbox = draw.textbbox((0, 0), footer, font=font_footer)
tw = bbox[2] - bbox[0]
draw.text(((W - tw) // 2, H - 52), footer, fill=MUTED, font=font_footer)

# Save
output = "/Users/tshei/transmacros/og-image.png"
img.convert("RGB").save(output, "PNG")
print(f"OG image saved to {output}")
