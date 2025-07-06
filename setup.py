from setuptools import setup, find_packages

setup(
    name="AniAlert",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "discord.py>=2.0.0",
        "python-dotenv>=0.19.0",
        "requests>=2.25.0",
    ],
    python_requires=">=3.8",
)