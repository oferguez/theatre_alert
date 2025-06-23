"""
Consumer Key	ZsknChi2tE4GxAWH4uSbfduzj5REVYEJ
Consumer Secret	npVnGcS0F36HZ8oP
Key Issued	Thu, 06/19/2025 - 13:22
Key Expires	Never
"""

from pprint import PrettyPrinter
from typing import List
import requests


api_key: str = 'ZsknChi2tE4GxAWH4uSbfduzj5REVYEJ'
base_url: str = 'https://app.ticketmaster.com/discovery/v2/'
_shows: List[str] = [
    'Gypsy'
]
shows: List[str] = [
        'Here We Are',

        'Saturday Night',
        'Candide',
        'West Side Story',
        'Gypsy',
        'A Funny Thing Happened on the Way to the Forum',
        'Anyone Can Whistle',
        'Do I Hear a Waltz?',
        'The Mad Show',
        'Evening Primrose',
        'Company',
        'Follies',
        'A Little Night Music',
        'The Frogs',
        'Pacific Overtures',
        'Side by Side by Sondheim',
        'Sweeney Todd',
        'Marry Me a Little',
        'Merrily We Roll Along',
        'Sunday in the Park with George',
        'Into the Woods',
        'Assassins',
        'Putting It Together',
        'Passion',
        'Road Show',
        'Here We Are',
        'Hot Spot'
        ]



def handler(_event, _context):
    """
    entry point for scheduled serverless function
    """

    for show in shows:
        show = show.replace(' ','+')
        query_url: str = f'{base_url}events.json?keyword={show}&apikey={api_key}'
        response = requests.get(query_url, timeout=30)
        result = response.json()
        if True or ('page' in result and result['page']['totalPages'] > 0):
            print(query_url)
            PrettyPrinter().pprint(result)
            print()

if __name__ == "__main__":
    handler({}, {})

"""
allocated key
curl -o obs/r.json 'https://app.ticketmaster.com/discovery/v2/events.json?keyword=sondheim&countryCode=GB&apikey=ZsknChi2tE4GxAWH4uSbfduzj5REVYEJ'


doc apikey ->
curl 'https://app.ticketmaster.com/discovery/v2/events.json?keyword=sondheim&countryCode=GB&apikey=ZsknChi2tE4GxAWH4uSbfduzj5REVYEJ'
"""

