"""
AI Config Manager - 负责终端交互
"""
import questionary
from questionary import Style as QStyle
from typing import Optional
from dataclasses import dataclass


# 自定义终端样式
CUSTOM_STYLE = QStyle([
    ('qmark', 'fg:#FFA500 bold'),
    ('question', 'fg:#00CED1 bold'),
    ('answer', 'fg:#90EE90 bold'),
    ('pointer', 'fg:#FF69B4 bold'),
    ('selected', 'fg:#32CD32'),
    ('separator', 'fg:#808080'),
    ('header', 'fg:#FF6347 bold'),
])


@dataclass
class MenuChoice:
    """菜单选择结果"""
    value: str
    index: int


def print_header(text: str):
    """打印彩色标题"""
    print(f"\n\x1b[1;35m{'='*50}\x1b[0m")
    print(f"\x1b[1;36m{text}\x1b[0m")
    print(f"\x1b[1;35m{'='*50}\x1b[0m\n")


def print_success(text: str):
    print(f"\x1b[1;32m✓ {text}\x1b[0m")


def print_error(text: str):
    print(f"\x1b[1;31m✗ {text}\x1b[0m")


def print_info(text: str):
    print(f"\x1b[1;34mℹ {text}\x1b[0m")


def print_menu(options: list) -> MenuChoice:
    """打印菜单并返回用户选择"""
    # 打印选项
    print()
    for i, option in enumerate(options, 1):
        print(f"  \x1b[1;33m{i}\x1b[0m. {option}")
    print()

    # 获取用户输入
    while True:
        choice = input("\x1b[1;32m请选择: \x1b[0m").strip()

        if choice == "":
            continue

        try:
            idx = int(choice)
            if 1 <= idx <= len(options):
                return MenuChoice(value=str(idx), index=idx - 1)
            else:
                print_error(f"请输入 1-{len(options)} 之间的数字")
        except ValueError:
            print_error("请输入有效数字")


def ask_back_to_menu():
    """按 Enter 返回主菜单"""
    input("\n\x1b[1;32m按 Enter 返回主菜单...\x1b[0m")


PROVIDER_OPTIONS = [
    "Anthropic (官方)",
    "自定义/其他"
]


def ask_provider() -> Optional[str]:
    """选择提供商"""
    print_info("请选择 AI 模型提供商 (按 Q 返回菜单)")

    choice = questionary.select(
        "提供商:",
        choices=PROVIDER_OPTIONS,
        style=CUSTOM_STYLE,
        default=PROVIDER_OPTIONS[0]
    ).ask()

    if choice is None:
        return None

    return "anthropic" if "Anthropic" in choice else "custom"


def ask_api_key(provider: str) -> Optional[str]:
    """输入 API Key"""
    if provider == "anthropic":
        print_info("请输入您的 Anthropic API Key (按 Q 返回菜单)")
        print_info("格式: sk-ant-xxxxx (在 console.anthropic.com 获取)")
    else:
        print_info("请输入您的 API Key (按 Q 返回菜单)")

    key = questionary.text(
        "API Key:",
        style=CUSTOM_STYLE,
        validate=lambda x: len(x) > 10 or "API Key 太短，请确认格式"
    ).ask()

    return key


def ask_base_url(provider: str) -> Optional[str]:
    """输入 Base URL"""
    if provider == "anthropic":
        default_url = "https://api.anthropic.com"
    else:
        default_url = ""

    print_info("请输入 API Base URL (按 Q 返回菜单)")
    if provider == "anthropic":
        print_info(f"默认: {default_url}")

    url = questionary.text(
        "Base URL:",
        style=CUSTOM_STYLE,
        default=default_url if default_url else "",
        validate=lambda x: x.startswith("http") or "URL 必须以 http:// 或 https:// 开头"
    ).ask()

    return url


def ask_model(provider: str) -> Optional[str]:
    """选择或输入模型"""
    if provider == "anthropic":
        models = [
            "claude-opus-4-6",
            "claude-sonnet-4-6",
            "claude-haiku-4-5-20251001",
            "自定义"
        ]
        print_info("请选择模型 (按 Q 返回菜单)")

        choice = questionary.select(
            "模型:",
            choices=models,
            style=CUSTOM_STYLE
        ).ask()

        if choice is None:
            return None

        if choice == "自定义":
            model = questionary.text(
                "请输入模型名称:",
                style=CUSTOM_STYLE
            ).ask()
        else:
            model = choice
    else:
        print_info("请输入要使用的模型名称 (按 Q 返回菜单)")
        model = questionary.text(
            "模型:",
            style=CUSTOM_STYLE,
            validate=lambda x: len(x) > 0 or "模型名称不能为空"
        ).ask()

    return model


def ask_config_name() -> Optional[str]:
    """输入配置名称"""
    print_info("为这个配置起个名字，方便识别 (按 Q 返回菜单)")

    name = questionary.text(
        "配置名称:",
        style=CUSTOM_STYLE,
        default="default",
        validate=lambda x: len(x) > 0 or "名称不能为空"
    ).ask()

    return name
