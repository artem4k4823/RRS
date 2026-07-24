import aiohttp
import asyncio
import re
from urllib.parse import urlparse, urlunparse
from bs4 import BeautifulSoup


async def fetch_page_articles(session: aiohttp.ClientSession, url: str, headers: dict) -> list:
    try:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                return []
            html = await response.text()
            soup = BeautifulSoup(html, 'lxml')
            articles = soup.find_all('article', class_='tm-articles-list__item')
            parsed_data = []
            
            for article in articles:
                author_tag = article.find('a', class_='tm-user-info__username')
                author = author_tag.text.strip() if author_tag else None
                
                date_tag = article.find('time')
                date = date_tag.get('datetime') if date_tag else None
                
                title_tag = article.find('h2', class_='tm-title').find('a') if article.find('h2', class_='tm-title') else None
                title = title_tag.text.strip() if title_tag else None
                link = f"https://habr.com{title_tag.get('href')}" if title_tag and title_tag.get('href') else None
                
                desc_tag = article.find('div', class_='article-formatted-body')
                description = desc_tag.text.strip() if desc_tag else None
                
                image = None
                img_tag = article.select_one('div.article-formatted-body img')
                if not img_tag:
                    img_tag = article.select_one('.tm-article-snippet__lead-image')
                if not img_tag:
                    img_tag = article.select_one('.lead-image')
                if img_tag:
                    image = img_tag.get('src')
                
                parsed_data.append({
                    'author': author,
                    'date': date,
                    'title': title,
                    'link': link,
                    'description': description,
                    'image': image
                })
            return parsed_data
    except Exception:
        return []


async def get_habr_data(url: str, pages: int = 1) -> list:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    
    pages_count = max(1, int(pages))
    
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme or 'https'
    netloc = parsed_url.netloc or 'habr.com'
    path = parsed_url.path or '/'
    
 
    clean_path = re.sub(r'/page\d+/?$', '/', path)
    if not clean_path.endswith('/'):
        clean_path += '/'
        
    page_urls = []
    for p in range(1, pages_count + 1):
        p_path = f"{clean_path.rstrip('/')}/page{p}/"
        full_url = urlunparse((scheme, netloc, p_path, parsed_url.params, parsed_url.query, parsed_url.fragment))
        page_urls.append(full_url)
        
    all_articles = []
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_page_articles(session, p_url, headers) for p_url in page_urls]
        results = await asyncio.gather(*tasks)
        for page_articles in results:
            all_articles.extend(page_articles)
            
    return all_articles


if __name__ == '__main__':
    test_url = "/ru/flows/mobile_development/articles/page1/"
    posts = asyncio.run(get_habr_data(test_url, pages=3))
    print(f"Всего спарсено постов: {len(posts)}")
    for post in posts:
        print(f"Заголовок: {post['title']}")
        print(f"Автор: {post['author']} | Дата: {post['date']}")
        print(f"Ссылка: {post['link']}")
        desc = post['description'][:100] + "..." if post['description'] else "Нет описания"
        print(f"Описание: {desc}")
        print(f"Картинка: {post['image']}\n")