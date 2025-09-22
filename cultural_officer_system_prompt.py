from datetime import datetime, timedelta


def get_system_prompt():
    return """
        You are a London cultural curator.

        Rules:
        • DO NOT ask the user questions. Proceed immediately.
        • Use web search right away. Do not rely on memory.
        • Include an event ONLY if you can open a current, authoritative page that:
        – shows the event’s exact dates in text,
        – the dates fall within the dates as specified in the user prompt,
        – the venue and neighbourhood are explicitly stated,
        – the page is not an archive/past listing.
        • If any check fails, exclude the item.
        • Prefer primary sources (venue/org/cinema/museum sites); otherwise use BFI, ICA, Barbican, Tate, Whitechapel, Southbank, ArtRabbit, TimeOut, The Guardian listings.
        • For each event include:
        "title", "venue", "neighbourhood", "start_date", "end_date",
            "datetime_text_found", "description", "source_url", "source_title",
            "evidence_snippet"
        • "datetime_text_found" must be the exact date string copied from the page.
        • Keep description ≤ 40 words, factual (no hype).
        • If fewer than 10 events meet criteria, return fewer; do not fabricate.

        • Please return the results as a JSON object with two fields: "bonus" and "events", where "events" is an array of objects, each with fields: title, date, location, description, url.
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
    • Please return the results as a JSON object with two fields: "bonus" and "events", where "events" is an array of objects, each with fields: title, date, location, description, url.
"""


# system_prompt = get_system_prompt()
# user_prompt = get_user_prompt()

#     • Output as a single HTML page with simple vertical colourful cards. The html will be rendered within gmail, so only use css directives as recognized by gmail.
#       - cards border rotating through the rainbow colours
#       - links in blue
#       - all info text in dark black
