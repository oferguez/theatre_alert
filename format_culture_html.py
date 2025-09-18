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
def parse_and_format_culture_html(events: list, bonus: str = None) -> str:
    """
    Accepts a list of event dicts and optional bonus, returns formatted HTML.
    """
    logger.info("parse_and_format_culture_html (structured input)...")
    return format_culture_html(events, bonus)


def format_culture_html(events: list, bonus: str = None) -> str:
    import re

    def md_to_html(text):
        # Convert **bold** and *italic* to HTML
        text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
        text = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", text)
        return text

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
    # Rainbow border colors
    rainbow_colors = [
        "#FF0000", # Red
        "#FF7F00", # Orange
        "#FFFF00", # Yellow
        "#00FF00", # Green
        "#0000FF", # Blue
        "#4B0082", # Indigo
        "#9400D3", # Violet
    ]
    # Optionally show an intro if present in the first event's desc
    if events and events[0].get("desc") and "selection of" in events[0]["desc"]:
        html += f"    <div class='intro'>{md_to_html(events[0]['desc'])}</div>\n"
        events = events[1:]
    for idx, event in enumerate(events):
        if not event.get("desc") or not event.get("venue"):
            html = (
                    "<!DOCTYPE html>\n"
                    "<html>\n"
                    "<head>\n"
                    "  <style>\n"
                    "    body { font-family: Arial, sans-serif; background: #f7f7f7; }\n"
                    "    .container { max-width: 700px; margin: 0 auto; }\n"
                    "    .header { font-size: 1.5em; margin: 30px 0 20px 0; font-weight: bold; }\n"
                    "    .intro { font-size: 1.1em; margin-bottom: 18px; color: #222; }\n"
                    "    .event-box {\n"
                    "      background: #fff;\n"
                    "      border-radius: 10px;\n"
                    "      box-shadow: 0 2px 8px rgba(0,0,0,0.07);\n"
                    "      margin-bottom: 24px;\n"
                    "      padding: 22px 28px 18px 28px;\n"
                    "      border: 6px solid #4a90e2;\n"
                    "    }\n"
                    "    .event-title { font-size: 1.15em; font-weight: bold; margin-bottom: 7px; }\n"
                    "    .event-meta { color: #555; margin-bottom: 7px; }\n"
                    "    .event-desc { font-size: 1.15em; margin-bottom: 7px; }\n"
                    "    .event-link a { color: #4a90e2; text-decoration: none; }\n"
                    "    .event-link a:hover { text-decoration: underline; }\n"
                    "  </style>\n"
                    "</head>\n"
                    "<body>\n"
                    "  <div class=\"container\">\n"
                    "    <div class=\"header\">Some Recommendations in London for the next 10 days</div>\n"
            )
            continue
        border_color = rainbow_colors[idx % len(rainbow_colors)]
        html += f'    <div class="event-box" style="border: 6px solid {border_color};">\n'
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
