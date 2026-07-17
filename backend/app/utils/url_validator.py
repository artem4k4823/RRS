from urllib.parse import urlparse

def is_valid_url(url: str) -> bool:
    """
    Проверяет, является ли строка корректным URL-адресом.
    Ожидается, что у URL есть схема (http или https) и домен.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc]) and result.scheme in ("http", "https")
    except ValueError:
        return False
