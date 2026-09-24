"""根据文件内容检测重复文件。

文件名不同也可能内容完全一样。比较内容时用哈希值：
把文件读成一段数字指纹，指纹相同就认为是同一份文件。
"""

from collections import defaultdict
from hashlib import sha256
from pathlib import Path


def file_hash(path: Path, chunk_size: int = 1024 * 1024) -> str:
    """计算文件的 SHA256 指纹。分块读取，避免大文件一次性进内存。"""
    hasher = sha256()
    with path.open("rb") as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


def find_duplicate_groups(files: list[Path]) -> list[list[Path]]:
    """返回重复文件分组。每一组里都是内容相同的文件。

    先按文件大小分组：大小不同，内容一定不同，可以少算很多哈希。
    """
    by_size: dict[int, list[Path]] = defaultdict(list)
    for path in files:
        by_size[path.stat().st_size].append(path)

    groups: list[list[Path]] = []
    for same_size_files in by_size.values():
        if len(same_size_files) < 2:
            continue

        by_hash: dict[str, list[Path]] = defaultdict(list)
        for path in same_size_files:
            by_hash[file_hash(path)].append(path)

        for hashed_files in by_hash.values():
            if len(hashed_files) >= 2:
                groups.append(sorted(hashed_files))

    return groups


def extra_copies(groups: list[list[Path]]) -> set[Path]:
    """每组保留名字排在最前面的那一份，其余视为重复副本。"""
    extras: set[Path] = set()
    for group in groups:
        extras.update(group[1:])
    return extras
