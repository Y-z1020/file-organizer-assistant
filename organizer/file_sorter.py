"""文件整理核心逻辑。

步骤：
1. 列出目标文件夹里的文件（默认只看当前层，不进入子文件夹）
2. 按后缀找到分类
3. 创建分类文件夹
4. 移动文件
5. 记录日志
"""

from pathlib import Path
import shutil

from .config import get_category
from .logger import OrganizerLogger


class FileOrganizer:
    def __init__(self, folder: Path, logger: OrganizerLogger):
        self.folder = folder
        self.logger = logger
        self.moved_count = 0
        self.failed_count = 0

    def organize(self) -> None:
        files = self._list_files()
        if not files:
            self.logger.warn("这个文件夹里没有可整理的文件。")
            return

        self.logger.info(f"找到 {len(files)} 个文件，开始整理。")

        for file_path in files:
            self._move_one_file(file_path)

        self.logger.info(
            f"整理完成：成功 {self.moved_count} 个，失败 {self.failed_count} 个。"
        )

    def _list_files(self) -> list[Path]:
        """只整理当前文件夹里的文件，不递归进入子目录。"""
        result = []
        for item in self.folder.iterdir():
            if item.is_dir():
                continue
            if item.name.startswith("整理日志_"):
                continue
            result.append(item)
        return sorted(result)

    def _move_one_file(self, file_path: Path) -> None:
        category = get_category(file_path.suffix)
        target_dir = self.folder / category

        # 分类文件夹已经存在时，mkdir 也不会报错
        try:
            target_dir.mkdir(exist_ok=True)
        except OSError as error:
            self.failed_count += 1
            self.logger.error(f"无法创建文件夹 {target_dir}：{error}")
            return

        destination = self._unique_path(target_dir / file_path.name)

        try:
            shutil.move(str(file_path), str(destination))
            self.moved_count += 1
            if destination.name != file_path.name:
                self.logger.info(
                    f"{file_path.name} -> {category}/{destination.name}（重名已自动改名）"
                )
            else:
                self.logger.info(f"{file_path.name} -> {category}/")
        except OSError as error:
            self.failed_count += 1
            self.logger.error(f"移动失败 {file_path.name}：{error}")

    def _unique_path(self, path: Path) -> Path:
        """如果目标位置已有同名文件，则自动改成 文件名_1.后缀。"""
        if not path.exists():
            return path

        stem = path.stem
        suffix = path.suffix
        parent = path.parent
        index = 1
        while True:
            candidate = parent / f"{stem}_{index}{suffix}"
            if not candidate.exists():
                return candidate
            index += 1
