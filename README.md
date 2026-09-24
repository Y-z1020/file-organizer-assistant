# 文件整理助手

一个适合初学者阅读的 Python 小项目：根据文件后缀自动分类，并移动到对应文件夹。

## 功能

1. 读取你输入的文件夹路径
2. 按后缀分类（图片、文档、视频等）
3. 自动创建分类文件夹
4. 把文件移动到对应目录
5. 在屏幕上输出整理日志，并保存到目标文件夹

## 如何运行

需要已安装 Python 3.10 或更高版本。本项目只用标准库，不需要 `pip install`。

```bash
cd D:\file-organizer-assistant
python main.py
```

然后输入要整理的文件夹路径，例如：

```text
D:\file-organizer-assistant\demo
```

项目里自带一个 `demo` 文件夹，里面放了几种不同类型的示例文件，适合第一次试运行。

输入 `y` 确认后开始整理。

## 项目结构

```text
file-organizer-assistant/
├── main.py                 # 程序入口：读取路径、确认、启动整理
└── organizer/
    ├── __init__.py
    ├── config.py           # 后缀 -> 分类名称
    ├── logger.py           # 打印并保存日志
    └── file_sorter.py      # 列出文件、创建文件夹、移动文件
```

学习建议：先看 `main.py` 的流程，再看 `config.py` 的规则，最后看 `file_sorter.py` 的移动逻辑。

## 注意事项

- 默认只整理当前这一层的文件，不会递归进入子文件夹
- 同名文件会自动改名为 `文件名_1.后缀`
- 日志文件本身不会被再次整理
- 整理前请先备份重要文件
