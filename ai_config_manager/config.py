"""
AI Config Manager - 配置数据模型
"""
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict


@dataclass
class ModelConfig:
    """模型配置数据类"""
    name: str = "default"
    provider: str = "anthropic"
    api_key: str = ""
    base_url: str = "https://api.anthropic.com"
    model: str = "claude-sonnet-4-6"

    def to_env_dict(self) -> Dict[str, str]:
        """转换为环境变量格式"""
        return {
            "ANTHROPIC_AUTH_TOKEN": self.api_key,
            "ANTHROPIC_BASE_URL": self.base_url,
            "ANTHROPIC_MODEL": self.model
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ModelConfig':
        """从字典创建配置"""
        return cls(
            name=data.get('name', 'default'),
            provider=data.get('provider', 'anthropic'),
            api_key=data.get('api_key', ''),
            base_url=data.get('base_url', 'https://api.anthropic.com'),
            model=data.get('model', 'claude-sonnet-4-6')
        )


class ConfigManager:
    """配置管理器"""

    def __init__(self, config_path: str):
        self.config_path = Path(config_path)

    def load_config(self) -> Optional[ModelConfig]:
        """加载配置"""
        if not self.config_path.exists():
            return None

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 优先从 env 字段读取
            env = data.get('env', {})
            if env:
                return ModelConfig(
                    name=data.get('name', 'default'),
                    provider=data.get('provider', 'anthropic'),
                    api_key=env.get('ANTHROPIC_AUTH_TOKEN', ''),
                    base_url=env.get('ANTHROPIC_BASE_URL', 'https://api.anthropic.com'),
                    model=env.get('ANTHROPIC_MODEL', 'claude-sonnet-4-6')
                )

            # 否则从根字段读取
            return ModelConfig.from_dict(data)
        except (json.JSONDecodeError, IOError):
            return None

    def save_config(self, config: ModelConfig) -> bool:
        """保存配置"""
        try:
            data = {
                "name": config.name,
                "provider": config.provider,
                "env": config.to_env_dict()
            }

            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            return True
        except IOError:
            return False


def load_config(config_path: str) -> Optional[ModelConfig]:
    """便捷函数：加载配置"""
    manager = ConfigManager(config_path)
    return manager.load_config()
