import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from typing import List, Dict
from datetime import datetime

class EmailSender:
    def __init__(self, api_key: str, sender_email: str):
        self.sg = sendgrid.SendGridAPIClient(api_key=api_key)
        self.sender_email = sender_email
    
    def send_venue_alert(self, recipient_email: str, venues: List[Dict], user_location: str, author_name: str) -> bool:
        """Send email alert with venue information"""
        try:
            subject = f"🎭 {author_name} Productions Near {user_location}"
            html_content = self._create_html_content(venues, user_location, author_name)
            text_content = self._create_text_content(venues, user_location, author_name)
            
            from_email = Email(self.sender_email)
            to_email = To(recipient_email)
            
            mail = Mail(
                from_email=from_email,
                to_emails=to_email,
                subject=subject,
                html_content=html_content,
                plain_text_content=text_content
            )
            
            response = self.sg.send(mail)
            return response.status_code == 202
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def _create_html_content(self, venues: List[Dict], user_location: str, author_name: str) -> str:
        """Create HTML email content"""
        if not venues:
            return f"""
            <html>
            <body>
                <h2>🎭 {author_name} Productions Alert</h2>
                <p>No {author_name} productions found near {user_location} at this time.</p>
                <p>We'll keep looking and notify you when something becomes available!</p>
                <hr>
                <p><small>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</small></p>
            </body>
            </html>
            """
        
        venue_html = ""
        for i, venue in enumerate(venues, 1):
            distance_info = f" ({venue['distance_miles']:.1f} miles away)" if 'distance_miles' in venue else ""
            venue_html += f"""
            <div style="margin-bottom: 20px; padding: 15px; border-left: 4px solid #8B4513; background-color: #f9f9f9;">
                <h3 style="margin-top: 0; color: #8B4513;">{i}. {venue.get('name', 'Unknown Show')}</h3>
                <p><strong>Venue:</strong> {venue.get('venue', 'Unknown Venue')}</p>
                <p><strong>Location:</strong> {venue.get('location', 'Unknown Location')}{distance_info}</p>
                <p><strong>Dates:</strong> {venue.get('dates', 'Dates TBA')}</p>
                {f'<p><a href="{venue["url"]}" style="color: #8B4513;">More Information</a></p>' if venue.get('url') else ''}
            </div>
            """
        
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #8B4513;">🎭 {author_name} Productions Near You</h2>
            <p>Found {len(venues)} {author_name} production(s) near {user_location}:</p>
            {venue_html}
            <hr style="margin: 30px 0;">
            <p style="font-size: 12px; color: #666;">
                Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}<br>
                {author_name} Alert Service
            </p>
        </body>
        </html>
        """
    
    def _create_text_content(self, venues: List[Dict], user_location: str, author_name: str) -> str:
        """Create plain text email content"""
        if not venues:
            return f"""
🎭 {author_name} PRODUCTIONS ALERT

No {author_name} productions found near {user_location} at this time.
We'll keep looking and notify you when something becomes available!

Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
            """.strip()
        
        venue_text = ""
        for i, venue in enumerate(venues, 1):
            distance_info = f" ({venue['distance_miles']:.1f} miles away)" if 'distance_miles' in venue else ""
            venue_text += f"""
{i}. {venue.get('name', 'Unknown Show')}
   Venue: {venue.get('venue', 'Unknown Venue')}
   Location: {venue.get('location', 'Unknown Location')}{distance_info}
   Dates: {venue.get('dates', 'Dates TBA')}
   {f'Info: {venue["url"]}' if venue.get('url') else ''}

"""
        
        return f"""
🎭 {author_name} PRODUCTIONS NEAR YOU

Found {len(venues)} {author_name} production(s) near {user_location}:

{venue_text}
Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
{author_name} Alert Service
        """.strip()