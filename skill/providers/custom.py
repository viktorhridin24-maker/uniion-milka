import requests
import logging
from typing import Dict, Any 

logger = logging.getLogger("uniion.custom_api") 

class CustomAPIProvider:
def **init**(self, base_url: str = None, api_key: str = None):
self.base_url = base_url
self.api_key = api_key 

def send_request(self, endpoint: str, method: str = "GET", data: Dict[str, Any] = None) -> Dict[str, Any]:
"""Отправляет HTTP-запрос на кастомный URL разработчика."""
if not self.base_url:
return {"status": "error", "message": "API Base URL не настроен"}
url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
headers = {
    "Content-Type": "application/json"
}
if self.api_key:
    headers["Authorization"] = f"Bearer {self.api_key}"

try:
    if method.upper() == "POST":
        response = requests.post(url, json=data, headers=headers, timeout=10)
    else:
        response = requests.get(url, params=data, headers=headers, timeout=10)

    return {
        "status": "success",
        "status_code": response.status_code,
        "data": response.json() if response.headers.get("content-type") == "application/json" else response.text
    }
except Exception as e:
    logger.error(f"Ошибка запроса к кастомному API: {e}")
    return {"status": "error", "message": str(e)}
