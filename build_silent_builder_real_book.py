from math import exp, log

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    KeepTogether,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


OUT = "The_Silent_Builder_Real_Book.pdf"

PAGE_W, PAGE_H = letter
MARGIN_X = 0.78 * inch
MARGIN_Y = 0.72 * inch
USABLE_W = PAGE_W - 2 * MARGIN_X

INK = colors.HexColor("#15211D")
MUTED = colors.HexColor("#66726E")
DEEP = colors.HexColor("#101A17")
DEEP_2 = colors.HexColor("#1D2B26")
PAPER = colors.HexColor("#F7F1E7")
SOFT = colors.HexColor("#FFFDF8")
LINE = colors.HexColor("#D9DED6")
OLIVE = colors.HexColor("#536B45")
CLAY = colors.HexColor("#A45D3C")
GOLD = colors.HexColor("#BD8B35")
BLUE = colors.HexColor("#315D70")
RED = colors.HexColor("#8A3D32")
MIST = colors.HexColor("#EEF1EA")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle("CoverKicker", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=GOLD, alignment=TA_CENTER, spaceAfter=12))
styles.add(ParagraphStyle("CoverTitle", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=35, leading=39, textColor=colors.white, alignment=TA_CENTER, spaceAfter=14))
styles.add(ParagraphStyle("CoverSub", parent=styles["Normal"], fontName="Helvetica", fontSize=13, leading=18, textColor=colors.HexColor("#EAE0D0"), alignment=TA_CENTER, spaceAfter=14))
styles.add(ParagraphStyle("PartLabel", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=9, leading=11, textColor=GOLD, alignment=TA_CENTER, spaceAfter=7))
styles.add(ParagraphStyle("ChapterTitle", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=27, leading=31, textColor=colors.white, alignment=TA_CENTER, spaceAfter=9))
styles.add(ParagraphStyle("ChapterSub", parent=styles["Normal"], fontName="Helvetica", fontSize=10.5, leading=15, textColor=colors.HexColor("#E9E0D0"), alignment=TA_CENTER))
styles.add(ParagraphStyle("H1", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=20, leading=25, textColor=INK, spaceBefore=5, spaceAfter=10))
styles.add(ParagraphStyle("H2", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=14, leading=18, textColor=CLAY, spaceBefore=13, spaceAfter=7))
styles.add(ParagraphStyle("Body", parent=styles["BodyText"], fontName="Helvetica", fontSize=10.45, leading=15.8, textColor=INK, spaceAfter=8))
styles.add(ParagraphStyle("BodyTight", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.5, leading=13.5, textColor=INK, spaceAfter=5))
styles.add(ParagraphStyle("Small", parent=styles["BodyText"], fontName="Helvetica", fontSize=8.4, leading=11.3, textColor=MUTED, spaceAfter=4))
styles.add(ParagraphStyle("Quote", parent=styles["BodyText"], fontName="Helvetica-Oblique", fontSize=10.1, leading=15, textColor=colors.HexColor("#3F4B47"), leftIndent=20, rightIndent=14, spaceBefore=7, spaceAfter=10))
styles.add(ParagraphStyle("BulletBook", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.9, leading=14.5, leftIndent=16, firstLineIndent=-8, textColor=INK, spaceAfter=5))
styles.add(ParagraphStyle("Callout", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.8, leading=14.2, textColor=INK))
styles.add(ParagraphStyle("CardTitle", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=10.0, leading=12.5, textColor=INK, spaceAfter=4))
styles.add(ParagraphStyle("CardText", parent=styles["BodyText"], fontName="Helvetica", fontSize=8.8, leading=11.8, textColor=colors.HexColor("#53615D")))
styles.add(ParagraphStyle("TOC", parent=styles["BodyText"], fontName="Helvetica", fontSize=10.2, leading=14.2, textColor=INK, spaceAfter=5))
styles.add(ParagraphStyle("Source", parent=styles["BodyText"], fontName="Helvetica", fontSize=8.2, leading=11.1, textColor=colors.HexColor("#4E5D59"), spaceAfter=5))


def P(text, style="Body"):
    return Paragraph(text, styles[style])


def H(text):
    return P(text, "H1")


def S(text):
    return P(text, "H2")


def Q(text):
    return P(text, "Quote")


def B(text):
    return P("- " + text, "BulletBook")


class ChapterOpener(Flowable):
    def __init__(self, number, title, subtitle):
        super().__init__()
        self.number = number
        self.title = title
        self.subtitle = subtitle
        self.height = 198

    def wrap(self, aw, ah):
        self.width = aw
        return aw, self.height

    def draw(self):
        c = self.canv
        w = self.width
        h = self.height
        c.saveState()
        c.setFillColor(DEEP)
        c.roundRect(0, 0, w, h, 8, fill=1, stroke=0)
        c.setFillColor(DEEP_2)
        c.roundRect(12, 12, w - 24, h - 24, 6, fill=1, stroke=0)
        c.setStrokeColor(GOLD)
        c.setLineWidth(1)
        c.roundRect(22, 22, w - 44, h - 44, 5, fill=0, stroke=1)
        c.restoreState()

        flow = [
            P(f"CHAPTER {self.number}", "PartLabel"),
            P(self.title, "ChapterTitle"),
            P(self.subtitle, "ChapterSub"),
        ]
        tw = w - 70
        th = 0
        wrapped = []
        for item in flow:
            iw, ih = item.wrap(tw, h)
            th += ih
            wrapped.append((item, iw, ih))
        y = (h + th) / 2 - 6
        for item, iw, ih in wrapped:
            y -= ih
            item.drawOn(c, 35, y)


class VisualPlate(Flowable):
    def __init__(self, kind, title, caption, height=210):
        super().__init__()
        self.kind = kind
        self.title = title
        self.caption = caption
        self.height = height

    def wrap(self, aw, ah):
        self.width = aw
        return aw, self.height

    def draw(self):
        c = self.canv
        w = self.width
        h = self.height
        c.saveState()
        c.setFillColor(colors.white)
        c.roundRect(0, 0, w, h, 8, fill=1, stroke=0)
        c.setStrokeColor(LINE)
        c.roundRect(0, 0, w, h, 8, fill=0, stroke=1)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(16, h - 24, self.title)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 8)
        c.drawString(16, 12, self.caption[:120])
        draw_method = getattr(self, f"draw_{self.kind}", self.draw_stack)
        draw_method(c, 18, 34, w - 36, h - 68)
        c.restoreState()

    def axes(self, c, x, y, w, h):
        c.setStrokeColor(colors.HexColor("#C8D0C6"))
        c.setLineWidth(0.8)
        c.line(x, y, x, y + h)
        c.line(x, y, x + w, y)

    def draw_compounding(self, c, x, y, w, h):
        self.axes(c, x, y, w, h)
        c.setFont("Helvetica", 7)
        c.setFillColor(MUTED)
        c.drawString(x, y - 12, "Day 1")
        c.drawRightString(x + w, y - 12, "Day 365")
        points = []
        for i in range(0, 61):
            t = i / 60
            linear = t
            comp = (exp(2.7 * t) - 1) / (exp(2.7) - 1)
            points.append((x + w * t, y + h * comp))
            if i > 0:
                x0 = x + w * (i - 1) / 60
                y0 = y + h * linear * ((i - 1) / i if i else 1)
        c.setStrokeColor(colors.HexColor("#9AA79C"))
        c.setDash(2, 3)
        c.line(x, y, x + w, y + h * 0.55)
        c.setDash()
        c.setStrokeColor(GOLD)
        c.setLineWidth(2.2)
        for a, b in zip(points, points[1:]):
            c.line(a[0], a[1], b[0], b[1])
        c.setFillColor(GOLD)
        c.circle(points[-1][0], points[-1][1], 3, fill=1, stroke=0)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 8.2)
        c.drawString(x + w * 0.47, y + h * 0.80, "compounded discipline")
        c.setFillColor(MUTED)
        c.drawString(x + w * 0.45, y + h * 0.47, "linear effort")

    def draw_feedback(self, c, x, y, w, h):
        boxes = [
            ("Stimulus", x + 0.03*w, y + 0.58*h),
            ("Desire", x + 0.36*w, y + 0.58*h),
            ("Action", x + 0.69*w, y + 0.58*h),
            ("Identity", x + 0.36*w, y + 0.18*h),
        ]
        for label, bx, by in boxes:
            c.setFillColor(MIST)
            c.roundRect(bx, by, 0.24*w, 0.20*h, 6, fill=1, stroke=0)
            c.setStrokeColor(LINE)
            c.roundRect(bx, by, 0.24*w, 0.20*h, 6, fill=0, stroke=1)
            c.setFillColor(INK)
            c.setFont("Helvetica-Bold", 9)
            c.drawCentredString(bx + 0.12*w, by + 0.09*h, label)
        c.setStrokeColor(CLAY)
        c.setLineWidth(1.6)
        def arrow(x1, y1, x2, y2):
            c.line(x1, y1, x2, y2)
            c.circle(x2, y2, 2.2, fill=1, stroke=0)
        arrow(x + 0.27*w, y + 0.68*h, x + 0.36*w, y + 0.68*h)
        arrow(x + 0.60*w, y + 0.68*h, x + 0.69*w, y + 0.68*h)
        arrow(x + 0.81*w, y + 0.58*h, x + 0.53*w, y + 0.38*h)
        arrow(x + 0.41*w, y + 0.38*h, x + 0.16*w, y + 0.58*h)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 8)
        c.drawString(x + 0.05*w, y + 0.02*h, "Whatever you repeat trains what feels normal next time.")

    def draw_trust(self, c, x, y, w, h):
        labels = ["Low trust", "High trust"]
        vals = [0.80, 0.28]
        for i, (lab, val) in enumerate(zip(labels, vals)):
            bx = x + i * (w * 0.50) + 0.06*w
            c.setFillColor(MIST if i else colors.HexColor("#F4E6E1"))
            c.roundRect(bx, y, 0.33*w, h, 6, fill=1, stroke=0)
            c.setFillColor(RED if i == 0 else OLIVE)
            c.rect(bx + 0.10*w, y + 0.16*h, 0.13*w, h * val, fill=1, stroke=0)
            c.setFillColor(INK)
            c.setFont("Helvetica-Bold", 9)
            c.drawCentredString(bx + 0.165*w, y + 0.05*h, lab)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 8)
        c.drawCentredString(x + 0.50*w, y + 0.88*h, "Monitoring, fear, contracts, checks, delay")

    def draw_ai(self, c, x, y, w, h):
        rows = [
            ("Routine output", 0.75, RED),
            ("Tool literacy", 0.62, BLUE),
            ("Judgment", 0.88, OLIVE),
            ("Trust", 0.82, OLIVE),
            ("Learning speed", 0.86, GOLD),
        ]
        c.setFont("Helvetica", 8)
        for i, (lab, val, col) in enumerate(rows):
            yy = y + h - (i + 1) * (h / 6)
            c.setFillColor(INK)
            c.drawString(x, yy + 4, lab)
            c.setFillColor(colors.HexColor("#E7ECE6"))
            c.roundRect(x + 120, yy, w - 140, 10, 5, fill=1, stroke=0)
            c.setFillColor(col)
            c.roundRect(x + 120, yy, (w - 140) * val, 10, 5, fill=1, stroke=0)
        c.setFillColor(MUTED)
        c.drawRightString(x + w, y + 4, "AI age value pressure")

    def draw_hours(self, c, x, y, w, h):
        labels = ["30 days", "1 year", "5 years"]
        vals = [60, 730, 3650]
        maxv = max(vals)
        c.setFont("Helvetica", 8)
        for i, (lab, val) in enumerate(zip(labels, vals)):
            yy = y + h - (i + 1) * (h / 4)
            c.setFillColor(INK)
            c.drawString(x, yy + 4, lab)
            c.setFillColor(colors.HexColor("#E7ECE6"))
            c.roundRect(x + 95, yy, w - 115, 12, 6, fill=1, stroke=0)
            c.setFillColor(CLAY if i < 2 else RED)
            c.roundRect(x + 95, yy, (w - 115) * (val / maxv), 12, 6, fill=1, stroke=0)
            c.setFillColor(MUTED)
            c.drawRightString(x + w, yy + 3, f"{val:,} hours")
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 8)
        c.drawString(x, y + 4, "Assumption: 2 hours/day of low-value scrolling or distraction.")

    def draw_pressure(self, c, x, y, w, h):
        centers = [
            ("Phone", x + 0.22*w, y + 0.68*h, RED),
            ("Friends", x + 0.78*w, y + 0.68*h, CLAY),
            ("Ego", x + 0.22*w, y + 0.25*h, GOLD),
            ("Fear", x + 0.78*w, y + 0.25*h, BLUE),
        ]
        c.setFillColor(OLIVE)
        c.circle(x + 0.50*w, y + 0.48*h, 34, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(x + 0.50*w, y + 0.48*h - 3, "Heart")
        c.setStrokeColor(MUTED)
        c.setLineWidth(1.2)
        for lab, cx, cy, col in centers:
            c.setFillColor(col)
            c.circle(cx, cy, 24, fill=1, stroke=0)
            c.setFillColor(colors.white)
            c.setFont("Helvetica-Bold", 8)
            c.drawCentredString(cx, cy - 3, lab)
            c.setStrokeColor(col)
            c.line(cx, cy, x + 0.50*w, y + 0.48*h)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 8)
        c.drawCentredString(x + 0.50*w, y + 0.02*h, "The heart sticks to what repeatedly pulls it.")

    def draw_horizon(self, c, x, y, w, h):
        segments = [("Tonight", 0.15, RED), ("1 year", 0.27, CLAY), ("10 years", 0.31, GOLD), ("Akhirah", 0.27, OLIVE)]
        cur = x
        for label, frac, col in segments:
            c.setFillColor(col)
            c.rect(cur, y + 0.36*h, w * frac, 0.16*h, fill=1, stroke=0)
            c.setFillColor(INK)
            c.setFont("Helvetica-Bold", 8)
            c.drawCentredString(cur + w*frac/2, y + 0.22*h, label)
            cur += w * frac
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 8)
        c.drawCentredString(x + w/2, y + 0.68*h, "A larger horizon changes what counts as a rational choice.")

    def draw_stack(self, c, x, y, w, h):
        layers = [
            ("Purpose", DEEP),
            ("Purification", OLIVE),
            ("Judgment", BLUE),
            ("Strength", GOLD),
            ("Service", CLAY),
        ]
        layer_h = h / len(layers)
        for i, (lab, col) in enumerate(layers):
            yy = y + i * layer_h
            c.setFillColor(col)
            c.roundRect(x + i*9, yy, w - i*18, layer_h - 6, 5, fill=1, stroke=0)
            c.setFillColor(colors.white)
            c.setFont("Helvetica-Bold", 9)
            c.drawCentredString(x + w/2, yy + layer_h/2 - 1, lab)


def callout(title, body, fill=PAPER, border=GOLD):
    t = Table([[P(f"<b>{title}</b><br/>{body}", "Callout")]], colWidths=[USABLE_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), fill),
        ("BOX", (0, 0), (-1, -1), 0.8, border),
        ("LEFTPADDING", (0, 0), (-1, -1), 13),
        ("RIGHTPADDING", (0, 0), (-1, -1), 13),
        ("TOPPADDING", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 11),
    ]))
    return t


def card(title, body):
    t = Table([[P(title, "CardTitle")], [P(body, "CardText")]], colWidths=[(USABLE_W - 12) / 2])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.white),
        ("BOX", (0, 0), (-1, -1), 0.6, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def card_grid(items):
    rows = []
    for i in range(0, len(items), 2):
        left = card(items[i][0], items[i][1])
        right = card(items[i + 1][0], items[i + 1][1]) if i + 1 < len(items) else ""
        rows.append([left, right])
    t = Table(rows, colWidths=[(USABLE_W - 12) / 2, (USABLE_W - 12) / 2])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def cover_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(DEEP)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setFillColor(DEEP_2)
    canvas.rect(0.45 * inch, 0.45 * inch, PAGE_W - 0.9 * inch, PAGE_H - 0.9 * inch, fill=1, stroke=0)
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(1.15)
    canvas.rect(0.72 * inch, 0.72 * inch, PAGE_W - 1.44 * inch, PAGE_H - 1.44 * inch, fill=0, stroke=1)
    canvas.restoreState()


def body_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7.8)
    canvas.drawString(MARGIN_X, 0.35 * inch, "The Silent Builder")
    canvas.drawRightString(PAGE_W - MARGIN_X, 0.35 * inch, str(doc.page))
    canvas.restoreState()


def chapter(st, number, title, subtitle):
    st.append(PageBreak())
    st.append(ChapterOpener(number, title, subtitle))
    st.append(Spacer(1, 10))


def build_story():
    st = []
    cover_box = Table([
        [P("A PRIVATE BOOK FOR KNOWLEDGE AND IMPLEMENTATION", "CoverKicker")],
        [P("The Silent Builder", "CoverTitle")],
        [P("An Islamic and evidence-informed book on deep growth, hidden leverage, self-mastery, future readiness, and building quietly for Allah.", "CoverSub")],
        [P("Read slowly. Return often. Implement quietly.", "CoverSub")],
    ], colWidths=[USABLE_W - 0.8 * inch])
    cover_box.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    st += [Spacer(1, 2.28 * inch), cover_box, NextPageTemplate("Body")]

    chapter(st, "0", "How To Read This Book", "This is not a dashboard or a reference table. It is a readable knowledge book: a map of purpose, hidden forces, skills, evidence, and implementation.")
    st.append(P("This book is meant to gather the whole analysis into one readable place. It is not a motivational speech. It is a worldview, a diagnosis, and a practical path. The aim is not to create a temporary emotional high. The aim is to make the truth easier to revisit until it becomes instinct."))
    st.append(P("Read it like a book first. Then return to the chapters that expose your current weakness. If you are distracted, return to attention and the nafs. If you are confused, return to the Islamic operating system. If you are talking too much, return to the silent builder principle. If you are inspired but not acting, return to implementation."))
    st.append(callout("The central conclusion", "The highest version of you is not the richest, loudest, or most admired version. It is the version that used the maximum of what Allah entrusted to him: faith, mind, body, time, wealth, speech, influence, pain, opportunity, and responsibility."))
    st.append(S("Plain-English meanings"))
    st.append(card_grid([
        ["Ibadah", "Worship as whole-life orientation: prayer, study, work, money, family duty, speech, and service when done lawfully and sincerely."],
        ["Akhirah", "The afterlife. It expands the time horizon beyond death and changes what success means."],
        ["Tazkiyah", "Cleaning the inner self: arrogance, showing off, envy, lust, anger, greed, laziness, and fear of people."],
        ["Hikmah", "Wisdom: knowing what matters, when it matters, and how to act without being ruled by impulse."],
        ["Quwwah", "Prepared strength: spiritual, physical, financial, intellectual, emotional, social, and technical capacity."],
        ["Amanah", "Trustworthiness: being safe with people's time, money, secrets, rights, and expectations."],
    ]))

    chapter(st, "1", "The Question Beneath Self-Improvement", "The real aim is not to become impressive. The real aim is to become a prepared servant of Allah.")
    st.append(P("Most self-improvement begins from anxiety. A person feels behind, weak, unseen, poor, unattractive, confused, or dependent. Then he asks: how can I become better? That question is not wrong, but it is incomplete. Better according to what? Better for whom? Better for how long? Better in the eyes of people, the market, the family, the ego, or Allah?"))
    st.append(P("This is where the Islamic lens changes the project. Islam does not ask you to become impressive. It asks you to become true. It does not rank skills only by salary, status, dominance, or social admiration. It asks whether those skills bring you closer to Allah, purify the self, benefit creation, establish justice, carry responsibility, and survive into the afterlife."))
    st.append(P("That does not make worldly strength irrelevant. It makes worldly strength accountable. A weak sincere person may be beloved, but their ability to protect, provide, build, teach, heal, and serve can be limited. A strong corrupt person may achieve scale, but their strength becomes a weapon for the ego. The target is neither weakness nor egoic dominance. The target is strength with trust."))
    st.append(VisualPlate("stack", "The Growth Stack", "Purpose supports purification; purification protects judgment; judgment directs strength; strength becomes service.", height=190))
    st.append(P("The secular world often says: build leverage. Islam says: purify the lever-holder. Both are needed. If you build leverage without purification, you become more efficient at spreading your diseases. If you purify yourself without building capacity, your benefit remains smaller than it could have been."))
    st.append(Q("The path is not skill collection. The path is orientation, purification, strength, service, and legacy."))

    chapter(st, "2", "The Islamic Operating System", "Islam is not a ritual compartment. It is a total life architecture: worship, stewardship, accountability, wisdom, strength, trust, and service.")
    st.append(P("The first correction is this: worship is not only ritual. Prayer, fasting, charity, and recitation are foundations, but the broader Islamic meaning of worship includes everything done sincerely, lawfully, and in alignment with Allah. Study can become worship. Work can become worship. Earning can become worship. Serving family can become worship. Learning a difficult skill can become worship. Restraining yourself from a sin can become worship."))
    st.append(P("This changes the emotional weight of life. You are not simply trying to optimize a career. You are trying to fulfill a trust. You are not merely a consumer of experiences. You are a responsible soul moving toward judgment. You are not just trying to survive dunya. You are planting through dunya."))
    st.append(S("Purpose and stewardship"))
    st.append(P("The Qur'an gives the purpose of creation as worship of Allah. If this is true, then your life cannot be divided into religious and non-religious compartments in the shallow sense. The question becomes: how do I make my mind, body, money, study, work, family, and influence obedient to the purpose of creation?"))
    st.append(P("Stewardship means you are responsible for what has been placed under your care: your body, mind, time, opportunities, family roles, speech, and decisions. This is not fantasy. It is accountable living."))
    st.append(S("The afterlife changes the mathematics"))
    st.append(P("A purely secular system optimizes for a short biological window. Islam expands the horizon beyond death. This means hidden worship matters. Quiet sacrifice matters. Pain nobody saw matters. Injustice nobody repaired matters. A small sincere deed may become more valuable than a public achievement built on ego."))
    st.append(VisualPlate("horizon", "Time Horizon Changes The Decision", "When the horizon expands, short-term pleasure loses some of its power.", height=170))
    st.append(S("Prepared strength"))
    st.append(P("The Qur'anic command to prepare whatever strength one is able teaches a principle of serious readiness. In personal life, this includes spiritual strength, physical health, knowledge, financial competence, technical skill, emotional regulation, family responsibility, and strategic awareness. Weakness should not be romanticized. Strength should not be worshipped. It should be prepared and disciplined."))

    chapter(st, "3", "Behind The Scenes Logic", "The same conclusion keeps appearing because revelation, history, biology, economics, and technology all expose the same human pattern.")
    st.append(P("The reason this framework feels like deja vu is that the same law keeps appearing in different clothing. Islam calls you to purify the self, prepare strength, seek wisdom, keep trust, and serve creation. Psychology says self-regulation, attention, identity, and environment shape behavior. Economics says incentives, scarcity, trust, and allocation shape outcomes. Future-of-work research says routine output becomes less protected while judgment, learning, resilience, and social trust rise in value. These are not disconnected ideas. They are different lenses on one reality."))
    st.append(P("Behind the scenes, most people lose because their operating system is not integrated. They may study, but their sleep is broken. They may want deen, but their phone owns their attention. They may want money, but they do not understand spending, debt, or skill markets. They may want confidence, but they keep breaking promises to themselves. They may want Allah, but their heart is trained daily by people, feeds, fantasies, and fears."))
    st.append(S("The chain nobody sees"))
    st.append(P("Input becomes attention. Attention becomes thought. Thought becomes desire. Desire becomes action. Action becomes habit. Habit becomes identity. Identity becomes destiny, unless Allah guides and the person interrupts the chain. This is why Islam is so serious about eyes, ears, speech, food, company, prayer, remembrance, and repentance. The heart is not isolated. It is being trained all day."))
    st.append(VisualPlate("pressure", "The Heart Is Pulled By Repeated Inputs", "The question is not only what you believe. The question is what repeatedly gets access to your heart.", height=205))
    st.append(S("The cold logic"))
    for item in [
        "If two people have equal intelligence, the one with better attention wins more often.",
        "If two people have equal skill, the more trustworthy one scales more safely.",
        "If two people have equal ambition, the one with longer patience survives more valleys.",
        "If two people have equal knowledge, the one with a cleaner heart uses it with less corruption.",
        "If two people have equal opportunity, the one who silently executes while the other talks usually moves further.",
    ]:
        st.append(B(item))
    st.append(callout("Why this matters", "You are not trying to collect impressive ideas. You are trying to find the few laws that keep repeating across deen, dunya, body, market, family, and history, then live by them before regret teaches them harder."))

    chapter(st, "4", "The Secret Of The World", "The visible world rewards invisible structures. People see outcomes late. Allah sees roots immediately.")
    st.append(P("The secret of this world is not a conspiracy. It is that most outcomes are produced by hidden structures long before they become visible. People see the job, the money, the calmness, the confidence, the body, the writing, the influence, the family stability, or the spiritual presence. They do not see the repeated private choices that made those things possible."))
    st.append(P("The world is full of systems designed to capture the weak parts of the human being. Attention is mined. Desire is monetized. Outrage is amplified. Lust is packaged. Envy is stimulated. Status anxiety is turned into consumption. Boredom is treated as a business opportunity. If a person does not govern himself, he becomes raw material for other people's algorithms."))
    st.append(VisualPlate("feedback", "Environment Becomes Identity", "Repeated inputs become repeated choices; repeated choices become identity.", height=205))
    st.append(S("The invisible forces"))
    for item in [
        "Time horizon: the person who can think in years beats the person trapped in tonight.",
        "Environment: friends, feeds, rooms, and routines repeatedly suggest what is normal.",
        "Trust: reliable people move faster because others do not waste energy protecting themselves from them.",
        "Compounding: repeated small actions become large realities later.",
        "The unseen: hidden effort, hidden sin, hidden pain, and hidden sincerity all matter before Allah.",
    ]:
        st.append(B(item))
    st.append(callout("The dangerous balance", "Dunya is not worthless. It is a tool, a test, a training ground, and a field for planting. The error is not using the world. The error is being used by it."))

    chapter(st, "5", "Why Most People Never Live This", "The problem is rarely lack of information. The problem is friction.")
    st.append(P("Most people know enough to begin. They know prayer matters. They know the phone wastes time. They know sleep matters. They know bad friends affect them. They know study requires focus. They know money requires discipline. They know anger damages relationships. Yet knowing does not automatically become living."))
    st.append(P("Why? Because the body wants comfort now. The ego wants praise without correction. The lower self wants reward without purification. The environment wants you to remain recognizable. The phone wants attention. The market wants consumption. Friends may want company in distraction. Even family pressure can make the future feel too heavy to face."))
    st.append(S("The common traps"))
    st.append(card_grid([
        ["Cheap dopamine", "Fast pleasure makes deep work feel painfully slow."],
        ["Information addiction", "Learning feels like action, so no real change happens."],
        ["Ego protection", "The self hates being a beginner, being corrected, or being seen changing."],
        ["Present-pull people", "People optimized for short-term pleasure often pull others toward the same horizon."],
        ["False reliance", "Trust in Allah is misused as passivity instead of effort plus surrender."],
        ["Hopelessness", "Stress can make the future feel fake and the present feel inescapable."],
    ]))
    st.append(callout("The hard truth", "If you wait until discipline feels natural, you may wait for years. Discipline often feels unnatural at first because you are training against an old identity."))

    st.append(S("Cold facts that should sober you"))
    st.append(P("A person does not need to become evil to waste his life. He only needs to remain distractible, inconsistent, emotionally reactive, and vague about responsibility. A young person can lose years without noticing because each day looks recoverable. But time does not return as raw material. It returns as consequences."))
    st.append(VisualPlate("hours", "The Cost Of Two Hours A Day", "Small daily leakage becomes a serious life tax.", height=190))
    st.append(P("This is why the phone is not a small side issue. If two hours a day disappear into low-value distraction, that is about 730 hours a year. In five years, it is about 3,650 hours. That is enough time to become serious at a valuable skill, memorize meaningful knowledge, build a portfolio, strengthen a body, repair family duties, and deepen worship. The issue is not that relaxation is haram. The issue is leakage without intention."))

    chapter(st, "6", "The Silent Builder Principle", "Do not announce every transformation. Build quietly until the root is strong enough to withstand weather.")
    st.append(P("One of the most important principles in this framework is silence. Not secrecy in an arrogant way. Not refusing to teach sincere people. Not acting mysterious. The point is protection. Early transformation is fragile. If you expose it too early, people can turn it into debate, mockery, performance, pressure, or identity."))
    st.append(P("Not everyone will understand a long-term view. Some people will tell you to enjoy the present. Sometimes they love you and simply cannot see what you see. Sometimes they are insecure because your effort reminds them of their own avoidance. Sometimes they are not malicious at all; they are just operating on a shorter horizon. But if you let every short-horizon voice enter your command center, your direction will dissolve."))
    st.append(P("Silent building means you remain warm with people, but private with your deepest intentions. You share what is beneficial. You do not explain your entire plan to people who are not responsible for helping you protect it. You do not turn discipline into a personality costume. You do not announce every streak, every repentance, every ambition, every inner change."))
    st.append(Q("The seed does not need applause. It needs soil, water, time, and protection."))
    st.append(callout("Silent builder sentence", "I do not need to be understood at the seed stage. I need to be sincere, consistent, and protected from unnecessary noise."))

    chapter(st, "7", "The Skills That Actually Multiply A Life", "Domain skills add. Meta-skills multiply. Islam gives the aim, hierarchy, and guardrails.")
    st.append(P("Coding, finance, design, writing, business, and AI tools matter. But they are not the deepest layer. They are domain skills. They can add value, but the skills underneath them multiply everything. The deeper skills determine how quickly you learn, how clearly you think, how well you communicate, how reliably people trust you, how calmly you act under pressure, and how ethically you use power."))
    for title, body in [
        ("Correct understanding and sound judgment", "Seeing truth, priority, consequence, and self-deception clearly. Without this, even good intentions can become harmful."),
        ("Self-mastery", "Governing desire, anger, laziness, ego, fear, envy, and attention. A person who cannot govern himself will be governed by the world."),
        ("Noble character", "Trustworthiness, honesty, dignity, courage, fairness, gentleness, restraint, and keeping promises. Poor character corrupts wealth, leadership, knowledge, influence, and even religious work."),
        ("Beneficial communication", "Speech can guide, reconcile, teach, heal, protect truth, or destroy families and communities. Writing is externalized thinking. Speaking is responsibility made audible."),
        ("Seeking and applying knowledge", "The higher sequence is learning, internalizing, implementing, and teaching. Knowledge that never changes action becomes evidence against a person."),
        ("Service and responsibility", "Islam values people who carry burdens, solve problems, provide stability, protect others, feed families, and uplift communities."),
        ("Systems and leverage", "The leap from effort to scale happens when you build systems: code, writing, teaching, products, institutions, workflows, capital, and communities."),
        ("Financial and technical literacy", "Money and technology determine independence, family protection, community capacity, and service. Learn them lawfully. Use them responsibly. Do not worship them."),
    ]:
        st.append(KeepTogether([S(title), P(body)]))
    st.append(VisualPlate("trust", "Trust Reduces Friction", "Amanah is not only moral beauty; it is also practical leverage.", height=190))

    chapter(st, "8", "The Body, Attention, And The Nafs", "Your spiritual and intellectual life is affected by sleep, stress, dopamine, food, movement, and what you repeatedly look at.")
    st.append(P("A person is not a floating mind. The body matters. Sleep deprivation weakens judgment. Chronic stress narrows perception. Constant stimulation makes silence painful. Lust clouds dignity. Anger hijacks speech. Poor food and no movement lower energy. This is not separate from spirituality. The body is a trust and a vehicle."))
    st.append(P("The lower self does not always attack through obvious evil. Sometimes it attacks through comfort, delay, entertainment, comparison, self-pity, or the sentence 'later'. The phone is especially dangerous because it combines novelty, social comparison, lust, outrage, entertainment, and escape in one object."))
    st.append(S("The practical correction"))
    for item in [
        "Guard sleep as a performance and worship tool.",
        "Move the body daily, even if modestly.",
        "Keep the phone away from the first and last part of the day.",
        "Use fasting and restraint to train desire.",
        "Do not make major decisions in an activated emotional state.",
        "Treat focus as a sacred resource, not an unlimited supply.",
    ]:
        st.append(B(item))

    S_title = "How to make the heart stick"
    st.append(S(S_title))
    st.append(P("The heart does not stick to truth by one emotional realization. It sticks through repeated exposure, repeated obedience, and repeated rescue from what weakens it. This is why reminders matter. This is why prayer repeats. This is why Qur'an is recited again and again. This is why company matters. This is why secret worship matters. The heart becomes loyal to what it repeatedly returns to."))
    for item in [
        "Give the heart a daily appointment with Allah before the world gets its first claim.",
        "Make repentance quick. Delay turns a mistake into a residence.",
        "Reduce the inputs that make obedience feel strange.",
        "Keep one private good deed that nobody can praise.",
        "Read or listen to something that reopens the unseen every day, even briefly.",
        "Attach your ambition to service, not ego. Ego burns out when unseen; service survives.",
    ]:
        st.append(B(item))
    st.append(callout("Heart rule", "The heart follows repetition more than claims. If you say Allah is first but give your freshest attention to the phone, the heart learns the phone is first."))

    chapter(st, "9", "Money, Work, AI, And The 2030 Shift", "The age is changing. Ordinary output gets cheaper. Judgment, trust, originality, and learning speed become more valuable.")
    st.append(P("AI commoditizes many shouting skills: ordinary coding, ordinary writing, ordinary analysis, ordinary design, ordinary research summaries. This does not make humans useless. It makes shallow skill less protected. The premium moves toward judgment, taste, trust, ethics, leadership, original thinking, human understanding, and the ability to learn continuously."))
    st.append(VisualPlate("ai", "Future Skill Pressure", "Directional synthesis from WEF and McKinsey: routine output is less protected; judgment, trust, and learning speed rise.", height=205))
    st.append(P("A Muslim should not respond to this shift with panic or passivity. The correct response is preparation. Learn useful tools. Understand AI. Build technical literacy. But do not outsource your thinking, conscience, or responsibility. A tool can accelerate you, but if it replaces your effort to understand, it weakens the very faculty that makes you valuable."))
    st.append(P("Money should also be understood. Income is flow. Wealth is stored capacity. Debt can become enslavement. Capital can become service. Halal earning protects dignity. Giving purifies the heart. Financial ignorance can make a person dependent, easily pressured, and unable to help those they love."))
    st.append(callout("Future-proof direction", "Become a person who can think, learn, communicate, build trust, use tools, serve real needs, and remain morally anchored under pressure.", fill=colors.HexColor("#E5EEF1"), border=BLUE))

    st.append(S("The uncomfortable work reality"))
    st.append(P("Future-of-work research does not say everyone must become a programmer and nothing else matters. It says the ground is shifting. Technology-related skills matter, but so do analytical thinking, resilience, leadership, social influence, curiosity, and lifelong learning. This means the lazy technical person is not safe, and the non-technical person who refuses to learn is not safe either. The safer path is an integrated stack: use tools, think clearly, communicate well, keep trust, learn quickly, and remain morally anchored."))
    st.append(P("AI also makes deception easier. It can generate confident text, images, summaries, and code. That increases the value of verification, sincerity, direct experience, and people who can take responsibility. In a world where output becomes cheap, the person behind the output matters more, not less."))

    chapter(st, "10", "The Simple Math Of Becoming", "The math is simple enough to live: repeated inputs, honest feedback, and long horizons create disproportionate futures.")
    st.append(P("Compounding means small repeated actions become large over time. This is why tiny habits are not tiny. One focused hour a day becomes hundreds of hours a year. One page of writing a day becomes a body of thought. One sincere act repeated becomes character. One ignored sin repeated becomes a chain."))
    st.append(VisualPlate("compounding", "Compounding Makes Early Effort Look Unfair Later", "The curve is flat early, which is why most people quit before the bend.", height=210))
    st.append(P("Opportunity cost means every yes is also a no. Saying yes to scrolling is saying no to attention. Saying yes to useless argument is saying no to dignity. Saying yes to sleep discipline is saying yes to tomorrow's mind."))
    st.append(P("Feedback loops mean actions shape future actions. Scrolling makes focus harder, which makes study painful, which causes more scrolling. Prayer, deep work, exercise, and service can create the opposite loop: self-respect, steadiness, and more ability to obey."))
    st.append(P("Bayesian updating is a complex name for a simple principle: update your belief when reality gives evidence. If a habit repeatedly harms you, stop calling it harmless. If a person repeatedly pulls you down, stop calling it loyalty. If a plan repeatedly fails, change the system, not only the emotion."))
    st.append(P("A local maximum is a small hill that feels like the top because climbing down first is painful. Many people stay in comfortable mediocrity because growth initially feels worse. Sometimes you must leave a lower comfort to reach a higher capacity."))
    st.append(callout("The core algorithm", "Choose the right aim. Remove the biggest blocker. Repeat the highest-leverage action. Measure honestly. Update quickly. Keep going quietly."))

    chapter(st, "11", "How Not To Be Diverted", "Clarity is not enough. You need anti-diversion systems for the moments when the old life pulls back.")
    st.append(P("Many people have moments of clarity. They feel the truth. They recognize the pattern. They experience a kind of deja vu: 'I have known this all along.' But then the old environment returns. The phone returns. Friends return. Desire returns. Stress returns. The person does not lose because the truth became false. He loses because he had no system for staying with the truth after the emotional moment faded."))
    st.append(S("The anti-diversion rules"))
    for item in [
        "Do not trust a realization until it becomes a schedule.",
        "Do not trust a goal until it has a daily minimum.",
        "Do not trust repentance until it has a changed boundary.",
        "Do not trust motivation until it survives boredom.",
        "Do not trust a friend with your future if they repeatedly mock your discipline.",
        "Do not trust your mood after poor sleep, too much scrolling, or private sin.",
    ]:
        st.append(B(item))
    st.append(P("This is the practical meaning of being a silent builder. You do not keep returning to the crowd for permission. You build small systems that preserve clarity when your feelings are no longer helping you."))
    st.append(callout("Deja vu to action", "When something feels deeply familiar and true, write the action immediately. Truth that does not become action becomes another memory of almost changing."))

    chapter(st, "12", "How To Actually Start", "Do not attempt to change everything in one emotional week. Change the direction, then walk daily.")
    st.append(P("The first move is not a perfect life plan. The first move is a stable daily minimum. If the minimum is too large, you will abandon it. If it is too small but consistent, it becomes a root."))
    st.append(S("Daily minimum"))
    for item in [
        "Protect the five prayers, or begin by protecting the weakest one until it becomes stable.",
        "Read Qur'an with meaning, even five minutes.",
        "Do one deep work block for your chosen arena.",
        "Move the body.",
        "Serve someone or fulfill one responsibility without needing praise.",
        "Do a three-minute night audit: repent, repair, reset.",
    ]:
        st.append(B(item))
    st.append(S("Weekly review"))
    for item in [
        "What brought me closer to Allah?",
        "What made me weaker?",
        "What repeated mistake needs a boundary?",
        "What skill improved visibly?",
        "Who did I benefit?",
        "What strength is Allah asking me to prepare next?",
    ]:
        st.append(B(item))
    st.append(P("For the next 90 days, choose one primary worldly arena. It may be CS, writing, business, finance, design, education, health, or another real domain. Do not keep switching. Potential stays imaginary until it is tested against responsibility."))

    chapter(st, "13", "Review Passages To Re-Read", "These are meant to be glanced through repeatedly until they become instinct.")
    for title, body in [
        ("Do not perform your transformation.", "Protect it. A seed dug up every day to show people will not grow."),
        ("The body wants now. The soul needs forever.", "Cheap pleasure speaks loudly because it pays immediately. Faith trains you to hear the longer truth."),
        ("Trust in Allah is not laziness.", "Plan, study, train, consult, execute, correct. Then surrender the result to Allah."),
        ("A weak sincere person is limited. A strong corrupt person is dangerous.", "The target is strength with trustworthiness."),
        ("If a pattern keeps harming you, update.", "Repeated damage is data. Build a boundary and learn."),
        ("Your environment has gravity.", "Do not hate short-term people, but do not let their time horizon become your command."),
        ("Knowledge must become action.", "If it does not change a habit, schedule, boundary, or output, it may only be refined entertainment."),
        ("Build what outlives the mood.", "Code, writing, teaching, wealth used well, family stability, and hidden service can keep producing benefit."),
        ("Opportunity is a trust.", "A degree, a mind, a working laptop, health, and free time are not small blessings."),
        ("Private worship protects public work.", "When nobody can reward you, sincerity gets trained."),
        ("The heart follows its repeated inputs.", "Do not only ask what you believe. Ask what you keep giving access to your eyes, ears, time, and imagination."),
        ("A realization is not yet a transformation.", "It becomes transformation when it changes a boundary, schedule, habit, relationship, or output."),
        ("The future is built while it still looks invisible.", "If you need everyone to understand early, you will keep abandoning seeds before roots form."),
    ]:
        st.append(KeepTogether([S(title), P(body)]))

    chapter(st, "14", "Sources And Anchors", "Sources are for verification. The real proof is whether the knowledge changes the life.")
    st.append(P("Qur'anic anchors: Qur'an 51:56 on purpose, Qur'an 8:60 on prepared strength, Qur'an 2:269 on wisdom, Qur'an 4:135 on justice even against oneself, and Qur'an 42:38 on consultation.", "Source"))
    st.append(P("Prophetic anchors: Bukhari 1 on intentions, Muslim 2664 on the strong believer, Bukhari 6114 on anger control, and Bukhari 893 on responsibility for what is under one's care.", "Source"))
    st.append(P("Modern anchors: World Economic Forum Future of Jobs Report 2025 for skill shifts; McKinsey Skill Shift for automation and changing work; American Academy of Pediatrics guidance on media and children; CDC youth mental health resources on connectedness and supportive environments. These are used as supporting evidence, not as replacements for revelation.", "Source"))
    st.append(callout("Final word", "Become inwardly owned by Allah, outwardly useful to creation, strategically prepared for the age you live in, and quiet enough to build without needing the world to clap while you are still becoming.", fill=colors.HexColor("#EEF1EA"), border=OLIVE))
    return st


def main():
    doc = BaseDocTemplate(
        OUT,
        pagesize=letter,
        leftMargin=MARGIN_X,
        rightMargin=MARGIN_X,
        topMargin=MARGIN_Y,
        bottomMargin=MARGIN_Y,
        title="The Silent Builder",
        author="Codex",
    )
    frame = Frame(MARGIN_X, MARGIN_Y, USABLE_W, PAGE_H - 2 * MARGIN_Y, id="normal", showBoundary=0)
    doc.addPageTemplates([
        PageTemplate(id="Cover", frames=frame, onPage=cover_page),
        PageTemplate(id="Body", frames=frame, onPage=body_page),
    ])
    doc.build(build_story())


if __name__ == "__main__":
    main()
