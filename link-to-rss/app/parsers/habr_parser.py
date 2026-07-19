import aiohttp
import asyncio
from bs4 import BeautifulSoup



async def get_habr_data(url: str) -> dict:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
           
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
                link = f"https://habr.com{title_tag.get('href')}" if title_tag else None
                
               
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

if __name__ == '__main__':
    
    posts = asyncio.run(get_habr_data())
    for post in posts[:3]:
        print(f"Заголовок: {post['title']}")
        print(f"Автор: {post['author']} | Дата: {post['date']}")
        print(f"Ссылка: {post['link']}")
        desc = post['description'][:100] + "..." if post['description'] else "Нет описания"
        print(f"Описание: {desc}")
        print(f"Картинка: {post['image']}\n")