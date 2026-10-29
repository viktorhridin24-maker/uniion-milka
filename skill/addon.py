import json
import logging
import sys
import traceback
from pathlib import Path
from typing import Dict, Any 

### Настройка путей

BASE_DIR = Path(**file**).resolve().parent
LOG_FILE = BASE_DIR / "error_log.txt" 

if str(BASE_DIR) not in sys.path:
sys.path.insert(0, str(BASE_DIR)) 

try:
# Пробуем импортировать модули
from providers.pc_control import PCController
from providers.custom import CustomAPIProvider 

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")
logger = logging.getLogger("uniion")

class UniionPlugin:
def **init**(self):
self.base_dir = BASE_DIR
self.config_path = self.base_dir / "config.json"
self.config = self._load_config()
    custom_cfg = self.config.get("custom_api", {})
    self.custom_api = CustomAPIProvider(
        base_url=custom_cfg.get("base_url"), 
        api_key=custom_cfg.get("api_key")
    )
    
    self.pc = PCController()
    logger.info("Плагин uniion успешно инициализирован.")

def _load_config(self) -> Dict[str, Any]:
    if not self.config_path.exists():
        template = {
            "custom_api": {
                "base_url": "https://example.com",
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
    logger.info(f"Запрос от Милки: сервис '{service}' -> действие '{action}'")
    if service == "pc":
        return self.pc.execute_system_command(action, data)
    elif service == "custom_api":
        endpoint = data.get("endpoint", "") if data else ""
        method = data.get("method", "GET") if data else "GET"
        payload = data.get("payload", {}) if data else {}
        return self.custom_api.send_request(endpoint, method, payload)
    return {"status": "error", "message": f"Сервис '{service}' не поддерживается."}

plugin = UniionPlugin()

except Exception as e: 

### Если падает — жестко пишем ошибку в файл в папке плагина

with open(LOG_FILE, "w", encoding="utf-8") as f:
f.write("=== КРИТИЧЕСКАЯ ОШИБКА ЗАГРУЗКИ ПЛАГИНА ===\n")
f.write(f"Тип ошибки: {type(e).**name**}\n")
f.write(f"Сообщение: {str(e)}\n\n")
f.write("След ошибки (Traceback):\n")
traceback.print_exc(file=f) 

### Пробрасываем ошибку дальше, чтобы Милка поняла, что плагин не загрузился

raise e
