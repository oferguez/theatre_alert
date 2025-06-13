"""
venue_finder.py

This module provides the VenueFinder class for searching, deduplicating,
and filtering theatre venues and productions by location and distance.
"""

from typing import List, Dict, Optional
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

class VenueFinder:
    """
    VenueFinder provides methods to search for theatre venues and productions, deduplicate results,
    filter by distance, and retrieve venue coordinates using geolocation services.
    """
    def __init__(self):
        self.geolocator = Nominatim(user_agent="theatre_alert")

    def search_author_productions(self) -> List[Dict]:
        """Search for current author productions"""
        venues = []

        # Search multiple sources
        venues.extend(self._search_broadway_world())
        venues.extend(self._search_playbill())
        venues.extend(self._search_theatreguide())

        return self._deduplicate_venues(venues)

    def _search_broadway_world(self) -> List[Dict]:
        """Search BroadwayWorld for your favourite author productions"""
        venues = []
        try:
            # Search for common author shows
            # TODO: Move shows list to configuration or external source
            shows = [
                "Into the Woods", "Sweeney Todd", "Company", "Sunday in the Park",
                "A Little Night Music", "Assassins", "Passion", "Follies",
                "Anyone Can Whistle", "Getting Away with Murder"
            ]

            for show in shows:
                venues.extend(self._search_show_on_broadwayworld(show))

        except Exception as e: # pylint: disable=broad-except
            print(f"Error searching BroadwayWorld: {e}")

        return venues

    def _search_show_on_broadwayworld(self, show_name: str) -> List[Dict]:
        """Search for a specific show on BroadwayWorld"""
        venues = []
        try:
            # This would need to be implemented with actual web scraping
            # For now, returning mock data structure
            # In real implementation, you'd use BeautifulSoup to scrape
            pass
        except Exception as e: # pylint: disable=broad-except
            print(f"Error searching for {show_name}: {e}")

        return venues

    def _search_playbill(self) -> List[Dict]:
        """Search Playbill for author's productions"""
        # Similar implementation to BroadwayWorld
        return []

    def _search_theatreguide(self) -> List[Dict]:
        """Search Theatre Guide for author's productions"""
        # Similar implementation to BroadwayWorld
        return []

    def _deduplicate_venues(self, venues: List[Dict]) -> List[Dict]:
        """Remove duplicate venues based on name and location"""
        seen = set()
        unique_venues = []

        for venue in venues:
            key = f"{venue.get('name', '').lower()}_{venue.get('location', '').lower()}"
            if key not in seen:
                seen.add(key)
                unique_venues.append(venue)

        return unique_venues

    def get_venue_coordinates(self, location: str) -> Optional[tuple]:
        """Get latitude and longitude for a location"""
        try:
            location_data = self.geolocator.geocode(location)
            if location_data:
                return (location_data.latitude, location_data.longitude)
        except Exception as e: # pylint: disable=broad-except
            print(f"Error geocoding {location}: {e}")
        return None

    def calculate_distance(self, coord1: tuple, coord2: tuple) -> float:
        """Calculate distance between two coordinates in miles"""
        return geodesic(coord1, coord2).miles

    def filter_by_distance(self, venues: List[Dict], user_location: str,
                           max_distance: int) -> List[Dict]:
        """Filter venues by distance from user location"""
        user_coords = self.get_venue_coordinates(user_location)
        if not user_coords:
            return venues

        filtered_venues = []
        for venue in venues:
            venue_coords = self.get_venue_coordinates(venue.get('location', ''))
            if venue_coords:
                distance = self.calculate_distance(user_coords, venue_coords)
                venue['distance_miles'] = distance
                if distance <= max_distance:
                    filtered_venues.append(venue)

        # Sort by distance
        return sorted(filtered_venues, key=lambda x: x.get('distance_miles', float('inf')))

    def get_mock_venues(self) -> List[Dict]:
        """Return mock data for testing purposes"""
        return [
            {
                'name': 'Into the Woods',
                'venue': 'Lincoln Center Theater',
                'location': 'New York, NY',
                'dates': 'Now through January 2025',
                'url': 'https://example.com/into-the-woods',
                'distance_miles': 5.2
            },
            {
                'name': 'Sweeney Todd',
                'venue': 'Broadway Theatre',
                'location': 'New York, NY',
                'dates': 'December 2024 - March 2025',
                'url': 'https://example.com/sweeney-todd',
                'distance_miles': 6.1
            },
            {
                'name': 'Company',
                'venue': 'Regional Theatre',
                'location': 'Philadelphia, PA',
                'dates': 'January - February 2025',
                'url': 'https://example.com/company',
                'distance_miles': 95.3
            }
        ]
