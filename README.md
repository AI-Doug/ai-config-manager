# AI Config Manager

管理 AI 产品模型配置的工具，目前支持 Claude Code。

如果你有多个 AI 模型配置需要切换使用，这个工具可以帮你管理，一键切换。

## 安装

```bash
pip install ai-config-manager
```

## 使用

```bash
ai-config
```

然后按提示操作：
- 新增配置组：添加一组新的模型配置
- 查看已有配置组：编辑或删除现有配置
- 应用配置到 Claude：将选中的配置应用到 Claude Code

## 配置说明

配置组包含：提供商、API Key、Base URL、模型名称。

支持 Anthropic 官方和自定义 provider。
