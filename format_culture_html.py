import logging

"""
Format GPT event recommendations into structured HTML with boxes and a custom header.
"""

# Configure logger
logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s"
)
logger = logging.getLogger("culture_officer")


# Dedicated parser/formatter for GPT output
def parse_and_format_culture_html(gpt_result: str) -> str:
    logger.info("parse_and_format_culture_html...")

    import re

    events = []
    bonus = None
    event_blocks = re.split(
        r"\n---\n\n.*?(?=[\U0001F3A8\U0001F3AD\U0001F3A5\U0001F3A4\U0001F4DA])",
        gpt_result,
    )
    for block in event_blocks:
        lines = block.strip().split("\n")
        if not lines or not lines[0].strip():
            continue
        if lines[0].startswith("✨") or lines[0].lower().startswith("for something"):
            bonus = " ".join(lines)
            continue
        title = lines[0].strip()
        venue = date = desc = link = link_text = ""
        for l in lines[1:]:
            l = l.strip()
            if l.startswith("📍"):
                venue = l.replace("📍", "").strip()
            elif l.startswith("📅"):
                date = l.replace("📅", "").strip()
            elif l.startswith("📖"):
                desc = l.replace("📖", "").strip()
            elif l.startswith("🔗"):
                match = re.search(r"\[(.*?)\]\((.*?)\)", l)
                if match:
                    link_text, link = match.groups()
        events.append(
            {
                "title": title,
                "venue": venue,
                "date": date,
                "desc": desc,
                "link": link,
                "link_text": link_text,
            }
        )
    return format_culture_html(events, bonus)


def format_culture_html(events: list, bonus: str = None) -> str:
    import re

    def md_to_html(text):
        # Convert **bold** and *italic* to HTML
        text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
        text = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", text)
        return text

    html = """<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: Arial, sans-serif; background: #f7f7f7; }
    .container { max-width: 700px; margin: 0 auto; }
    .header { font-size: 1.5em; margin: 30px 0 20px 0; font-weight: bold; }
    .intro { font-size: 1.1em; margin-bottom: 18px; color: #222; }
    .event-box {
      background: #fff;
      border-radius: 10px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.07);
      margin-bottom: 24px;
      padding: 22px 28px 18px 28px;
      border: 6px solid #4a90e2;
    }
    .event-title { font-size: 1.15em; font-weight: bold; margin-bottom: 7px; }
    .event-meta { color: #555; margin-bottom: 7px; }
    .event-desc { font-size: 1.15em; margin-bottom: 7px; }
    .event-link a { color: #4a90e2; text-decoration: none; }
    .event-link a:hover { text-decoration: underline; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">Some Recommendations in London for the next 10 days</div>
"""
    # Optionally show an intro if present in the first event's desc
    if events and events[0]["desc"] and "selection of" in events[0]["desc"]:
        html += f"    <div class='intro'>{md_to_html(events[0]['desc'])}</div>\n"
        events = events[1:]
    for event in events:
        if not event.get("desc") or not event.get("venue"):
            continue
        html += f'    <div class="event-box">\n'
        html += f"      <div class=\"event-title\">{md_to_html(event.get('title',''))}</div>\n"
        html += f"      <div class=\"event-meta\"><b>{md_to_html(event.get('venue',''))}</b> &mdash; {md_to_html(event.get('date',''))}</div>\n"
        html += f"      <div class=\"event-desc\">{md_to_html(event.get('desc',''))}</div>\n"
        if event.get("link", ""):
            html += f"      <div class=\"event-link\"><a href=\"{event.get('link','')}\" target=\"_blank\">{md_to_html(event.get('link_text','More Info'))}</a></div>\n"
        html += "    </div>\n"
    if bonus:
        html += f'    <div class="event-box" style="border-left: 6px solid #e26a4a;">\n'
        html += f'      <div class="event-title">✨ Bonus Suggestion</div>\n'
        html += f'      <div class="event-desc">{md_to_html(bonus)}</div>\n'
        html += "    </div>\n"
    html += "  </div>\n</body>\n</html>"
    logger.info(f"Formatted HTML output successfully. size={len(html)} characters")
    return html


# Example usage:
if __name__ == "__main__":
    events = [
        {
            "title": '🖼️ Exhibition: "Queer Spaces: London, 1980s–Today"',
            "venue": "Whitechapel Gallery, Whitechapel",
            "date": "Until October 10, 2021",
            "desc": "Explore the evolution of queer spaces in London through photography, film, and personal testimonies, reflecting on the ongoing struggle for LGBTQ+ rights.",
            "link": "https://www.whitechapelgallery.org/exhibitions/queer-spaces-london-1980s-today/",
            "link_text": "Whitechapel Gallery - Queer Spaces Exhibition",
        },
        # ... more events ...
    ]
    bonus = "For something unexpected but potentially captivating, you might enjoy exploring a pop-up immersive theatre experience that challenges traditional narratives and invites audience participation in a thought-provoking way."
    print(format_culture_html(events, bonus))
