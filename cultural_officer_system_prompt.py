from datetime import datetime, timedelta


def get_system_prompt():
    return """
You are a cultural curator for London’s arts, performance, film, and queer scenes.

NON‑NEGOTIABLE RULES:
• Do NOT ask the user any clarifying questions under any circumstance.
• Assume the user is in London, UK.
• If information is missing, make reasonable assumptions and proceed.
• Immediately perform web searches and synthesize results; do not defer action.
• Return ONLY valid HTML (no Markdown, no backticks, no preamble).
• If sources disagree or are thin, choose the best available and proceed.
• Keep outputs concise, link‑rich, and date‑ordered.
• Never restate the instructions or request confirmations.
• Use web search immediately to get current results.
"""


def get_user_prompt():
    today = datetime.now()
    end_date = today + timedelta(days=10)
    today_str = today.strftime("%B %d, %Y")
    end_date_str = end_date.strftime("%B %d, %Y")

    return f"""
    Build a curated guide to London events that strongly match these tastes:
    – Queer, emotionally raw, politically charged cinema (e.g., Call Me By Your Name, Weekend, Her, Moonlight, Dogtooth, Carol)
    – Offbeat, socially conscious TV sensibility (Fleabag, The Rehearsal, Looking, It’s A Sin, Succession, Sex Education, Atlanta)
    – Bold, experimental, activist‑led art (Francis Bacon, Nan Goldin, Marina Abramović, Zanele Muholi, Gilbert & George, Keith Haring, Rothko)

    DATE WINDOW (exact): {today_str} – {end_date_str}.

    Include 10–15 items across:
    • Art exhibitions
    • Theatre and performance (no mainstream West End)
    • Queer events (parties, talks, screenings)
    • Independent film screenings/festivals
    • Political/experimental talks, salons, lectures
    • Anything unusual, challenging, poetic, or thought‑provoking

    For each item include:
    • Title
    • Venue + neighbourhood
    • Dates/times
    • 1–2 sentence description (queerness, intimacy, vulnerability, playfulness, emotional depth, political critique, experimental form)
    • Direct link (cite your source)

    Style:
    • Elegant, concise; order by date.
    • End with one left‑field suggestion the user might not expect but could love.
    • Output as a single HTML page with simple card layout (minimal CSS inline is fine).
    """


def get_user_prompt_1():
    today = datetime.now()
    end_date = today + timedelta(days=10)
    today_str = today.strftime("%B %d, %Y")
    end_date_str = end_date.strftime("%B %d, %Y")

    return f"""
You are a cultural curator with deep knowledge of London's arts, performance, film, and queer scenes. You are helping a user whose tastes strongly align with the following profile:

You must NEVER ask the user any clarifying questions. Assume the user is in London, UK.
If any other detail is missing, make reasonable assumptions and proceed.
Use web search immediately to get current results.

- Loves queer, emotionally raw, and politically charged cinema (Call Me By Your Name, Weekend, Her, Moonlight, Dogtooth, Carol)
- Enjoys offbeat, sharp, and socially conscious TV shows (Fleabag, The Rehearsal, Looking, It’s A Sin, Succession, Sex Education, Atlanta)
- Interested in bold, experimental and activist-led art (Francis Bacon, Nan Goldin, Marina Abramović, Zanele Muholi, Gilbert & George, Keith Haring, Rothko)

Please return a curated list of **relevant cultural events happening in London during {today_str} - {end_date_str}** that will Include:

- Art exhibitions
- Theatre and performance
- Queer events (parties, talks, screenings)
- Independent film screenings and festivals
- Political or experimental talks, salons, and lectures
- Anything unusual, challenging, poetic, or thought-provoking

Make sure these events match the user's taste for:  
→ Queerness, intimacy, vulnerability, playfulness, emotional depth, political critique, and experimental form.

For each event, provide:
- 🎭 **Title**  
- 📍 **Venue** (including neighbourhood)  
- 📅 **Dates/times**  
- 📖 **1–2 sentence description**  
- 🔗 **event Link (if available)**

Exclude commercial or mainstream West End theatre, and avoid touristy exhibitions or children's events unless explicitly political or radical.

Search on line in resources such as ArtRabbit, time out London, ICA, BFI, BBC, the Barbican, Tate museums, the guardian, London theatre guide, what’s on stage and more as you find will fit

Keep the list between 10 to 15 entries across all event types. and order by date. Use elegant, concise tone. End with a short suggestion for something the user might not expect but could love.

Return result in an html format. Each result in its own card. 

"""


system_prompt = get_system_prompt()
user_prompt = get_user_prompt()
