from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle,
    KeepTogether,
    NextPageTemplate,
)


OUT = "Silent_Builder_Field_Manual.pdf"

PAGE_W, PAGE_H = letter
MARGIN_X = 0.72 * inch
MARGIN_Y = 0.66 * inch
USABLE_W = PAGE_W - 2 * MARGIN_X

INK = colors.HexColor("#14211D")
MUTED = colors.HexColor("#5F6C68")
DEEP = colors.HexColor("#101A17")
PAPER = colors.HexColor("#F7F1E7")
PANEL = colors.HexColor("#FFFDF8")
LINE = colors.HexColor("#DADFD6")
OLIVE = colors.HexColor("#526B45")
CLAY = colors.HexColor("#A45D3C")
GOLD = colors.HexColor("#BD8B35")
BLUE = colors.HexColor("#315D70")
RED = colors.HexColor("#8A3D32")


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="CoverKicker",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=GOLD,
        alignment=TA_CENTER,
        spaceAfter=12,
    )
)
styles.add(
    ParagraphStyle(
        name="CoverTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=34,
        leading=38,
        textColor=colors.white,
        alignment=TA_CENTER,
        spaceAfter=14,
    )
)
styles.add(
    ParagraphStyle(
        name="CoverSub",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=13,
        leading=18,
        textColor=colors.HexColor("#E9E0D0"),
        alignment=TA_CENTER,
        spaceAfter=18,
    )
)
styles.add(
    ParagraphStyle(
        name="H1x",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=INK,
        spaceBefore=8,
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="H2x",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=CLAY,
        spaceBefore=10,
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="Bodyx",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10.1,
        leading=14.5,
        textColor=INK,
        spaceAfter=7,
    )
)
styles.add(
    ParagraphStyle(
        name="Smallx",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.4,
        leading=11.5,
        textColor=MUTED,
        spaceAfter=5,
    )
)
styles.add(
    ParagraphStyle(
        name="Bulx",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.7,
        leading=13.8,
        leftIndent=15,
        firstLineIndent=-9,
        textColor=INK,
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        name="Calloutx",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.3,
        leading=13.5,
        textColor=INK,
        spaceAfter=0,
    )
)
styles.add(
    ParagraphStyle(
        name="TableHead",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=8.4,
        leading=10.5,
        textColor=colors.white,
        alignment=TA_LEFT,
    )
)
styles.add(
    ParagraphStyle(
        name="TableCell",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.0,
        leading=10.4,
        textColor=INK,
    )
)
styles.add(
    ParagraphStyle(
        name="ChapterNum",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=11,
        textColor=GOLD,
        alignment=TA_CENTER,
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="ChapterTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=25,
        leading=29,
        textColor=colors.white,
        alignment=TA_CENTER,
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="ChapterSub",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10.4,
        leading=14.5,
        textColor=colors.HexColor("#E9E0D0"),
        alignment=TA_CENTER,
        spaceAfter=0,
    )
)
styles.add(
    ParagraphStyle(
        name="CardTitle",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=10.2,
        leading=12.5,
        textColor=INK,
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        name="CardText",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.8,
        leading=12.0,
        textColor=colors.HexColor("#53615D"),
        spaceAfter=0,
    )
)


def P(text, style="Bodyx"):
    return Paragraph(text, styles[style])


def h1(text):
    return P(text, "H1x")


def h2(text):
    return P(text, "H2x")


def bullet(text):
    return P("- " + text, "Bulx")


def space(h=8):
    return Spacer(1, h)


def chapter(num, title, subtitle):
    box = Table(
        [[P(num.upper(), "ChapterNum")], [P(title, "ChapterTitle")], [P(subtitle, "ChapterSub")]],
        colWidths=[USABLE_W],
    )
    box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), DEEP),
                ("BOX", (0, 0), (-1, -1), 0.8, DEEP),
                ("LEFTPADDING", (0, 0), (-1, -1), 18),
                ("RIGHTPADDING", (0, 0), (-1, -1), 18),
                ("TOPPADDING", (0, 0), (-1, 0), 16),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 2),
                ("TOPPADDING", (0, 1), (-1, 1), 0),
                ("BOTTOMPADDING", (0, 1), (-1, 1), 4),
                ("TOPPADDING", (0, 2), (-1, 2), 0),
                ("BOTTOMPADDING", (0, 2), (-1, 2), 16),
            ]
        )
    )
    return KeepTogether([box, Spacer(1, 12)])


def card(title, body, fill=colors.white, border=LINE):
    data = [[P(title, "CardTitle")], [P(body, "CardText")]]
    t = Table(data, colWidths=[(USABLE_W - 12) / 2])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), fill),
                ("BOX", (0, 0), (-1, -1), 0.6, border),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return t


def card_grid(items, fill=colors.white):
    rows = []
    for i in range(0, len(items), 2):
        left = card(items[i][0], items[i][1], fill=fill)
        right = card(items[i + 1][0], items[i + 1][1], fill=fill) if i + 1 < len(items) else ""
        rows.append([left, right])
    t = Table(rows, colWidths=[(USABLE_W - 12) / 2, (USABLE_W - 12) / 2], hAlign="LEFT")
    t.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return t


def callout(title, body, fill=PAPER, border=GOLD):
    data = [[P(f"<b>{title}</b><br/>{body}", "Calloutx")]]
    t = Table(data, colWidths=[USABLE_W])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), fill),
                ("BOX", (0, 0), (-1, -1), 0.8, border),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    return t


def matrix(headers, rows, widths=None):
    widths = widths or [USABLE_W / len(headers)] * len(headers)
    data = [[P(h, "TableHead") for h in headers]]
    for row in rows:
        data.append([P(cell, "TableCell") for cell in row])
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), DEEP),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.45, LINE),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return t


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(DEEP)
    canvas.rect(0, PAGE_H - 0.18 * inch, PAGE_W, 0.18 * inch, fill=1, stroke=0)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7.8)
    canvas.drawString(MARGIN_X, 0.35 * inch, "The Silent Builder Field Manual")
    canvas.drawRightString(PAGE_W - MARGIN_X, 0.35 * inch, f"{doc.page}")
    canvas.restoreState()


def cover_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(DEEP)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor("#1D2D27"))
    canvas.rect(0.45 * inch, 0.45 * inch, PAGE_W - 0.9 * inch, PAGE_H - 0.9 * inch, fill=1, stroke=0)
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(1.2)
    canvas.rect(0.72 * inch, 0.72 * inch, PAGE_W - 1.44 * inch, PAGE_H - 1.44 * inch, fill=0, stroke=1)
    canvas.restoreState()


def build_story():
    story = []

    cover_box = Table(
        [
            [P("PRIVATE FIELD MANUAL", "CoverKicker")],
            [P("The Silent Builder", "CoverTitle")],
            [
                P(
                    "An Islamic and evidence-informed guide to deep growth, hidden leverage, self-mastery, future readiness, family responsibility, and building quietly for Allah.",
                    "CoverSub",
                )
            ],
            [
                P(
                    "Core principle: do not become impressive. Become prepared, trustworthy, useful, and sincere.",
                    "CoverSub",
                )
            ],
        ],
        colWidths=[USABLE_W - 0.7 * inch],
    )
    cover_box.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    story.extend([Spacer(1, 2.25 * inch), cover_box, NextPageTemplate("Body"), PageBreak()])

    story.append(chapter("Orientation", "How To Read This Manual", "A compact guide for understanding, repeating, and implementing the whole framework."))
    story.append(
        P(
            "This PDF is not a motivational essay. It is a compressed map of the whole analysis: Qur'an, Sunnah, Islamic civilization, psychology, neuroscience, economics, future-of-work research, AI disruption, simple math models, and lived reality. Its aim is not to make you feel inspired for one night. Its aim is to give you a repeatable frame for becoming a stronger servant of Allah."
        )
    )
    story.append(
        callout(
            "The central conclusion",
            "The highest version of you is not the richest, loudest, most admired, or most dominant version. It is the version that used the maximum of what Allah entrusted to him: faith, mind, body, time, wealth, speech, influence, pain, opportunity, and responsibility.",
        )
    )
    story.append(space())
    story.append(h2("Plain-English glossary"))
    story.append(card_grid([
        ["Ibadah", "Worship as whole-life orientation. Prayer matters, but so do work, study, money, family duty, speech, and service when done lawfully and sincerely."],
        ["Akhirah", "The afterlife. It expands the time horizon beyond death and changes what success means."],
        ["Tazkiyah", "Cleaning the inner self: arrogance, showing off, envy, lust, anger, greed, laziness, and fear of people."],
        ["Hikmah", "Wisdom: knowing what matters, when it matters, and how to act without being ruled by impulse."],
        ["Quwwah", "Prepared strength: spiritual, physical, financial, intellectual, social, and technical capacity."],
        ["Amanah", "Trustworthiness: being safe with people's time, money, secrets, rights, and expectations."],
        ["Barakah", "Blessed increase from Allah that raw math cannot fully capture."],
        ["Tawakkul", "Effort plus reliance on Allah: tie the camel, then surrender the outcome."],
    ]))
    story.append(PageBreak())

    story.append(chapter("Chapter 1", "The One Thesis", "Strength without purification becomes danger. Sincerity without capacity remains limited."))
    story.append(
        P(
            "The secular world often asks: how can I become more powerful, more productive, more visible, more wealthy, more persuasive? Islam asks a more dangerous and more complete question: how can I become pleasing to Allah, beneficial to creation, purified from inner corruption, and prepared for the responsibility placed on me?"
        )
    )
    story.append(
        P(
            "That does not make worldly strength irrelevant. It makes worldly strength accountable. A weak sincere person may be beloved, but their ability to protect, provide, teach, build, and serve is limited. A strong corrupt person may achieve worldly scale, but they spread damage through their competence. The target is neither weakness nor egoic dominance. The target is strength with trust."
        )
    )
    story.append(
        callout(
            "The formula",
            "Falah, meaning complete success, is not produced by skill alone. It is the product of sincerity, purification, wisdom, prepared strength, trustworthiness, excellence, patience, and Allah's help. If sincerity is zero, the result collapses. If strength is zero, benefit is limited. If trust is zero, scale becomes dangerous.",
            fill=colors.HexColor("#EEF1EA"),
            border=OLIVE,
        )
    )
    story.append(h2("The corrected aim"))
    for item in [
        "Not: how do I become impressive?",
        "Not: how do I dominate people?",
        "Not: how do I look religious while avoiding responsibility?",
        "Yes: how do I become a prepared servant of Allah?",
        "Yes: how do I quietly build strength that benefits family, community, and the afterlife?",
    ]:
        story.append(bullet(item))

    story.append(chapter("Chapter 2", "How The Analysis Reached This", "Different fields, one repeated pattern: govern impulse, see clearly, build trust, prepare strength."))
    story.append(
        P(
            "The conclusion came from converging evidence. Different fields use different language, but they keep pointing to the same structure: long-term success belongs to those who govern impulse, see reality clearly, build trust, learn continuously, allocate resources well, and operate from a meaning system bigger than immediate pleasure."
        )
    )
    story.append(card_grid([
        ["Qur'an", "Life is worship, accountability is real, wisdom is great good, and strength must be prepared. Growth is judged by closeness to Allah, benefit, justice, and akhirah."],
        ["Sunnah", "The Prophet combined worship, trade, leadership, family duty, courage, mercy, consultation, and restraint. There is no split between deen and real responsibility."],
        ["Islamic civilization", "Muslims led when they pursued religious, scientific, legal, economic, and civilizational knowledge together. Decline followed fragmentation."],
        ["Neuroscience", "Attention, reward, sleep, stress, and impulse control shape performance and character. Self-mastery is biological as well as spiritual."],
        ["Economics", "Trust reduces friction, capital compounds, skill scarcity is rewarded, and incentives shape behavior. Amanah and financial literacy are force multipliers."],
        ["AI and future work", "Routine output is commoditized. Judgment, learning, ethics, taste, and leadership become more valuable, not less."],
        ["Math and algorithms", "Compounding, feedback loops, opportunity cost, and updating explain why small repeated habits create large futures."],
        ["Lived reality", "Family pressure, illness, death, unstable income, and bad environments make the framework practical, not theoretical."],
    ]))
    story.append(PageBreak())

    story.append(chapter("Chapter 3", "The Secret Of This World", "The visible world rewards hidden structures. Most people chase fruit and ignore roots."))
    story.append(
        P(
            "The 'secret' is not a conspiracy. It is that the visible world rewards hidden structures. People see success, but not the invisible architecture: time horizon, nervous-system control, environment design, family responsibility, trust networks, capital allocation, and private worship. Most people chase the visible fruit and ignore the root."
        )
    )
    story.append(h2("The world runs on hidden laws"))
    for item in [
        "Attention is mined. If you cannot control attention, others will rent your mind for their profit.",
        "Desire is monetized. Lust, envy, outrage, status anxiety, and boredom are business models.",
        "Trust is capital. Reliable people move faster because others do not waste energy protecting themselves from them.",
        "Environment is an algorithm. Friends, feeds, rooms, routines, and family culture repeatedly suggest what is normal.",
        "Time horizon is power. A person optimizing for five years beats a person optimizing for tonight. A person optimizing for akhirah has an even larger frame.",
        "The unseen is not abstract. If judgment is real, then hidden effort, hidden sin, hidden pain, and hidden sacrifice all matter.",
    ]:
        story.append(bullet(item))
    story.append(
        callout(
            "The dangerous balance",
            "Dunya, the worldly life, is not worthless. It is a tool, a test, a training ground, and a field for planting. The error is not using dunya. The error is being used by it.",
        )
    )

    story.append(chapter("Chapter 4", "Why Most People Do Not Live This", "The obstacle is rarely information. The obstacle is friction."))
    story.append(
        P(
            "The barrier is rarely lack of information. The barrier is friction. The body wants comfort. The ego wants praise. The environment wants you to remain recognizable. The phone wants attention. The market wants consumption. The nafs, the lower self, wants the reward without the purification."
        )
    )
    story.append(card_grid([
        ["Cheap dopamine", "Fast pleasure makes deep work feel boring. Counter-practice: phone boundaries, fasting, exercise, prayer, and focused work blocks."],
        ["Ego", "It wants growth without correction or humiliation. Counter-practice: seek feedback, admit error quickly, serve secretly."],
        ["Information addiction", "Learning feels like action. Counter-practice: convert every lesson into one behavior, boundary, or output."],
        ["Present-pull people", "They tell you to relax, enjoy now, and not be too serious. Counter-practice: build silently, stay warm, limit explanation."],
        ["False tawakkul", "Trust in Allah is misused as an excuse for passivity. Counter-practice: plan, prepare, act, then surrender the outcome."],
        ["Hopeless environment", "Stress makes the future feel fake. Counter-practice: use tiny repeated wins to rebuild evidence that change is possible."],
        ["Fear of being seen changing", "People may mock the early stage. Counter-practice: protect the seed and let results speak later."],
        ["Comfort identity", "A person may prefer familiar weakness over unfamiliar responsibility. Counter-practice: attach identity to obedience, not mood."],
    ]))
    story.append(PageBreak())

    story.append(chapter("Chapter 5", "The Silent Builder Principle", "Do not shout every intention. Protect the seed until it has roots."))
    story.append(
        P(
            "Do not shout the blueprint everywhere. Not because you are better than people, and not because guidance should be hidden from those who sincerely need it. The reason is more practical: not everyone can hold a long-term view without attacking it, misunderstanding it, mocking it, or pulling it back into short-term living."
        )
    )
    for item in [
        "Share wisdom with people who are sincere, serious, and able to benefit.",
        "Do not explain your whole transformation to people who are committed to the habits you are leaving.",
        "Do not turn growth into a public identity. Public identity creates pressure to perform instead of purify.",
        "Be warm and useful in public, disciplined and private in your deepest work.",
        "Keep your largest intentions between you and Allah, your notebook, and a tiny circle of serious people.",
    ]:
        story.append(bullet(item))
    story.append(
        callout(
            "Silent builder sentence",
            "I do not need to be understood at the seed stage. I need to be sincere, consistent, and protected from unnecessary noise.",
            fill=colors.HexColor("#EEF1EA"),
            border=OLIVE,
        )
    )

    story.append(chapter("Chapter 6", "The Core Human Skills", "Domain skills add. Meta-skills multiply. Islam gives the aim and the guardrails."))
    story.append(
        P(
            "The strongest skills are not merely domain skills like coding, finance, or copywriting. Those matter, but they add. Meta-skills multiply. Islam does not rank them by status or market value alone, but by how they bring closeness to Allah, benefit creation, purify the self, protect justice, and survive into the akhirah."
        )
    )
    story.append(
        matrix(
            ["Rank", "Skill", "Plain meaning", "Why it matters"],
            [
                ["1", "Correct understanding and judgment", "Seeing truth, priority, consequence, and self-deception clearly.", "Without this, even good intentions can harm."],
                ["2", "Self-mastery", "Governing desire, anger, laziness, ego, fear, envy, and attention.", "A person who cannot govern himself is governed by the world."],
                ["3", "Noble character", "Honesty, dignity, reliability, courage, restraint, fairness, and mercy.", "Character multiplies every other skill and prevents corruption."],
                ["4", "Beneficial communication", "Writing, speaking, listening, teaching, negotiation, and reconciliation.", "Truth must become understandable and useful."],
                ["5", "Seeking and applying knowledge", "Learning, internalizing, implementing, teaching.", "Information is not enough; knowledge must become action."],
                ["6", "Service and responsibility", "Carrying burdens, solving problems, providing, protecting, and building.", "Spirituality is not escape from duty."],
                ["7", "Systems and leverage", "Building assets, workflows, code, institutions, and media that repeat value.", "This turns individual effort into compounding benefit."],
                ["8", "Financial literacy", "Understanding income, wealth, debt, investing, halal earning, and giving.", "Money can become protection and service, or temptation and slavery."],
            ],
            widths=[0.45 * inch, 1.55 * inch, 2.25 * inch, USABLE_W - 4.25 * inch],
        )
    )
    story.append(PageBreak())

    story.append(chapter("Chapter 7", "The Simple Math Behind Growth", "The complex names matter less than the practical meanings."))
    story.append(
        P(
            "The complex names are less important than the simple meanings. These models explain why private habits matter, why environments are dangerous, and why long-term builders seem unusual at first."
        )
    )
    story.append(card_grid([
        ["Compounding", "Small gains multiply over time. One focused hour daily becomes hundreds of hours yearly. Prayer, study, fitness, money, and writing compound."],
        ["Opportunity cost", "Every yes is a no to something else. Scrolling costs attention, sleep, study, worship, and future confidence."],
        ["Feedback loop", "An action changes the next action. Scrolling makes focus harder; prayer and work create the opposite loop."],
        ["Delayed gratification", "You accept discomfort now for greater later reward. This is the backbone of study, career, savings, fitness, and deen."],
        ["Transaction cost", "Low trust makes cooperation expensive. Amanah reduces monitoring, arguing, contracts, and fear."],
        ["Bayesian updating", "Update beliefs when evidence arrives. If a person, app, habit, or environment repeatedly harms you, stop pretending it is harmless."],
        ["Local maximum", "A small comfort-zone peak can block a higher peak. Temporary discomfort may be needed to leave a mediocre life."],
        ["Power law", "A few inputs create most results. A few habits, friends, books, skills, and decisions may shape most of your future."],
    ]))
    story.append(
        callout(
            "The core algorithm",
            "Choose the right aim. Remove the biggest blocker. Repeat the highest-leverage action. Measure honestly. Update quickly. Keep going quietly.",
        )
    )

    story.append(chapter("Chapter 8", "AI, Work, And The 2030 Shift", "Ordinary output gets cheaper. Judgment, trust, and learning become more valuable."))
    story.append(
        P(
            "AI makes ordinary output cheaper. This does not mean human beings become useless. It means shallow technical performance becomes less protected, while judgment, taste, trust, leadership, original thinking, ethical responsibility, and the ability to learn quickly become more valuable."
        )
    )
    for item in [
        "Coding matters, but code without judgment becomes commodity labor.",
        "Writing matters, but generic writing becomes cheap; clear original thinking becomes rarer.",
        "Financial modeling matters, but decisions, incentives, risk, and trust matter more.",
        "Communication matters, but persuasion without character becomes manipulation.",
        "AI literacy matters, but outsourcing your thinking to tools weakens the very faculty that makes you valuable.",
    ]:
        story.append(bullet(item))
    story.append(
        callout(
            "Future-proof direction",
            "Become a person who can think, learn, communicate, build trust, use tools, serve real needs, and stay morally anchored under pressure.",
            fill=colors.HexColor("#E5EEF1"),
            border=BLUE,
        )
    )
    story.append(PageBreak())

    story.append(chapter("Chapter 9", "Family Reality And Responsibility", "Growth is not abstract when the people near you are under pressure."))
    story.append(
        P(
            "Growth is not abstract when the family is under pressure: illness, death, unstable income, emotional pain, siblings drifting, studies at risk, and a home environment that does not feel easy. In Islam, responsibility begins with what is near. You do not need to carry what only Allah can carry, but you must not abandon what He placed within your reach."
        )
    )
    story.append(
        matrix(
            ["Person/context", "Main risk", "Helpful frame"],
            [
                ["You", "Turning analysis into endless analysis.", "Choose one main arena, build quietly, and convert knowledge into weekly visible output."],
                ["Sister, 22, CS final year", "Weak salah, phone drain, emotional pain, low confidence, non-religious college environment, family pressure.", "Her degree is an amanah and opportunity. Deen protects dignity and steadiness; CS can become service and family strength."],
                ["Zohran, 16", "Hopelessness, bad friends, attraction/chatting, weak salah, wasted time, unclear ambition, family financial stress.", "He needs missions, small wins, prayer anchor, body movement, study proof, friend audit, and a believable path to compounding."],
            ],
            widths=[1.65 * inch, 2.55 * inch, USABLE_W - 4.2 * inch],
        )
    )
    story.append(
        P(
            "The point is not to scare them with pressure. The point is to show them that opportunity is not random. A modern education, especially in CS, is not only a career path. It can become family protection, halal earning, sadaqah, dignity, and a way to serve people at scale."
        )
    )

    story.append(chapter("Chapter 10", "Personalized Translation", "The same truth must be spoken differently to different souls and situations."))
    story.append(h2("For you"))
    for item in [
        "Your danger is not lack of depth. Your danger is living in depth without execution.",
        "Pick one battlefield for 90 days. Build output, not only worldview.",
        "Keep your deepest growth quiet. Let Allah see the root before people see the fruit.",
    ]:
        story.append(bullet(item))
    story.append(h2("For your sister"))
    for item in [
        "Islam should be presented as anchoring, healing, dignity, unseen reality, and protection, not as a lecture.",
        "Her CS opportunity is rare and serious. Wasting it through phone addiction, emotional fog, or environment drift is not a small loss.",
        "She does not need to fight every non-religious influence publicly. She needs private standards, prayer return, phone boundaries, study rhythm, and a quiet religious oxygen line.",
    ]:
        story.append(bullet(item))
    story.append(h2("For Zohran"))
    for item in [
        "He needs hope made visible through small wins. Hopeless environments make the future feel fake.",
        "His energy should be aimed, not crushed: prayer streak, body challenge, focus mission, CS path, anger control, family help.",
        "He must learn that bad friends and useless attraction loops are not harmless entertainment. They are future-shaping environments.",
    ]:
        story.append(bullet(item))
    story.append(PageBreak())

    story.append(chapter("Chapter 11", "The 90-Day Silent Builder Protocol", "Small enough to repeat. Serious enough to change direction."))
    story.append(
        P(
            "Do not try to redesign your whole life in one emotional week. Change the direction, then walk daily. The protocol is deliberately simple because the goal is repeatability."
        )
    )
    story.append(
        matrix(
            ["Frequency", "Practice", "Reason"],
            [
                ["Daily", "Prayer protected as the anchor.", "You need a non-negotiable connection to Allah before the world defines the day."],
                ["Daily", "Qur'an with meaning, even five minutes.", "Revelation recalibrates the worldview."],
                ["Daily", "One deep work block.", "Deep work turns intention into skill and skill into capacity."],
                ["Daily", "Body movement or training.", "Energy, mood, discipline, and worship are affected by the body."],
                ["Daily", "One act of service or responsibility.", "Benefit proves sincerity."],
                ["Nightly", "Three-minute self-audit.", "Repent, repair, and update before repeated mistakes become identity."],
                ["Weekly", "Review money, time, phone, worship, study, family, and output.", "What is measured honestly can be corrected."],
                ["Monthly", "Cut one drain and strengthen one system.", "Growth becomes structural, not motivational."],
            ],
            widths=[1.05 * inch, 2.35 * inch, USABLE_W - 3.4 * inch],
        )
    )
    story.append(h2("Choose one battlefield"))
    story.append(
        P(
            "For the next 90 days, choose one primary worldly arena: CS, writing, business, finance, design, health, education, community building, or another real domain. Potential stays imaginary until it is tested against responsibility."
        )
    )

    story.append(chapter("Chapter 12", "Daily And Weekly Audit", "Do not negotiate with the mirror. Measure honestly, then repair."))
    story.append(h2("Daily questions"))
    for item in [
        "Did I protect prayer or let the day own me?",
        "What desire, fear, anger, or laziness tried to govern me?",
        "What useful output did I produce?",
        "Who did I help or protect?",
        "What must I repair before sleeping?",
    ]:
        story.append(bullet(item))
    story.append(h2("Weekly questions"))
    for item in [
        "What made me closer to Allah?",
        "What made me weaker?",
        "What repeated mistake needs a new boundary?",
        "What skill improved visibly?",
        "What relationship or family duty did I neglect?",
        "What strength is Allah asking me to prepare next?",
    ]:
        story.append(bullet(item))
    story.append(PageBreak())

    story.append(chapter("Chapter 13", "Review Cards For Repetition", "Repetition moves a worldview from idea to instinct."))
    review_cards = [
        ["Do not perform your transformation.", "Protect it. A seed dug up every day to show people will not grow."],
        ["The body wants now. The soul needs forever.", "Cheap pleasure speaks loudly because it pays immediately. Faith trains you to hear the longer truth."],
        ["Trust in Allah is not laziness.", "Plan, study, train, consult, execute, correct. Then surrender the result to Allah."],
        ["A weak sincere person is limited. A strong corrupt person is dangerous.", "The target is strength with trustworthiness."],
        ["If a pattern keeps harming you, update.", "Repeated damage is data. Build a boundary and learn."],
        ["Your environment has gravity.", "Do not hate short-term people, but do not let their time horizon become your command."],
        ["Knowledge must become action.", "If it does not change a habit, schedule, boundary, or output, it may only be refined entertainment."],
        ["Build what outlives the mood.", "Code, writing, teaching, wealth used well, family stability, and hidden service can keep producing benefit."],
        ["Opportunity is a trust.", "A degree, a mind, a working laptop, health, and free time are not small blessings."],
        ["Private worship protects public work.", "When nobody can reward you, sincerity gets trained."],
    ]
    rows = [[title, body] for title, body in review_cards]
    story.append(matrix(["Card", "Meaning"], rows, widths=[2.05 * inch, USABLE_W - 2.05 * inch]))

    story.append(h1("14. Research And Source Layer"))
    story.append(P("These are the anchor sources behind the framework. Use them for verification, not as decoration."))
    source_rows = [
        ["Qur'an 51:56", "Purpose of creation: worship Allah.", "quran.com/51/56"],
        ["Qur'an 8:60", "Prepare whatever strength you are able.", "quran.com/8/60"],
        ["Qur'an 2:269", "Wisdom is tremendous good.", "quran.com/2/269"],
        ["Qur'an 4:135", "Stand for justice even against yourself.", "quran.com/4/135"],
        ["Qur'an 42:38", "Consultation as a feature of believers.", "quran.com/42/38"],
        ["Bukhari 1", "Actions are judged by intentions.", "sunnah.com/bukhari:1"],
        ["Muslim 2664", "The strong believer is better and more beloved to Allah, while both have good.", "sunnah.com/muslim:2664"],
        ["Bukhari 6114", "Real strength includes controlling anger.", "sunnah.com/bukhari:6114"],
        ["Bukhari 893", "Each person is responsible for what is under their care.", "sunnah.com/bukhari:893"],
        ["WEF Future of Jobs 2025", "Skills outlook: analytical thinking, resilience, AI, big data, leadership, lifelong learning.", "WEF - Skills Outlook"],
        ["McKinsey Skill Shift", "Automation increases demand for technological, higher cognitive, and social-emotional skills.", "McKinsey - Skill Shift"],
        ["AAP Media and Children", "Media habits affect sleep, attention, and development.", "aap.org - Media and Children"],
        ["CDC Adolescent Mental Health", "Connectedness and supportive environments protect young people.", "cdc.gov - Youth Mental Health"],
    ]
    story.append(matrix(["Source", "Why it matters", "Link"], source_rows, widths=[1.55 * inch, 2.6 * inch, USABLE_W - 4.15 * inch]))

    story.append(space())
    story.append(
        callout(
            "Final word",
            "Become inwardly owned by Allah, outwardly useful to creation, strategically prepared for the age you live in, and quiet enough to build without needing the world to clap while you are still becoming.",
            fill=colors.HexColor("#EEF1EA"),
            border=OLIVE,
        )
    )

    return story


def main():
    doc = BaseDocTemplate(
        OUT,
        pagesize=letter,
        leftMargin=MARGIN_X,
        rightMargin=MARGIN_X,
        topMargin=MARGIN_Y,
        bottomMargin=MARGIN_Y,
        title="The Silent Builder Field Manual",
        author="Codex",
    )
    frame = Frame(
        MARGIN_X,
        MARGIN_Y,
        USABLE_W,
        PAGE_H - 2 * MARGIN_Y,
        id="normal",
        showBoundary=0,
    )
    doc.addPageTemplates(
        [
            PageTemplate(id="Cover", frames=frame, onPage=cover_page),
            PageTemplate(id="Body", frames=frame, onPage=on_page),
        ]
    )
    story = build_story()
    doc.build(story)


if __name__ == "__main__":
    main()
