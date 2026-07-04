from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
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
    NextPageTemplate,
    KeepTogether,
)


OUT = "The_Silent_Builder_Book.pdf"

PAGE_W, PAGE_H = letter
MARGIN_X = 0.82 * inch
MARGIN_Y = 0.72 * inch
USABLE_W = PAGE_W - 2 * MARGIN_X

INK = colors.HexColor("#17231F")
MUTED = colors.HexColor("#64706C")
DEEP = colors.HexColor("#101A17")
PAPER = colors.HexColor("#F6F0E6")
SOFT = colors.HexColor("#FFFDF8")
LINE = colors.HexColor("#DADFD6")
OLIVE = colors.HexColor("#536B45")
CLAY = colors.HexColor("#A45D3C")
GOLD = colors.HexColor("#BD8B35")
BLUE = colors.HexColor("#315D70")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle("CoverKicker", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=GOLD, alignment=TA_CENTER, spaceAfter=12))
styles.add(ParagraphStyle("CoverTitle", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=34, leading=38, textColor=colors.white, alignment=TA_CENTER, spaceAfter=14))
styles.add(ParagraphStyle("CoverSub", parent=styles["Normal"], fontName="Helvetica", fontSize=13, leading=18, textColor=colors.HexColor("#EAE0D0"), alignment=TA_CENTER, spaceAfter=14))
styles.add(ParagraphStyle("Chapter", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=24, leading=29, textColor=INK, spaceBefore=6, spaceAfter=12))
styles.add(ParagraphStyle("Section", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=14.5, leading=18, textColor=CLAY, spaceBefore=12, spaceAfter=7))
styles.add(ParagraphStyle("Body", parent=styles["BodyText"], fontName="Helvetica", fontSize=10.8, leading=16.2, textColor=INK, spaceAfter=9))
styles.add(ParagraphStyle("Small", parent=styles["BodyText"], fontName="Helvetica", fontSize=8.5, leading=11.5, textColor=MUTED, spaceAfter=5))
styles.add(ParagraphStyle("Quote", parent=styles["BodyText"], fontName="Helvetica-Oblique", fontSize=10.4, leading=15.2, textColor=colors.HexColor("#3F4B47"), leftIndent=18, rightIndent=12, spaceBefore=6, spaceAfter=10))
styles.add(ParagraphStyle("BookBullet", parent=styles["BodyText"], fontName="Helvetica", fontSize=10.3, leading=15.0, leftIndent=16, firstLineIndent=-8, textColor=INK, spaceAfter=5))
styles.add(ParagraphStyle("Callout", parent=styles["BodyText"], fontName="Helvetica", fontSize=10.2, leading=15.0, textColor=INK, spaceAfter=0))
styles.add(ParagraphStyle("TOC", parent=styles["BodyText"], fontName="Helvetica", fontSize=10.3, leading=14.2, textColor=INK, spaceAfter=5))


def P(text, style="Body"):
    return Paragraph(text, styles[style])


def H(text):
    return P(text, "Chapter")


def S(text):
    return P(text, "Section")


def B(text):
    return P("- " + text, "BookBullet")


def Q(text):
    return P(text, "Quote")


def callout(title, body, fill=PAPER, border=GOLD):
    box = Table([[P(f"<b>{title}</b><br/>{body}", "Callout")]], colWidths=[USABLE_W])
    box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), fill),
        ("BOX", (0, 0), (-1, -1), 0.8, border),
        ("LEFTPADDING", (0, 0), (-1, -1), 13),
        ("RIGHTPADDING", (0, 0), (-1, -1), 13),
        ("TOPPADDING", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 11),
    ]))
    return box


def chapter_title(number, title, subtitle):
    return KeepTogether([
        Spacer(1, 4),
        P(f"Chapter {number}", "Small"),
        H(title),
        callout("Chapter compass", subtitle, fill=colors.HexColor("#EEF1EA"), border=OLIVE),
        Spacer(1, 8),
    ])


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(MARGIN_X, 0.35 * inch, "The Silent Builder Book")
    canvas.drawRightString(PAGE_W - MARGIN_X, 0.35 * inch, str(doc.page))
    canvas.restoreState()


def cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(DEEP)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor("#1C2A25"))
    canvas.rect(0.52 * inch, 0.52 * inch, PAGE_W - 1.04 * inch, PAGE_H - 1.04 * inch, fill=1, stroke=0)
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(1.1)
    canvas.rect(0.78 * inch, 0.78 * inch, PAGE_W - 1.56 * inch, PAGE_H - 1.56 * inch, fill=0, stroke=1)
    canvas.restoreState()


def story():
    st = []
    cover_box = Table([
        [P("A PRIVATE BOOK FOR KNOWLEDGE AND IMPLEMENTATION", "CoverKicker")],
        [P("The Silent Builder", "CoverTitle")],
        [P("An Islamic and evidence-informed reading manual on deep growth, hidden leverage, self-mastery, future readiness, and building quietly for Allah.", "CoverSub")],
        [P("Read slowly. Return often. Implement quietly.", "CoverSub")],
    ], colWidths=[USABLE_W - 0.65 * inch])
    cover_box.setStyle(TableStyle([("ALIGN", (0,0), (-1,-1), "CENTER"), ("VALIGN", (0,0), (-1,-1), "MIDDLE"), ("TOPPADDING", (0,0), (-1,-1), 9), ("BOTTOMPADDING", (0,0), (-1,-1), 9)]))
    st += [Spacer(1, 2.35 * inch), cover_box, NextPageTemplate("Body"), PageBreak()]

    st.append(H("Contents"))
    for line in [
        "1. The Question Beneath All Self-Improvement",
        "2. The Islamic Operating System",
        "3. The Secret Of The World",
        "4. Why Most People Never Live This",
        "5. The Silent Builder Principle",
        "6. The Skills That Actually Multiply A Life",
        "7. The Body, Attention, And The Nafs",
        "8. Money, Work, AI, And The 2030 Shift",
        "9. The Simple Math Of Becoming",
        "10. How To Actually Start",
        "11. Review Passages To Re-Read",
        "12. Sources And Anchors",
    ]:
        st.append(P(line, "TOC"))
    st.append(PageBreak())

    st.append(chapter_title("1", "The Question Beneath All Self-Improvement", "The real aim is not to become impressive. The real aim is to become a prepared servant of Allah: inwardly clean, outwardly useful, and strong enough to carry responsibility."))
    st.append(P("Most self-improvement begins from anxiety. A person feels behind, weak, unseen, poor, unattractive, confused, or dependent. Then he asks: how can I become better? That question is not wrong, but it is incomplete. Better according to what? Better for whom? Better for how long? Better in the eyes of people, the market, the family, the ego, or Allah?"))
    st.append(P("This is where the Islamic lens changes the whole project. Islam does not ask you to become impressive. It asks you to become true. It does not rank skills only by salary, status, dominance, or social admiration. It asks whether those skills bring you closer to Allah, purify the self, benefit creation, establish justice, carry responsibility, and survive into the afterlife."))
    st.append(P("That does not make worldly strength irrelevant. It makes worldly strength accountable. A weak sincere person may be beloved to Allah, but their ability to protect, provide, build, teach, heal, and serve can be limited. A strong corrupt person may achieve scale, but their strength becomes a weapon for the ego. The target is neither weakness nor egoic dominance. The target is strength with trust."))
    st.append(callout("The one-line thesis", "Become strong enough to carry responsibility, and sincere enough not to be corrupted by it."))
    st.append(P("This is why the phrase 'highest potential' must be purified. Your highest potential is not the most famous version of you, the richest version of you, or the version that gets the most praise. Your highest potential is the version that used the maximum of what Allah entrusted to you: faith, mind, body, time, wealth, pain, opportunity, speech, family, influence, and attention."))
    st.append(P("The secular world often says: build leverage. Islam says: purify the lever-holder. Both are needed. If you build leverage without purification, you become more efficient at spreading your diseases. If you purify yourself without building capacity, your benefit remains smaller than it could have been."))
    st.append(Q("So the path is not skill collection. The path is orientation, purification, strength, service, and legacy."))

    st.append(chapter_title("2", "The Islamic Operating System", "Islam is not a ritual compartment. It is a total life architecture: worship, stewardship, accountability, wisdom, strength, trust, and service."))
    st.append(P("The first correction is this: worship is not only ritual. Prayer, fasting, charity, and recitation are foundations, but the broader Islamic meaning of worship includes everything done sincerely, lawfully, and in alignment with Allah. Study can become worship. Work can become worship. Earning can become worship. Serving family can become worship. Learning a difficult skill can become worship. Restraining yourself from a sin can become worship."))
    st.append(P("This changes the emotional weight of life. You are not simply trying to optimize a career. You are trying to fulfill a trust. You are not merely a consumer of experiences. You are a responsible soul moving toward judgment. You are not just trying to survive dunya. You are planting through dunya."))
    st.append(S("Purpose"))
    st.append(P("The Qur'an gives the purpose of creation as worship of Allah. If this is true, then your life cannot be divided into religious and non-religious compartments in the shallow sense. The question becomes: how do I make my mind, body, money, study, work, family, and influence obedient to the purpose of creation?"))
    st.append(S("Stewardship"))
    st.append(P("The idea of stewardship means you are responsible for what has been placed under your care. You are responsible for your body, your mind, your time, your opportunities, your family roles, your speech, and your decisions. This is not political fantasy or reckless confrontation. It is accountable living."))
    st.append(S("The afterlife"))
    st.append(P("The afterlife changes the mathematics. A purely secular system optimizes for a short biological window. Islam expands the horizon beyond death. This means hidden worship matters. Quiet sacrifice matters. Pain nobody saw matters. Injustice nobody repaired matters. A small sincere deed may become more valuable than a public achievement built on ego."))
    st.append(S("Prepared strength"))
    st.append(P("The Qur'anic command to prepare whatever strength you are able teaches a principle of serious readiness. In personal life, that includes spiritual strength, physical health, knowledge, financial competence, technical skill, emotional regulation, family responsibility, and strategic awareness. Weakness should not be romanticized. Strength should not be worshipped. It should be prepared and disciplined."))
    st.append(callout("Plain meaning", "Islam does not ask you to choose between worship and competence. It asks you to make competence worshipful and worship transformative."))

    st.append(chapter_title("3", "The Secret Of The World", "The visible world rewards invisible structures. People see outcomes late. Allah sees roots immediately."))
    st.append(P("The secret of this world is not a conspiracy. It is that most outcomes are produced by hidden structures long before they become visible. People see the job, the money, the calmness, the confidence, the body, the writing, the influence, the family stability, or the spiritual presence. They do not see the repeated private choices that made those things possible."))
    st.append(P("The world is full of systems designed to capture the weak parts of the human being. Attention is mined. Desire is monetized. Outrage is amplified. Lust is packaged. Envy is stimulated. Status anxiety is turned into consumption. Boredom is treated as a business opportunity. If a person does not govern himself, he becomes raw material for other people's algorithms."))
    st.append(P("This is why attention is not a small matter. What repeatedly enters the eyes and ears eventually shapes the heart. What shapes the heart shapes desire. What shapes desire shapes choices. What shapes choices shapes destiny, by Allah's permission."))
    st.append(S("The invisible forces"))
    for item in [
        "Time horizon: the person who can think in years beats the person trapped in tonight.",
        "Environment: friends, feeds, rooms, and routines repeatedly suggest what is normal.",
        "Trust: reliable people move faster because others do not waste energy protecting themselves from them.",
        "Compounding: repeated small actions become large realities later.",
        "The unseen: hidden effort, hidden sin, hidden pain, and hidden sincerity all matter before Allah.",
    ]:
        st.append(B(item))
    st.append(P("Dunya is not worthless. It is a tool, a test, a training ground, and a field for planting. The error is not using the world. The error is being used by it."))

    st.append(chapter_title("4", "Why Most People Never Live This", "The problem is rarely lack of information. The problem is friction: biological, social, emotional, spiritual, and environmental."))
    st.append(P("Most people know enough to begin. They know prayer matters. They know the phone wastes time. They know sleep matters. They know bad friends affect them. They know study requires focus. They know money requires discipline. They know anger damages relationships. Yet knowing does not automatically become living."))
    st.append(P("Why? Because the body wants comfort now. The ego wants praise without correction. The lower self wants reward without purification. The environment wants you to remain recognizable. The phone wants attention. The market wants consumption. Friends may want company in distraction. Even family pressure can make the future feel too heavy to face."))
    st.append(S("The common traps"))
    for item in [
        "Cheap dopamine: fast pleasure makes deep work feel painfully slow.",
        "Information addiction: learning feels like action, so no real change happens.",
        "Ego protection: the self hates being a beginner, being corrected, or being seen changing.",
        "Present-pull people: people optimized for short-term pleasure often pull others toward the same horizon.",
        "False reliance: trust in Allah is misused as passivity instead of effort plus surrender.",
        "Hopelessness: stress can make the future feel fake and the present feel inescapable.",
    ]:
        st.append(B(item))
    st.append(callout("The hard truth", "If you wait until discipline feels natural, you may wait for years. Discipline often feels unnatural at first because you are training against an old identity."))

    st.append(chapter_title("5", "The Silent Builder Principle", "Do not announce every transformation. Build quietly until the root is strong enough to withstand weather."))
    st.append(P("One of the most important principles in this whole framework is silence. Not secrecy in an arrogant way. Not refusing to teach sincere people. Not acting mysterious. The point is protection. Early transformation is fragile. If you expose it too early, people can turn it into debate, mockery, performance, pressure, or identity."))
    st.append(P("Not everyone will understand a long-term view. Some people will tell you to enjoy the present. Sometimes they love you and simply cannot see what you see. Sometimes they are insecure because your effort reminds them of their own avoidance. Sometimes they are not malicious at all; they are just operating on a shorter horizon. But if you let every short-horizon voice enter your command center, your direction will dissolve."))
    st.append(P("Silent building means you remain warm with people, but private with your deepest intentions. You share what is beneficial. You do not explain your entire plan to people who are not responsible for helping you protect it. You do not turn discipline into a personality costume. You do not announce every streak, every repentance, every ambition, every inner change."))
    st.append(Q("The seed does not need applause. It needs soil, water, time, and protection."))
    st.append(callout("Silent builder sentence", "I do not need to be understood at the seed stage. I need to be sincere, consistent, and protected from unnecessary noise."))

    st.append(chapter_title("6", "The Skills That Actually Multiply A Life", "Domain skills add. Meta-skills multiply. Islam gives the aim, hierarchy, and guardrails."))
    st.append(P("Coding, finance, design, writing, business, and AI tools matter. But they are not the deepest layer. They are domain skills. They can add value, but the skills underneath them multiply everything. The deeper skills determine how quickly you learn, how clearly you think, how well you communicate, how reliably people trust you, how calmly you act under pressure, and how ethically you use power."))
    st.append(S("1. Correct understanding and sound judgment"))
    st.append(P("This is the ability to see truth, priority, consequence, and self-deception clearly. Without it, even good intentions can become harmful. A person may have religious information, intelligence, money, charisma, and ambition, but still destroy himself through poor judgment."))
    st.append(S("2. Self-mastery"))
    st.append(P("This is governing desire, anger, laziness, ego, fear, envy, and attention. A person who cannot govern himself will be governed by trends, validation, lust, greed, anxiety, or bad company."))
    st.append(S("3. Noble character"))
    st.append(P("Trustworthiness, honesty, dignity, courage, fairness, gentleness, restraint, and keeping promises are not decorative. They are central. Poor character corrupts wealth, leadership, knowledge, influence, and even religious work."))
    st.append(S("4. Beneficial communication"))
    st.append(P("Speech can guide, reconcile, teach, heal, protect truth, or destroy families and communities. Writing is externalized thinking. Speaking is responsibility made audible. The goal is not manipulation. The goal is making truth understandable and useful."))
    st.append(S("5. Seeking and applying knowledge"))
    st.append(P("Real knowledge is not information addiction. The higher sequence is learning, internalizing, implementing, and teaching. Knowledge that never changes action becomes evidence against a person."))
    st.append(S("6. Service and responsibility"))
    st.append(P("Islam values people who carry burdens, solve problems, provide stability, protect others, feed families, and uplift communities. Spirituality is not escape from responsibility."))
    st.append(S("7. Systems and leverage"))
    st.append(P("The leap from effort to scale happens when you build systems: code, writing, teaching, products, institutions, workflows, capital, and communities. The Islamic correction is that systems must solve real problems cleanly and not exploit people."))
    st.append(S("8. Financial and technical literacy"))
    st.append(P("Money and technology are not separate from deen when they determine independence, family protection, community capacity, and service. Learn them lawfully. Use them responsibly. Do not worship them."))

    st.append(chapter_title("7", "The Body, Attention, And The Nafs", "Your spiritual and intellectual life is affected by sleep, stress, dopamine, food, movement, and what you repeatedly look at."))
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

    st.append(chapter_title("8", "Money, Work, AI, And The 2030 Shift", "The age is changing. Ordinary output gets cheaper. Judgment, trust, originality, and learning speed become more valuable."))
    st.append(P("AI commoditizes many shouting skills: ordinary coding, ordinary writing, ordinary analysis, ordinary design, ordinary research summaries. This does not make humans useless. It makes shallow skill less protected. The premium moves toward judgment, taste, trust, ethics, leadership, original thinking, human understanding, and the ability to learn continuously."))
    st.append(P("A Muslim should not respond to this shift with panic or passivity. The correct response is preparation. Learn useful tools. Understand AI. Build technical literacy. But do not outsource your thinking, conscience, or responsibility. A tool can accelerate you, but if it replaces your effort to understand, it weakens the very faculty that makes you valuable."))
    st.append(P("Money should also be understood. Income is flow. Wealth is stored capacity. Debt can become enslavement. Capital can become service. Halal earning protects dignity. Giving purifies the heart. Financial ignorance can make a person dependent, easily pressured, and unable to help those they love."))
    st.append(callout("Future-proof direction", "Become a person who can think, learn, communicate, build trust, use tools, serve real needs, and remain morally anchored under pressure.", fill=colors.HexColor("#E5EEF1"), border=BLUE))

    st.append(chapter_title("9", "The Simple Math Of Becoming", "The math is simple enough to live: repeated inputs, honest feedback, and long horizons create disproportionate futures."))
    st.append(P("Compounding means small repeated actions become large over time. This is why tiny habits are not tiny. One focused hour a day becomes hundreds of hours a year. One page of writing a day becomes a body of thought. One sincere act repeated becomes character. One ignored sin repeated becomes a chain."))
    st.append(P("Opportunity cost means every yes is also a no. Saying yes to scrolling is saying no to attention. Saying yes to useless argument is saying no to dignity. Saying yes to sleep discipline is saying yes to tomorrow's mind."))
    st.append(P("Feedback loops mean actions shape future actions. Scrolling makes focus harder, which makes study painful, which causes more scrolling. Prayer, deep work, exercise, and service can create the opposite loop: self-respect, steadiness, and more ability to obey."))
    st.append(P("Bayesian updating is a complex name for a simple principle: update your belief when reality gives evidence. If a habit repeatedly harms you, stop calling it harmless. If a person repeatedly pulls you down, stop calling it loyalty. If a plan repeatedly fails, change the system, not only the emotion."))
    st.append(P("A local maximum is a small hill that feels like the top because climbing down first is painful. Many people stay in comfortable mediocrity because growth initially feels worse. Sometimes you must leave a lower comfort to reach a higher capacity."))
    st.append(callout("The core algorithm", "Choose the right aim. Remove the biggest blocker. Repeat the highest-leverage action. Measure honestly. Update quickly. Keep going quietly."))

    st.append(chapter_title("10", "How To Actually Start", "Do not attempt to change everything in one emotional week. Change the direction, then walk daily."))
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

    st.append(chapter_title("11", "Review Passages To Re-Read", "These are meant to be glanced through repeatedly until they become instinct."))
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
    ]:
        st.append(KeepTogether([S(title), P(body)]))

    st.append(chapter_title("12", "Sources And Anchors", "These sources are for verification. The real proof is whether the knowledge changes the life."))
    st.append(P("Qur'anic anchors: Qur'an 51:56 on purpose, Qur'an 8:60 on prepared strength, Qur'an 2:269 on wisdom, Qur'an 4:135 on justice even against oneself, and Qur'an 42:38 on consultation."))
    st.append(P("Prophetic anchors: Bukhari 1 on intentions, Muslim 2664 on the strong believer, Bukhari 6114 on anger control, and Bukhari 893 on responsibility for what is under one's care."))
    st.append(P("Modern anchors: World Economic Forum Future of Jobs Report 2025 for skill shifts; McKinsey Skill Shift for automation and changing work; American Academy of Pediatrics guidance on media and children; CDC youth mental health resources on connectedness and supportive environments."))
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
        title="The Silent Builder Book",
        author="Codex",
    )
    frame = Frame(MARGIN_X, MARGIN_Y, USABLE_W, PAGE_H - 2 * MARGIN_Y, id="normal", showBoundary=0)
    doc.addPageTemplates([PageTemplate(id="Cover", frames=frame, onPage=cover), PageTemplate(id="Body", frames=frame, onPage=on_page)])
    doc.build(story())


if __name__ == "__main__":
    main()
