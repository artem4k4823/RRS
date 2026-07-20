from app.schemas.url import UrlRequest
import base64
from uuid import uuid4



def encode_url(body: UrlRequest):
    return base64.urlsafe_b64encode(body.url.encode('utf-8')).decode('utf-8')

def decode_url(encoded_url: str):
    return base64.urlsafe_b64decode(encoded_url.encode('utf-8')).decode('utf-8')
