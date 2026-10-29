import json
import logging
import sys
import traceback
from pathlib import Path
from typing import Dict, Any, List

BASE_DIR = Path(__file__).resolve().parent
LOG_FILE = BASE_DIR / "error_log.txt"

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

try:
    from providers.pc_control import PCController
    from providers.custom import CustomAPIProvider

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")
    logger = logging.getLogger("uniion")

    class UniionPlugin:
        def __init__(self):
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

        def get_system_prompt(self) -> str:
            """Передает Милке инструкцию о том, что она умеет управлять ПК."""
            return (
                "Ты — ИИ Милка с установленным плагином uniion. "
                "Ты ИМЕЕШЬ ДОСТУП к компьютеру пользователя и МОЖЕШЬ открывать программы, "
                "сайты и файлы локально. Когда тебя просят запустить программу (например, VS Code), "
                "используй функцию execute_command с сервисом 'pc' и действием 'open_program'."
            )

        def get_tools(self) -> List[Dict[str, Any]]:
            """Передает список доступных функций для отображения в Milky."""
            return [
                {
                    "name": "open_program",
                    "description": "Запускает указанную программу, открывает файл или веб-сайт на компьютере.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Полный путь к программе, её системное имя (например, 'code') или URL сайта."
                            }
                        },
                        "required": ["path"]
                    }
                }
            ]

        def execute_command(self, service: str, action: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
            logger.info(f"Запрос от Милки: сервис '{service}' -> действие '{action}'")
            
            # Поддерживаем вызов как через сервис 'pc', так и напрямую через имя экшена
            if service == "pc" or action == "open_program":
                path_param = data.get("path", "") if data else ""
                return self.pc.execute_system_command("open_program", {"path": path_param})
                
            elif service == "custom_api":
                endpoint = data.get("endpoint", "") if data else ""
                method = data.get("method", "GET") if data else "GET"
                payload = data.get("payload", {}) if data else {}
                return self.custom_api.send_request(endpoint, method, payload)
                
            return {"status": "error", "message": f"Сервис '{service}' не поддерживается."}

    plugin = UniionPlugin()

except Exception as e:
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("=== КРИТИЧЕСКАЯ ОШИБКА ЗАГРУЗКИ ПЛАГИНА ===\n")
        f.write(f"Тип ошибки: {type(e).__name__}\n")
        f.write(f"Сообщение: {str(e)}\n\n")
        f.write("След ошибки (Traceback):\n")
        traceback.print_exc(file=f)
    raise e
