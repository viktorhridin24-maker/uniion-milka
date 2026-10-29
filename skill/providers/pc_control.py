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
        
        # Переводим в нижний регистр для проверки синонимов
        clean_path = path.lower().strip()
        
        # Умный маппинг популярных программ
        if clean_path in ["vs code", "vscode", "вс код", "вскод"]:
            path = "code"
        elif clean_path in ["браузер", "chrome", "хром"]:
            path = "google-chrome" if self.platform != "win32" else "chrome"

        logger.info(f"Попытка запустить: {path}")

        if self.platform == "win32":
            # На Windows используем start через shell, чтобы подхватывать системные алиасы типа 'code'
            os.system(f"start {path}")
        else:
            # На Linux запускаем процесс напрямую
            subprocess.Popen([path], shell=True)
            
        return {"status": "success", "message": f"Запущено приложение: {path}"}

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
