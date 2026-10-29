import sys
import json
import logging
from pathlib import Path
from addon_api import tool, AddonContext

# Настройка путей для внутренней папки providers
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

try:
    from providers.pc_control import PCController
    from providers.custom import CustomAPIProvider
    pc_handler = PCController()
except Exception as e:
    # Защита от падения при импорте (Best Practices из доки Стёпы)
    pc_handler = None


def setup(ctx: AddonContext):
    """Вызывается движком Milky один раз при успешной загрузке плагина."""
    ctx.log("Плагин uniion успешно загружен в систему Milky!")


@tool(
    "open_program",
    "Запускает указанную программу, открывает локальный файл или веб-сайт на компьютере пользователя.",
    {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Системное имя программы (например, 'code' для VS Code), путь к файлу или URL сайта."
            }
        },
        "required": ["path"]
    }
)
def open_program(path: str, ctx: AddonContext):
    """Инструмент открытия программ, который Милка сможет вызывать из чата."""
    if not pc_handler:
        return "Ошибка: Модуль управления ПК не был инициализирован."
    
    ctx.log(f"Милка вызвала инструмент open_program для пути: {path}")
    result = pc_handler.execute_system_command("open_program", {"path": path})
    return result.get("message", "Команда выполнена")


@tool(
    "custom_api_request",
    "Отправляет HTTP-запрос к кастомному API разработчика.",
    {
        "type": "object",
        "properties": {
            "endpoint": {"type": "string", "description": "Эндпоинт, например '/status'"},
            "method": {"type": "string", "description": "HTTP метод: GET или POST"},
            "payload": {"type": "object", "description": "JSON-данные для POST-запроса"}
        },
        "required": ["endpoint"]
    }
)
def custom_api_request(endpoint: str, method: str = "GET", payload: dict = None, ctx: AddonContext = None):
    """Инструмент для веб-запросов к твоим продуктам."""
    # Получаем настройки из родного settings.json Милки (как просил Стёпа!)
    base_url = ctx.settings.get("custom_api_url") if ctx else None
    api_key = ctx.settings.get("custom_api_key") if ctx else None
    
    if not base_url:
        return "Ошибка: В настройках Милки не задан Custom API Base URL."
        
    provider = CustomAPIProvider(base_url=base_url, api_key=api_key)
    result = provider.send_request(endpoint, method, payload)
    return json.dumps(result, ensure_ascii=False)
