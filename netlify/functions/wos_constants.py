# constants for wos_sondheim_alert
from typing import List

SHOWS: List[str] = [
    "Saturday Night",
    "Candide",
    "West Side Story",
    "Gypsy",
    "A Funny Thing Happened on the Way to the Forum",
    "Anyone Can Whistle",
    "Do I Hear a Waltz?",
    "The Mad Show",
    "Evening Primrose",
    "Company",
    "Follies",
    "A Little Night Music",
    "The Frogs",
    "Pacific Overtures",
    "Side by Side by Sondheim",
    "Sweeney Todd",
    "Marry Me a Little",
    "Merrily We Roll Along",
    "Sunday in the Park with George",
    "Into the Woods",
    "Assassins",
    "Putting It Together",
    "Passion",
    "Road Show",
    "Here We Are",
    "Hot Spot",
]

HTML_TEMPLATE: str = '''
<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1.0'>
  <title>Sondheim Shows Weekly Report</title>
</head>
<body style='background:#f4f6f8; margin:0; padding:32px;'>
{content}
</body>
</html>
'''

HTML_SHOW_TEMPLATE: str = '''
    <div style="border:3px solid #e67e22; border-radius:16px; padding:24px; margin-bottom:32px; font-family:'Segoe UI', 'Arial', 'Helvetica Neue', Arial, sans-serif; background:linear-gradient(135deg,#fffbe6 0%,#ffe0b2 100%); box-shadow:0 4px 24px rgba(230,126,34,0.15);">
        <h2 style="margin-top:0; color:#c0392b; font-size:2em; letter-spacing:1px; text-shadow:1px 1px 0 #f9ca24, 2px 2px 0 #e67e22; font-family:'Segoe UI', Arial, sans-serif;">🎭 {show_name} 🎶</h2>
        <ul style="list-style:none; padding-left:0; font-size:1.05em;">
            <li style="margin-bottom:8px;"><strong style="color:#8e44ad;">First Preview:</strong> <span style="color:#2d3436;">{first_preview}</span></li>
            <li style="margin-bottom:8px;"><strong style="color:#16a085;">Opening Night:</strong> <span style="color:#2d3436;">{opening_night}</span></li>
            <li style="margin-bottom:8px;"><strong style="color:#d35400;">Closing Night:</strong> <span style="color:#2d3436;">{closing_night}</span></li>
            <li style="margin-bottom:8px;"><strong style="color:#2980b9;">Venue:</strong> <a href="{venue_url}" style="color:#e84393; font-weight:bold; text-decoration:underline;">{venue_name}</a></li>
            <li><strong style="color:#e67e22;">More Info:</strong> <a href="{info_url}" style="color:#27ae60; font-weight:bold; background:#fff3e0; padding:4px 10px; border-radius:6px; text-decoration:none; box-shadow:1px 1px 0 #e67e22;">Show Page</a></li>
        </ul>
    </div>
'''
