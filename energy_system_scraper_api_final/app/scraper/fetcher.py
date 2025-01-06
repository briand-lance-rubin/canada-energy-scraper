import aiohttp
import asyncio
from config import logger

class Fetcher:
    """
    Fetcher class for retrieving raw HTML content from a given URL asynchronously.
    """

    def __init__(self, url):
        """
        Initializes the Fetcher with the given URL.

        Args:
            url (str): The URL to fetch data from.
        """
        self.url = url

    async def fetch(self):
        """
        Fetches the raw HTML content from the specified URL asynchronously.

        Returns:
            str: Raw HTML content as a string.
        """
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.url) as response:
                    # Ensure a successful response
                    response.raise_for_status()
                    html_content = await response.text()
                    logger.info(f"Data fetched successfully from {self.url}")
                    return html_content
            except Exception as e:
                logger.error(f"Error fetching data from {self.url}: {e}")
                raise
