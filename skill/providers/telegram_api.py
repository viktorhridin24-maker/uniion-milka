import logging
import urllib.request
import urllib.parse
import json
from typing import Dict, Any

logger = logging.getLogger("uniion.telegram")

class TelegramProvider:
    def __init__(self, token: str = None, chat_id: str = None):
        self.token = token
        self.chat_id = chat_id

    def send_message(self, text: str, custom_token: str = None, custom_chat_id: str = None) -> Dict[str, Any]:
        """Отправляет текстовое сообщение в Telegram через официальный Bot API."""
        bot_token = custom_token or self.token
        target_chat = custom_chat_id or self.chat_id

        if not bot_token or not target_chat:
            return {"status": "error", "message": "Пропущен Telegram Token или Chat ID"}

        url = f"https://telegram.org{bot_token}/sendMessage"
        data = urllib.parse.urlencode({"chat_id": target_chat, "text": text}).encode("utf-8")
        
        try:
            req = urllib.request.Request(url, data=data, method="POST")
            with urllib.request.urlopen(req, timeout=5) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                if res_data.get("ok"):
                    return {"status": "success", "message": "Сообщение успешно отправлено в Telegram."}
                return {"status": "error", "message": res_data.get("description", "Неизвестная ошибка API")}
        except Exception as e:
            logger.error(f"Ошибка отправки в Telegram: {e}")
            return {"status": "error", "message": str(e)}
