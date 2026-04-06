#!/usr/bin/env python3
"""Generate Transform Fitness Macro Guide PDF."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import Paragraph, Frame, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle

W, H = letter  # 612 x 792

# Brand colors
NAVY = HexColor("#16213E")
RED = HexColor("#E94560")
WHITE = HexColor("#FFFFFF")
GRAY = HexColor("#B0B8C1")
DARK_NAVY = HexColor("#0F1829")
CARD_BG = HexColor("#1C2A4A")
TRANS_BLUE = HexColor("#5BCEFA")
TRANS_PINK = HexColor("#F5A9B8")
TRANS_WHITE = HexColor("#FFFFFF")

STRIPE_COLORS = [TRANS_BLUE, TRANS_PINK, TRANS_WHITE, TRANS_PINK, TRANS_BLUE]


def draw_bg(c):
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)


def draw_trans_stripe(c, y, height=6, width=None):
    if width is None:
        width = W
    sw = width / 5
    x_start = (W - width) / 2
    for i, color in enumerate(STRIPE_COLORS):
        c.setFillColor(color)
        c.rect(x_start + sw * i, y, sw + 0.5, height, fill=1, stroke=0)


def draw_red_bar(c, y, width=80):
    c.setFillColor(RED)
    c.rect(72, y, width, 3, fill=1, stroke=0)


def draw_card(c, x, y, w, h, fill=CARD_BG, border=None):
    c.setFillColor(fill)
    c.roundRect(x, y, w, h, 8, fill=1, stroke=0)
    if border:
        c.setStrokeColor(border)
        c.setLineWidth(1)
        c.roundRect(x, y, w, h, 8, fill=0, stroke=1)


def draw_footer(c, text="Transform Fitness Coaching by Trey Sheidler"):
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 7)
    c.drawCentredString(W / 2, 30, text)


def wrap_text(c, text, x, y, max_width, font="Helvetica", size=10, color=WHITE, leading=14):
    """Draw wrapped text and return the final y position."""
    c.setFont(font, size)
    c.setFillColor(color)
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test = current_line + (" " if current_line else "") + word
        if c.stringWidth(test, font, size) <= max_width:
            current_line = test
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def draw_section_header(c, text, y):
    draw_red_bar(c, y + 4)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, y - 18, text)
    return y - 36


def draw_subsection(c, text, y):
    c.setFillColor(RED)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(72, y, text)
    return y - 18


# ─── PAGE 1: COVER ───────────────────────────────────────────────────

def page_cover(c):
    draw_bg(c)

    # Top trans stripe
    draw_trans_stripe(c, H - 8, height=8)

    # Subtle glow circle — sized to contain all cover text
    cx, cy, cr = W / 2, H / 2 + 20, 260
    c.setFillColor(HexColor("#1A2D52"))
    c.circle(cx, cy, cr, fill=1, stroke=0)

    # Small stripe bar
    draw_trans_stripe(c, cy + 150, height=4, width=100)

    # Eyebrow
    c.setFillColor(TRANS_BLUE)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(cx, cy + 125, "TRANSFORM FITNESS COACHING")

    # Title
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 32)
    c.drawCentredString(cx, cy + 72, "Your Personalized")
    c.drawCentredString(cx, cy + 34, "Macro Guide")

    # Red accent line
    c.setFillColor(RED)
    c.rect(cx - 40, cy + 16, 80, 3, fill=1, stroke=0)

    # Subtitle
    c.setFillColor(TRANS_PINK)
    c.setFont("Helvetica", 14)
    c.drawCentredString(cx, cy - 14, "Built for trans, non-binary and intersex bodies")

    # Body text — wrapped to fit inside circle
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 10)
    body = "This guide explains your macro targets, how hormone therapy affects your metabolism, and how to adjust as your body evolves through transition."
    words = body.split()
    lines = []
    line = ""
    for w in words:
        test = line + (" " if line else "") + w
        if c.stringWidth(test, "Helvetica", 10) <= 340:
            line = test
        else:
            lines.append(line)
            line = w
    lines.append(line)
    ty = cy - 60
    for line in lines:
        c.drawCentredString(cx, ty, line)
        ty -= 16

    # Bottom trans stripe
    draw_trans_stripe(c, 55, height=4, width=100)

    # Footer
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 8)
    c.drawCentredString(W / 2, 38, "Transform Fitness Coaching by Trey Sheidler | Powered by Mystical Transcendence")

    c.showPage()


# ─── PAGE 2: UNDERSTANDING YOUR MACROS ──────────────────────────────

def page_macros(c):
    draw_bg(c)
    draw_trans_stripe(c, H - 6, height=6)

    y = draw_section_header(c, "UNDERSTANDING YOUR MACROS", H - 50)

    c.setFillColor(GRAY)
    c.setFont("Helvetica", 9.5)
    c.drawString(72, y, "Your macros are the three building blocks of every calorie you eat. Here's what each one does and why it matters.")
    y -= 30

    # Three macro cards
    card_w = (W - 144 - 24) / 3  # 3 cards with 12px gaps
    macros = [
        ("PROTEIN", TRANS_BLUE,
         "Builds and repairs muscle tissue. Your minimum is set based on your weight, goal, and how long "
         "you've been on hormones. This is a floor to protect muscle, not a ceiling. "
         "You can go higher if it fits your calories, but hitting this minimum is what matters most."),
        ("CARBOHYDRATES", TRANS_PINK,
         "Your body's primary fuel source for training and daily function. Carbs fill the calorie gap after protein and fats are set. "
         "More on training days for performance. Fewer on rest days in a deficit. "
         "They're flexible — this is the macro you adjust most when fine-tuning."),
        ("FATS", WHITE,
         "Essential for hormone production — especially important during HRT. Set at 25% of total calories as a floor. "
         "Supports brain function, vitamin absorption, and joint health. "
         "Don't cut below this — your body needs fats to regulate estrogen and testosterone."),
    ]

    for i, (title, accent, desc) in enumerate(macros):
        cx = 72 + i * (card_w + 12)
        card_h = 230
        draw_card(c, cx, y - card_h, card_w, card_h)

        # Accent top bar
        c.setFillColor(accent)
        c.rect(cx, y - 1, card_w, 3, fill=1, stroke=0)

        # Title
        c.setFillColor(accent)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(cx + 12, y - 22, title)

        # Description
        wrap_text(c, desc, cx + 12, y - 42, card_w - 24,
                  font="Helvetica", size=8, color=GRAY, leading=12)

    y -= 260

    # Calorie Cycling section
    y = draw_subsection(c, "CALORIE CYCLING", y)

    c.setFillColor(GRAY)
    c.setFont("Helvetica", 9.5)
    desc_text = ("Eating more on training days and less on rest days optimizes body recomposition. "
                 "Your calculator splits calories into training (+10%) and rest (-10%) targets.")
    y = wrap_text(c, desc_text, 72, y, W - 144, font="Helvetica", size=9.5, color=GRAY, leading=14)
    y -= 12

    # Two cycling cards side by side
    half = (W - 144 - 12) / 2
    # Training card
    draw_card(c, 72, y - 80, half, 80, border=TRANS_BLUE)
    c.setFillColor(TRANS_BLUE)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(72 + half / 2, y - 20, "TRAINING DAYS")
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(72 + half / 2, y - 48, "+10% Calories")
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 8)
    c.drawCentredString(72 + half / 2, y - 66, "More carbs to fuel performance")

    # Rest card
    rx = 72 + half + 12
    draw_card(c, rx, y - 80, half, 80, border=TRANS_PINK)
    c.setFillColor(TRANS_PINK)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(rx + half / 2, y - 20, "REST DAYS")
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(rx + half / 2, y - 48, "-10% Calories")
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 8)
    c.drawCentredString(rx + half / 2, y - 66, "Maintain deficit without losing muscle")

    y -= 110

    # Goal adjustment box
    draw_card(c, 72, y - 100, W - 144, 100, border=HexColor("#2A3F6A"))
    c.setFillColor(RED)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(86, y - 20, "GOAL ADJUSTMENTS")
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 9)
    goals = [
        ("Fat Loss:", "-500 cal/day from TDEE — targets ~1 lb/week loss"),
        ("Muscle Gain:", "+300 cal/day — fuels growth without excess fat"),
        ("Recomp:", "-200 cal/day — slow cut while building muscle"),
        ("Maintenance:", "No adjustment — sustain current composition"),
    ]
    gy = y - 38
    for label, desc in goals:
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(86, gy, label)
        lw = c.stringWidth(label, "Helvetica-Bold", 8.5)
        c.setFillColor(GRAY)
        c.setFont("Helvetica", 8.5)
        c.drawString(86 + lw + 6, gy, desc)
        gy -= 16

    draw_footer(c)
    c.showPage()


# ─── PAGE 3: HORMONES — TESTOSTERONE ────────────────────────────────

def page_hormones_t(c):
    draw_bg(c)
    draw_trans_stripe(c, H - 6, height=6)

    y = draw_section_header(c, "HOW HORMONES AFFECT YOUR METABOLISM", H - 50)

    c.setFillColor(GRAY)
    c.setFont("Helvetica", 9.5)
    intro = ("Standard macro calculators assume a static metabolism based on binary sex. "
             "But HRT fundamentally changes how your body burns calories, builds muscle, and stores fat. "
             "This section breaks down what happens and when.")
    y = wrap_text(c, intro, 72, y, W - 144, size=9.5, color=GRAY, leading=14)
    y -= 20

    # Trans Men section
    draw_red_bar(c, y + 4, width=60)
    c.setFillColor(TRANS_BLUE)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(72, y - 16, "Trans Men & AFAB Non-Binary on Testosterone")
    y -= 36

    c.setFillColor(GRAY)
    c.setFont("Helvetica", 9.5)
    t_intro = ("Testosterone increases your basal metabolic rate by up to 22% over 24 months. "
               "This is the most significant metabolic shift of any HRT protocol. "
               "Your body will require progressively more fuel as lean mass increases and fat distribution shifts.")
    y = wrap_text(c, t_intro, 72, y, W - 144, size=9.5, color=GRAY, leading=13)
    y -= 16

    # T Timeline table
    t_data = [
        ["TIMELINE", "METABOLIC CHANGE", "WHAT'S HAPPENING"],
        ["Months 1-3", "+1.5% per month",
         "Initial metabolic increase. Appetite rises. Body\ntemperature may increase. Early fat redistribution begins."],
        ["Months 3-6", "+4.5 to 9%",
         "Noticeable muscle gain with training. Metabolic rate\naccelerating. Calorie needs increasing meaningfully."],
        ["Months 6-12", "+9 to 18%",
         "Significant body recomposition. Fat shifting from\nhips/thighs to abdomen. Muscle protein synthesis\nelevated — protein needs are highest here."],
        ["Year 1-2+", "+18 to 22%",
         "Approaching metabolic plateau. BMR now closer to\ncis male range. Maintenance calories significantly\nhigher than pre-T baseline."],
    ]

    col_widths = [85, 110, W - 144 - 195]
    table_y = y
    row_heights = [22, 48, 48, 56, 56]

    for row_i, row in enumerate(t_data):
        rh = row_heights[row_i]
        ry = table_y - rh

        if row_i == 0:
            c.setFillColor(HexColor("#1A2D52"))
            c.rect(72, ry, W - 144, rh, fill=1, stroke=0)
            c.setFillColor(TRANS_BLUE)
            c.setFont("Helvetica-Bold", 7.5)
        else:
            if row_i % 2 == 0:
                c.setFillColor(CARD_BG)
                c.rect(72, ry, W - 144, rh, fill=1, stroke=0)

        cx = 72
        for col_i, cell in enumerate(row):
            if row_i == 0:
                c.setFillColor(TRANS_BLUE)
                c.setFont("Helvetica-Bold", 7.5)
                c.drawString(cx + 8, ry + rh - 14, cell)
            else:
                if col_i == 0:
                    c.setFillColor(WHITE)
                    c.setFont("Helvetica-Bold", 8.5)
                    c.drawString(cx + 8, ry + rh - 14, cell)
                elif col_i == 1:
                    c.setFillColor(TRANS_BLUE)
                    c.setFont("Helvetica-Bold", 9)
                    c.drawString(cx + 8, ry + rh - 14, cell)
                else:
                    c.setFillColor(GRAY)
                    c.setFont("Helvetica", 8)
                    lines = cell.split("\n")
                    ly = ry + rh - 14
                    for line in lines:
                        c.drawString(cx + 8, ly, line)
                        ly -= 11
            cx += col_widths[col_i]

        # Row border
        c.setStrokeColor(HexColor("#2A3F6A"))
        c.setLineWidth(0.5)
        c.line(72, ry, W - 72, ry)

        table_y = ry

    y = table_y - 20

    # Protein callout
    draw_card(c, 72, y - 60, W - 144, 60, border=TRANS_BLUE)
    c.setFillColor(TRANS_BLUE)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(86, y - 18, "PROTEIN NOTE FOR TRANS MEN")
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 8.5)
    c.drawString(86, y - 34, "After 12 months on T, protein minimum is bumped by +0.1g/lb (capped at 0.9g/lb) to support")
    c.drawString(86, y - 46, "increased muscle protein synthesis. This keeps the floor protective without overemphasizing protein.")

    draw_footer(c)
    c.showPage()


# ─── PAGE 4: HORMONES — ESTROGEN + NON-BINARY/INTERSEX ──────────────

def page_hormones_e(c):
    draw_bg(c)
    draw_trans_stripe(c, H - 6, height=6)

    y = H - 50
    draw_red_bar(c, y + 4, width=60)
    c.setFillColor(TRANS_PINK)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(72, y - 16, "Trans Women & AMAB Non-Binary on Estrogen")
    y -= 36

    c.setFillColor(GRAY)
    c.setFont("Helvetica", 9.5)
    e_intro = ("Estrogen combined with anti-androgens gradually reduces your basal metabolic rate by up to 6% over 6 months. "
               "While the percentage is smaller than testosterone's effect, it's metabolically significant — "
               "and under-eating during this period is one of the most common mistakes.")
    y = wrap_text(c, e_intro, 72, y, W - 144, size=9.5, color=GRAY, leading=13)
    y -= 16

    e_data = [
        ["TIMELINE", "METABOLIC CHANGE", "WHAT'S HAPPENING"],
        ["Months 1-3", "-1% per month",
         "Early metabolic slowdown. Body begins retaining\nmore subcutaneous fat. Muscle mass slowly decreasing."],
        ["Months 3-6", "-3 to 6%",
         "Fat redistribution accelerating (breasts, hips, thighs).\nMetabolic rate stabilizing at new baseline. Appetite\nmay decrease."],
        ["Month 6+", "Plateau at -6%",
         "Metabolic rate stabilized. Body composition closer to\ncis female ranges. Maintenance calories now\npermanently lower than pre-HRT."],
    ]

    col_widths = [85, 110, W - 144 - 195]
    row_heights = [22, 48, 56, 48]

    for row_i, row in enumerate(e_data):
        rh = row_heights[row_i]
        ry = y - rh

        if row_i == 0:
            c.setFillColor(HexColor("#1A2D52"))
            c.rect(72, ry, W - 144, rh, fill=1, stroke=0)
            c.setFillColor(TRANS_PINK)
            c.setFont("Helvetica-Bold", 7.5)
        else:
            if row_i % 2 == 0:
                c.setFillColor(CARD_BG)
                c.rect(72, ry, W - 144, rh, fill=1, stroke=0)

        cx = 72
        for col_i, cell in enumerate(row):
            if row_i == 0:
                c.setFillColor(TRANS_PINK)
                c.setFont("Helvetica-Bold", 7.5)
                c.drawString(cx + 8, ry + rh - 14, cell)
            else:
                if col_i == 0:
                    c.setFillColor(WHITE)
                    c.setFont("Helvetica-Bold", 8.5)
                    c.drawString(cx + 8, ry + rh - 14, cell)
                elif col_i == 1:
                    c.setFillColor(TRANS_PINK)
                    c.setFont("Helvetica-Bold", 9)
                    c.drawString(cx + 8, ry + rh - 14, cell)
                else:
                    c.setFillColor(GRAY)
                    c.setFont("Helvetica", 8)
                    lines = cell.split("\n")
                    ly = ry + rh - 14
                    for line in lines:
                        c.drawString(cx + 8, ly, line)
                        ly -= 11
            cx += col_widths[col_i]

        c.setStrokeColor(HexColor("#2A3F6A"))
        c.setLineWidth(0.5)
        c.line(72, ry, W - 72, ry)
        y = ry

    y -= 14

    # Warning callout
    draw_card(c, 72, y - 52, W - 144, 52, border=TRANS_PINK)
    c.setFillColor(TRANS_PINK)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(86, y - 16, "DON'T UNDER-EAT")
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 8.5)
    c.drawString(86, y - 32, "Your body needs adequate fuel to transition safely. Aggressive calorie cuts during early HRT")
    c.drawString(86, y - 44, "can stall fat redistribution and compromise breast development. Eat at or near maintenance for the first 6 months.")

    y -= 80

    # Non-Binary section
    draw_trans_stripe(c, y + 8, height=3, width=60)
    y -= 6
    y = draw_subsection(c, "NON-BINARY CONSIDERATIONS", y)

    nb_text = ("Non-binary individuals on partial or low-dose HRT receive a partial metabolic adjustment: "
               "+9% for AFAB on low-dose T, -3% for AMAB on low-dose E. "
               "These reflect the reduced hormonal impact of non-standard dosing protocols. "
               "If you're on a full dose, the full adjustment applies regardless of identity.")
    y = wrap_text(c, nb_text, 72, y, W - 144, size=9.5, color=GRAY, leading=13)
    y -= 24

    # Intersex section
    draw_trans_stripe(c, y + 8, height=3, width=60)
    y -= 6
    y = draw_subsection(c, "INTERSEX INDIVIDUALS", y)

    ix_text = ("For intersex individuals, the calculator uses your current hormonal environment — "
               "not a binary birth sex assumption — to calculate BMR. "
               "Options include primarily estrogenic, primarily androgenic, mixed/uncertain, or on HRT. "
               "This gives a more accurate metabolic baseline than any calculator that forces a binary choice.")
    y = wrap_text(c, ix_text, 72, y, W - 144, size=9.5, color=GRAY, leading=13)
    y -= 20

    draw_card(c, 72, y - 45, W - 144, 45, border=HexColor("#2A3F6A"))
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(86, y - 16, "Mixed/uncertain hormonal environment:")
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 8.5)
    c.drawString(86, y - 32, "BMR uses the midpoint between male and female Mifflin-St Jeor constants (-78 instead of +5 or -161).")

    draw_footer(c)
    c.showPage()


# ─── PAGE 5: WHEN TO RECALCULATE ────────────────────────────────────

def page_recalculate(c):
    draw_bg(c)
    draw_trans_stripe(c, H - 6, height=6)

    y = draw_section_header(c, "WHEN TO RECALCULATE YOUR MACROS", H - 50)

    c.setFillColor(GRAY)
    c.setFont("Helvetica", 9.5)
    c.drawString(72, y, "Your macros aren't set in stone. Recalculate when any of these happen:")
    y -= 28

    triggers = [
        ("Weight changes by 10+ lbs", "Your calorie needs scale with body weight. A 10-lb shift means your protein minimum, TDEE, and macro split all need updating."),
        ("HRT milestone (3, 6, 12, 24 mo)", "Each milestone brings measurable metabolic changes. The calculator's HRT adjustment curve updates at these points."),
        ("Goal changes", "Switching from fat loss to muscle gain (or vice versa) changes your calorie target by 500-800 calories. Don't keep old macros for a new goal."),
        ("Activity level changes", "Starting a new training program, changing jobs, or going from sedentary to active shifts your TDEE significantly."),
        ("Plateau lasting 3+ weeks", "If the scale hasn't moved and measurements are flat for 3 weeks, your body has adapted. Time for new numbers."),
        ("Surgery recovery", "Top surgery, bottom surgery, or any major procedure changes your activity level and recovery needs temporarily."),
        ("Stopping or starting HRT", "Any change to your hormone protocol means your metabolic rate is shifting. Recalculate immediately."),
    ]

    for trigger, desc in triggers:
        # Row background
        draw_card(c, 72, y - 46, W - 144, 44)
        c.setFillColor(RED)
        c.rect(72, y - 46, 4, 44, fill=1, stroke=0)

        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(86, y - 14, trigger)
        c.setFillColor(GRAY)
        c.setFont("Helvetica", 8)
        # Wrap description
        wrap_text(c, desc, 86, y - 28, W - 144 - 28, font="Helvetica", size=8, color=GRAY, leading=11)
        y -= 52

    y -= 10

    # Five tips header
    draw_red_bar(c, y + 4, width=60)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(72, y - 14, "5 PRACTICAL TIPS")
    y -= 34

    tips_5 = [
        "Weigh yourself at the same time daily (morning, post-bathroom) and use a weekly average — not daily fluctuations.",
        "Track your food for at least 2 weeks before deciding your macros aren't working. Consistency reveals patterns.",
        "If you're on injectable T or E, expect slight water weight fluctuations around injection days. This is normal.",
        "Take progress photos monthly. The mirror and scale lie — photos over time tell the real story.",
        "Don't compare your timeline to anyone else's. HRT affects everyone differently.",
    ]

    for i, tip in enumerate(tips_5):
        c.setFillColor(RED)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(72, y, str(i + 1))
        y = wrap_text(c, tip, 90, y, W - 144 - 18, font="Helvetica", size=9, color=GRAY, leading=12)
        y -= 10

    draw_footer(c)
    c.showPage()


# ─── PAGE 6: MAKING IT WORK ─────────────────────────────────────────

def page_daily(c):
    draw_bg(c)
    draw_trans_stripe(c, H - 6, height=6)

    y = draw_section_header(c, "MAKING IT WORK DAY TO DAY", H - 50)

    c.setFillColor(GRAY)
    c.setFont("Helvetica", 9.5)
    intro = "Knowing your macros is step one. Here's how to actually hit them consistently."
    y = wrap_text(c, intro, 72, y, W - 144, size=9.5, color=GRAY, leading=14)
    y -= 16

    daily_tips = [
        ("Hit your protein minimum every day",
         "Spread your protein across 3-4 meals. Front-loading protein at breakfast makes the rest of the day easier. "
         "Aim for 20-35g per meal depending on your total. If you're struggling to hit it, a protein shake counts. "
         "Going over is fine. Just make sure you clear the floor."),
        ("Prep your carbs around training",
         "Eat the majority of your carbs before and after your workout. This fuels performance and speeds recovery. "
         "On rest days, shift some carb calories to fats for satiety. The total stays the same — just the timing changes."),
        ("Don't fear fats — but measure them",
         "Fats are calorically dense (9 cal/g vs 4 cal/g for protein and carbs). A tablespoon of olive oil is 120 calories. "
         "Measure cooking fats and dressings until you can eyeball portions accurately. This is where most tracking errors hide."),
        ("Use the calorie slider for real life",
         "The adjustment slider on your results page exists for a reason. Had a light day? Slide down 100-150 calories. "
         "Heavy training session? Slide up. The goal is a weekly average, not daily perfection."),
        ("Build a meal rotation",
         "You don't need 30 different recipes. Find 4-5 meals that hit your macros and rotate them. "
         "Meal prep on Sunday. Eat the same lunch Monday through Friday. Boring works. "
         "Save variety for dinner and weekends."),
    ]

    for i, (title, desc) in enumerate(daily_tips):
        # Number circle
        c.setFillColor(RED)
        c.circle(84, y - 2, 11, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(84, y - 6, str(i + 1))

        # Title
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(102, y, title)
        y -= 16

        # Description
        y = wrap_text(c, desc, 102, y, W - 144 - 30, font="Helvetica", size=8.5, color=GRAY, leading=12)
        y -= 16

    y -= 4

    # CTA Box
    cta_h = 110
    # Gradient-ish effect with layered rects
    c.setFillColor(HexColor("#1C2A4A"))
    c.roundRect(72, y - cta_h, W - 144, cta_h, 10, fill=1, stroke=0)
    # Top accent
    c.setFillColor(RED)
    c.rect(72, y - 1, W - 144, 3, fill=1, stroke=0)

    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(W / 2, y - 28, "Want support that actually understands your body?")

    c.setFillColor(GRAY)
    c.setFont("Helvetica", 9.5)
    c.drawCentredString(W / 2, y - 48, "Get personalized coaching, community, and accountability from someone who gets it.")

    c.setFillColor(TRANS_BLUE)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(W / 2, y - 72, "transformfitness.net")

    ig_text = "@treynertrey on Instagram"
    c.setFillColor(TRANS_PINK)
    c.setFont("Helvetica", 10)
    ig_width = c.stringWidth(ig_text, "Helvetica", 10)
    ig_x = (W - ig_width) / 2
    ig_y = y - 90
    c.drawString(ig_x, ig_y, ig_text)
    c.linkURL("https://www.instagram.com/treynertrey", (ig_x, ig_y - 2, ig_x + ig_width, ig_y + 12), relative=0)

    # Bottom trans stripe
    draw_trans_stripe(c, 50, height=4, width=100)

    draw_footer(c, "© 2026 Transform Fitness Coaching by Trey Sheidler | Powered by Mystical Transcendence")
    c.showPage()


# ─── BUILD PDF ───────────────────────────────────────────────────────

def main():
    output = "/Users/tshei/transmacros/transform_fitness_macro_guide.pdf"
    c = canvas.Canvas(output, pagesize=letter)
    c.setTitle("Your Personalized Macro Guide — Transform Fitness")
    c.setAuthor("Trey Sheidler / Transform Fitness Coaching")

    page_cover(c)
    page_macros(c)
    page_hormones_t(c)
    page_hormones_e(c)
    page_recalculate(c)
    page_daily(c)

    c.save()
    print(f"PDF saved to {output}")


if __name__ == "__main__":
    main()
