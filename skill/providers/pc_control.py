import sys
import os
import subprocess
import logging
from typing import Dict, Any 

logger = logging.getLogger("uniion.pc_control") 

class PCController:
def **init**(self):
# Определяем операционную систему при старте
self.platform = sys.platform
logger.info(f"Модуль управления ПК инициализирован для ОС: {self.platform}") 

def execute_system_command(self, action: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
"""Обрабатывает команды управления компьютером."""
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
"""Открывает программу или файл."""
if not path:
return {"status": "error", "message": "Путь к программе не указан"} 

if self.platform == "win32":
os.startfile(path)
else:  # Linux / macOS
subprocess.Popen(["xdg-open", path])

return {"status": "success", "message": f"Запущено приложение по пути: {path}"}

def _shutdown_pc(self) -> Dict[str, Any]:
"""Выключает ПК с учетом операционной системы."""
if self.platform == "win32":
subprocess.run(["shutdown", "/s", "/t", "1"])
else:  # Linux
subprocess.run(["shutdown", "now"]) 

return {"status": "success", "message": "Команда на выключение ПК отправлена"}
def _run_shell_command(self, command: str) -> Dict[str, Any]:
"""Безопасно запускает консольную команду и возвращает текстовый ответ."""
if not command:
return {"status": "error", "message": "Команда пуста"} 

# Выполняем команду в системной оболочке
result = subprocess.run(command, shell=True, text=True, capture_output=True, timeout=10)

if result.returncode == 0:
    return {"status": "success", "output": result.stdout}
else:
    return {"status": "error", "output": result.stderr}

if **name** == "**main**": 

### Быстрый тест модуля

controller = PCController()
test_cmd = "dir" if sys.platform == "win32" else "ls"
print(controller.execute_system_command("run_shell", {"command": test_cmd}))
