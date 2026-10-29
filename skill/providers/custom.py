import urllib.request
import urllib.error
import json
import logging
from typing import Dict, Any

logger = logging.getLogger("uniion.custom_api")

class CustomAPIProvider:
    def __init__(self, base_url: str = None, api_key: str = None):
        self.base_url = base_url
        self.api_key = api_key

    def send_request(self, endpoint: str, method: str = "GET", data: Dict[str, Any] = None) -> Dict[str, Any]:
        if not self.base_url:
            return {"status": "error", "message": "API Base URL не настроен"}
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        try:
            req_data = None
            if data and method.upper() == "POST":
                req_data = json.dumps(data).encode("utf-8")
            req = urllib.request.Request(url, data=req_data, headers=headers, method=method.upper())
            with urllib.request.urlopen(req, timeout=10) as response:
                resp_data = response.read().decode("utf-8")
                try:
                    return {"status": "success", "status_code": response.status, "data": json.loads(resp_data)}
                except json.JSONDecodeError:
                    return {"status": "success", "status_code": response.status, "data": resp_data}
        except urllib.error.HTTPError as e:
            return {"status": "error", "status_code": e.code, "message": str(e)}
        except Exception as e:
            logger.error(f"Ошибка запроса: {e}")
            return {"status": "error", "message": str(e)}
