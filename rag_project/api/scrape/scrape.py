'''
import asyncio
from crawl4ai import AsyncWebCrawler

async def crawl4ai_scraper():
    # Create an instance of AsyncWebCrawler
    async with AsyncWebCrawler() as crawler:
        # Run the crawler on a URL
        result = await crawler.arun(url="https://crawl4ai.com")

        # Print the extracted content
        print(result.markdown)

# Run the async main function
asyncio.run(main())
'''

from langchain_community.document_loaders import RecursiveUrlLoader
def web_scraper(urls):
    loader = RecursiveUrlLoader(url=urls)
    docs = loader.load()
    return docs