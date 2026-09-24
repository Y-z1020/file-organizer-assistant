"""分类规则：根据文件后缀决定放到哪个文件夹。

想新增分类时，只需要改这个文件，不用改整理逻辑。
"""

# 后缀统一写成小写，后面比较时也会先转成小写
CATEGORY_BY_EXTENSION = {
    # 图片
    ".jpg": "图片",
    ".jpeg": "图片",
    ".png": "图片",
    ".gif": "图片",
    ".bmp": "图片",
    ".webp": "图片",
    ".svg": "图片",
    ".ico": "图片",
    # 文档
    ".pdf": "文档",
    ".doc": "文档",
    ".docx": "文档",
    ".txt": "文档",
    ".md": "文档",
    ".xls": "文档",
    ".xlsx": "文档",
    ".ppt": "文档",
    ".pptx": "文档",
    ".csv": "文档",
    # 压缩包
    ".zip": "压缩包",
    ".rar": "压缩包",
    ".7z": "压缩包",
    ".tar": "压缩包",
    ".gz": "压缩包",
    # 音频
    ".mp3": "音频",
    ".wav": "音频",
    ".flac": "音频",
    ".aac": "音频",
    ".m4a": "音频",
    # 视频
    ".mp4": "视频",
    ".mkv": "视频",
    ".avi": "视频",
    ".mov": "视频",
    ".wmv": "视频",
    # 代码
    ".py": "代码",
    ".js": "代码",
    ".ts": "代码",
    ".java": "代码",
    ".c": "代码",
    ".cpp": "代码",
    ".html": "代码",
    ".css": "代码",
    ".json": "代码",
}

# 没有匹配到规则时，放到这个文件夹
DEFAULT_CATEGORY = "其他"

# 内容重复的副本放到这个文件夹（每组只保留一份在正常分类里）
DUPLICATE_FOLDER = "重复文件"

# 整理时不要动这些目录（程序自己创建的分类文件夹）
PROTECTED_FOLDER_NAMES = set(CATEGORY_BY_EXTENSION.values()) | {
    DEFAULT_CATEGORY,
    DUPLICATE_FOLDER,
}


def get_category(extension: str) -> str:
    """根据后缀返回分类文件夹名称。"""
    key = extension.lower()
    return CATEGORY_BY_EXTENSION.get(key, DEFAULT_CATEGORY)
