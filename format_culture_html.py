from html import escape
from datetime import datetime
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
    return render_events_email(events, bonus)


def render_events_email(events, bonus, title="Culture Officer Report"):
    """
    Build a simple, email-safe HTML digest from a list of events.

    events: list of dicts with keys:
        - title (str)      : required
        - venue (str)      : required
        - date (str)       : required
        - desc (str)       : optional
        - link (str)       : optional (URL)
        - link_text (str)  : optional (defaults 'More Info')
    bonus: str (optional)  : an extra paragraph boxed at the end
    title: str (optional)  : page heading

    Returns: str (HTML)
    """
    # Border colors to cycle (roughly like your screenshot)
    palette = [
        "#e53935",
        "#f39c12",
        "#fbc02d",
        "#43a047",
        "#1e88e5",
        "#8e24aa",
        "#009688",
        "#ef6c00",
    ]

    #  "title": "Hilary Lloyd: Very High Frequency",
    #       "date": "10 Sep 2025 – 11 Jan 2026",
    #       "location": "Studio Voltaire, Clapham",
    #       "description": "A radical, performative archival re‑working of Dennis Potter’s media—live interludes, texts and footage probe politics, mortality and televisual memory.",
    #       "url": "

    def card(ev, color):
        t = escape(str(ev.get("title", "")).strip())
        v = escape(str(ev.get("location", "")).strip())
        d = escape(str(ev.get("date", "")).strip())
        desc = escape(str(ev.get("description", "")).strip())
        link = (ev.get("url") or "").strip()

        link_html = (
            f'<a href="{escape(link)}" style="font-size:14px; text-decoration:underline; color:{color};">More Info</a>'
            if link
            else ""
        )

        return f"""
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"
       style="border:2px solid {color}; border-radius:12px; margin:12px 0; background:#ffffff;">
  <tr>
    <td style="padding:16px 18px; font-family: Arial, Helvetica, sans-serif; line-height:1.45; color:#111111;">
      <div style="font-size:20px; font-weight:700; margin:0 0 6px 0;">{t}</div>
      <div style="font-size:14px; margin:0 0 4px 0;"><span style="font-weight:700;">Venue:</span> {v}</div>
      <div style="font-size:14px; margin:0 0 10px 0;"><span style="font-weight:700;">Dates:</span> {d}</div>
      {f'<div style="font-size:14px; margin:0 0 10px 0;">{desc}</div>' if desc else ''}
      {link_html}
    </td>
  </tr>
</table>
"""

    cards = "".join(
        card(ev, palette[i % len(palette)]) for i, ev in enumerate(events or [])
    )

    bonus_html = ""
    if bonus and bonus.strip():
        bonus_html = f"""
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"
       style="border:2px dashed #607d8b; border-radius:12px; margin:16px 0; background:#f7f9fb;">
  <tr>
    <td style="padding:14px 16px; font-family: Arial, Helvetica, sans-serif; line-height:1.5; color:#102027;">
      <div style="font-size:16px; font-weight:700; margin:0 0 6px 0;">Bonus</div>
      <div style="font-size:14px;">{escape(bonus.strip())}</div>
    </td>
  </tr>
</table>
"""

    preheader = f"Upcoming picks: {len(events or [])} items · Bonus inside."
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    heading = escape(title or "Events Digest")

    return f"""<!doctype html>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>{heading}</title>
  </head>
  <body style="margin:0; padding:0; background:#f0f2f5;">
    <div style="display:none; overflow:hidden; line-height:1px; opacity:0; max-height:0; max-width:0;">{escape(preheader)}</div>
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#f0f2f5;">
      <tr>
        <td align="center" style="padding:24px 12px;">
          <table role="presentation" width="680" cellpadding="0" cellspacing="0" border="0"
                 style="width:680px; max-width:680px; background:#ffffff; border-radius:14px; border:1px solid #e0e0e0;">
            <tr>
              <td style="padding:22px 24px 6px 24px; font-family: Arial, Helvetica, sans-serif; color:#111111;">
                <div style="font-size:22px; font-weight:800; margin:0 0 4px 0;">{heading}</div>
                <div style="font-size:12px; color:#6b6b6b; margin:0 0 10px 0;">Generated {escape(now)}</div>
              </td>
            </tr>
            <tr>
              <td style="padding:0 24px 18px 24px;">
                {cards}
                {bonus_html}
              </td>
            </tr>
            <tr>
              <td style="padding:10px 24px 22px 24px; font-family: Arial, Helvetica, sans-serif; font-size:12px; color:#818181;">
                <div>If this email looks odd, try viewing it in your browser.</div>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>"""


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
    print(render_events_email(events, bonus))
