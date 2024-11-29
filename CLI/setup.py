from setuptools import setup, find_packages

setup(
    name="cas",
    version="1.0.0",
    packages=find_packages(),  # Automatically find packages
    entry_points={
        'console_scripts': [
            'cas=cas.cli:main',  # Command name points to main function
        ],
    },
    install_requires=[
        "rich",
    ],
)
