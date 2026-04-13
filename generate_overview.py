#!/usr/bin/env python3
"""Generate Transform Fitness TransMacros System Overview PDF."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas

W, H = letter

NAVY = HexColor("#16213E")
RED = HexColor("#E94560")
WHITE = HexColor("#FFFFFF")
GRAY = HexColor("#B0B8C1")
CARD_BG = HexColor("#1C2A4A")
TRANS_BLUE = HexColor("#5BCEFA")
TRANS_PINK = HexColor("#F5A9B8")
TRANS_WHITE = HexColor("#FFFFFF")
STRIPE_COLORS = [TRANS_BLUE, TRANS_PINK, TRANS_WHITE, TRANS_PINK, TRANS_BLUE]
BORDER_COLOR = HexColor("#2A3F6A")


def draw_bg(c):
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)


def draw_stripe(c, y, height=6, width=None):
    if width is None:
        width = W
    sw = width / 5
    x0 = (W - width) / 2
    for i, color in enumerate(STRIPE_COLORS):
        c.setFillColor(color)
        c.rect(x0 + sw * i, y, sw + 0.5, height, fill=1, stroke=0)


def draw_red_bar(c, y, width=80):
    c.setFillColor(RED)
    c.rect(72, y, width, 3, fill=1, stroke=0)


def section_header(c, text, y):
    draw_red_bar(c, y + 4)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(72, y - 16, text)
    return y - 32


def subsection(c, text, y, color=RED):
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(72, y, text)
    return y - 16


def body(c, text, x, y, max_w=None, size=9, color=GRAY, leading=13, font="Helvetica"):
    if max_w is None:
        max_w = W - 144
    c.setFont(font, size)
    c.setFillColor(color)
    words = text.split()
    lines, line = [], ""
    for w in words:
        test = line + (" " if line else "") + w
        if c.stringWidth(test, font, size) <= max_w:
            line = test
        else:
            lines.append(line)
            line = w
    if line:
        lines.append(line)
    for ln in lines:
        c.drawString(x, y, ln)
        y -= leading
    return y


def bullet(c, text, y, indent=84, size=9, leading=13):
    c.setFillColor(TRANS_BLUE)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(74, y + 1, "\u2022")
    return body(c, text, indent, y, max_w=W - indent - 72, size=size, leading=leading)


def card(c, x, y, w, h, border=None):
    c.setFillColor(CARD_BG)
    c.roundRect(x, y, w, h, 6, fill=1, stroke=0)
    if border:
        c.setStrokeColor(border)
        c.setLineWidth(1)
        c.roundRect(x, y, w, h, 6, fill=0, stroke=1)


def footer(c, text="Transform Fitness Coaching by Trey Sheidler"):
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 7)
    c.drawCentredString(W / 2, 28, text)


# ═══════════════════════════════════════════════════════════════
# PAGE 1 — COVER
# ═══════════════════════════════════════════════════════════════
def page_cover(c):
    draw_bg(c)
    draw_stripe(c, H - 8, 8)

    # Glow
    c.setFillColor(HexColor("#1A2D52"))
    c.circle(W / 2, H / 2 + 20, 220, fill=1, stroke=0)

    draw_stripe(c, H / 2 + 155, 4, 100)

    c.setFillColor(TRANS_BLUE)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(W / 2, H / 2 + 125, "TRANSFORM FITNESS COACHING")

    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(W / 2, H / 2 + 70, "Trans Macro Calculator")

    c.setFillColor(RED)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(W / 2, H / 2 + 40, "System Overview")

    c.setFillColor(RED)
    c.rect(W / 2 - 40, H / 2 + 22, 80, 3, fill=1, stroke=0)

    c.setFillColor(GRAY)
    c.setFont("Helvetica", 11)
    c.drawCentredString(W / 2, H / 2 - 10, "How we attract, capture, nurture, and convert")
    c.drawCentredString(W / 2, H / 2 - 26, "trans and queer leads into clients")

    draw_stripe(c, 55, 4, 100)
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 8)
    c.drawCentredString(W / 2, 38, "Transform Fitness Coaching by Trey Sheidler | Powered by Mystical Transcendence")

    c.showPage()


# ═══════════════════════════════════════════════════════════════
# PAGE 2 — THE CALCULATOR
# ═══════════════════════════════════════════════════════════════
def page_calculator(c):
    draw_bg(c)
    draw_stripe(c, H - 6, 6)
    y = section_header(c, "THE CALCULATOR", H - 50)

    y = subsection(c, "WHAT IT IS", y, TRANS_BLUE)
    y = body(c, "transmacros.com \u2014 the first macro calculator built specifically for trans, non-binary, and intersex bodies. "
             "Accounts for HRT stage, hormonal environment, gender identity, and fitness goals. Free, always.", 72, y)
    y -= 10

    y = subsection(c, "HOW IT WORKS", y, TRANS_BLUE)
    y = body(c, "6-step form collecting body stats, gender identity, HRT status, activity level, goals, and segmentation questions. "
             "Results include personalized macros, HRT adjustment explanation, calorie cycling, supplement recommendations, "
             "and a shareable results card with download and social sharing.", 72, y)
    y -= 10

    # 6 steps in a grid
    steps = [
        ("Step 1: Stats", "Weight, height, age,\nimperial/metric toggle"),
        ("Step 2: Identity", "Birth sex, intersex options,\ngender identity, hormonal env"),
        ("Step 3: HRT", "On/off toggle, duration\nin months, TDEE preview"),
        ("Step 4: Goals", "Activity level (1.2\u20131.9),\ngoal: cut/gain/recomp/maintain"),
        ("Step 5: You", "Challenge, GLP-1 awareness,\ncommunity interest"),
        ("Step 6: Results", "Email gate, first name,\nphone (optional), unlock"),
    ]
    col_w = (W - 144 - 12) / 3
    row_h = 62
    for i, (title, desc) in enumerate(steps):
        col = i % 3
        row = i // 3
        sx = 72 + col * (col_w + 6)
        sy = y - row * (row_h + 6) - row_h
        card(c, sx, sy, col_w, row_h, border=BORDER_COLOR)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(sx + 10, sy + row_h - 16, title)
        c.setFillColor(GRAY)
        c.setFont("Helvetica", 7.5)
        for j, line in enumerate(desc.split("\n")):
            c.drawString(sx + 10, sy + row_h - 30 - j * 10, line)

    y -= 2 * (row_h + 6) + 16

    y = subsection(c, "LEAD CAPTURE", y, TRANS_BLUE)
    y = body(c, "Email gate before results. Collects first name, email, and optional phone number. "
             "All data is sent to GoHighLevel via inbound webhook on form submission.", 72, y)
    y -= 10

    y = subsection(c, "TAGS APPLIED", y, TRANS_BLUE)
    tags = [
        "macro-calculator (always)",
        "trans-man / trans-woman / non-binary (based on identity)",
        "on-hrt (if HRT toggle is on)",
        "fat-loss / muscle-gain / recomp / maintenance (based on goal)",
        "glp1-interested (if any GLP-1 interest expressed)",
        "scale-not-moving / dont-know-what-to-eat / no-structured-program / need-accountability / just-starting-out (challenge)",
    ]
    for tag in tags:
        y = bullet(c, tag, y, size=8.5, leading=12)
        y -= 1

    footer(c)
    c.showPage()


# ═══════════════════════════════════════════════════════════════
# PAGE 3 — EMAIL NURTURE SEQUENCE
# ═══════════════════════════════════════════════════════════════
def page_nurture(c):
    draw_bg(c)
    draw_stripe(c, H - 6, 6)
    y = section_header(c, "EMAIL NURTURE SEQUENCE", H - 50)

    y = body(c, "Automated email sequence triggered when a contact is created from the calculator webhook. "
             "Each email is personalized based on the contact's tags — gender identity, goal, HRT status, and challenge.", 72, y)
    y -= 14

    emails = [
        ("EMAIL 1", "Immediate", "Welcome + Macro Guide",
         "Welcome email with personalized macro guide PDF attached. Confirms their results, "
         "explains how to use the guide, and sets expectations for the sequence."),
        ("EMAIL 2", "Day 2", "Gender-Specific Nutrition",
         "Trans men receive testosterone and metabolism content \u2014 protein timing, muscle synthesis on T, calorie increases. "
         "Trans women receive estrogen and body composition content \u2014 fat redistribution, not under-eating, hormone-supportive nutrition. "
         "Non-binary contacts receive HRT-aware content tailored to partial or low-dose protocols."),
        ("EMAIL 3", "Day 5", "Goal-Specific Supplements",
         "Supplement recommendation email matched to their goal tag. Fat loss: protein + recovery stack. "
         "Muscle gain: Surge creatine + protein. Recomp: creatine + recovery. Maintenance: general sports nutrition. "
         "All products from Mystical Transcendence with direct shop links."),
        ("EMAIL 4", "Day 9", "Recalculation Guide",
         "When and how to update macros as body and HRT change. Covers the 7 triggers: weight change, "
         "HRT milestones, goal changes, activity changes, plateaus, surgery recovery, starting/stopping HRT. "
         "Links back to transmacros.com to recalculate."),
        ("EMAIL 5", "Day 14", "Challenge-Specific",
         "Personalized email based on their biggest challenge tag. Scale not moving: plateau-breaking strategies. "
         "Don't know what to eat: simple meal rotation framework. No structured program: Essentials intro. "
         "Need accountability: coaching CTA. Just starting out: beginner orientation."),
        ("EMAIL 6", "Day 21", "Community Invite",
         "Free Skool community invite \u2014 skool.com/transformfitnesscommunity. Positions the community as "
         "a space for trans people supporting each other without needing to explain pronouns or identity."),
    ]

    for label, timing, subject, desc in emails:
        card_h = 72 if len(desc) < 200 else 82
        card(c, 72, y - card_h, W - 144, card_h, border=BORDER_COLOR)

        # Red left accent
        c.setFillColor(RED)
        c.rect(72, y - card_h, 4, card_h, fill=1, stroke=0)

        # Label + timing
        c.setFillColor(TRANS_BLUE)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(86, y - 14, label)
        c.setFillColor(GRAY)
        c.setFont("Helvetica", 8)
        lw = c.stringWidth(label, "Helvetica-Bold", 9)
        c.drawString(86 + lw + 8, y - 14, "(" + timing + ")")

        # Subject
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(86, y - 28, subject)

        # Description
        body(c, desc, 86, y - 42, max_w=W - 144 - 28, size=7.5, leading=10)

        y -= card_h + 6

    footer(c)
    c.showPage()


# ═══════════════════════════════════════════════════════════════
# PAGE 4 — DOWNSTREAM OFFERS
# ═══════════════════════════════════════════════════════════════
def page_offers(c):
    draw_bg(c)
    draw_stripe(c, H - 6, 6)
    y = section_header(c, "DOWNSTREAM OFFERS", H - 50)

    y = body(c, "Calculator leads are funneled into paid products through targeted email sequences, "
             "results page CTAs, and tag-based workflow triggers.", 72, y)
    y -= 14

    # GLP-1
    card_h = 115
    card(c, 72, y - card_h, W - 144, card_h, border=TRANS_PINK)
    c.setFillColor(TRANS_PINK)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(86, y - 18, "GLP-1 MEDICAL WEIGHT LOSS PROGRAM")
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 8.5)
    body(c, "Contacts tagged glp1-interested enter a separate nurture sequence. Day 1 email explains the program. "
         "Day 5 email covers the 90-day journey and results.", 86, y - 34, max_w=W - 144 - 28, size=8.5, leading=12)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(86, y - 68, "Landing page:")
    c.setFillColor(TRANS_BLUE)
    c.setFont("Helvetica", 8.5)
    c.drawString(160, y - 68, "glp1.transformfitness.net")
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(86, y - 82, "Pricing:")
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 8.5)
    c.drawString(130, y - 82, "Semaglutide $689/12 weeks  |  Tirzepatide $999/12 weeks")
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 8)
    c.drawString(86, y - 96, "Essentials membership included free with all GLP-1 programs.")
    y -= card_h + 12

    # Essentials
    card_h = 80
    card(c, 72, y - card_h, W - 144, card_h, border=TRANS_BLUE)
    c.setFillColor(TRANS_BLUE)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(86, y - 18, "ESSENTIALS MEMBERSHIP")
    c.setFillColor(GRAY)
    body(c, "Promoted in every email sequence. $29/month recurring. Structured workout programs, meal planner, "
         "and progress tracking built for trans bodies.", 86, y - 34, max_w=W - 144 - 28, size=8.5, leading=12)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(86, y - 62, "Landing page:")
    c.setFillColor(TRANS_BLUE)
    c.setFont("Helvetica", 8.5)
    c.drawString(160, y - 62, "essentials.transformfitness.net")
    y -= card_h + 12

    # Supplements
    card_h = 80
    card(c, 72, y - card_h, W - 144, card_h, border=HexColor("#8134AF"))
    c.setFillColor(HexColor("#8134AF"))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(86, y - 18, "MYSTICAL TRANSCENDENCE SUPPLEMENTS")
    c.setFillColor(GRAY)
    body(c, "Dynamic supplement recommendations on the results page based on goal. Products: Surge creatine, "
         "protein line, recovery and hydration formulas.", 86, y - 34, max_w=W - 144 - 28, size=8.5, leading=12)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(86, y - 62, "Store:")
    c.setFillColor(TRANS_BLUE)
    c.setFont("Helvetica", 8.5)
    c.drawString(118, y - 62, "mysticaltranscendence.com")
    y -= card_h + 12

    # 1:1 Coaching
    card_h = 90
    card(c, 72, y - card_h, W - 144, card_h, border=RED)
    c.setFillColor(RED)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(86, y - 18, "1:1 COACHING")
    c.setFillColor(GRAY)
    body(c, "Referenced as the premium option for personalized accountability. Three tiers based on level of support and access.", 86, y - 34, max_w=W - 144 - 28, size=8.5, leading=12)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 8.5)
    tiers = [
        ("Momentum", "$247/mo"),
        ("All-In", "$397/mo"),
        ("Elite", "$997/mo"),
    ]
    tx = 86
    for name, price in tiers:
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(tx, y - 60, name)
        nw = c.stringWidth(name, "Helvetica-Bold", 8.5)
        c.setFillColor(GRAY)
        c.setFont("Helvetica", 8.5)
        c.drawString(tx + nw + 4, y - 60, price)
        tx += nw + c.stringWidth(price, "Helvetica", 8.5) + 24

    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(86, y - 76, "Landing page:")
    c.setFillColor(TRANS_BLUE)
    c.setFont("Helvetica", 8.5)
    c.drawString(160, y - 76, "transformfitness.net")

    footer(c)
    c.showPage()


# ═══════════════════════════════════════════════════════════════
# PAGE 5 — PROGRESS AND REVIEW SEQUENCE
# ═══════════════════════════════════════════════════════════════
def page_progress(c):
    draw_bg(c)
    draw_stripe(c, H - 6, 6)
    y = section_header(c, "PROGRESS AND REVIEW SEQUENCE", H - 50)

    y = body(c, "Three-email check-in sequence starting Day 14 after the main nurture completes. "
             "Designed to re-engage contacts, prompt recalculation, and collect testimonials.", 72, y)
    y -= 14

    checkins = [
        ("DAY 14", "2-Week Check-In Survey",
         "Short survey asking about progress, whether macros feel right, and if they've started tracking. "
         "Links to the GHL survey widget. Responses are stored on the contact record for coaching follow-up."),
        ("DAY 30", "1-Month Check-In + Recalculation Prompt",
         "Checks in on progress and prompts a macro recalculation if weight has changed by 10+ lbs or they've hit "
         "an HRT milestone. Links back to transmacros.com. Includes Essentials CTA for contacts not yet subscribed."),
        ("DAY 60", "Testimonial and Story Request",
         "Asks the contact to share their experience. Includes a link to a testimonial submission form with fields for "
         "their story, a before/after photo upload (optional), and a share permission checkbox."),
    ]

    for timing, subject, desc in checkins:
        card_h = 78
        card(c, 72, y - card_h, W - 144, card_h, border=BORDER_COLOR)
        c.setFillColor(RED)
        c.rect(72, y - card_h, 4, card_h, fill=1, stroke=0)

        c.setFillColor(TRANS_BLUE)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(86, y - 16, timing)
        tw = c.stringWidth(timing, "Helvetica-Bold", 10)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(86 + tw + 10, y - 16, subject)

        body(c, desc, 86, y - 34, max_w=W - 144 - 28, size=8.5, leading=12)
        y -= card_h + 8

    y -= 10
    draw_stripe(c, y + 6, 3, 60)
    y -= 8
    y = subsection(c, "TESTIMONIAL APPROVAL WORKFLOW", y)

    y = body(c, "When a contact submits the 60-day survey and grants share permission:", 72, y)
    y -= 4
    y = bullet(c, "Contact is tagged testimonial-approved in GHL", y)
    y -= 2
    y = bullet(c, "Internal notification is sent to Trey via email and in-app alert", y)
    y -= 2
    y = bullet(c, "Testimonial text and photo are stored as custom fields on the contact record", y)
    y -= 2
    y = bullet(c, "Approved testimonials can be added to the calculator landing page and marketing materials", y)
    y -= 16

    # Future state box
    card(c, 72, y - 70, W - 144, 70, border=BORDER_COLOR)
    c.setFillColor(RED)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(86, y - 18, "FUTURE STATE")
    c.setFillColor(GRAY)
    body(c, "Automated testimonial display on transmacros.com \u2014 pulling approved testimonials from GHL "
         "via API and rendering them in the social proof section. Currently using a placeholder CTA: "
         "\"Real results coming soon. Be one of the first to share yours.\"", 86, y - 34, max_w=W - 144 - 28, size=8.5, leading=12)

    footer(c)
    c.showPage()


# ═══════════════════════════════════════════════════════════════
# PAGE 6 — TECH STACK AND KEY URLS
# ═══════════════════════════════════════════════════════════════
def page_tech(c):
    draw_bg(c)
    draw_stripe(c, H - 6, 6)
    y = section_header(c, "TECH STACK AND KEY URLS", H - 50)

    # URLs table
    urls = [
        ("Calculator", "transmacros.com", "GitHub Pages"),
        ("GHL Account", "app.transformfitness.net", "GoHighLevel"),
        ("Essentials", "essentials.transformfitness.net", "Trainerize-backed"),
        ("GLP-1 Program", "glp1.transformfitness.net", "GHL Funnel"),
        ("Coaching", "transformfitness.net", "Main site"),
        ("Supplements", "mysticaltranscendence.com", "Shopify"),
        ("Community", "skool.com/transformfitnesscommunity", "Skool"),
    ]

    # Table header
    card(c, 72, y - 24, W - 144, 24)
    c.setFillColor(TRANS_BLUE)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(86, y - 16, "PROPERTY")
    c.drawString(230, y - 16, "URL")
    c.drawString(440, y - 16, "PLATFORM")
    y -= 24

    for prop, url, platform in urls:
        row_h = 22
        if urls.index((prop, url, platform)) % 2 == 0:
            c.setFillColor(CARD_BG)
            c.rect(72, y - row_h, W - 144, row_h, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(86, y - 14, prop)
        c.setFillColor(TRANS_BLUE)
        c.setFont("Helvetica", 8.5)
        c.drawString(230, y - 14, url)
        c.setFillColor(GRAY)
        c.setFont("Helvetica", 8.5)
        c.drawString(440, y - 14, platform)
        y -= row_h

    y -= 20
    draw_stripe(c, y + 6, 3, 60)
    y -= 8
    y = subsection(c, "KEY TOOLS", y)

    tools = [
        ("GoHighLevel", "CRM, workflows, email sequences, SMS, webhooks, surveys, funnels. Central hub for all lead management and automation."),
        ("GitHub Pages", "Hosts transmacros.com. Calculator is a single index.html file with inline CSS and JS. Deployed via git push to main."),
        ("ReportLab + Pillow", "Python libraries for PDF guide generation (macro guide) and OG image generation. Scripts stored in the repo."),
        ("Trainerize", "Fitness app backend powering the Essentials membership. Handles workout programming, meal plans, and client metrics. Never referenced publicly \u2014 clients see it as \"Essentials by Transform Fitness.\""),
        ("Shopify", "Powers mysticaltranscendence.com for supplement sales. Integrated with calculator results page via direct product links."),
        ("Skool", "Free community platform. Positioned as a safe space for trans fitness support. Promoted in email sequence and on results page conditionally."),
    ]

    for name, desc in tools:
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(72, y, name)
        y -= 14
        y = body(c, desc, 72, y, size=8.5, leading=11)
        y -= 8

    # Bottom box
    y -= 6
    card(c, 72, y - 55, W - 144, 55, border=RED)
    c.setFillColor(RED)
    c.rect(72, y - 1, W - 144, 3, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(W / 2, y - 22, "Transform Fitness Coaching by Trey Sheidler")
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 9)
    c.drawCentredString(W / 2, y - 38, "transmacros.com  |  transformfitness.net  |  mysticaltranscendence.com")

    draw_stripe(c, 50, 4, 100)
    footer(c, "\u00a9 2026 Transform Fitness Coaching by Trey Sheidler | Powered by Mystical Transcendence")
    c.showPage()


# ═══════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════
def main():
    output = "/Users/tshei/transmacros/transform_fitness_transmacros_overview.pdf"
    c = canvas.Canvas(output, pagesize=letter)
    c.setTitle("Trans Macro Calculator \u2014 System Overview")
    c.setAuthor("Trey Sheidler / Transform Fitness Coaching")

    page_cover(c)
    page_calculator(c)
    page_nurture(c)
    page_offers(c)
    page_progress(c)
    page_tech(c)

    c.save()
    print(f"PDF saved to {output}")


if __name__ == "__main__":
    main()
