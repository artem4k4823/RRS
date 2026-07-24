from feedgen.feed import FeedGenerator
import datetime
from app.parsers.habr_parser import get_habr_data


async def generate_rss_for_url(url: str, pages: int = 1, title: str = "Generated RSS Feed", description: str = "Автоматически сгенерированный RSS") -> str:
    
    fg = FeedGenerator()
    
    
    articles = await get_habr_data(url, pages=pages)
    
   
    fg.id(url)
    fg.title(title)
    fg.description(description)
    fg.link(href=url, rel='alternate')
    fg.language('ru')
    
    
    for article in articles:
        fe = fg.add_entry()
        
        
        article_link = article.get("link") or url
        fe.id(article_link)
        fe.link(href=article_link)
        
       
        fe.title(article.get("title") or "Без заголовка")
        
       
        desc = article.get("description") or "Нет описания"
        fe.description(desc)
        
        
        author = article.get("author")
        if author:
            fe.author({'name': author})
            
       
        date_str = article.get("date")
        if date_str:
            try:
                dt = datetime.datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                fe.pubDate(dt)
            except ValueError:
                fe.pubDate(datetime.datetime.now(datetime.timezone.utc))
        else:
            fe.pubDate(datetime.datetime.now(datetime.timezone.utc))
        
    rss_xml = fg.rss_str(pretty=True)
    return rss_xml.decode('utf-8')

