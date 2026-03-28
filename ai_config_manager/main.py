"""
AI Config Manager - 主入口
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from ai_config_manager.config import ModelConfig
from ai_config_manager.storage import StorageManager, ProfileStorage
from ai_config_manager.interactive import (
    print_header, print_success, print_error, print_info,
    print_menu, MenuChoice,
    ask_provider, ask_api_key, ask_base_url, ask_model,
    ask_config_name, ask_back_to_menu
)

# Claude settings.json 路径
DEFAULT_CONFIG_PATH = Path.home() / ".claude" / "settings.json"
TEST_CONFIG_PATH = project_root / "settings.json"
# 配置组存储路径
PROFILES_PATH = Path.home() / ".ai-config-manager" / "profiles.json"


def show_main_menu(test_mode: bool = False) -> MenuChoice:
    """显示主菜单"""
    print_header("AI Config Manager")

    return print_menu([
        "新增配置组",
        "查看已有配置组",
        "应用配置到 Claude",
        "退出"
    ])


def create_new_profile(profiles: ProfileStorage, test_mode: bool = False) -> bool:
    """新增配置组"""
    print_header("新增配置组")

    # 输入配置名称
    config_name = ask_config_name()
    if config_name is None:
        return False

    # 选择提供商
    provider = ask_provider()
    if provider is None:
        return False

    # 输入 API Key
    api_key = ask_api_key(provider)
    if api_key is None:
        return False

    # 输入 Base URL
    base_url = ask_base_url(provider)
    if base_url is None:
        return False

    # 选择/输入模型
    model = ask_model(provider)
    if model is None:
        return False

    # 构建配置
    new_config = ModelConfig(
        name=config_name,
        provider=provider,
        api_key=api_key,
        base_url=base_url,
        model=model
    )

    # 保存到配置组
    profiles.add_profile(new_config)
    print_success(f"配置组 '{config_name}' 已保存")

    return True


def view_profiles(profiles: ProfileStorage, test_mode: bool = False):
    """查看已有配置组"""
    print_header("查看已有配置组")

    all_profiles = profiles.list_profiles()
    if not all_profiles:
        print_info("暂无配置组，请先新增配置")
        ask_back_to_menu()
        return

    # 显示所有配置组
    print("\n\x1b[1;33m已有配置组：\x1b[0m\n")
    for i, profile in enumerate(all_profiles, 1):
        mask_key = profile.api_key[:8] + "****" if len(profile.api_key) > 8 else "****"
        print(f"  \x1b[1;36m{i}\x1b[0m. {profile.name}")
        print(f"     提供商: {profile.provider}")
        print(f"     API Key: {mask_key}")
        print(f"     Base URL: {profile.base_url}")
        print(f"     模型: {profile.model}")
        print()

    # 选择操作
    choice = print_menu([
        "编辑配置组",
        "删除配置组",
        "返回主菜单"
    ])

    if choice.value == "1":  # 编辑
        edit_profile(profiles, all_profiles, test_mode)
    elif choice.value == "2":  # 删除
        delete_profile(profiles, all_profiles, test_mode)


def edit_profile(profiles: ProfileStorage, all_profiles: list, test_mode: bool = False):
    """编辑配置组"""
    print_header("编辑配置组")

    # 选择要编辑的配置
    print_info("选择要编辑的配置组:")
    for i, profile in enumerate(all_profiles, 1):
        print(f"  \x1b[1;36m{i}\x1b[0m. {profile.name}")

    idx = input("\n请输入编号 (或按 Enter 返回): ").strip()
    if idx == "":
        return

    try:
        idx = int(idx) - 1
        if idx < 0 or idx >= len(all_profiles):
            print_error("无效编号")
            ask_back_to_menu()
            return
    except ValueError:
        print_error("无效输入")
        ask_back_to_menu()
        return

    profile = all_profiles[idx]
    print_info(f"编辑配置组: {profile.name}")

    # 重新输入各字段
    provider = ask_provider()
    if provider is None:
        return
    api_key = ask_api_key(provider)
    if api_key is None:
        return
    base_url = ask_base_url(provider)
    if base_url is None:
        return
    model = ask_model(provider)
    if model is None:
        return

    # 更新配置
    updated = ModelConfig(
        name=profile.name,
        provider=provider,
        api_key=api_key,
        base_url=base_url,
        model=model
    )
    profiles.update_profile(profile.name, updated)
    print_success(f"配置组 '{profile.name}' 已更新")


def delete_profile(profiles: ProfileStorage, all_profiles: list, test_mode: bool = False):
    """删除配置组"""
    print_header("删除配置组")

    # 选择要删除的配置
    print_info("选择要删除的配置组:")
    for i, profile in enumerate(all_profiles, 1):
        print(f"  \x1b[1;36m{i}\x1b[0m. {profile.name}")

    idx = input("\n请输入编号 (或按 Enter 返回): ").strip()
    if idx == "":
        return

    try:
        idx = int(idx) - 1
        if idx < 0 or idx >= len(all_profiles):
            print_error("无效编号")
            ask_back_to_menu()
            return
    except ValueError:
        print_error("无效输入")
        ask_back_to_menu()
        return

    profile = all_profiles[idx]
    confirm = input(f"确认删除配置组 '{profile.name}'? (y/N): ").strip().lower()
    if confirm == 'y':
        profiles.delete_profile(profile.name)
        print_success(f"配置组 '{profile.name}' 已删除")
    else:
        print_info("已取消删除")


def apply_to_claude(profiles: ProfileStorage, test_mode: bool = False):
    """应用配置到 Claude"""
    print_header("应用配置到 Claude")

    all_profiles = profiles.list_profiles()
    if not all_profiles:
        print_error("暂无配置组，请先新增配置")
        ask_back_to_menu()
        return

    # 显示所有配置组
    print_info("选择要应用的配置组:\n")
    for i, profile in enumerate(all_profiles, 1):
        print(f"  \x1b[1;36m{i}\x1b[0m. {profile.name} ({profile.model})")

    idx = input("\n请输入编号 (或按 Enter 返回): ").strip()
    if idx == "":
        return

    try:
        idx = int(idx) - 1
        if idx < 0 or idx >= len(all_profiles):
            print_error("无效编号")
            ask_back_to_menu()
            return
    except ValueError:
        print_error("无效输入")
        ask_back_to_menu()
        return

    profile = all_profiles[idx]
    config_path = TEST_CONFIG_PATH if test_mode else DEFAULT_CONFIG_PATH

    # 确认应用
    print(f"\n\x1b[1;33m即将应用到:\x1b[0m {config_path}")
    print(f"\x1b[1;33m配置组:\x1b[0m {profile.name}")
    print(f"\x1b[1;33mAPI Key:\x1b[0m {profile.api_key[:8]}****")
    print(f"\x1b[1;33mBase URL:\x1b[0m {profile.base_url}")
    print(f"\x1b[1;33m模型:\x1b[0m {profile.model}")

    confirm = input("\n确认应用? (y/N): ").strip().lower()
    if confirm != 'y':
        print_info("已取消应用")
        return

    # 应用配置
    storage = StorageManager(str(config_path))
    config_dict = {
        "name": profile.name,
        "provider": profile.provider,
        "api_key": profile.api_key,
        "base_url": profile.base_url,
        "model": profile.model
    }
    storage.update_settings(config_dict)
    print_success(f"配置已应用到: {config_path}")
    print_info("请重启 Claude Code 使配置生效")


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Claude 配置管理器",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--test", "-t", action="store_true", help="测试模式")

    args = parser.parse_args()
    test_mode = args.test

    # 初始化存储
    profiles = ProfileStorage(str(PROFILES_PATH))

    while True:
        choice = show_main_menu(test_mode)

        if choice.value == "1":  # 新增配置组
            create_new_profile(profiles, test_mode)
            ask_back_to_menu()

        elif choice.value == "2":  # 查看已有配置组
            view_profiles(profiles, test_mode)

        elif choice.value == "3":  # 应用配置到 Claude
            apply_to_claude(profiles, test_mode)
            ask_back_to_menu()

        elif choice.value == "4":  # 退出
            print_info("感谢使用，再见！")
            break


if __name__ == "__main__":
    main()
