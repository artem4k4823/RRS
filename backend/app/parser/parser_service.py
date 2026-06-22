import fastfeedparser


# class Parser:
#     def __init__(self, url: str):
#         self.url = url
#         self.feed = fastfeedparser.parse(url)


    


# feed = fastfeedparser.parse('https://habr.com/ru/rss/hub/python/all/')

# for entry in feed.entries:
#     print(entry.title)
#     print(entry.link)
#     print(entry.published)  


# app/services/rss_parser.py

import httpx
import fastfeedparser
from fastapi import HTTPException, status
from typing import Dict, Any


class RSSParserService:
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
    
    async def parse_feed(self, urls: list) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
                for url in urls:
                    response = await client.get(url)
                    response.raise_for_status()
                    
                    feed = fastfeedparser.parse(response.text)
                
                if not feed:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Не удалось распарсить RSS: лента пуста"
                    )
                
                if not feed.get('entries'):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="RSS-лента не содержит записей"
                    )
                
                return feed
                
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                detail=f"Таймаут при загрузке RSS: {url}"
            )
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"HTTP ошибка {e.response.status_code} при загрузке RSS"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Не удалось прочитать RSS: {str(e)}"
            )
            



rss_parser_service = RSSParserService()