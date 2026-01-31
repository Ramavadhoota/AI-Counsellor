import httpx
from typing import List, Dict, Any, Optional
from app.config import settings
import asyncio

class UniversityService:
    """Service to fetch university data from external API"""
    
    def __init__(self):
        self.base_url = settings.UNIVERSITY_API_URL
        self.timeout = 10.0
    
    async def search_universities(
        self,
        country: Optional[str] = None,
        name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search universities by country and/or name
        
        Args:
            country: Country name or code
            name: University name search query
        
        Returns:
            List of universities
        """
        params = {}
        
        if country:
            params['country'] = country
        
        if name:
            params['name'] = name
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/search",
                    params=params
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            return []
        except Exception as e:
            print(f"Error fetching universities: {e}")
            return []
    
    async def get_universities_by_country(self, country: str) -> List[Dict[str, Any]]:
        """Get all universities in a country"""
        return await self.search_universities(country=country)
    
    async def get_universities_by_name(self, name: str) -> List[Dict[str, Any]]:
        """Search universities by name"""
        return await self.search_universities(name=name)
    
    def format_university_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format raw university data into standardized structure
        
        Args:
            raw_data: Raw data from API
        
        Returns:
            Formatted university data
        """
        return {
            "name": raw_data.get("name", "Unknown"),
            "country": raw_data.get("country", "Unknown"),
            "web_pages": raw_data.get("web_pages", []),
            "domains": raw_data.get("domains", []),
            "alpha_two_code": raw_data.get("alpha_two_code", ""),
            "state_province": raw_data.get("state-province")
        }
    
    async def get_multiple_countries(
        self,
        countries: List[str],
        limit_per_country: int = 10
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Fetch universities from multiple countries concurrently
        
        Args:
            countries: List of country names/codes
            limit_per_country: Max universities per country
        
        Returns:
            Dictionary mapping country to universities
        """
        tasks = [
            self.search_universities(country=country)
            for country in countries
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        country_universities = {}
        for country, result in zip(countries, results):
            if isinstance(result, list):
                country_universities[country] = result[:limit_per_country]
            else:
                country_universities[country] = []
        
        return country_universities

# Singleton instance
university_service = UniversityService()
