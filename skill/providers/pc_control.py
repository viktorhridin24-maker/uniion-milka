import sys
import os
import subprocess
import logging
from typing import Dict, Any 

logger = logging.getLogger("uniion.pc_control") 

class PCController:
def **init**(self):
self.platform = sys.platform
logger.info(f"Модуль управления ПК инициализирован для ОС: {self.platform}") 

def execute_system_command(self, action: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
params = params or {}
try:
if action == "open_program":
return self._open_program(params.get("path", ""))
elif action == "create_file":
return self._create_file(params.get("path", ""), params.get("content", ""))
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

### 1. Синонимы для VS Code (ищем в AppData локального пользователя)

if clean_path in ["vs code", "vscode", "вс код", "вскод"]:
if self.platform == "win32":
appdata_local = os.environ.get("LOCALAPPDATA", "")
path = os.path.join(appdata_local, "Programs", "Microsoft VS Code", "Code.exe")
else:
path = "code" 

### 2. Синонимы для Spotify (Твой точный путь из Roaming!)

elif clean_path in ["spotify", "спотифай", "музыка", "спотик"]:
if self.platform == "win32":
appdata_roaming = os.environ.get("APPDATA", "")
path = os.path.join(appdata_roaming, "Spotify", "Spotify.exe")
else:
path = "spotify" 

### 3. Браузеры из анонса в посте (Chrome, Firefox, Brave, Vivaldi)

elif clean_path in ["браузер", "chrome", "хром", "google chrome"]:
path = r"C:\Program Files\Google\Chrome\Application\chrome.exe" if self.platform == "win32" else "google-chrome"
elif clean_path in ["firefox", "фаерфокс", "лиса"]:
path = r"C:\Program Files\Mozilla Firefox\firefox.exe" if self.platform == "win32" else "firefox"
elif clean_path in ["brave", "брейв"]:
path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe" if self.platform == "win32" else "brave-browser"
elif clean_path in ["vivaldi", "вивальди"]:
path = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Vivaldi", "Application", "vivaldi.exe") if self.platform == "win32" else "vivaldi" 

logger.info(f"Запуск через os.startfile или Popen: {path}") 

try:
if self.platform == "win32": 

### Родной запуск Windows — открывает само приложение БЕЗ консоли cmd

if os.path.exists(path):
os.startfile(path)
else:
# Если жесткий путь не найден, пробуем запустить как глобальную команду
os.startfile(path if not path.endswith('.exe') else path.split('\')[-1])
else:
subprocess.Popen([path], shell=True if " " in path else False) 

return {"status": "success", "message": f"Программа успешно запущена."}

except Exception as e:
return {"status": "error", "message": f"Не удалось открыть: {str(e)}"}

def _create_file(self, path: str, content: str) -> Dict[str, Any]:
"""Создает файл со скриптом или кодом на ПК."""
if not path:
return {"status": "error", "message": "Путь к файлу не указан"}
try:
file_path = Path(path)
file_path.parent.mkdir(parents=True, exist_ok=True)
with open(file_path, "w", encoding="utf-8") as f:
f.write(content)
return {"status": "success", "message": f"Файл успешно создан по пути: {path}"}
except Exception as e:
return {"status": "error", "message": str(e)} 

def _shutdown_pc(self) -> Dict[str, Any]:
if self.platform == "win32":
subprocess.run(["shutdown", "/s", "/t", "1"])
else:
subprocess.run(["shutdown", "now"])
return {"status": "success", "message": "Команда на выключение ПК отправлена"}
