from setuptools import setup, find_packages

setup(
    name="ai-config-manager",
    version="1.0.0",
    description="AI Model Config Manager",
    packages=find_packages(),
    install_requires=[
        "questionary>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "ai-config=ai_config_manager.main:main",
        ],
    },
    package_data={
        "ai_config_manager": ["py.typed"],
    },
)
