from app.schemas.url import UrlRequest
import base64
import json


def encode_url(body: UrlRequest) -> str:
    data = {"url": body.url, "pages": body.pages}
    return base64.urlsafe_b64encode(json.dumps(data).encode('utf-8')).decode('utf-8')


def decode_url(encoded_url: str) -> dict:
    decoded_str = base64.urlsafe_b64decode(encoded_url.encode('utf-8')).decode('utf-8')
    try:
        data = json.loads(decoded_str)
        if isinstance(data, dict):
            return data
    except (json.JSONDecodeError, TypeError):
        pass
    return {"url": decoded_str, "pages": 1}

