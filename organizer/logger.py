"""简单日志：一边打印到屏幕，一边写入文件。"""

from datetime import datetime
from pathlib import Path


class OrganizerLogger:
    def __init__(self, log_file: Path):
        self.log_file = log_file
        self.lines = []

    def info(self, message: str) -> None:
        self._write("INFO", message)

    def warn(self, message: str) -> None:
        self._write("WARN", message)

    def error(self, message: str) -> None:
        self._write("ERROR", message)

    def _write(self, level: str, message: str) -> None:
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{stamp}] [{level}] {message}"
        print(line)
        self.lines.append(line)

    def save(self) -> None:
        """把本次整理的全部日志保存到文件。"""
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        text = "\n".join(self.lines) + "\n"
        self.log_file.write_text(text, encoding="utf-8")
        print(f"\n日志已保存：{self.log_file}")
