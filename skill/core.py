import json
import logging
from pathlib import Path
from typing import Dict, Any 

### Импортируем модули управления ПК и кастомных API

from skill.providers.pc_control import PCController
from skill.providers.custom import CustomAPIProvider 

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")
logger = logging.getLogger("uniion") 

class UniionPlugin:
def **init**(self): 

### Настройка путей для Windows/Linux

self.base_dir = Path(**file**).resolve().parent
self.config_path = self.base_dir / "config.json"
self.config = self._load_config() 

### Фича 1: Запуск продуктов с помощью API-ключей & Фича 3: Кастомные API

custom_cfg = self.config.get("custom_api", {})
self.custom_api = CustomAPIProvider(
base_url=custom_cfg.get("base_url"),
api_key=custom_cfg.get("api_key")
) 

# Фича 2: Управление ПК (локальные команды)

self.pc = PCController()

logger.info("Плагин uniion успешно инициализирован со всеми модулями.")

def _load_config(self) -> Dict[str, Any]:
if not self.config_path.exists():
template = {
"custom_api": {
"base_url": "https://api.example.com",
"api_key": "YOUR_API_KEY_HERE"
}
}
with open(self.config_path, "w", encoding="utf-8") as f:
json.dump(template, f, indent=4, ensure_ascii=False)
return template
try:
with open(self.config_path, "r", encoding="utf-8") as f:
return json.load(f)
except Exception as e:
return {} 

def execute_command(self, service: str, action: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
"""Точка входа, обрабатывающая вызовы от ИИ Милка."""
logger.info(f"Запрос от Милки: сервис '{service}' -> действие '{action}'") 

### Маршрутизация на управление ПК

if service == "pc":
return self.pc.execute_system_command(action, data) 

# Маршрутизация на кастомные API веб-сервисов
elif service == "custom_api":
    endpoint = data.get("endpoint", "") if data else ""
    method = data.get("method", "GET") if data else "GET"
    payload = data.get("payload", {}) if data else {}
    return self.custom_api.send_request(endpoint, method, payload)
    
return {"status": "error", "message": f"Сервис '{service}' не поддерживается плагином uniion."}

if **name** == "**main**":
plugin = UniionPlugin()
