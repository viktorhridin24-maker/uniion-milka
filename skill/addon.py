import sys
import json
import logging
from pathlib import Path
from addon_api import tool, AddonContext

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

try:
    from providers.pc_control import PCController
    from providers.custom import CustomAPIProvider
    from providers.telegram_api import TelegramProvider
    pc_handler = PCController()
except Exception as e:
    pc_handler = None


def setup(ctx: AddonContext):
    ctx.log("Плагин uniion успешно загружен в систему Milky!")


@tool(
    "open_program",
    "Запускает указанную программу, открывает локальный файл или веб-сайт на компьютере пользователя.",
    {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Системное имя программы (например, 'code' или 'spotify'), путь к файлу или URL сайта."
            }
        },
        "required": ["path"]
    }
)
def open_program(path: str, ctx: AddonContext):
    if not pc_handler:
        return "Ошибка: Модуль управления ПК не был инициализирован."
    
    clean_path = path.lower().strip()
    
    if clean_path in ["spotify", "спотифай", "музыка", "спотик"]:
        if sys.platform == "win32":
            appdata_roaming = os.environ.get("APPDATA", "")
            target_path = Path(appdata_roaming) / "Spotify" / "Spotify.exe"
            if target_path.exists():
                path = str(target_path)
                ctx.log(f"Путь Spotify переопределен на: {path}")
    
    ctx.log(f"Вызов open_program для пути: {path}")
    result = pc_handler.execute_system_command("open_program", {"path": path})
    return result.get("message", "Команда выполнена")


@tool(
    "create_file",
    "Создает новый файл с указанным кодом или текстом по выбранному пути на ПК.",
    {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Полный абсолютный путь к создаваемому файлу"},
            "content": {"type": "string", "description": "Текстовое содержимое файла"}
        },
        "required": ["path", "content"]
    }
)
def create_file(path: str, content: str, ctx: AddonContext):
    if not pc_handler:
        return "Ошибка: Модуль управления ПК не был инициализирован."
    
    ctx.log(f"Вызов create_file для пути: {path}")
    result = pc_handler.execute_system_command("create_file", {"path": path, "content": content})
    return result.get("message", "Файл обработан")


@tool(
    "read_file",
    "Читает содержимое текстового файла или скрипта по указанному пути на компьютере.",
    {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Полный абсолютный путь к читаемому файлу"}
        },
        "required": ["path"]
    }
)
def read_file(path: str, ctx: AddonContext):
    if not pc_handler:
        return "Ошибка: Модуль управления ПК не был инициализирован."
    
    ctx.log(f"Вызов read_file для пути: {path}")
    result = pc_handler.execute_system_command("read_file", {"path": path})
    if result.get("status") == "success":
        return result.get("content", "Файл пуст")
    return f"Ошибка: {result.get('message', 'Не удалось прочитать файл')}"


@tool(
    "send_telegram_alert",
    "Отправляет текстовое уведомление пользователю в Telegram через Bot API.",
    {
        "type": "object",
        "properties": {
            "text": {"type": "string", "description": "Текст сообщения для отправки в чат"}
        },
        "required": ["text"]
    }
)
def send_telegram_alert(text: str, ctx: AddonContext):
    tg_token = ctx.settings.get("telegram_token")
    tg_chat_id = ctx.settings.get("telegram_chat_id")
    
    if not tg_token or not tg_chat_id:
        return "Ошибка: В настройках плагина не заполнены telegram_token или telegram_chat_id."
        
    provider = TelegramProvider(token=tg_token, chat_id=tg_chat_id)
    result = provider.send_message(text)
    return result.get("message", "Статус отправки неизвестен")


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
    base_url = ctx.settings.get("custom_api_url") if ctx else None
    api_key = ctx.settings.get("custom_api_key") if ctx else None
    
    if not base_url:
        return "Ошибка: В настройках Милки не задан Custom API Base URL."
        
    provider = CustomAPIProvider(base_url=base_url, api_key=api_key)
    result = provider.send_request(endpoint, method, payload)
    return json.dumps(result, ensure_ascii=False)
