import sys
import os
import subprocess
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger("uniion.pc_control")

class PCController:
    def __init__(self):
        self.platform = sys.platform
        logger.info(f"Модуль управления ПК инициализирован для ОС: {self.platform}")

    def execute_system_command(self, action: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        params = params or {}
        try:
            if action == "open_program":
                return self._open_program(params.get("path", ""))
            elif action == "create_file":
                return self._create_file(params.get("path", ""), params.get("content", ""))
            elif action == "read_file":
                return self._read_file(params.get("path", ""))
            elif action == "shutdown":
                return self._shutdown_pc()
            else:
                return {"status": "error", "message": f"Неизвестное действие: {action}"}
        except Exception as e:
            logger.error(f"Ошибка при выполнении {action}: {e}")
            return {"status": "error", "message": str(e)}

    def _open_program(self, path: str) -> Dict[str, Any]:
        if not path:
            return {"status": "error", "message": "Путь к программе не указан"}
        
        clean_path = path.lower().strip()
        
        if clean_path in ["vs code", "vscode", "вс код", "вскод"]:
            if self.platform == "win32":
                appdata_local = os.environ.get("LOCALAPPDATA", "")
                path = os.path.join(appdata_local, "Programs", "Microsoft VS Code", "Code.exe")
            else:
                path = "code"
        elif clean_path in ["spotify", "спотифай", "музыка", "спотик"]:
            if self.platform == "win32":
                appdata_roaming = os.environ.get("APPDATA", "")
                path = os.path.join(appdata_roaming, "Spotify", "Spotify.exe")
            else:
                path = "spotify"
        elif clean_path in ["браузер", "chrome", "хром", "google chrome"]:
            path = r"C:\Program Files\Google\Chrome\Application\chrome.exe" if self.platform == "win32" else "google-chrome"
        elif clean_path in ["firefox", "фаерфокс", "лиса"]:
            path = r"C:\Program Files\Mozilla Firefox\firefox.exe" if self.platform == "win32" else "firefox"

        logger.info(f"Запуск процесса: {path}")

        try:
            if self.platform == "win32":
                os.startfile(path)
            else:
                subprocess.Popen([path], shell=True if " " in path else False)
            return {"status": "success", "message": f"Программа {clean_path} успешно открыта."}
        except Exception as e:
            return {"status": "error", "message": f"Не удалось открыть: {str(e)}"}

    def _create_file(self, path: str, content: str) -> Dict[str, Any]:
        if not path:
            return {"status": "error", "message": "Путь к файлу не указан"}
        try:
            safe_path = path.replace("\\", "/")
            file_path = Path(safe_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return {"status": "success", "message": "Файл успешно создан."}
        except Exception as e:
            logger.error(f"Ошибка создания файла: {e}")
            return {"status": "error", "message": str(e)}

    def _read_file(self, path: str) -> Dict[str, Any]:
        """Читает содержимое указанного файла на ПК, чтобы передать его ИИ."""
        if not path:
            return {"status": "error", "message": "Путь к файлу не указан"}
        try:
            safe_path = path.replace("\\", "/")
            file_path = Path(safe_path)
            if not file_path.exists():
                return {"status": "error", "message": "Указанный файл не найден."}
            
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            return {"status": "success", "content": content}
        except Exception as e:
            logger.error(f"Ошибка чтения файла: {e}")
            return {"status": "error", "message": str(e)}

    def _shutdown_pc(self) -> Dict[str, Any]:
        if self.platform == "win32":
            subprocess.run(["shutdown", "/s", "/t", "1"])
        else:
            subprocess.run(["shutdown", "now"])
        return {"status": "success", "message": "Команда на выключение ПК отправлена"}
