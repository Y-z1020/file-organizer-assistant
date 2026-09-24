"""文件整理助手入口。

运行方式：
    python main.py
然后输入要整理的文件夹路径。
"""

import sys
from datetime import datetime
from pathlib import Path

# Windows 终端默认编码可能导致中文乱码
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from organizer import FileOrganizer
from organizer.config import PROTECTED_FOLDER_NAMES
from organizer.logger import OrganizerLogger


def ask_folder_path() -> Path | None:
    """读取用户输入，并检查路径是否有效。"""
    raw = input("请输入要整理的文件夹路径：").strip().strip('"').strip("'")
    if not raw:
        print("没有输入路径。")
        return None

    folder = Path(raw).expanduser().resolve()
    if not folder.exists():
        print(f"路径不存在：{folder}")
        return None
    if not folder.is_dir():
        print(f"这不是文件夹：{folder}")
        return None
    return folder


def confirm(folder: Path) -> bool:
    print(f"\n即将整理：{folder}")
    print("说明：只会移动该文件夹“当前这一层”的文件，不会进入子文件夹。")
    print("分类文件夹：" + "、".join(sorted(PROTECTED_FOLDER_NAMES)))
    answer = input("确认开始整理吗？(y/n)：").strip().lower()
    return answer in {"y", "yes", "是"}


def main() -> None:
    print("=" * 40)
    print("文件整理助手")
    print("=" * 40)

    folder = ask_folder_path()
    if folder is None:
        return

    if not confirm(folder):
        print("已取消。")
        return

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = folder / f"整理日志_{stamp}.txt"
    logger = OrganizerLogger(log_file)

    logger.info(f"目标文件夹：{folder}")
    organizer = FileOrganizer(folder, logger)
    organizer.organize()
    logger.save()


if __name__ == "__main__":
    main()
