"""文件整理助手入口。

运行方式：
    python main.py
然后输入要整理的文件夹路径，并选择功能。
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


def ask_action() -> str | None:
    print("请选择功能：")
    print("  1. 整理文件（含重复检测，副本移到“重复文件”）")
    print("  2. 仅检测重复文件（不移动）")
    choice = input("输入 1 或 2：").strip()
    if choice == "1":
        return "organize"
    if choice == "2":
        return "detect"
    print("无效选项。")
    return None


def confirm(folder: Path, action: str) -> bool:
    print(f"\n目标文件夹：{folder}")
    print("说明：只会处理该文件夹“当前这一层”的文件，不会进入子文件夹。")
    if action == "organize":
        print("分类文件夹：" + "、".join(sorted(PROTECTED_FOLDER_NAMES)))
        print("内容相同的文件会保留一份到正常分类，其余副本移到“重复文件”。")
    else:
        print("本次只检测重复，不会移动或删除任何文件。")
    answer = input("确认开始吗？(y/n)：").strip().lower()
    return answer in {"y", "yes", "是"}


def main() -> None:
    print("=" * 40)
    print("文件整理助手")
    print("=" * 40)

    folder = ask_folder_path()
    if folder is None:
        return

    action = ask_action()
    if action is None:
        return

    if not confirm(folder, action):
        print("已取消。")
        return

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    prefix = "整理日志" if action == "organize" else "重复检测日志"
    log_file = folder / f"{prefix}_{stamp}.txt"
    logger = OrganizerLogger(log_file)

    logger.info(f"目标文件夹：{folder}")
    organizer = FileOrganizer(folder, logger)
    if action == "organize":
        organizer.organize()
    else:
        organizer.detect_only()
    logger.save()


if __name__ == "__main__":
    main()
