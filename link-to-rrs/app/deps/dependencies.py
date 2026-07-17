from fastapi import HTTPException, status, Query

def verify_habr_url(url: str = Query(..., description="Ссылка для парсинга (должна быть с habr.com)")) -> str:
    """
    FastAPI Dependency для проверки того, что переданная ссылка 
    действительно ведет на домен habr.com.
    """
    if not url.startswith("https://habr.com/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Указанная ссылка не является ссылкой на Habr. Ссылка должна начинаться с 'https://habr.com/'"
        )
    return url
