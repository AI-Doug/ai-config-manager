"""
AI Config Manager - 文件存储逻辑
"""
import json
import shutil
from pathlib import Path
from typing import Dict, Any, Optional, List
from .config import ModelConfig
from .interactive import print_success, print_error, print_info


class StorageManager:
    """Claude settings.json 管理器"""

    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self._ensure_parent_dir()

    def _ensure_parent_dir(self):
        """确保父目录存在"""
        parent = self.config_path.parent
        if not parent.exists():
            parent.mkdir(parents=True, exist_ok=True)

    def load_settings(self) -> Optional[Dict[str, Any]]:
        """加载现有配置"""
        if not self.config_path.exists():
            return None

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print_error(f"读取配置失败: {e}")
            return None

    def save_to_file(self, config: Dict[str, Any]) -> bool:
        """保存配置到文件（不更新 settings）"""
        try:
            data = {
                "name": config.get("name", "default"),
                "provider": config.get("provider", "anthropic"),
                "api_key": config.get("api_key", ""),
                "base_url": config.get("base_url", "https://api.anthropic.com"),
                "model": config.get("model", "claude-sonnet-4-6")
            }

            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            return True
        except IOError as e:
            print_error(f"保存配置失败: {e}")
            return False

    def update_settings(self, config: Dict[str, Any]) -> bool:
        """更新 Claude settings.json"""
        settings = self.load_settings() or {}

        # 确保 env 字段存在
        if 'env' not in settings:
            settings['env'] = {}

        # 更新 env 配置
        settings['env']['ANTHROPIC_AUTH_TOKEN'] = config.get('api_key', '')
        settings['env']['ANTHROPIC_BASE_URL'] = config.get('base_url', 'https://api.anthropic.com')
        settings['env']['ANTHROPIC_MODEL'] = config.get('model', 'claude-sonnet-4-6')

        # 保存配置名称用于识别
        if 'name' not in settings:
            settings['name'] = config.get('name', 'default')

        try:
            # 备份原文件
            if self.config_path.exists():
                backup_path = self.config_path.with_suffix('.json.bak')
                shutil.copy2(self.config_path, backup_path)
                print_info(f"已备份原配置到: {backup_path}")

            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)

            print_success("配置已更新")
            return True
        except IOError as e:
            print_error(f"更新配置失败: {e}")
            return False

    def export_config(self, config: Dict[str, Any], export_path: str) -> bool:
        """导出配置到指定路径"""
        try:
            export_data = {
                "name": config.get("name", "default"),
                "provider": config.get("provider", "anthropic"),
                "api_key": config.get("api_key", ""),
                "base_url": config.get("base_url", "https://api.anthropic.com"),
                "model": config.get("model", "claude-sonnet-4-6"),
                "env": {
                    "ANTHROPIC_AUTH_TOKEN": config.get("api_key", ""),
                    "ANTHROPIC_BASE_URL": config.get("base_url", "https://api.anthropic.com"),
                    "ANTHROPIC_MODEL": config.get("model", "claude-sonnet-4-6")
                }
            }

            export_file = Path(export_path)
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)

            return True
        except IOError as e:
            print_error(f"导出配置失败: {e}")
            return False


class ProfileStorage:
    """配置组存储器 - 管理多个配置组"""

    def __init__(self, profiles_path: str):
        self.profiles_path = Path(profiles_path)
        self._ensure_parent_dir()

    def _ensure_parent_dir(self):
        """确保父目录存在"""
        parent = self.profiles_path.parent
        if not parent.exists():
            parent.mkdir(parents=True, exist_ok=True)

    def _load_profiles(self) -> Dict[str, Any]:
        """加载所有配置组"""
        if not self.profiles_path.exists():
            return {}

        try:
            with open(self.profiles_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def _save_profiles(self, profiles: Dict[str, Any]) -> bool:
        """保存所有配置组"""
        try:
            with open(self.profiles_path, 'w', encoding='utf-8') as f:
                json.dump(profiles, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print_error(f"保存配置组失败: {e}")
            return False

    def list_profiles(self) -> List[ModelConfig]:
        """列出所有配置组"""
        profiles = self._load_profiles()
        result = []

        for name, data in profiles.items():
            result.append(ModelConfig(
                name=name,
                provider=data.get('provider', 'anthropic'),
                api_key=data.get('api_key', ''),
                base_url=data.get('base_url', 'https://api.anthropic.com'),
                model=data.get('model', 'claude-sonnet-4-6')
            ))

        return result

    def get_profile(self, name: str) -> Optional[ModelConfig]:
        """获取指定配置组"""
        profiles = self._load_profiles()

        if name not in profiles:
            return None

        data = profiles[name]
        return ModelConfig(
            name=name,
            provider=data.get('provider', 'anthropic'),
            api_key=data.get('api_key', ''),
            base_url=data.get('base_url', 'https://api.anthropic.com'),
            model=data.get('model', 'claude-sonnet-4-6')
        )

    def add_profile(self, config: ModelConfig) -> bool:
        """添加配置组"""
        profiles = self._load_profiles()

        profiles[config.name] = {
            'provider': config.provider,
            'api_key': config.api_key,
            'base_url': config.base_url,
            'model': config.model
        }

        return self._save_profiles(profiles)

    def update_profile(self, name: str, config: ModelConfig) -> bool:
        """更新配置组"""
        profiles = self._load_profiles()

        if name not in profiles:
            print_error(f"配置组 '{name}' 不存在")
            return False

        # 如果名称改变，删除旧的
        if name != config.name:
            del profiles[name]

        profiles[config.name] = {
            'provider': config.provider,
            'api_key': config.api_key,
            'base_url': config.base_url,
            'model': config.model
        }

        return self._save_profiles(profiles)

    def delete_profile(self, name: str) -> bool:
        """删除配置组"""
        profiles = self._load_profiles()

        if name not in profiles:
            print_error(f"配置组 '{name}' 不存在")
            return False

        del profiles[name]
        return self._save_profiles(profiles)
