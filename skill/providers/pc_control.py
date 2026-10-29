import sys
import os
import subprocess
import logging
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
            elif action == "shutdown":
                return self._shutdown_pc()
            elif action == "run_shell":
                return self._run_shell_command(params.get("command", ""))
            else:
                return {"status": "error", "message": f"Неизвестное действие: {action}"}
        except Exception as e:
            logger.error(f"Ошибка при выполнении {action}: {e}")
            return {"status": "error", "message": str(e)}

    def _open_program(self, path: str) -> Dict[str, Any]:
        if not path:
            return {"status": "error", "message": "Путь к программе не указан"}
        
        clean_path = path.lower().strip()
        
        # Синонимы для VS Code
        if clean_path in ["vs code", "vscode", "вс код", "вскод"]:
            path = "code"
            
        # Синонимы для Хрома с жесткими путями (для обхода проблем с PATH)
        elif clean_path in ["braузер", "chrome", "хром", "google chrome"]:
            if self.platform == "win32":
                possible_paths = [
                    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
                ]
                path = "chrome"
                for p in possible_paths:
                    if os.path.exists(p):
                        path = f'"{p}"'
                        break
            else:
                path = "google-chrome"

        logger.info(f"Попытка запустить: {path}")

        if self.platform == "win32":
            os.system(f"start {path}")
        else:
            subprocess.Popen([path], shell=True)
            
        return {"status": "success", "message": f"Запущен процесс: {path}"}

    def _shutdown_pc(self) -> Dict[str, Any]:
        if self.platform == "win32":
            subprocess.run(["shutdown", "/s", "/t", "1"])
        else:
            subprocess.run(["shutdown", "now"])
        return {"status": "success", "message": "Команда на выключение ПК отправлена"}

    def _run_shell_command(self, command: str) -> Dict[str, Any]:
        if not command:
            return {"status": "error", "message": "Команда пуста"}
        result = subprocess.run(command, shell=True, text=True, capture_output=True, timeout=10)
        if result.returncode == 0:
            return {"status": "success", "output": result.stdout}
        else:
            return {"status": "error", "output": result.stderr}

